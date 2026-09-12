"""Run native slot updates/injections with the director's ordinary-slot pause."""
from project_env import GAME, SOURCES
from lupa.luajit21 import LuaRuntime
L=LuaRuntime(unpack_returned_tuples=True)
path=GAME/'scripts/managers/pacing/specials_pacing/specials_pacing.lua'
source=path.read_text(encoding='utf-8-sig')
def native(name,prefix=''):
    body=source.split('SpecialsPacing.'+name+' = function',1)[1].split('\nend',1)[0]
    return L.execute(prefix+'\nreturn function'+body+'\nend')
L.execute('''
SP={}; D={}; active=true; attempts=0; disablers=0; failures=0; cleanup=0
function D.is_active() return active end
function D:hook(target,name,fn)
    local original=target[name]; target[name]=function(...) return fn(original,...) end
end
function table.clear(t) for k in pairs(t) do t[k]=nil end end
function math.random_range(a,b) return (a+b)/2 end
HEALTH_ALIVE={living=true}; Log={info=function() end}
Managers={state={pacing={get_mission_progression=function() return 100,0,0 end,
    spawn_type_enabled=function() return true end,spawn_type_allowed=function() return true end,
    get_ramp_up_frequency_modifier=function() return 1 end,total_challenge_rating=function() return 0 end},
    mutator={mutator=function() end}},server_metrics={add_annotation=function() failures=failures+1 end}}
function SP:_travel_distance_spawning() return false end
function SP:_get_timer_reduction_multiplier() return 1 end
function SP:_get_special_slot_breed_name(slot) return slot.breed_name end
function SP:_check_disabler_override() disablers=disablers+1 end
function SP:_spawn_special(slot)
    attempts=attempts+1
    if slot.injected then return true,"injected" end
    return false
end
function SP:_on_special_spawned(slot,unit) slot.spawned=true; slot.spawned_unit=unit end
function SP:_check_stuck_special() cleanup=cleanup+1 end
function SP:_check_and_activate_coordinated_strike() return false end
function SP:_check_monster_override() end
function SP:_update_rush_prevention() end
function SP:_update_loner_prevention() end
function SP:_update_speed_running_prevention()
    if self.inject_during_update then
        self.inject_during_update=nil
        assert(self:try_inject_special("renegade_sniper",nil,nil,nil,nil,nil,nil,"condition_event"))
    end
end
function instance(slots)
    return setmetatable({_specials_slots=slots,_max_alive_specials=#slots,_old_furthest_travel_distance=100,
        _template={spawn_failed_wait_time=1,foreshadow_stinger_timers={},foreshadow_stingers={},timer_range={2,2},min_timer_diff_range={0,0},
            breeds={all={"renegade_sniper"}},max_of_same={}},
        _timer_modifier=1,_timer_multiplier=1,_num_spawned_specials=1},{__index=SP})
end
''')
prefix='''local TRAVEL_DISTANCE_CHANGE_ALLOWANCE_BEHIND_MIN=5
local TRAVEL_DISTANCE_CHANGE_ALLOWANCE_BEHIND_MAX=15
local TRAVEL_DISTANCE_CHANGE_ALLOWANCE_FORWARD_MIN=8
local TRAVEL_DISTANCE_CHANGE_ALLOWANCE_FORWARD_MAX=20
local NO_MODIFIER_TIME=10
local HORDE_TYPES={}
'''
L.globals().SP.update=native('update',prefix)
L.globals().SP.try_inject_special=native('try_inject_special')
L.globals().SP._setup_specials_slot=native('_setup_specials_slot','local USED_BREEDS={}')
L.execute('''
local ordinary=instance({{spawn_timer=0,breed_name="renegade_sniper"}})
for i=1,100 do ordinary:update(0.1,i*0.1,1,1) end
assert(failures>1 and disablers==attempts,"Reproduce repeated failed native ordinary slots")
''')
install=L.execute((SOURCES/'HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_specials.lua').read_text(encoding='utf-8-sig'))
install(L.globals().D,L.globals().SP)
L.execute('''
attempts=0; disablers=0; failures=0
local expired={spawn_timer=-1,breed_name="renegade_sniper"}
local positive={spawn_timer=2,foreshadow_stinger="cue",foreshadow_stinger_timer=0}
local s=instance({expired,positive})
for i=1,600 do s:update(1/60,i/60,1,1) end
assert(attempts==0 and disablers==0 and failures==0)
assert(expired.spawn_timer==-1 and positive.spawn_timer==2 and positive.foreshadow_stinger_timer==0)
assert(s._only_update_injected_specials==nil and expired._hed_parked_timer==nil)
-- Injection into a temporarily parked slot uses native setup; don't restore its old timer.
s.inject_during_update=true; s:update(0.1,11,1,1)
assert(expired.injected and expired.spawn_timer==0 and expired.optional_auto_event_id=="condition_event")
s:update(0.1,11.1,1,1)
assert(attempts==1 and expired.spawned and expired.spawned_unit=="injected")
-- Existing native live/queued/dead slots keep bookkeeping and cleanup.
local queued={spawn_timer=0,spawner_queue_id=7,spawner={is_spawning=function() return false end,
    spawned_minions_by_queue_id=function(_,id) assert(id==7); return {"queued"} end}}
local dead={spawned=true,spawned_unit="dead",spawn_timer=0}
local live={spawned=true,spawned_unit="living",next_stuck_check_t=0,spawn_timer=0}
local owned=instance({queued,dead,live}); owned._only_update_injected_specials=false
owned:update(0.1,12,1,1)
assert(queued.spawned_unit=="queued" and not dead.spawned and dead.spawn_timer==2 and cleanup==1)
assert(owned._only_update_injected_specials==false)
-- Disabled/client/native paths do not park, including an existing native true flag.
active=false; local passthrough=instance({{spawn_timer=0}})
passthrough._only_update_injected_specials=true
local n=attempts; passthrough:update(0.1,13,1,1)
assert(attempts==n+1 and passthrough._only_update_injected_specials==true)
-- No temporary state is left after failure, template replacement or mission exit.
active=true; local broken=instance({{spawn_timer=-2}})
broken._update_speed_running_prevention=function() error("simulated native failure") end
assert(not pcall(broken.update,broken,0.1,14,1,1))
assert(broken._only_update_injected_specials==nil and broken._specials_slots[1].spawn_timer==-2)
local old=broken._specials_slots
broken._update_speed_running_prevention=function(self) self._specials_slots={{spawn_timer=8}} end
broken:update(0.1,15,1,1)
assert(old[1].spawn_timer==-2 and broken._specials_slots[1].spawn_timer==8)
''')
print('Native specials: repeated ordinary attempts/overrides/telemetry removed; native injections, live/queued/dead slots, disabled paths, exception and template-change restoration: PASS')
