"""Run native event nodes and the native event state machine with scene spawning off."""
from pathlib import Path
import subprocess
import sys


def run():
    from project_env import PROJECT, GAME, SOURCES
    root = PROJECT
    
    from lupa.luajit21 import LuaRuntime
    lua = LuaRuntime(unpack_returned_tuples=True)

    def source(path):
        return subprocess.check_output(['git', 'show', 'HEAD:' + path + '.lua'], cwd=GAME).decode('utf-8-sig')

    lua.execute('''
deps={}; registrations={}; native_injections=0; flow_count=0
function require(path) return assert(deps[path],path) end
function class() return {} end
function settings(_,v) return v end
function table.clear(t) for k in pairs(t) do t[k]=nil end end
function table.clone(t) local r={} for k,v in pairs(t) do r[k]=v end return r end
function table.array_contains(t,v) for _,a in ipairs(t) do if a==v then return true end end end
for _,path in ipairs({"scripts/managers/bot/bot_spawning","scripts/settings/breed/breeds",
    "scripts/utilities/minion_attack_selection/minion_attack_selection","scripts/foundation/utilities/script_world",
    "scripts/utilities/loaded_dice","scripts/settings/terror_event/terror_event_templates"}) do deps[path]={} end
deps["scripts/settings/perception/perception_settings"]={aggro_states={}}
deps["scripts/settings/difficulty/minion_difficulty_settings"]={terror_event_point_costs=1,terror_event_duration_modifier=1}
deps["scripts/settings/horde/horde_settings"]={horde_types={trickle_horde="trickle_horde"}}
deps["scripts/managers/terror_event/terror_trickle_templates"]={standard_melee={num_waves={1,1}}}
deps["scripts/managers/terror_event/utilities/terror_event_queries"]={num_alive_minions=function() return 0 end}
deps["scripts/utilities/breed_queries"]={match_minions_by_tags=function() return {} end,
    pick_random_minion_by_points=function() return {name="renegade_netgunner"},1 end}
local side={side_id=2,relation_sides=function() return {{side_id=1}} end}
local side_system={get_side_from_name=function() return side end}
Managers={event={trigger=function() end},state={
    difficulty={get_table_entry_by_resistance=function(_,v) return v end},
    pacing={spawn_type_allowed=function() return false end,current_faction=function() return "renegade" end,
        try_inject_special=function() native_injections=native_injections+1 end},
    extension={system=function(_,name)
        if name=="side_system" then return side_system end
        if name=="fx_system" then return {trigger_wwise_event=function() end} end
        error(name)
    end}}}
active=true; cfg={generators={scripted_encounters={deleted=true}},native_extras_enabled=false}
mod={is_active=function() return active end,get_session_config=function() return cfg end}
function get_mod() return mod end
function mod:hook_require(path,fn) registrations[path]=fn end
function mod:hook(target,key,fn)
    local original=assert(target[key],key)
    target[key]=function(...) return fn(original,...) end
end
''')
    nodes_path = 'scripts/managers/terror_event/terror_event_nodes'
    manager_path = 'scripts/managers/terror_event/terror_event_manager'
    lua.globals().deps[nodes_path] = lua.execute(source(nodes_path))
    lua.globals().deps[manager_path] = lua.execute(source(manager_path))
    lua.globals().court = lua.execute(source('scripts/settings/terror_event/terror_event_templates/terror_events_km_enforcer'))
    lua.execute('''
Nodes=require("scripts/managers/terror_event/terror_event_nodes")
Manager=require("scripts/managers/terror_event/terror_event_manager")
native_flow=Nodes.flow_event.init
native_named_spawn=Nodes.spawn_by_breed_name.init
native_twin_fight=Nodes.start_twin_fight.init
manager=setmetatable({_terror_trickle_data={},trigger_network_synced_level_flow=function() flow_count=flow_count+1 end},{__index=Manager})
Managers.state.terror_event=manager
''')
    if '--unpatched' not in sys.argv:
        module = PROJECT / 'src/HavocEnemyDirector/scripts/mods/HavocEnemyDirector/mission_events.lua'
        lua.execute(module.read_text(encoding='utf-8'))
        lua.execute('for path,fn in pairs(registrations) do fn(require(path)) end')
    lua.execute('''
local wave={"spawn_by_points",points=12,breed_tags={{"close","elite"}}}
assert(Nodes.spawn_by_points.update(wave,{},0,0)==true,"Disabled scene must complete the wave without spawning or waiting")
Nodes.try_inject_special_minion.init({points=12,breed_tags={{"special"}}},{},0)
manager:start_terror_trickle("standard_melee","test",0)
assert(native_injections==0 and not manager._terror_trickle_data.active)
-- Native task actors and objective waves are retained, not silently cancelled.
assert(Nodes.flow_event.init==native_flow and Nodes.spawn_by_breed_name.init==native_named_spawn)
assert(Nodes.start_twin_fight.init==native_twin_fight)
for _,node in ipairs({{mission_objective_id="kill_target"},{side_name="heroes"},{breed_tags={{"captain"}}}}) do
    assert(Nodes.spawn_by_points.update(node,{},0,0)==false)
end
-- Both open scenes and an inactive director keep the original behavior.
for _,case in ipairs({"enabled","inactive"}) do
    active=case~="inactive"; cfg.generators.scripted_encounters.deleted=case=="inactive"
    assert(Nodes.spawn_by_points.update(wave,{},0,0)==false)
    Nodes.try_inject_special_minion.init({points=12,breed_tags={{"special"}}},{},0)
    manager:start_terror_trickle("standard_melee","test",0)
    assert(manager._terror_trickle_data.active)
    manager:stop_terror_trickle()
end
assert(native_injections==2)
active=true; cfg.generators.scripted_encounters.deleted=true
local function run_event(nodes)
    local event={nodes=nodes,node_index=1,scratchpad={},spawned_minion_data={},data={level=1}}
    Nodes[nodes[1][1]].init(nodes[1],event,0)
    for tick=1,1000 do if manager:_update_event(event,100,tick*100) then return end end
    error("Event stopped advancing")
end
-- Use the actual map's two ascender waves, including delays and continue_when.
for _,name in ipairs({"event_ascender_trickle_a","event_ascender_trickle_b"}) do
    run_event(assert(court.events[name]))
    assert(not manager._terror_trickle_data.active)
end
-- A skipped spawn followed by a door/level flow must reach that flow exactly once.
run_event({wave,{"try_inject_special_minion",points=12,breed_tags={{"special"}}},
    {"start_terror_trickle",template_name="standard_melee"},
    {"continue_when",condition=function() return true end},
    {"flow_event",flow_event_name="open_door"}})
assert(flow_count==1 and native_injections==2 and not manager._terror_trickle_data.active)
''')
    print('Native court ascender events: waves/injections/trickles blocked, delays/conditions/door flow advance; objective/named actors and disabled director pass through: PASS')


run()
