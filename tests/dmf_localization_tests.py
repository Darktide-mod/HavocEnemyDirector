"""Run after integration setup; use the installed DMF formatter, not a permissive mock."""
dmf_file=FIXTURES/'mods/dmf/scripts/mods/dmf/modules/core/localization.lua'
dmf_source=dmf_file.read_text(encoding='utf-8-sig')
mod_names=('HavocConditionManager','HavocEnemyDirector')
old_user_setting=L.globals().Application.user_setting
old_localizers={name:L.globals().mods[name].localize for name in mod_names}
old_errors={name:L.globals().mods[name].error for name in mod_names}
checks=0
for language in ('en','zh-cn','zh-tw'):
    L.globals().test_language=language
    L.execute('''
Application.user_setting=function() return test_language end
DMFMod={}; CLASS.LocalizationManager={}
local dmf=new_test_mod("DMF")
dmf.io_dofile=function() return {} end
function dmf:get_name() return "DMF" end
dmf_errors={}
''')
    L.execute(dmf_source,name='@'+str(dmf_file))
    for name in mod_names:
        m=L.globals().mods[name]
        m.get_name=L.eval('function() return "'+name+'" end')
        m.error=L.eval('function(self,fmt,...) dmf_errors[#dmf_errors+1]=string.format(fmt,...) end')
        m.localize=L.globals().DMFMod.localize
        L.globals().mods.DMF.initialize_mod_localization(m,m.localization)
    # The exact old call must reproduce DMF's error + English fallback behavior.
    L.execute('''
assert(mods.HavocConditionManager:localize("ui_066")=="<ui_066>")
assert(#dmf_errors==2 and dmf_errors[1]:find("value expected",1,true))
dmf_errors={}
assert(mods.HavocConditionManager:localize("ui_066",2,4,6):find("2 / 4",1,true))
''')
    for name in mod_names:
        m=L.globals().mods[name]
        for key,value in m.localization.items():
            specs=re.findall(r'%(?:[-+ #0]*\d*(?:\.\d+)?[cdfgiousxXq]|%)',value[language])
            args=[3 for spec in specs if spec!='%%']
            result=m.localize(m,key,*args)
            assert isinstance(result,str) and result!='<'+key+'>',(name,key,language)
            checks+=1
    catalog=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_catalog')
    L.globals().mods.HavocConditionManager.condition_catalog=catalog
    catalog.extend(settings)
    load_mod('HavocEnemyDirector/scripts/mods/HavocEnemyDirector/editor')
    native_paging=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging')
    for page in range(1,5):
        view=L.globals().test_view
        view._hcm_page=page;view._hcm_choice=None;view._hcm_number=None
        native_paging.refresh(view,settings)
        for item in plain_items(view._hcm_ui):
            assert not re.search(r'<ui_\d+>|%[dfs]',item['text']),(language,page,item)
    # Explicitly render both status branches that contain decimal formatting.
    original_collect=L.globals().mods.HavocEnemyDirector.collect_sources
    L.execute('''
dmf_test_collect=mods.HavocEnemyDirector.collect_sources
mods.HavocEnemyDirector.collect_sources=function()
    return {{id="dmf_timer",kind="timer",pool={chaos_poxwalker=1},interval=20},
            {id="dmf_ambient",kind="ambient",pool={chaos_poxwalker=1},interval=20}}
end
dmf_test_generators=mods.HavocEnemyDirector.planner.compile(mods.HavocEnemyDirector.collect_sources(),
    mods.HavocEnemyDirector.planner.defaults(),mods.HavocEnemyDirector.breeds,mods.HavocEnemyDirector.category_for,mods.HavocEnemyDirector.preview_resolve)
''')
    assert len(L.globals().dmf_test_generators)>=2
    for g in L.globals().dmf_test_generators.values():
        L.globals().test_view._hed_generator_id=g.id
        native_paging.refresh(L.globals().test_view,settings)
    L.globals().mods.HavocEnemyDirector.collect_sources=original_collect
    errors=list(L.globals().dmf_errors.values())
    assert not errors,(language,errors)

for name in mod_names:
    L.globals().mods[name].localize=old_localizers[name]
    L.globals().mods[name].error=old_errors[name]
L.globals().Application.user_setting=old_user_setting
L.globals().test_language=None
print(f'Installed DMF formatter: original error reproduced; {checks} translations, all pages, timer/ambient status, zero errors after fix: PASS')
