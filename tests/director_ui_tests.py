"""Exercise the new pages through live widget callbacks and export real layouts."""
from pathlib import Path
import sys,runpy,json
HED_PROJECT=Path(__file__).resolve().parents[1]
HCM_TESTS=HED_PROJECT.parent/"HavocConditionManager/tests"
sys.path.insert(0,str(HCM_TESTS))
environment=runpy.run_path(str(HCM_TESTS/"native_ui_tests.py"))
L=environment["L"];plain_items=environment["plain_items"];load_mod=environment["load_mod"]
L.execute("""
test_language="zh-cn"
local D=mods.HavocEnemyDirector
assert(D.restore_defaults())
view._hcm_page=4;view._hed_section="overview";view._hed_tab="parameters";view._hcm_choice=nil;refresh()
click("hed_director_enabled")
assert(D.peek_config().director.enabled)
edit("hed_director_admission_interval_value","3")
assert(D.peek_config().director.admission_interval==3)
click("hed_overview_seeds")
assert(select(2,find("hed_director_seed_value")).content.hotspot.disabled and select(2,find("hed_layout_seed_value")).content.hotspot.disabled)
click("hed_director_seed_enabled");click("hed_layout_seed_enabled")
edit("hed_director_seed_value","2147483646")
edit("hed_layout_seed_value","888")
assert(D.peek_config().director.seed==2147483646 and D.peek_config().seed==888)
click("hed_director_seed_enabled");click("hed_layout_seed_enabled")
assert(not D.peek_config().director.seed_enabled and not D.peek_config().seed_enabled)
assert(D.peek_config().director.seed==2147483646 and D.peek_config().seed==888 and D.get_config().seed==nil)
assert(select(2,find("hed_director_seed_value")).content.hotspot.disabled and select(2,find("hed_layout_seed_value")).content.hotspot.disabled)
click("hed_director_seed_enabled");click("hed_layout_seed_enabled")
assert(D.get_config().seed==888)
click("hed_section_formations")
click("hed_form_new_family")
local checked,total=0,0
for _,item in ipairs(view._hcm_ui.items) do
    if item.key:find("^choice_hed_form_new_family_") then
        total=total+1;if item.checkbox then checked=checked+1;assert(item.selected) end
    end
end
assert(total==5 and checked==1)
click("choice_hed_form_new_family_hordes")
click("hed_form_add")
local f=D.peek_config().formations[1]
assert(f and #f.variants==1)
click("hed_form_name")
assert(view._hed_text and view._hed_text_widget and find("hed_section_overview").blocked)
view._hed_text_widget.content.input_text="第一独立编队"
click("hed_text_save")
assert(not view._hed_text and D.peek_config().formations[1].name=="第一独立编队")
edit("hed_member_amount_1_1","3");edit("hed_member_amount_1_2","5")
assert(D.peek_config().formations[1].variants[1].members[1].amount[1]==3)
click("hed_form_variant_add")
edit("hed_form_weight_value","2")
assert(#D.peek_config().formations[1].variants==2 and D.peek_config().formations[1].variants[2].weight==2)
click("hed_form_copy")
assert(#D.peek_config().formations==2 and D.peek_config().formations[1].id~=D.peek_config().formations[2].id)
click("hed_section_deployments")
click("hed_deploy_add")
local first=D.peek_config().deployments[1].id
click("hed_deploy_trigger");click("choice_hed_deploy_trigger_condition")
assert(view._hed_deployment_tab=="conditions" and #D.peek_config().deployments[1].conditions.clauses==1)
edit("hed_deploy_condition_value_1","42")
assert(D.peek_config().deployments[1].conditions.clauses[1].value==42)
assert(not find("hed_deploy_condition_remove_1").action)
click("hed_deploy_tab_quotas")
edit("hed_deploy_max_occurrences_value","7")
click("hed_deploy_copy")
assert(#D.peek_config().deployments==2 and D.peek_config().deployments[2].id~=first)
assert(D.peek_config().deployments[1].max_occurrences==7 and D.peek_config().deployments[2].max_occurrences==7)
edit("hed_deploy_max_occurrences_value","2")
assert(D.peek_config().deployments[1].max_occurrences==7)
click("hed_deploy_tab_inheritance")
click("hed_deploy_inherit_size")
edit("hed_deploy_size_multiplier_value","1.5")
assert(not D.peek_config().deployments[2].inherit_size and D.peek_config().deployments[2].size_multiplier==1.5)
-- A referenced formation cannot be removed by the list's delete control.
click("hed_section_formations")
view._hed_formation_id=D.peek_config().formations[1].id;refresh()
assert(not find("hed_form_delete").action)
-- Native values support an explicit relative mode, with separate HCM/source
-- cards and a multiplier edit. Percentage fields present 0.25 as 25.
click("hed_section_native")
view._hed_family="specials";view._hed_entry="specials/default_specials/1";view._hed_item="max_alive_specials";view._hed_path={};refresh()
click("hed_value_mode");click("choice_hed_value_mode_relative")
edit("hed_relative_value","1.5")
assert(D.peek_config().relative["specials/default_specials/1"].max_alive_specials==1.5)
assert(find("hed_field_base") and find("hed_field_coarse") and find("hed_field_effective"))
local entry,item
for _,candidate in ipairs(A.entries) do
    for _,field in ipairs(candidate.items) do if field.kind=="number" and field.definition.unit=="percent" then entry=candidate;item=field;break end end
    if item then break end
end
assert(item)
view._hed_family=entry.family;view._hed_entry=entry.id;view._hed_item=item.id;view._hed_path={};refresh()
edit("hed_value_value","25")
assert(D.peek_config().patches[entry.id][item.id]==0.25)
assert(find("hed_value_value").text=="25" and not find("hed_field_effective").text:find("%%%%",1,true))
local doc=assert(D.presets.capture("Director round trip"))
assert(doc.version==4 and #doc.config.formations==2 and #doc.config.deployments==2 and doc.config.director.seed==2147483646)
assert(D.restore_defaults());assert(D.presets.apply(doc))
assert(#D.peek_config().deployments==2 and D.peek_config().director.seed==2147483646)
print("Director UI: navigation, seed input, checked dropdown rows, name modal, formations/variants, independent rule copies, references, conditions, relative overrides and percent units: PASS")
""")

layouts={}
for language in ("en","zh-cn","zh-tw"):
    L.globals().test_language=language
    L.globals().Paging=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging")
    # Each language uses localized example names, rather than translating a
    # user's arbitrary saved name during rendering.
    L.execute("""
    local D=mods.HavocEnemyDirector
    assert(D.restore_defaults())
    local cfg=D.get_saved_config()
    cfg.director.enabled=true;cfg.director.mode="adaptive";cfg.director.seed=2147483646;cfg.director.seed_enabled=true;cfg.seed=2147483646;cfg.seed_enabled=true
    local f=D.director_config.new_formation(cfg,D:localize("director_new_formation",1),"hordes","chaos_poxwalker")
    f.variants[1].members={{name="chaos_poxwalker",amount={12,18}},{name="renegade_berzerker",amount={2,3}}}
    f.variants[2]=S.copy(f.variants[1]);f.variants[2].weight=2
    local d=D.director_config.new_deployment(cfg,D:localize("director_new_deployment",1),f.id)
    d.conditions.clauses={{condition="load_max",value=35},{condition="players_min",value=2},{condition="monster_idle"}}
    assert(D.save_config(cfg))
    view._hcm_page=4;view._hcm_choice=nil;view._hcm_offsets={};view._hed_status=nil
    view._hed_formation_id=f.id;view._hed_deployment_id=d.id;view._hed_variant=1
    """)
    states={
        "overview":'view._hed_section="overview";view._hed_overview_tab="general"',
        "pressure":'view._hed_section="overview";view._hed_overview_tab="pressure"',
        "seeds":'view._hed_section="overview";view._hed_overview_tab="seeds"',
        "seeds-off":'local c=mods.HavocEnemyDirector.get_saved_config();c.director.seed_enabled=false;c.seed_enabled=false;assert(mods.HavocEnemyDirector.save_config(c));view._hed_section="overview";view._hed_overview_tab="seeds"',
        "summary":'view._hed_section="overview";view._hed_overview_tab="summary"',
        "formations":'view._hed_section="formations"',
        "deployment-time":'view._hed_section="deployments";view._hed_deployment_tab="timing"',
        "deployment-conditions":'view._hed_section="deployments";view._hed_deployment_tab="conditions"',
        "deployment-quotas":'view._hed_section="deployments";view._hed_deployment_tab="quotas"',
        "deployment-hcm":'view._hed_section="deployments";view._hed_deployment_tab="inheritance"',
        "native":'view._hed_section="native";view._hed_tab="parameters";view._hed_family="specials";view._hed_entry="specials/default_specials/1";view._hed_path={};view._hed_item="max_alive_specials"',
        "native-relative":'mods.HavocEnemyDirector.set_relative("specials/default_specials/1","max_alive_specials",1.5);view._hed_section="native";view._hed_tab="parameters";view._hed_family="specials";view._hed_entry="specials/default_specials/1";view._hed_path={};view._hed_item="max_alive_specials"',
        "native-rules":'view._hed_section="native";view._hed_tab="rules";view._hed_family="specials";view._hed_entry="specials/default_specials/1"',
    }
    for name,setup in states.items():
        L.execute(setup+";refresh()")
        records=plain_items(L.globals().view._hcm_ui)
        assert all(item["x"]>=0 and item["y"]>=0 and item["x"]+item["w"]<=1920 and item["y"]+item["h"]<=1080 for item in records),(language,name)
        layouts[language+"_"+name]=records
    L.execute('view._hed_section="formations";refresh();click("hed_form_name")')
    records=plain_items(L.globals().view._hcm_ui)
    records.append(dict(key="director_name_input",x=550,y=465,w=820,h=56,text=L.globals().view._hed_text_widget.content.input_text,font=24,input=True))
    layouts[language+"_name-input"]=records
    L.execute('click("hed_text_cancel");click("hed_form_new_family")')
    layouts[language+"_category-menu"]=plain_items(L.globals().view._hcm_ui)
    L.execute('view._hcm_choice=nil;view._hed_section="presets";view._hed_tab="presets";refresh()')
    records=plain_items(L.globals().view._hcm_ui)
    layouts[language+"_presets"]=records
    L.execute('mods.HavocEnemyDirector.cleanup_template_ui();view._hed_tab="parameters"')
out=HED_PROJECT/"build/checks/director-ui-layouts.json"
out.write_text(json.dumps(layouts,ensure_ascii=False,indent=2),encoding="utf-8")
print("Exported",len(layouts),"director layouts:",out)
