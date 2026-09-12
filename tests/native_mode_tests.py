# Runs in the shared real-template harness.
L.execute("""
local D,B=mods.HavocEnemyDirector,mods.HavocConditionManager
local saved_cfg,saved_state,saved_authority=D.get_config(),Managers.state,B.has_local_gameplay_authority
D.reset_runtime(); B.has_local_gameplay_authority=function() return true end
local cfg=D.get_config(); cfg.enabled=true; D.save_config(cfg)
test_view._hcm_page=4; test_view._hcm_choice=nil; test_view._hcm_number=nil
Paging.refresh(test_view,test_settings)
local stale_action=find_control("total_cap_plus").action
local stale_set=find_control("total_cap_value").number.set
local stale_choice=test_view._hcm_ui.choices.new_category.choose
local saved_category=test_view._hed_add_category
click_control("total_cap_value")
assert(test_view._hcm_number)
local stale_edit=test_view._hcm_number
cfg=D.get_config(); cfg.enabled=false; cfg.native_extras_enabled=false; cfg.havoc_twins_enabled=false
cfg.generators.scripted_encounters={deleted=true}; D.save_config(cfg)
Paging.refresh(test_view,test_settings)
assert(not test_view._hcm_number and not test_view._hcm_hold and not test_view._hcm_ui.popup)
local revision=D.get_config().revision
stale_action(); stale_set(999); stale_choice(4); stale_edit.spec.set(888)
assert(D.get_config().revision==revision and test_view._hed_add_category==saved_category)
for _,item in ipairs(test_view._hcm_ui.items) do
    if item.key~="director_enabled" and not item.key:match("^buff_proc_capacity_") and not item.key:match("^tab_") and item.key~="page_indicator" and item.key~="saved_status" then
        assert(item.blocked and not item.action and not item.number and not item.selected and item.color=="muted",item.key)
        local _,widget=find_control(item.key); assert(widget.content.hotspot.disabled)
        widget.content.hotspot.pressed_callback()
    end
end
assert(D.get_config().revision==revision)
assert(find_control("generator_count_effective").text=="—")
click_control("director_enabled"); click_control("choice_director_enabled_advanced")
assert(D.get_config().enabled and find_control("total_cap_value").number)
click_control("director_enabled"); click_control("choice_director_enabled_native")
assert(not D.get_config().enabled)
click_control("tab_3"); assert(find_control("multiplier_common5").action)
-- Native session must never compile/update custom generators or copy pacing data.
local t=test_templates.havoc
local pacing={_horde_pacing={_template=t.horde_pacing_template.resistance_templates[5]},
    _specials_pacing={_template=t.specials_pacing_template.resistance_templates[5]}}
Managers.state={pacing=pacing,difficulty={get_parsed_havoc_data=function() return {circumstances={}} end}}
local collect=D.collect_sources; D.collect_sources=function() error("Native runtime collected advanced sources") end
for i=1,120 do D.update_director(1/60) end
assert(not D.is_active())
local names={add_trickle_horde=true,_update_horde_pacing=true,_update_trickle_horde_pacing=true,
    _spawn_special=true,_update_rush_prevention=true,_update_loner_prevention=true,_update_speed_running_prevention=true,
    _update_special_injection=true,_spawn_boss_patrol=true,_spawn_monster=true,_fill_spawns_by_timer=true,spawn_group=true,
    spawn_type_enabled=true,mutator_breed_init=true,replacement_breed=true,horde=true,_limit_roamer_breeds=true,
    _try_activate_roamer=true,_trigger_runtime_spawn=true,_generate_roamers=true}
local reached={}
for _,h in ipairs(hooks) do
    if h.owner==D and names[h.name] then
        local owner,arg={},{}
        local result=h.fn(function(self,value) assert(self==owner and value==arg); return arg end,owner,arg)
        assert(result==arg,h.name); reached[h.name]=true
    elseif h.owner==D and h.name=="add_pacing_modifiers" then
        h.fn(pacing,{override_faction="renegade"}); assert(not pacing._hed_applied_modifiers)
    end
end
for name in pairs(names) do assert(reached[name],name) end
-- Saved mode changes cannot silently change a running native mission.
local next_cfg=D.get_config(); next_cfg.enabled=true; D.save_config(next_cfg)
assert(not D.is_active() and not D.get_session_config().enabled)
D.collect_sources=collect
D.reset_runtime(); assert(D.is_active())
Managers.state=saved_state; B.has_local_gameplay_authority=saved_authority; D.save_config(saved_cfg)
test_view._hcm_page=4; Paging.refresh(test_view,test_settings)
""")
print('Native mode: grey controls, stale edits/holds, mode and navigation; 20 native producer/pool/cap routes, no custom compilation or modifier copy, mission snapshot: PASS')
