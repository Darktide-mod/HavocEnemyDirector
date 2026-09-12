"""Actual runtime paths with counted engine calls, plus the native cleanup rule."""
from project_env import PROJECT, SOURCES, GAME
from lupa.luajit21 import LuaRuntime
L=LuaRuntime(unpack_returned_tuples=True)
def module(mod,name):
    return L.execute((SOURCES/mod/'scripts/mods'/mod/(name+'.lua')).read_text(encoding='utf-8-sig'))
L.globals().load_module=module
L.execute('''
D={}; B={}; hooks={}; deps={}; HEALTH_ALIVE={}; Managers={state={}}
function get_mod(name) return name=="HavocEnemyDirector" and D or B end
function D:io_dofile(path) return load_module("HavocEnemyDirector",path:match("([^/]+)$")) end
function B:io_dofile(path) return load_module("HavocConditionManager",path:match("([^/]+)$")) end
function B:get(key) return nil end
function B.has_local_gameplay_authority() return true end
function D.is_gameplay_enabled() return true end
function D:info(...) end
function D:hook(target,name,fn) hooks[name]={target=target,fn=fn} end
function D:hook_safe(target,name,fn) end
deps["scripts/settings/breed/breeds"]={
    chaos_poxwalker={name="chaos_poxwalker",tags={},breed_type="minion"},
    renegade_netgunner={name="renegade_netgunner",tags={special=true},breed_type="minion"},
    renegade_sniper={name="renegade_sniper",tags={special=true},breed_type="minion"}}
function require(path) deps[path]=deps[path] or {}; return deps[path] end
''')
L.globals().D.planner=module('HavocEnemyDirector','planner')
L.globals().D.capacity_stats=module('HavocEnemyDirector','capacity_stats')
module('HavocEnemyDirector','runtime')
L.execute('''
local P=D.planner
local registry=require("scripts/settings/breed/breeds")
local units,scans,lookups={},0,0
local MS=require("scripts/managers/minion/minion_spawn_manager")
local HM=require("scripts/managers/horde/horde_manager")
local minions=setmetatable({},{__index=MS})
function MS:spawned_minions() scans=scans+1; return units end
function MS:total_allocated_num_enemies() return #units end
function MS:replacement_breed() return nil end
function MS:spawn_minion(name)
    local unit={breed=registry[name]}; units[#units+1]=unit; HEALTH_ALIVE[unit]=true; return unit
end
function MS:unregister_unit(unit)
    for i,u in ipairs(units) do if u==unit then table.remove(units,i); return true end end
    return false
end
ScriptUnit={extension=function(unit) lookups=lookups+1; return {breed=function() return unit.breed end} end}
function HM:horde(_,_,_,_,comp)
    for _,e in ipairs(comp.breeds) do for i=1,e.amount[1] do minions:spawn_minion(e.name) end end
    return true
end
for _,name in ipairs({"spawn_minion","unregister_unit"}) do
    local h=hooks[name]; local original=h.target[name]
    h.target[name]=function(...) return h.fn(original,...) end
end
local pacing={_horde_pacing={_template={}},_specials_pacing={_template={},_get_breed_name=function(_,name) return name end},
    get_mission_progression=function() return 0 end,_paused_spawn_types={},spawn_type_enabled=function() return true end}
Managers.state={pacing=pacing,minion_spawn=minions,horde=setmetatable({},{__index=HM}),
    difficulty={get_parsed_havoc_data=function() return {} end},
    main_path={is_main_path_available=function() return true end,ahead_unit=function() return true end}}
local cfg,sources
D.get_config=function() return cfg end; D.peek_config=D.get_config
D.collect_sources=function() return sources end
local function reset()
    D.reset_runtime(); units={}; HEALTH_ALIVE={}; cfg=P.defaults(); sources={}
    scans=0; lookups=0
end
-- Idle missions defer population reads; active capacity checks reconcile deaths.
for _,n in ipairs({80,240,600}) do
    reset(); sources={{id="idle",kind="timer",pool={renegade_sniper=1},interval=3600}}
    for i=1,n do minions:spawn_minion("chaos_poxwalker") end
    D.update_director(0.25); assert(lookups==0,"Idle initialization must defer population work")
    scans=0; lookups=0
    for i=1,100 do
        assert(hooks._try_activate_roamer.fn(function() error("deleted lane activated") end,{}, {breed_name="chaos_poxwalker"})==false)
    end
    assert(scans==0 and lookups==0,"Deleted ambient lanes must do no population work")
    for i=1,4 do D.update_director(0.25) end
    assert(scans==0 and lookups==0,"Idle generators must not scan unchanged populations")
end
-- Two lanes due together share a strict total cap; an external spawn between
-- ticks is counted immediately, and removal releases its capacity immediately.
reset(); cfg.total_cap=3
cfg.generators.timer_common={count=2,interval=1,cap=3}
cfg.generators.timer_special={count=2,interval=1,cap=3}
sources={{id="common",pool={chaos_poxwalker=2},interval=1},{id="special",pool={renegade_sniper=2},interval=1}}
D.update_director(0.25)
scans=0
for i=1,4 do D.update_director(0.25) end
assert(#units==3 and scans==1,"Due lanes share one fresh snapshot and strict total cap")
reset(); cfg.total_cap=2; cfg.category_caps.common=2
sources={{id="ambient",kind="ambient",pool={chaos_poxwalker=1},interval=60}}
D.update_director(0.25)
local external=minions:spawn_minion("chaos_poxwalker")
local function activate(_,entry) minions:spawn_minion(entry.breed_name); return true end
local hook=hooks._try_activate_roamer.fn
scans=0
assert(hook(activate,{}, {breed_name="chaos_poxwalker"}))
assert(not hook(activate,{}, {breed_name="chaos_poxwalker"}) and #units==2)
assert(minions:unregister_unit(external))
assert(hook(activate,{}, {breed_name="chaos_poxwalker"}) and #units==2 and scans==1)
HEALTH_ALIVE[units[1]]=false
D.update_director(0.25)
-- Allocated corpses still consume the native hard cap until unregistered.
assert(not hook(activate,{}, {breed_name="chaos_poxwalker"}))
assert(minions:unregister_unit(units[1]))
assert(hook(activate,{}, {breed_name="chaos_poxwalker"}))
-- Breed caps still constrain a batch after one choice is exhausted.
reset(); sources={{id="special",pool={renegade_sniper=1,renegade_netgunner=1},interval=1,
    breed_caps={renegade_sniper=1,renegade_netgunner=1}}}
cfg.generators.timer_special={count=10,interval=1,cap=16}
D.update_director(0.25); for i=1,4 do D.update_director(0.25) end
assert(#units==2 and units[1].breed~=units[2].breed)
for i=1,8 do D.update_director(0.25) end
assert(#units==2)
-- The runtime enrolls only its own specialists, never native injections or
-- boss/ritual actors. Unregistration must also cancel pending cleanup.
reset()
registry.chaos_spawn={name="chaos_spawn",tags={monster=true},breed_type="minion"}
registry.ritual_actor={name="ritual_actor",tags={ritualist=true},breed_type="minion"}
sources={{id="special",pool={renegade_sniper=1},interval=1},{id="boss",pool={chaos_spawn=1},interval=1}}
cfg.generators.timer_special={count=1,interval=1,cap=1}
cfg.generators.timer_boss={count=1,interval=1,cap=1}
local checked={}
pacing._specials_pacing._nav_world={}
pacing._specials_pacing._destroy_special_distance_sq=400
pacing._specials_pacing._check_stuck_special=function(_,unit,slot,_,side,t)
    checked[unit]=true; slot.next_stuck_check_t=t+0.5; assert(side==1)
end
D.update_director(0.25)
local injected=minions:spawn_minion("renegade_sniper")
local ritual=minions:spawn_minion("ritual_actor")
for i=1,6 do D.update_director(0.25) end
local owned
for _,unit in ipairs(units) do
    if checked[unit] then assert(unit~=injected and unit.breed.name=="renegade_sniper"); owned=unit end
end
assert(owned and not checked[injected] and not checked[ritual])
assert(minions:unregister_unit(owned)); checked={}
D.update_director(0.25); assert(not checked[owned])
D.reset_runtime()
-- Expensive source gates run only on enabled, due generators.
reset(); sources={{id="gated",kind="timer",pool={renegade_sniper=1},interval=3600,rules={required_challenge=1}}}
local challenges=0
pacing.total_challenge_rating=function() challenges=challenges+1;return 2 end
D.update_director(.25)
local initial=challenges
for i=1,120 do D.update_director(.25) end
assert(challenges==initial,"Waiting generators must not query source gates")
D.reset_runtime();pacing.total_challenge_rating=nil
-- Runtime timing samples are bounded and report only on the 30-second cadence.
reset(); sources={{id="idle",kind="timer",pool={renegade_sniper=1},interval=3600}}
local timer_calls,reports=0,0
local original_clock=os.clock
os.clock=function() timer_calls=timer_calls+1; return timer_calls*0.0001 end
Application={time_since_launch=function() return 0 end}
local saved_info=D.info
D.info=function(_,fmt,...)
    if fmt:find("Director performance",1,true) then reports=reports+1; assert(string.format(fmt,...):find("mean=0.100ms",1,true)) end
end
for i=1,1870 do D.update_director(1/60) end
assert(timer_calls>=100 and timer_calls<=132 and reports==1,"At most two sampled phases/second, one summary/30s")
D.reset_runtime(); assert(reports==2,"Final partial sample is reported on reset")
timer_calls=0; cfg.enabled=false
for i=1,120 do D.update_director(1/60) end
assert(timer_calls==0,"Disabled director does not profile")
D.reset_runtime(); D.info=saved_info; Application=nil; os.clock=original_clock
-- Prepared draws preserve sorted weighted selection and consume one random
-- value per draw, including zero-weight exclusions and fractional weights.
local function original(pool,roll)
    local names,total={},0
    for name,w in pairs(pool) do if w>0 then names[#names+1]=name end end
    table.sort(names); for _,name in ipairs(names) do total=total+pool[name] end
    if total<=0 then return end
    local r=roll*total
    for _,name in ipairs(names) do r=r-pool[name]; if r<=0 then return name end end
    return names[#names]
end
local pool={a=0.001,b=2,c=0,d=5}
local prepared=P.prepare_pool(pool)
local sort,sorts=table.sort,0
table.sort=function(...) sorts=sorts+1; return sort(...) end
for i=0,1000 do
    local r=i/1001
    local expected=original(pool,r)
    local before=sorts
    assert(P.pick_prepared(prepared,function() return r end)==expected and sorts==before)
end
table.sort=sort
P.exclude_from_pool(prepared,"a"); assert(P.pick_prepared(prepared,function() return 0 end)=="b")
P.exclude_from_pool(prepared,"b"); P.exclude_from_pool(prepared,"d"); assert(P.pick_prepared(prepared)==nil)
assert(pool.a==0.001 and pool.d==5)
''')
print('Runtime: 80/240/600-unit snapshots, zero scans for deleted lanes, cached breed metadata, strict same-tick/external spawn caps, removal/death reconciliation, per-breed limits and equivalent weighted draws: PASS')
print('Director timing: at most one sample/phase/second, thirty-second and final partial summaries, no profiling when disabled or timer unavailable: PASS')

# Run the game's actual stuck/distance method. Geometry and navigation queries
# are deterministic fixtures; the decision thresholds and branches are native.
source=(GAME/'scripts/managers/pacing/specials_pacing/specials_pacing.lua').read_text(encoding='utf-8-sig')
body=source.split('SpecialsPacing._check_stuck_special = function',1)[1].split('\nend',1)[0]
L.globals().native_cleanup=L.execute('''
local NUM_FAILED_MOVE_TO_DESPAWN=8
local STUCK_CHECK_FREQUENCY=0.5
local ABOVE,BELOW,LATERAL=1,1,1
local NavQueries={position_on_mesh_with_outside_position=function(_,_,p) return p and p.on_mesh~=false and p or nil end}
return function'''+body+'\nend')
L.globals().Cleanup=module('HavocEnemyDirector','special_cleanup')
L.execute('''
local C=Cleanup
local q=C.new(); local calls,removed=0,{}
POSITION_LOOKUP={}; HEALTH_ALIVE={}
Vector3={distance_squared=function(a,b) return (a.x-b.x)^2 end}
ScriptUnit={extension=function(unit) return {failed_move_attempts=function() return unit.failed or 0 end} end}
Managers.state.main_path={ahead_unit=function() return {},100,{x=100} end,
    behind_unit=function() return {},90,{x=90} end,travel_distance_from_position=function(_,p) return p.x end}
Managers.state.minion_spawn={despawn_minion=function(_,unit) removed[unit]=true; C.remove(q,unit) end}
local specials={_template={},_nav_world={},_destroy_special_distance_sq=400,
    _check_stuck_special=function(...) calls=calls+1; return native_cleanup(...) end}
local function add(x,failed,on_mesh)
    local u={failed=failed}; POSITION_LOOKUP[u]={x=x,on_mesh=on_mesh}; HEALTH_ALIVE[u]=true; C.add(q,u,0); return u
end
local nearby=add(95,0)
local threshold=add(95,8)
local stuck=add(95,9)
local far=add(200,0)
local offmesh=add(200,0,false)
local unowned={}; POSITION_LOOKUP[unowned]={x=200}; HEALTH_ALIVE[unowned]=true
C.update(q,specials,0.49,HEALTH_ALIVE); assert(calls==0)
for i=1,10 do
    local before=calls; C.update(q,specials,0.5+i/60,HEALTH_ALIVE)
    assert(calls-before<=2,"Cleanup must not bunch all navigation checks into one frame")
end
assert(removed[stuck] and removed[far] and not removed[nearby] and not removed[threshold] and not removed[offmesh] and not removed[unowned])
assert(q.lookup[stuck]==nil and q.lookup[far]==nil)
q=C.new(); calls=0
local one=add(95,0); C.add(q,one,0) -- duplicate registration is ignored
C.update(q,specials,0.5,HEALTH_ALIVE); assert(calls==1)
for i=1,29 do C.update(q,specials,0.5+i/60,HEALTH_ALIVE) end
assert(calls==1,"One specialist must retain native 0.5-second cadence")
C.update(q,specials,1,HEALTH_ALIVE); assert(calls==2)
HEALTH_ALIVE[one]=false; C.update(q,specials,1.01,HEALTH_ALIVE)
assert(#q.slots==0 and q.lookup[one]==nil)
q=C.new(); calls=0
for i=1,80 do add(95,0) end
for i=1,40 do C.update(q,specials,0.5+i/1000,HEALTH_ALIVE) end
assert(calls==80,"Round-robin cleanup must not starve later units")
''')
print('Native specialist cleanup: failed-move threshold, distant/nearby/off-mesh cases, unowned exclusion, two-check frame budget, 0.5s cadence, duplicate/dead removal and fair rotation: PASS')

Perf=module('HavocEnemyDirector','performance_stats')
L.globals().Perf=Perf
L.execute('''
local saved_clock=os.clock; os.clock=function() return 1 end
local stats=Perf.new(); local start=Perf.begin(stats,"tick",1);Perf.finish(stats,"tick",start)
local report
Perf.report(stats,30,function(fmt,...) report=string.format(fmt,...) end)
assert(report:find("below clock resolution",1,true) and not report:find("mean=0.000",1,true))
os.clock=nil;assert(Perf.begin(stats,"tick",32)==nil);os.clock=saved_clock
local old_get=D.get
D.get=function() return false end
stats=Perf.new()
assert(Perf.begin(stats,"tick",100)==nil)
Perf.count(stats,"ignored",10);assert(next(stats.counters)==nil)
Perf.report(stats,100,function() error("Disabled diagnostics logged") end,true)
D.get=old_get
''')
print('Performance clock: frame-latched engine time bypassed; zero deltas reported as below resolution; unavailable clock safely skipped: PASS')
