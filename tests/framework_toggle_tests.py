"""Run in the real-template harness. Exercise the installed DMF state machine."""
old_state=L.globals().Managers.state
old_ui=L.globals().Managers.ui
old_dmf=L.globals().mods.DMF
old_solo_authority=L.globals().mods.SoloPlay.has_local_gameplay_authority
old_context=L.globals().mods.SoloPlay._havoc_condition_manager_context_wrapper
old_view=L.globals().mods.SoloPlay._havoc_condition_manager_view_wrapper
for name in ('HavocConditionManager','HavocEnemyDirector'):
    data=load_mod(f'{name}/scripts/mods/{name}/{name}_data')
    assert data.is_togglable is True,name
    L.globals().mods[name]._togglable=True
L.execute('''
local dmf=new_test_mod("DMF")
for _,name in ipairs({"HavocConditionManager","HavocEnemyDirector"}) do
    local m=mods[name]
    function m:get_name() return name end
    function m:get_internal_data(key)
        if key=="is_togglable" then return self._togglable end
        if key=="is_enabled" then return self:is_enabled() end
        return false
    end
end
function dmf.set_internal_data(m,key,value) if key=="is_enabled" then m._enabled=value end end
function dmf.inject_hud_elements() end
function dmf.remove_injected_hud_elements() end
function dmf.mod_enabled_event(m,initial) if m.on_enabled then m.on_enabled(initial) end end
function dmf.mod_disabled_event(m,initial) if m.on_disabled then m.on_disabled(initial) end end
Managers.state={}
Managers.ui={view_instance=function() return nil end}
open_count=0; close_count=0; open_view=nil; closing=false
Managers.ui.view_instance=function() return open_view end
Managers.ui.is_view_closing=function() return closing end
Managers.ui.open_view=function(_,name) open_view={name=name}; closing=false; open_count=open_count+1 end
Managers.ui.close_view=function(_,name)
    assert(open_view and open_view.name==name and not closing,"duplicate native close")
    closing=true; close_count=close_count+1
end
toggle_authority=false
mods.SoloPlay.has_local_gameplay_authority=function() return toggle_authority end
''')
lua_file(FIXTURES/'mods/dmf/scripts/mods/dmf/modules/core/toggling.lua')
L.execute('''
local dmf,H,D=mods.DMF,mods.HavocConditionManager,mods.HavocEnemyDirector
dmf.initialize_mod_state(H); dmf.initialize_mod_state(D)
H.extend_condition_settings(test_settings)
assert(H:is_enabled() and D:is_enabled() and H._hooks_enabled and D._hooks_enabled)
local preferences=H:get("havoc_circumstances_serialized")
local configuration=D:get("director_config_v1")
D.open_settings(); assert(open_count==1 and D._open_settings_requested)
mods.SoloPlay._havoc_condition_manager_context_wrapper=function(marker) return {marker=marker,havoc_data="native"} end
mods.SoloPlay._havoc_condition_manager_view_wrapper=function(marker) return marker end
-- Reproduce the original false declaration: the actual DMF refuses the change.
H._togglable=false
dmf.mod_state_changed("HavocConditionManager",false)
assert(H:is_enabled())
H._togglable=true
dmf.mod_state_changed("HavocConditionManager",false)
assert(not H:is_enabled() and not H._hooks_enabled and not D._hooks_enabled)
assert(close_count==1 and not D._open_settings_requested)
-- The shared page may still be fading out; the HED notification must not close it twice.
H.close_condition_manager_view(); D.open_settings(); H.open_condition_manager_view()
assert(close_count==1 and open_count==1)
open_view=nil; closing=false
assert(test_settings.order.havoc_circumstances==hcm_native_order)
assert(test_settings.lookup.havoc_circumstances==hcm_native_lookup)
assert(not D.is_gameplay_enabled())
local context=mods.SoloPlay.gen_havoc_mission_context("unchanged")
assert(context.marker=="unchanged" and context.havoc_data=="native")
assert(H.apply_havoc_conditions(context)==context)
assert(mods.SoloPlay.open_solo_view("native menu")=="native menu")
assert(H:get("havoc_circumstances_serialized")==preferences)
-- Off state is persisted by DMF; initial calls must not create a pending mission toggle.
assert(dmf:get("disabled_mods_list").HavocConditionManager)
dmf.initialize_mod_state(H)
assert(not H:is_enabled() and not H._hooks_enabled)
dmf.mod_state_changed("HavocConditionManager",true)
assert(H._hooks_enabled and D._hooks_enabled and D.is_gameplay_enabled())
assert(not dmf:get("disabled_mods_list").HavocConditionManager)
dmf.mod_state_changed("HavocEnemyDirector",false)
assert(H._hooks_enabled and not D._hooks_enabled and not D.is_gameplay_enabled())
D.open_settings(); assert(open_count==1 and not D._open_settings_requested)
test_view._hcm_page=4
Paging.refresh(test_view,test_settings)
assert(test_view._hcm_ui.page_count==3 and test_view._hcm_page==3)
assert(not find_control("open_director"))
dmf.mod_state_changed("HavocEnemyDirector",true)
Paging.refresh(test_view,test_settings)
assert(test_view._hcm_ui.page_count==4)
-- Both enabled before a mission: disabling either retains its existing mission.
toggle_authority=true
Managers.state={game_session={},difficulty={get_parsed_havoc_data=function() return {circumstances={}} end}}
H.on_game_state_changed("enter","GameplayStateRun"); D.on_game_state_changed("enter","GameplayStateRun")
assert(H.is_gameplay_enabled() and D.is_gameplay_enabled())
dmf.mod_state_changed("HavocEnemyDirector",false)
assert(not D:is_enabled() and D._hooks_enabled and D.is_gameplay_enabled())
dmf.mod_state_changed("HavocConditionManager",false)
assert(not H:is_enabled() and H._hooks_enabled and H.is_gameplay_enabled())
assert(D._hooks_enabled and D.is_gameplay_enabled())
-- Event order must not matter, including reuse of the same session manager.
D.on_game_state_changed("exit","GameplayStateRun"); H.on_game_state_changed("exit","GameplayStateRun")
assert(not H._hooks_enabled and not D._hooks_enabled)
H.on_game_state_changed("enter","GameplayStateRun"); D.on_game_state_changed("enter","GameplayStateRun")
assert(not H.is_gameplay_enabled() and not D.is_gameplay_enabled())
-- Enabling during a run started disabled must also wait until the next mission.
dmf.mod_state_changed("HavocConditionManager",true)
dmf.mod_state_changed("HavocEnemyDirector",true)
assert(H:is_enabled() and D:is_enabled() and not H._hooks_enabled and not D._hooks_enabled)
assert(not H.is_gameplay_enabled() and not D.is_gameplay_enabled())
H.on_game_state_changed("exit","GameplayStateRun"); D.on_game_state_changed("exit","GameplayStateRun")
Managers.state={game_session={},difficulty={get_parsed_havoc_data=function() return {} end}}
D.on_game_state_changed("enter","GameplayStateRun"); H.on_game_state_changed("enter","GameplayStateRun")
assert(H._hooks_enabled and D._hooks_enabled and H.is_gameplay_enabled() and D.is_gameplay_enabled())
H.on_game_state_changed("exit","GameplayStateRun"); D.on_game_state_changed("exit","GameplayStateRun")
toggle_authority=false; Managers.state={}
-- A disabled parent in the hub suspends its enabled companion and restores it on enable.
dmf.mod_state_changed("HavocConditionManager",false)
assert(D:is_enabled() and not D.is_gameplay_enabled() and not D._hooks_enabled)
dmf.mod_state_changed("HavocConditionManager",true)
assert(D:is_enabled() and D.is_gameplay_enabled() and D._hooks_enabled)
assert(H:get("havoc_circumstances_serialized")==preferences)
''')
L.globals().Managers.state=old_state
L.globals().Managers.ui=old_ui
L.globals().mods.DMF=old_dmf
L.globals().mods.SoloPlay.has_local_gameplay_authority=old_solo_authority
L.globals().mods.SoloPlay._havoc_condition_manager_context_wrapper=old_context
L.globals().mods.SoloPlay._havoc_condition_manager_view_wrapper=old_view
print('Installed DMF toggling: original refusal reproduced; HCM/HED declarations, persisted states, native menu/context, dependent director, hub/mission boundaries, both event orders, hidden disabled page: PASS')
