# Execute the game's own wave function, not a reimplementation of its rules.
native_horde_source=(game/'scripts/managers/pacing/horde_pacing/horde_pacing.lua').read_text(encoding='utf-8')
native_wave=native_horde_source.split('HordePacing._spawn_trickle_horde_wave = function',1)[1].split('\nend',1)[0]
L.globals().native_rotten_wave=L.execute('''
local HordeTemplates=require("scripts/managers/horde/horde_templates")
local HORDE_TYPES={trickle_horde="trickle_horde"}
return function'''+native_wave+'\nend')
L.execute('''
local D=mods.HavocEnemyDirector
local base=mods.HavocConditionManager
local selected=base:get("havoc_circumstances_serialized")
base:set("havoc_circumstances_serialized","mutator_havoc_rotten_armor")
local native=require("scripts/settings/mutator/mutator_templates").mutator_live_rotten_armor_trickle_horde.trickle_horde_templates[1]
local saved_state,saved_event=Managers.state,Managers.event
local captured,paused
local pacing={current_faction=function() return "renegade" end,current_stage_name=function() end,
    current_density_type=function() return "high" end,waiting_for_ramp_clear=function() return false end,
    pause_spawn_type=function(_,kind,enabled,reason,duration) paused[kind]=duration end}
Managers.event={trigger=function() end}
Managers.state={pacing=pacing,extension={system=function() return {group_from_id=function() return {} end} end}}
local owner={_spawn_horde=function(_,_,_,comp) captured=comp; return true,{}, {},1 end}
for tier=1,5 do
    captured=nil; paused={}
    Managers.state.difficulty={get_table_entry_by_resistance=function(_,t) return t[math.min(tier,#t)] end,
        get_table_entry_by_challenge=function(_,t) return t[math.min(tier,#t)] end}
    local success=native_rotten_wave(owner,2,1,nil,nil,native,{pause_pacing_on_spawn=native.pause_pacing_on_spawn},0)
    assert(success and captured)
    local pool=D.planner.collect(captured,D.breeds)
    assert(pool.chaos_ogryn_executor and pool.renegade_executor and pool.renegade_berzerker)
    local count=0; for _ in pairs(pool) do count=count+1 end
    assert(count==3,"The native rotten-armor reinforcement contains exactly these three breed types")
    local source
    for _,s in ipairs(D.collect_sources(true)) do if s.id=="mutator_live_rotten_armor_trickle_horde:1" then source=s end end
    assert(source and source.rules)
    for kind,duration in pairs(paused) do assert(source.rules.pause[kind]==duration) end
end
local original_status=ScriptUnit.extension
local status=require("scripts/utilities/attack/player_unit_status")
local original_help=status.requires_help
status.requires_help=function(state) return state.disabled end
local players={{disabled=false},{disabled=false}}
ScriptUnit.extension=function(unit) return {read_component=function() return unit end} end
Managers.state.extension={system=function() return {get_side=function() return {valid_player_units=players} end} end}
local active_hordes=0
Managers.state.horde={num_active_hordes=function() return active_hordes end}
Managers.state.terror_event={num_active_events=function() return 0 end}
local g={rules={min_players=native.min_players_alive,active_limit=native.num_trickle_hordes_active_for_cooldown,
    cooldown=(native.trickle_horde_cooldown[1]+native.trickle_horde_cooldown[2])/2}}
assert(D.source_allowed(g,{},0))
players[2].disabled=true; assert(not D.source_allowed(g,{},0))
players[2].disabled=false; active_hordes=native.num_trickle_hordes_active_for_cooldown
local next_at={}; assert(not D.source_allowed(g,next_at,0) and next_at.cooldown>0)
active_hordes=0
assert(D.source_allowed(g,next_at,1),"Cooldown must clear when native active-horde condition clears; it is not a fixed timer")
ScriptUnit.extension=original_status; status.requires_help=original_help
Managers.state=saved_state; Managers.event=saved_event
base:set("havoc_circumstances_serialized",selected)
''')
print('Executed native rotten-armor wave function at 5 tiers: exact three-breed composition and pause rules; minimum non-disabled players and conditional active-horde cooldown: PASS')
