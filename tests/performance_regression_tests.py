"""Run the changed scheduling paths both with diagnostics and after stripping."""
from pathlib import Path
import re
from project_env import SOURCES
from lupa.luajit21 import LuaRuntime

for stripped in (False, True):
    L=LuaRuntime(unpack_returned_tuples=True)
    L.globals().stripped_build=stripped
    def module(mod,name):
        assert not (stripped and name in ('performance_stats','capacity_stats')), 'Stripped runtime imported diagnostics'
        source=(SOURCES/mod/'scripts/mods'/mod/(name+'.lua')).read_text(encoding='utf-8-sig')
        if stripped: source=re.sub(r'(?m)^\s*-- PERF_DEBUG_BEGIN\n.*?^\s*-- PERF_DEBUG_END\n?', '', source, flags=re.S)
        return L.execute(source,name='@'+mod+'/'+name)
    L.globals().load_module=module
    L.execute('''
D={values={}}; B={}; hooks={}; deps={}; HEALTH_ALIVE={}; Managers={state={}}
function get_mod(name) return name=="HavocEnemyDirector" and D or B end
function D:io_dofile(path) return load_module("HavocEnemyDirector",path:match("([^/]+)$")) end
function B:io_dofile(path) return load_module("HavocConditionManager",path:match("([^/]+)$")) end
function B:get() return nil end
function D:get(k) return self.values[k] end
function B.has_local_gameplay_authority() return true end
function D.is_gameplay_enabled() return true end
function D:info() end
function D:hook(target,name,fn) hooks[name]={target=target,fn=fn} end
function D:hook_safe() end
deps["scripts/settings/breed/breeds"]={
    common={name="common",tags={},breed_type="minion"},
    special={name="special",tags={special=true},breed_type="minion"},
    boss={name="boss",tags={monster=true},breed_type="minion"}}
function require(path) deps[path]=deps[path] or {}; return deps[path] end
''')
    L.globals().D.planner=module('HavocEnemyDirector','planner')
    if not stripped: L.globals().D.capacity_stats=module('HavocEnemyDirector','capacity_stats')
    module('HavocEnemyDirector','runtime')
    L.execute('''
local P=D.planner
local original_clock=os.clock
os.clock=function() return 0 end -- deterministic counted-engine work
local registry=require("scripts/settings/breed/breeds")
local units,scans,emissions,frame,fail_mode,visits={},0,{},0,nil,0
local MS=require("scripts/managers/minion/minion_spawn_manager")
local HM=require("scripts/managers/horde/horde_manager")
local minions=setmetatable({},{__index=MS})
function MS:spawned_minions() scans=scans+1; visits=visits+#units; return units end
function MS:total_allocated_num_enemies() return #units end
function MS:replacement_breed() return nil end
function MS:spawn_minion(name)
    local u={breed=registry[name]}; units[#units+1]=u; HEALTH_ALIVE[u]=true; return u
end
function MS:unregister_unit(u)
    for i,x in ipairs(units) do if x==u then table.remove(units,i); return true end end
    return false
end
for _,name in ipairs({"spawn_minion","unregister_unit"}) do
    local h=hooks[name]; local original=h.target[name]
    h.target[name]=function(...) return h.fn(original,...) end
end
ScriptUnit={extension=function(u) return {breed=function() return u.breed end} end}
function HM:horde(_,_,side,_,comp)
    if fail_mode=="error" then error("native spawn error") end
    local amount=0
    for _,e in ipairs(comp.breeds) do amount=amount+e.amount[1] end
    emissions[#emissions+1]={frame=frame,requested=amount,owner=D._spawning_generator}
    if fail_mode=="fail" then return false end
    local remaining=fail_mode=="partial" and math.floor(amount/2) or amount
    fail_mode=nil
    for _,e in ipairs(comp.breeds) do for i=1,e.amount[1] do
        if remaining>0 then minions:spawn_minion(e.name,nil,nil,side,{});remaining=remaining-1 end
    end end
    self._hordes.trickle_horde[#self._hordes.trickle_horde+1]={group_id=#self._hordes.trickle_horde+1}
    return true
end
function HM:num_active_hordes() return #self._hordes.trickle_horde end
local cfg,sources,pacing,horde
D.get_config=function() return cfg end; D.peek_config=D.get_config
D.collect_sources=function() return sources end
local function reset()
    D.reset_runtime(); units={}; HEALTH_ALIVE={};scans=0;visits=0;emissions={};frame=0;fail_mode=nil
    cfg=P.defaults();sources={};cfg.total_cap=600
    for _,c in ipairs(P.categories) do cfg.category_caps[c]=600 end
    horde=setmetatable({_hordes={trickle_horde={}}},{__index=HM})
    pacing={_horde_pacing={_template={}},_specials_pacing={_template={},_get_breed_name=function(_,n) return n end},
        get_mission_progression=function() return 100 end,_paused_spawn_types={},_frozen_spawn_types={},
        _allowed_spawn_types={hordes=true,trickle_hordes=true,specials=true,monsters=true,roamers=true,terror_events=true},
        _heat_pacing={active=function() return false end},_challenge_rating_thresholds={},_total_challenge_rating=0,
        pause_spawn_type=function() end}
    pacing.spawn_type_enabled=function(self,kind) return hooks.spawn_type_enabled.fn(function() error("unexpected native gate") end,self,kind) end
    Managers.state={pacing=pacing,minion_spawn=minions,horde=horde,
        difficulty={get_parsed_havoc_data=function() return {} end},
        main_path={is_main_path_available=function() return true end,ahead_unit=function() return true end}}
end
local function step(dt) frame=frame+1; D.update_director(dt or 1/60) end
local function due() step(.25); for i=1,4 do step(.25) end end
-- Reproduce the former 400-creation spike. Every frame is bounded, all four
-- lanes receive service promptly, and final population/caps remain exact.
reset()
for i=1,4 do
    local id="custom_"..i
    cfg.custom[i]={id=id,category="common",pool={common=1}}
    cfg.generators[id]={count=100,interval=1,cap=100}
end
due(); assert(#units==24,"First due frame must create 24, previously 400")
step(); local served={}
for _,e in ipairs(emissions) do served[e.owner]=true end
for i=1,4 do assert(served["custom_"..i],"Round robin starved a due lane") end
for i=1,80 do step() end
assert(#units==400)
local frames={}
for _,e in ipairs(emissions) do
    local f=frames[e.frame] or {calls=0,amount=0};frames[e.frame]=f
    f.calls=f.calls+1;f.amount=f.amount+e.requested
    assert(e.requested<=16 and f.calls<=2 and f.amount<=24)
end
-- Frozen, paused, heat-disabled and over-pressure specialists cannot use a
-- When only one batch fits, the next freed capacity goes to the next due
-- owner, not repeatedly to the first generator in the configuration.
reset();cfg.total_cap=16
for i=1,4 do
    local id="custom_"..i;cfg.custom[i]={id=id,category="common",pool={common=1}}
    cfg.generators[id]={count=16,interval=1,cap=32}
end
due()
for i=1,4 do
    assert(emissions[#emissions].owner=="custom_"..i,"Capacity admission starved a later generator")
    while #units>0 do minions:unregister_unit(units[1]) end
    step(.25)
end
-- Frozen, paused, heat-disabled and over-pressure specialists cannot use a
-- permissive trickle gate. The exact native pressure boundary is retained.
for _,reason in ipairs({"frozen","paused","heat","pressure"}) do
    reset(); sources={{id="special_source",pool={special=1},interval=1}}
    cfg.generators.timer_special={count=2,interval=1,cap=2}
    if reason=="frozen" then pacing._frozen_spawn_types.specials=true
    elseif reason=="paused" then pacing._paused_spawn_types.specials=true
    elseif reason=="heat" then pacing._heat_pacing={active=function() return true end,current_stage_settings=function() return {allowed_spawn_types={trickle_hordes=true}} end}
    else pacing._challenge_rating_thresholds.specials=10;pacing._total_challenge_rating=11 end
    due();assert(#units==0 and scans==0,reason.." admitted blocked work")
    pacing._frozen_spawn_types={};pacing._paused_spawn_types={};pacing._heat_pacing={active=function() return false end};pacing._total_challenge_rating=10
    step(.25);assert(#units==2,reason.." did not resume")
end
reset();sources={{id="weak_boss",spawn_type="specials",profile="weak",pool={boss=1},interval=1}}
cfg.generators.timer_boss_weak={count=1,interval=1,cap=2};pacing._frozen_spawn_types.specials=true
due();assert(#units==0,"Weak boss lost its native special-source gate")
pacing._frozen_spawn_types={monsters=true};step(.25);assert(#units==1,"Weak boss was gated by its category instead of its source")
reset();sources={{id="hound_trickle",spawn_type="trickle_hordes",pool={special=1},interval=1}}
cfg.generators.timer_special={count=1,interval=1,cap=1};pacing._frozen_spawn_types.specials=true
due();assert(#units==1,"Trickle-sourced specialist must retain the trickle gate")
-- Reservations also constrain native map activations. Cancellation releases
-- the full unused balance immediately; created units still consume capacity.
reset();cfg.total_cap=100
sources={{id="batch",pool={common=1},interval=1},{id="map",kind="ambient",pool={common=1}}}
cfg.generators.timer_common={count=100,interval=1,cap=100}
cfg.generators.ambient_common={cap=100}
due();assert(#units==16)
local function activate(_,r) minions:spawn_minion(r.breed_name);return true end
local function ambient() return hooks._try_activate_roamer.fn(activate,{}, {breed_name="common"}) end
assert(not ambient(),"Map activation spent a queued reservation")
pacing._frozen_spawn_types.hordes=true;step()
for i=1,84 do assert(ambient(),"Cancelled reservation leaked") end
assert(#units==100 and not ambient())
-- A batch split into native groups remains one active horde for its source,
-- and does not cancel itself when its own first chunk reaches active_limit.
reset();sources={{id="limited",spawn_type="trickle_hordes",kind="travel",pool={common=1},interval=1,distance=1,
    rules={active_limit=1,cooldown=1}}}
cfg.generators.travel_common={count=40,interval=1,distance=1,cap=100}
step(.25);pacing.get_mission_progression=function() return 200 end
for i=1,4 do step(.25) end
for i=1,5 do step() end
assert(#units==40 and #horde._hordes.trickle_horde==3,"Split batch counted its own chunks as new hordes")
for i=1,8 do step(.25) end;assert(#units==40,"Logical active-horde limit was bypassed")
-- Admission checks once, and each later native chunk checks live state again.
-- A new external horde between frames cancels the remaining reservation.
reset();sources={{id="checks",pool={common=1},interval=1,rules={active_limit=1,cooldown=1}}}
cfg.generators.timer_common={count=40,interval=1,cap=100}
local active_reads=0
local previous_active=HM.num_active_hordes
HM.num_active_hordes=function(self) active_reads=active_reads+1;return previous_active(self) end
step(.25);for i=1,3 do step(.25) end
active_reads=0;step(.25)
assert(#units==16 and active_reads==2,"Expected one admission check plus one dispatch check")
horde._hordes.trickle_horde[#horde._hordes.trickle_horde+1]={group_id="external"}
step();assert(#units==16 and active_reads==3,"Queued work must recheck changed source state")
HM.num_active_hordes=previous_active
-- Partial native creation consumes only confirmed event tokens. No retries
-- invent reinforcements, and all uncreated tokens remain available later.
reset();sources={{id="event",kind="event",pool={common=1},interval=1}}
cfg.generators.event_common={count=6,interval=1,cap=100}
step(.25);hooks.spawn_group.fn(function() error("native event should be intercepted") end,{}, {breeds={{name="common",amount={10,10}}}},{})
fail_mode="partial";for i=1,4 do step(.25) end;assert(#units==3)
for i=1,30 do step(.25) end;assert(#units==10,"Partial failure lost or duplicated event quota")
-- Errors clear every temporary marker, and a new mission has no pending work.
reset();sources={{id="error",pool={common=1},interval=1}}
cfg.generators.timer_common={count=30,interval=1,cap=100}
step(.25);for i=1,3 do step(.25) end;fail_mode="error"
local ok=pcall(step,.25);assert(not ok)
assert(D._spawning_generator==nil and D._spawning_health==nil and D._emitted_count==nil)
reset();for i=1,100 do step() end;assert(#units==0)
-- No idle full scans, even at 600 units. A later due request refreshes before
-- its budget; caches cannot erase allocated corpses or ignore external births.
reset();sources={{id="idle",pool={special=1},interval=3600}}
for i=1,600 do minions:spawn_minion("common") end
for i=1,240 do step() end;assert(scans==0 and visits==0)
D.reset_runtime()
-- Idle cached counts must not fabricate time spent at a population cap.
reset();sources={{id="sample",pool={common=1},interval=1}}
cfg.generators.timer_common={count=16,interval=1,cap=16}
local sampled
local old_info=D.info
D.info=function(_,fmt,...)
    local message=string.format(fmt,...)
    if message:find("Capacity summary",1,true) then sampled=tonumber(message:match("population sampled=([%d%.]+)s")) end
end
due();pacing._frozen_spawn_types.hordes=true
for i=1,125 do step(.25) end
if stripped_build then assert(sampled==nil,"Stripped runtime retained capacity reports")
else assert(sampled and sampled>0 and sampled<=.5,"Idle snapshot invented population observation time") end
D.reset_runtime();D.info=old_info
local Queue=load_module("HavocEnemyDirector","spawn_queue")
local q=Queue.new()
for i=1,2 do Queue.add(q,{generator={id="budget_"..i,category="common"},remaining=50}) end
local timer_reads=0
os.clock=function() timer_reads=timer_reads+1;return timer_reads==1 and 0 or .01 end
local calls,created=Queue.drain(q,function(_,n) return n end,function(_,n) return n end,function() end)
assert(calls==1 and created==16,"Soft budget must stop before another native call")
os.clock=nil
calls,created=Queue.drain(q,function(_,n) return n end,function(_,n) return n end,function() end)
assert(calls==2 and created==24,"Hard budgets must work when the timer is absent")
os.clock=original_clock
''')
    print(('Stripped' if stripped else 'Diagnostic')+' runtime: 400 -> 24 first-frame creations; hard frame/call budgets, fair service, exact final population; source/pressure gates, reserved map capacity, cancellation, logical horde counts, partial event failure, marker cleanup, mission reset and zero idle scans: PASS')
