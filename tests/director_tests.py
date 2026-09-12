"""Exercise the configurable scheduler against real template/breed metadata."""
from pathlib import Path
import sys
PROJECT_HED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT_HED.parent/"HavocConditionManager/tests"))
from native_harness import *

L.execute('new_test_mod("HavocEnemyDirector"); mods.SoloPlay.has_local_gameplay_authority=function() return host end')
load_mod("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_director")
L.execute("""
local D=mods.HavocEnemyDirector
local C=D.director_config
local Engine=D:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_engine")
local Random=D:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_random")
local function checked(raw)
    local cfg,bad=C.validate(raw);assert(#bad==0,bad[1]);return cfg
end
local function fresh()
    local cfg=checked({})
    cfg.director.enabled=true
    local f=C.new_formation(cfg,"第一编队","hordes","chaos_poxwalker")
    f.variants[1].members[1].amount={2,5}
    local d=C.new_deployment(cfg,"第一投放",f.id)
    d.first_delay=0;d.interval={10,10};d.cooldown=1;d.max_occurrences=3
    return cfg,f,d
end
local function rig(cfg,seed,coarse)
    local a={started={},cancelled=0,blocked=false,hold=false,living=0}
    function a.allowed() return not a.blocked end
    function a.update(job,context,t)
        if a.hold then return end
        a.started[#a.started+1]={id=job.state.definition.id,members=table.clone(job.members),waves=job.waves,t=t}
        job.started=true;job.done=true;job.test_alive=a.living
    end
    function a.alive(job) return job.test_alive or 0 end
    function a.cancel(job) a.cancelled=a.cancelled+1;job.done=true end
    local e=Engine.new(checked(cfg),seed or 123,S.coarse_config(coarse),R,a)
    return e,a,{players=4,load=0,events=0,hordes=0,monsters=0,progress=0}
end
local function advance(e,c,seconds,dt)
    dt=dt or 0.5
    for _=1,math.floor(seconds/dt) do e.tick(dt,c) end
end
local cfg,f,d=fresh()
cfg.director.seed=876;cfg.director.seed_enabled=false
assert(rig(cfg,321).seed==321,'disabled seed preserves value but follows mission seed')
cfg.director.seed_enabled=true
local fixed_a=rig(cfg,321);local fixed_b=rig(cfg,654)
assert(fixed_a.seed==876 and fixed_b.seed==876 and fixed_a.phase_until==fixed_b.phase_until)
assert(checked({director={seed=456}}).director.seed_enabled,'legacy nonzero scheduler seed migrates to fixed')
assert(not checked({director={seed=0}}).director.seed_enabled)
assert(checked({seed=456}).seed_enabled,'legacy map seed migrates to fixed')
cfg.director.seed_enabled=false;cfg.director.seed=0
assert(C.breed_allowed("hordes","chaos_poxwalker"))
assert(not C.breed_allowed("hordes","chaos_plague_ogryn"))
assert(not C.breed_allowed("monsters","chaos_daemonhost"))
assert(C.breed_allowed("monsters","chaos_plague_ogryn"))
assert(not C.breed_allowed("specials","chaos_poxwalker"))
local function reject(change)
    local raw=table.clone(cfg);change(raw);local _,bad=C.validate(raw);assert(#bad>0)
end
reject(function(x) x.director.seed=-1 end)
reject(function(x) x.director.low_load=x.director.high_load end)
reject(function(x) x.formations[1].variants[1].weight=0 end)
reject(function(x) x.formations[1].variants[1].members[1].amount={9,1} end)
reject(function(x) x.formations[1].variants[1].members[1].name="evil" end)
reject(function(x) x.formations[1].variants[1].members[1].amount={300,301} end)
reject(function(x) x.formations[1].variants[1].members.callback="return true" end)
reject(function(x) x.formations[2]=x.formations[1] end)
reject(function(x) x.deployments[1].formation_id="missing" end)
reject(function(x) x.deployments[1].trigger="condition" end)
reject(function(x) x.deployments[1].conditions.mode="replace" end)
reject(function(x) x.deployments[1].end_time=1;x.deployments[1].start_time=2 end)
reject(function(x) x.director.seed=0/0 end)
assert(checked({version=2,patches={},rules={},seed=771}).seed==771)
local id="specials/default_specials/1"
cfg.relative[id]={max_alive_specials=1.5}
assert(D.save_config(cfg))
local coarse=S.coarse_config({special_slots=2})
B:set("native_configuration_v3",coarse)
local item=A.by_id[id].fields.max_alive_specials
local resolved=D.preview_config()
assert(resolved.patches[id].max_alive_specials==S.scaled(item,"specials",coarse)*1.5)
assert(D.peek_config().relative[id].max_alive_specials==1.5 and #D.get_saved_config().formations==1)
assert(D.set_patch(id,"max_alive_specials",9))
assert(not D.peek_config().relative[id] and D.get_config().patches[id].max_alive_specials==9)
assert(D.set_relative(id,"max_alive_specials",2))
assert(not D.peek_config().patches[id] and D.get_saved_config().relative[id].max_alive_specials==2)
B:set("native_configuration_v3",nil)

-- The dedicated RNG must not consume or reseed native randomness.
local native_random,native_seed=math.random,math.randomseed
math.random=function() error("native random consumed") end
math.randomseed=function() error("native random reseeded") end
local a,b=Random.new(123,"d1/timer"),Random.new(123,"d1/timer")
local other=Random.new(123,"d2/timer")
local different=false
for _=1,100 do local x=a.next();assert(x>=0 and x<1 and x==b.next());different=different or x~=other.next() end
assert(different)
cfg,f,d=fresh()
local e,adapter,c=rig(cfg)
advance(e,c,60)
assert(#adapter.started==3 and e.states[1].occurrences==3)
assert(adapter.started[2].t-adapter.started[1].t>=10)
assert(#e.jobs==0)
-- The interval starts at the first accepted member even when later waves
-- remain pending; completion does not silently restart the countdown.
local slow,slow_adapter,slow_context=rig(cfg)
slow_adapter.update=function(job,context,t)
    if not job.started then job.started=true;job.first=t end
    if t-job.first>=5 then job.done=true end
end
advance(slow,slow_context,6)
assert(slow.states[1].remaining<=5.5 and slow.states[1].remaining>0)
local e2,a2,c2=rig(cfg)
advance(e2,c2,60)
for i,v in ipairs(adapter.started) do
    assert(v.t==a2.started[i].t and #v.members==#a2.started[i].members)
end
-- A second same-family formation has independent cadence and quota; list
-- reorder must preserve each stable ID's sequence.
cfg,f,d=fresh();d.interval={8,15}
local f2=C.new_formation(cfg,"第二编队","hordes","chaos_poxwalker")
f2.variants[1].members[1].amount={7,9}
local d2=C.new_deployment(cfg,"第二投放",f2.id)
d2.first_delay=3;d2.interval={17,20};d2.cooldown=1;d2.max_occurrences=2
local e3,a3,c3=rig(cfg);advance(e3,c3,100)
local by_id={}
for _,v in ipairs(a3.started) do by_id[v.id]=(by_id[v.id] or 0)+1 end
assert(by_id[d.id]==3 and by_id[d2.id]==2)
cfg.deployments={d2,d}
local e4,a4,c4=rig(cfg);advance(e4,c4,100)
for i,v in ipairs(a3.started) do assert(v.id==a4.started[i].id and v.t==a4.started[i].t and #v.members==#a4.started[i].members) end

-- Relative timing follows HCM frequency. Distance steps cannot accumulate
-- catch-up attacks after crossing several thresholds during a pause.
cfg,f,d=fresh();d.trigger="progress";d.progress_start=100;d.progress_step=100
local ep,ap,cp=rig(cfg,1,{horde_frequency=2})
advance(ep,cp,30);assert(#ap.started==0)
cp.progress=100;advance(ep,cp,2);assert(#ap.started==1)
assert(ep.states[1].next_progress==150)
cp.progress=1000;advance(ep,cp,2);assert(#ap.started==2)
advance(ep,cp,10);assert(#ap.started==2 and ep.states[1].next_progress==1050)

-- Edge triggering rearms only after the condition becomes false; a persistent
-- true condition cannot repeatedly drain the quota.
cfg,f,d=fresh();d.trigger="condition"
d.conditions.clauses={{condition="load_min",value=20}}
local ee,ae,ce=rig(cfg)
advance(ee,ce,5);ce.load=25;advance(ee,ce,20);assert(#ae.started==1)
ce.load=10;advance(ee,ce,2);ce.load=25;advance(ee,ce,2);assert(#ae.started==2)
-- A start-only condition does not invalidate its own multi-member encounter.
-- Rechecking throughout an encounter is an explicit opt-in.
for _,recheck in ipairs({false,true}) do
    cfg,f,d=fresh();d.conditions.clauses={{condition="load_max",value=40}};d.recheck_conditions=recheck
    local check,emit,state=rig(cfg)
    emit.update=function(job)
        job.accepts=(job.accepts or 0)+1;job.started=true
        if job.accepts==2 then job.done=true end
    end
    advance(check,state,1);assert(check.jobs[1].accepts==1)
    state.load=45;advance(check,state,0.5)
    assert(recheck and #check.jobs==1 or not recheck and #check.jobs==0)
end

-- Failed placement expires once, backs off, and does not spend successful
-- encounter quota. Admission and per-rule live group limits reserve pending
-- groups as well as living ones.
cfg,f,d=fresh();d.max_alive=1
local ef,af,cf=rig(cfg);af.hold=true
advance(ef,cf,130)
assert(af.cancelled==1 and ef.states[1].occurrences==0 and #ef.jobs<=1)
af.hold=false;advance(ef,cf,15);assert(#af.started>=1)
local el,al,cl=rig(cfg);al.living=1;advance(el,cl,80)
assert(#al.started==1 and #el.jobs==1)
el.jobs[1].test_alive=0;advance(el,cl,3);assert(#al.started==2)
el.finish();assert(#el.jobs==0 and al.cancelled==1)

cfg,f,d=fresh();d.end_time=2
local ew,aw,cw=rig(cfg);cw.safe=true;advance(ew,cw,4);cw.safe=false;advance(ew,cw,10);assert(#aw.started==0)
cfg,f,d=fresh()
local eg,ag,cg=rig(cfg);cg.events=1;advance(eg,cg,15);assert(#ag.started==0)
cg.events=0;cg.players=0;advance(eg,cg,15);assert(#ag.started==0)
cg.players=4;ag.blocked=true;advance(eg,cg,15);assert(#ag.started==0)
ag.blocked=false;advance(eg,cg,2);assert(#ag.started==1)

-- Pressure state uses actual combat load, capable-player count and minimum
-- recovery time. Zero recovery rate pauses both pending and new HED requests.
cfg,f,d=fresh();cfg.director.mode="adaptive"
cfg.director.build_duration={2,2};cfg.director.pressure_duration={2,2};cfg.director.recovery_duration={3,3}
d.max_occurrences=0;d.interval={1,1};cfg.director.admission_interval=0.5
local ed,ad,cd=rig(cfg);advance(ed,cd,2);assert(ed.phase=="pressure")
cd.load=70;advance(ed,cd,0.5);assert(ed.phase=="recovery")
local n=#ad.started;advance(ed,cd,4);assert(ed.phase=="recovery" and #ad.started==n)
cd.load=10;advance(ed,cd,0.5);assert(ed.phase=="build")
advance(ed,cd,1);assert(#ad.started>n)

-- Per-encounter budgets remain bounded even at combined HCM, HED and phase
-- multipliers, and weighted variants produce one chosen member list.
cfg,f,d=fresh();f.variants[1].members[1].amount={100,100}
d.size_multiplier=10;d.waves=12
local eb,ab,cb=rig(cfg,1,{horde_size=10})
advance(eb,cb,2);assert(#ab.started[1].members*ab.started[1].waves<=256)
-- External requests share admission, pause, expiration and active budgets.
cfg,f,d=fresh();cfg.deployments={}
local ex,ax,cx=rig(cfg)
local accepted,id=ex.submit({source="HavocConditionManager/split/death",seed=991},f)
assert(accepted and id=="diy-1" and #ex.states==1)
cx.diy_paused=true;advance(ex,cx,2);assert(#ax.started==0 and #ex.jobs==0)
cx.diy_paused=false;ex.tick(.1,cx);assert(#ex.jobs==1)
cx.diy_paused=true;advance(ex,cx,1);assert(#ax.started==0,"Pause holds already admitted requests")
cx.diy_paused=false;advance(ex,cx,2);assert(#ax.started==1 and #ex.states==0)
advance(ex,cx,120);assert(#ax.started==1,"External request cannot repeat")
local expiry,ae,ce=rig(cfg);ce.safe=true
assert(expiry.submit({source="test",seed=1},f));advance(expiry,ce,121);assert(#expiry.states==0 and #ae.started==0)
local bounded,ab,cb=rig(cfg)
for i=1,32 do assert(bounded.submit({source="test",seed=i},f)) end
assert(not bounded.submit({source="test",seed=99},f))
cb.safe=true;advance(bounded,cb,121)
for batch=1,3 do
 for i=1,32 do assert(bounded.submit({source="test",seed=i},f)) end
 advance(bounded,cb,121)
end
local ok,why=bounded.submit({source="test",seed=99},f);assert(not ok and why=="mission_request_budget")
ex.finish();assert(not ex.submit({source="test"},f));ex.tick(2,cx);assert(#ax.started==1)
assert(R.validate({mode="append",match="all",clauses={{condition="affix_active",value="monster_health_150"},{condition="signal_active",value="wave_ready"}}}))
assert(R.evaluate({mode="append",match="all",clauses={{condition="affix_active",value="monster_health_150"},{condition="signal_active",value="wave_ready"}}},{affix={monster_health_150=true},signal={wave_ready=true}}))
assert(not R.evaluate({mode="append",match="all",clauses={{condition="signal_active",value="wave_ready"}}},{signal={}}))
math.random=native_random;math.randomseed=native_seed
print("Director: strict config, HCM relative values, isolated seeds, independent formations, scheduling, quotas, failure expiry, conditions, pressure recovery and bounded waves: PASS")
""")
