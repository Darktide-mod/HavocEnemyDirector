"""Export only this project's actual UI definitions, without launching the game."""
from pathlib import Path
import argparse, json, re, runpy, sys
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT/'tests'))
from project_env import CHECKS
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=CHECKS/'ui-layouts.json')
layout_output=parser.parse_args().output
globals().update(runpy.run_path(str(PROJECT/'tests/integration_tests.py')))
result={}
L.execute('''
-- Match the installed game's currently available event catalogue (latest console log).
require("scripts/settings/mutator/mutator_templates").mutator_gameplay_barren_odin=nil
test_view._current.havoc_circumstances={"hcm_auric_hounds","hcm_auric_monsters","hcm_auric_patrols"}
mods.HavocConditionManager:set("havoc_circumstances_serialized",table.concat(test_view._current.havoc_circumstances,":"))
for _,category in ipairs({"common","elite","special","boss"}) do
    mods.HavocConditionManager:set("spawn_multiplier_"..category,1)
    mods.HavocConditionManager:set("spawn_mode_"..category,"quantity")
end
mods.HavocEnemyDirector.save_config(mods.HavocEnemyDirector.planner.defaults())
mods.HavocEnemyDirector:set("buff_proc_capacity",300)
test_view._hcm_condition_filter="maelstrom"
test_view._current.havoc_theme_circumstance="default"
test_view._hcm_offsets={}
''')
for lang in ('en','zh-cn','zh-tw'):
    L.globals().test_language=lang
    catalog=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_catalog')
    L.globals().mods.HavocConditionManager.condition_catalog=catalog
    catalog.extend(settings)
    load_mod('HavocEnemyDirector/scripts/mods/HavocEnemyDirector/editor')
    paging=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging')
    L.globals().Paging=paging
    labels={'en':['No special environment','Power supply interruption','Ventilation purge','Toxic gas'],
            'zh-cn':['无特殊环境','停电','通风净化','毒气'],
            'zh-tw':['無特殊環境','停電','通風淨化','毒氣']}[lang]
    L.globals().test_view._options.havoc_theme_circumstance=tbl([{'id':id,'display_name':name} for id,name in zip(['default','darkness_01','ventilation_purge_01','toxic_gas_01'],labels)])
    for page,name in [(4,'director')]:
        view=L.globals().test_view;view._hcm_page=page;view._hcm_choice=None;view._hcm_number=None;view._hcm_offsets=tbl({})
        if page==4:view._hed_generator_id=None
        paging.refresh(view,settings)
        result[lang+'_'+name]=plain_items(view._hcm_ui)
        if page==2:
            L.execute('click_control("environment")')
            result[lang+'_environment']=plain_items(view._hcm_ui)
            paging.close_choice(view)
        if page==4:
            L.execute('local item=find_control("total_cap_value"); Paging.numeric.open(test_view,item); Paging.refresh(test_view,test_settings)')
            result[lang+'_numeric']=plain_items(view._hcm_ui)
            # Native text inputs are persistent widgets outside the builder's item list.
            widget=view._widgets_by_name.hcm_number_input
            position=view._positions.hcm_number_input
            size=paging.numeric.definition().size
            assert widget.visible and widget.content.is_writing
            result[lang+'_numeric'].append(dict(
                key='hcm_number_input',x=position[1],y=position[2],w=size[1],h=size[2],
                text=widget.content.input_text,font=24,fill=True,overlay=True,input=True))
            paging.numeric.cancel(view)
            L.execute('''
ui_sample_cfg=mods.HavocEnemyDirector.get_config()
test_view._hed_add_category=1
Paging.refresh(test_view,test_settings)
click_control("add_generator")
click_control("clear_pool")
click_control("add_pool_unit")
''')
            result[lang+'_add_unit']=plain_items(view._hcm_ui)
            paging.close_choice(view)
            L.execute('''
mods.HavocEnemyDirector.save_config(ui_sample_cfg)
local cfg=mods.HavocEnemyDirector.get_config(); cfg.enabled=false
mods.HavocEnemyDirector.save_config(cfg)
test_view._hed_generator_id=nil
Paging.refresh(test_view,test_settings)
''')
            result[lang+'_native']=plain_items(view._hcm_ui)
            L.execute('mods.HavocEnemyDirector.save_config(ui_sample_cfg)')
            names={'en':['Mixed pressure 5x','Boss practice','Scab patrols','Specialist waves','Low density'],
                   'zh-cn':['混合压力五倍','Boss练习','血痂巡逻','特感波次','低密度配置'],
                   'zh-tw':['混合壓力五倍','Boss練習','血痂巡邏','特感波次','低密度設定']}[lang]
            L.globals().sample_template_names=tbl(names)
            L.execute('''
local D=mods.HavocEnemyDirector
local old_list=D.presets.list
local doc=assert(D.presets.capture(sample_template_names[1]))
doc.config.total_cap=600
doc.config.custom={{id="custom_1",category="common",kind="timer",pool={chaos_poxwalker=1}},
    {id="custom_2",category="common",kind="travel",pool={chaos_poxwalker=1}}}
for _,c in ipairs(D.planner.categories) do doc.context.scaling[c].multiplier=5 end
D.presets.list=function()
 local entries={}
 for i,name in ipairs(sample_template_names) do local d=D.planner.copy(doc);d.name=name;entries[i]={file="sample_"..i..".json",name=name,document=d} end
 return entries
end
D.open_template_library(test_view)
test_view._hed_library.name=doc.name
Paging.refresh(test_view,test_settings)
test_view._hed_library.pending={kind="load",doc=doc}
test_view._hed_library.status=D:localize("template_load_hint")
Paging.refresh(test_view,test_settings)
D.presets.list=old_list
''')
            result[lang+'_templates']=plain_items(view._hcm_ui)
            result[lang+'_templates'].append(dict(key='hed_template_name',x=637,y=374,w=1140,h=50,
                text=view._hed_name_widget.content.input_text,font=24,fill=True,input=True))
            L.execute('click_control("template_delete")')
            result[lang+'_delete_template']=plain_items(view._hcm_ui)
            result[lang+'_delete_template'].append(dict(key='hed_template_name',x=637,y=374,w=1140,h=50,
                text=view._hed_name_widget.content.input_text,font=24,fill=True,input=True))
            for part in ('shade','border','body'):
                style=view._hed_delete_backdrop.style[part]
                result[lang+'_delete_template'].append(dict(key='delete_'+part,x=style.offset[1],y=style.offset[2],
                    w=style.size[1],h=style.size[2],z=style.offset[3],text='',overlay=True,panel=True,
                    rgba=[style.color[i] for i in (2,3,4,1)]))
            L.globals().mods.HavocEnemyDirector.cleanup_template_ui()
assert result and all(not re.search(r'<ui_\d+>|%[dfs]',i['text']) for items in result.values() for i in items)
layout_output.parent.mkdir(parents=True,exist_ok=True)
layout_output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Exported',len(result),'localized pages for',PROJECT.name)
