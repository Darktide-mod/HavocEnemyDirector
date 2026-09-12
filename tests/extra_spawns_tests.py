# Runs inside the real-template integration harness.
L.execute('''
local D,B=mods.HavocEnemyDirector,mods.HavocConditionManager
local P=D.planner
local saved_cfg,saved_state,saved_selection,saved_authority=D.get_config(),Managers.state,B.get_selected_conditions,B.has_local_gameplay_authority
D.reset_runtime(); Managers.state={}; B.has_local_gameplay_authority=function() return true end
B.get_selected_conditions=function() return {} end
assert(P.config({}).native_extras_enabled and P.defaults().native_extras_enabled)
local cfg=P.defaults(); cfg.native_extras_enabled=false; D.save_config(cfg)
test_view._hcm_page=4; test_view._hcm_choice=nil; Paging.refresh(test_view,test_settings)
assert(find_control("native_extras") and not D.get_config().native_extras_enabled)
click_control("native_extras"); assert(D.get_config().native_extras_enabled)
click_control("native_extras"); assert(not D.get_config().native_extras_enabled)
B.get_selected_conditions=function() return {"hcm_auric_patrols","hcm_auric_hounds"} end
D.synchronize_conditions(); assert(not D.get_config().native_extras_enabled)
D.restore_defaults(); assert(not D.get_config().native_extras_enabled)
assert(D.collect_sources(true).forced_boss_patrols)
B.get_selected_conditions=function() return {"hcm_auric_hounds"} end
D.synchronize_conditions(); assert(not D.collect_sources(true).forced_boss_patrols)
local source_count=#D.collect_sources(true)
local current=D.get_config(); current.native_extras_enabled=true; D.save_config(current)
assert(#D.collect_sources(true)==source_count,"Switch must not edit condition sources")
local function hook_for(name)
    for _,h in ipairs(hooks) do if h.owner==D and h.name==name then return h.fn end end
    error("Missing hook "..name)
end
local PM=game_classes["scripts/managers/pacing/pacing_manager"]
local SP=game_classes["scripts/managers/pacing/specials_pacing/specials_pacing"]
local t=test_templates.havoc
local pacing=setmetatable({_template=t,_horde_pacing={_template=t.horde_pacing_template.resistance_templates[5]},
    _specials_pacing=setmetatable({_template=t.specials_pacing_template.resistance_templates[5]},{__index=SP})},{__index=PM})
local ids={"hcm_auric_hounds"}
Managers.state={pacing=pacing,difficulty={get_parsed_havoc_data=function() return {circumstances=ids} end,
    get_table_entry_by_resistance=function(_,v) return v[math.min(5,#v)] end,
    get_table_entry_by_challenge=function(_,v) return v[math.min(5,#v)] end}}
local originals=0
local function original(self,a,b) originals=originals+1; assert(a==17 and b==23); return "retained",a end
local mechanisms={"_update_rush_prevention","_update_loner_prevention","_update_speed_running_prevention","_update_special_injection","_spawn_boss_patrol"}
for _,name in ipairs(mechanisms) do assert(hook_for(name)(original,{},17,23)=="retained") end
current.native_extras_enabled=false; current.havoc_twins_enabled=false; D.save_config(current)
for _,name in ipairs(mechanisms) do assert(hook_for(name)(original,{},17,23)==nil) end
assert(originals==5)
-- Condition-required patrols retain their native route; ordinary patrols do not.
ids={"hcm_auric_patrols"}
assert(hook_for("_spawn_boss_patrol")(original,{},17,23)=="retained")
ids={"hcm_auric_hounds"}
assert(hook_for("_spawn_boss_patrol")(original,{},17,23)==nil)
-- Common injected API and tagged event slots remain usable with extras off.
for _,h in ipairs(hooks) do assert(not (h.owner==D and h.name=="try_inject_special")) end
local spawn=hook_for("_spawn_special")
for _,tag in ipairs({"condition","mission","auto_event"}) do
    local slot={injected=true,breed_name="renegade_netgunner",optional_auto_event_id=tag=="auto_event" and "event-1" or nil}
    assert(spawn(function(_,s) assert(s==slot); return tag end,pacing._specials_pacing,slot)==tag)
end
-- Settings are a mission snapshot, including the forced-patrol exception.
D.update_director(0.25)
assert(not D.get_session_config().native_extras_enabled)
assert(not D.get_session_config().havoc_twins_enabled)
current.native_extras_enabled=true; current.havoc_twins_enabled=true; D.save_config(current)
assert(not D.get_session_config().native_extras_enabled)
assert(not D.get_session_config().havoc_twins_enabled)
assert(hook_for("_update_rush_prevention")(original,{},17,23)==nil)
D.reset_runtime(); D.update_director(0.25)
assert(D.get_session_config().native_extras_enabled)
assert(D.get_session_config().havoc_twins_enabled)
assert(hook_for("_update_rush_prevention")(original,{},17,23)=="retained")
D.reset_runtime(); current.enabled=false; current.native_extras_enabled=false; D.save_config(current)
for _,name in ipairs(mechanisms) do assert(hook_for(name)(original,{},17,23)=="retained") end
current.enabled=true; D.save_config(current); B.has_local_gameplay_authority=function() return false end
for _,name in ipairs(mechanisms) do assert(hook_for(name)(original,{},17,23)=="retained") end
D.reset_runtime(); Managers.state=saved_state; B.get_selected_conditions=saved_selection; B.has_local_gameplay_authority=saved_authority
D.save_config(saved_cfg)
''')
print('Extra-spawn switch: UI persistence, all five producer routes, forced native patrols/events, unchanged condition sources, mission snapshot and inactive/remote pass-through: PASS')
