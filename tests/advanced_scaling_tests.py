# Regression tests against actual native source data and installed DMF wrappers.
cache['scripts/extension_systems/blackboard/utilities/blackboard']=L.eval('{write_component=function(bb,key) return bb[key] end}')
L.globals().NativePatrols=lua_file(game/'scripts/utilities/minion_patrols.lua')
L.execute('''
local D,base,solo=mods.HavocEnemyDirector,mods.HavocConditionManager,mods.SoloPlay
local P=D.planner
local old_state,old_authority=Managers.state,base.has_local_gameplay_authority
Managers.state={}; D.reset_runtime()
base.has_local_gameplay_authority=function() return true end
solo:set("havoc_faction","renegade")
solo:set("havoc_theme_circumstance","default")
solo:set("havoc_difficulty_circumstance","mutator_highest_difficulty")
local function select(value) base:set("havoc_circumstances_serialized",value); D.synchronize_conditions() end
local function find(gs,id) for _,g in ipairs(gs) do if g.id==id then return g end end end
local function share(g,name)
    local sum=0; for _,w in pairs(g.pool) do sum=sum+w end
    return (g.pool[name] or 0)/sum
end
select("")
local baseline_sources=D.collect_sources(true)
select("mutator_havoc_rotten_armor")
local extra
for _,g in ipairs(D.preview_generators()) do
    if g.sources["mutator_live_rotten_armor_trickle_horde:1"] then extra=g end
end
assert(extra and extra.pool.chaos_ogryn_executor)
assert(math.abs(share(extra,"chaos_ogryn_executor")-1/3)<1e-10)
local native=require("scripts/settings/mutator/mutator_templates").mutator_live_rotten_armor_trickle_horde.trickle_horde_templates[1]
assert(extra.rules.min_players==native.min_players_alive and extra.rules.active_limit==native.num_trickle_hordes_active_for_cooldown)
assert(extra.rules.pause.trickle_hordes==native.pause_pacing_on_spawn[5].trickle_hordes)
local selected_sources=D.collect_sources(true)
local native_count=0
for _,s in ipairs(selected_sources) do
    if s.id=="native_hordes" then
        native_count=native_count+1
        -- Native _setup_next_horde never chooses the trickle table as a timed wave.
        assert(not s.pool.chaos_ogryn_executor)
    end
    assert(s.id~="mutator_havoc_override_horde_pacing_02","A replacement must not become an additional source")
end
assert(native_count==1)
-- Mixed-faction selection really does change native pools; do not turn it into
-- an arbitrary Crusher weight boost. Check pool ratios retain source rates.
local sources=D.collect_sources(true)
for _,g in ipairs(D.preview_generators()) do
    if g.category=="elite" and (g.kind=="timer" or g.kind=="travel") then
        local rate=0
        for _,s in ipairs(sources) do
            if g.sources[s.id] then rate=rate+(s.pool.chaos_ogryn_executor or 0)/s.interval end
        end
        if rate>0 then assert(math.abs(g.count/g.interval*share(g,"chaos_ogryn_executor")-rate)<1e-10,
            g.id.." generated="..g.count/g.interval*share(g,"chaos_ogryn_executor").." source="..rate) end
    end
end
-- A very small source must not be rounded up to the same probability as a
-- much larger source, or change its peers' expected rate when merged.
local registry=D.breeds
local synthetic={{id="base",pool={chaos_ogryn_executor=1,renegade_gunner=0.001},interval=60},
    {id="added",pool={renegade_gunner=2},interval=30}}
local merged=find(P.compile(synthetic,P.defaults(),registry,D.category_for),"timer_elite")
assert(math.abs(merged.count/merged.interval*share(merged,"chaos_ogryn_executor")-1/60)<1e-12)
local alias={breeds={{name="chaos_ogryn_executor",amount={2,2}}}}
local copied=P.copy({first=alias,second=alias})
assert(copied.first==copied.second and copied.first~=alias)

-- Every category and mode keeps the pool, manual base parameters and caps.
for _,category in ipairs(P.categories) do
    for n=1,5 do for _,mode in ipairs({"quantity","speed","mixed"}) do
        base:set("spawn_multiplier_"..category,n); base:set("spawn_mode_"..category,mode)
        local scaling=D.get_spawn_scaling()
        local g={category=category,kind="travel",count=3,interval=60,distance=120,cap=45,pool={chaos_ogryn_executor=0.001}}
        local effective=P.effective(g,scaling)
        assert(math.abs((effective.count/effective.interval)/(g.count/g.interval)-n)<1e-10)
        assert(math.abs((effective.count/effective.distance)/(g.count/g.distance)-n)<1e-10)
        assert(effective.pool.chaos_ogryn_executor==0.001 and effective.cap==45 and g.count==3 and g.interval==60)
        local count,remainder=0,0
        for _=1,1000 do local amount; amount,remainder=P.batch(effective,remainder); count=count+amount end
        assert(math.abs(count-1000*effective.count)<1.001)
    end end
    base:set("spawn_multiplier_"..category,1); base:set("spawn_mode_"..category,"quantity")
end
-- The actual UI edits base parameters even while its summary shows 5x.
select(""); solo:set("havoc_difficulty_circumstance","default"); D.synchronize_conditions()
base:set("spawn_multiplier_common",5)
test_view._hcm_page=4; test_view._hed_generator_id="timer_common"; test_view._hcm_step=1
Paging.refresh(test_view,test_settings)
local raw=find(D.preview_generators(),"timer_common")
local cfg_before=D.get_config()
click_control("generator_count_plus")
assert(D.get_config().generators.timer_common.count==raw.count+1)
assert(find(D.preview_generators(),"timer_common").count==raw.count+1)
assert(find_control("generator_explanation").text:find("5×",1,true))
local revision=D.get_config().revision
base:set("spawn_multiplier_common",2)
assert(D.get_config().revision==revision,"Changing only a multiplier must not reset manual configuration")

local MS=game_classes["scripts/managers/minion/minion_spawn_manager"]
local HM=game_classes["scripts/managers/horde/horde_manager"]
local PM=game_classes["scripts/managers/pacing/pacing_manager"]
local SP=game_classes["scripts/managers/pacing/specials_pacing/specials_pacing"]
local RP=game_classes["scripts/managers/pacing/roamer_pacing/roamer_pacing"]
local NW=game_classes["scripts/managers/mutator/mutators/mutator_nurgle_warp"]
local original_sources=D.collect_sources
local live_units,emissions={},{ }
local minions=setmetatable({units=live_units},{__index=MS})
local horde={horde=function(_,_,_,side,_,comp)
    local emitted=0
    for _,e in ipairs(comp.breeds) do
        for _=1,e.amount[1] do minions:spawn_minion(e.name,nil,nil,side,{}); emitted=emitted+1 end
    end
    emissions[#emissions+1]=emitted
    return true
end}
local template=test_templates.havoc
local travel=0
local pacing=setmetatable({_template=template,
    _horde_pacing={_template=template.horde_pacing_template.resistance_templates[5]},
    _specials_pacing=setmetatable({_template=template.specials_pacing_template.resistance_templates[5]},{__index=SP}),
    _paused_spawn_types={},_frozen_spawn_types={},_allowed_spawn_types={trickle_hordes=true,hordes=true,specials=true,monsters=true,roamers=true,terror_events=true},
    _heat_pacing={active=function() return false end},get_mission_progression=function() return travel end},{__index=PM})
Managers.state={pacing=pacing,minion_spawn=minions,horde=horde,
    difficulty={get_parsed_havoc_data=function() return {} end},
    main_path={is_main_path_available=function() return true end,ahead_unit=function() return {} end}}
local breeds_by_category={common="chaos_poxwalker",elite="chaos_ogryn_executor",special="renegade_netgunner",boss="chaos_spawn"}
local function setup(category,n,mode,kind,cap)
    D.reset_runtime(); minions.units={}; emissions={}; travel=0
    base:set("spawn_multiplier_"..category,n); base:set("spawn_mode_"..category,mode)
    local breed=breeds_by_category[category]
    D.collect_sources=function() return {{id="regression",kind=kind,pool={[breed]=2},interval=1,distance=10}} end
    local cfg=P.defaults(); cfg.total_cap=512
    for _,c in ipairs(P.categories) do cfg.category_caps[c]=512 end
    cfg.generators[kind.."_"..category]={count=2,interval=1,distance=10,cap=cap or 512}
    D.save_config(cfg)
end
local function advance(seconds,move)
    for _=1,math.floor(seconds/0.05+0.5) do
        if move then travel=travel+0.5 end
        D.update_director(0.05)
    end
end
for _,category in ipairs(P.categories) do
    for _,kind in ipairs({"timer","travel"}) do
        for n=1,5 do for _,mode in ipairs({"quantity","speed","mixed"}) do
            setup(category,n,mode,kind)
            advance(10,true)
            -- Startup/cadence plus the final partially drained batch can defer
            -- at most three batches; individual native calls are now bounded.
            local q=D.get_session_scaling()[category].quantity
            assert(math.abs(#minions.units-20*n)<=6*q+0.01,category.." "..kind.." "..mode.." "..n.." count="..#minions.units)
            if mode=="speed" then for _,count in ipairs(emissions) do assert(count==math.min(2,category=="boss" and 1 or 2)) end end
            setup(category,n,mode,kind,3); advance(10,true)
            assert(#minions.units==3,"Scaled batches must not bypass the generator cap")
        end end
    end
end
setup("elite",5,"mixed","travel")
advance(10,false); assert(#minions.units==0,"Speed scaling must not remove the travel gate")
travel=1000; pacing._paused_spawn_types.trickle_hordes=true
advance(1); assert(#minions.units==0)
pacing._paused_spawn_types.trickle_hordes=nil
advance(1); assert(#minions.units>0)
setup("elite",5,"quantity","timer")
advance(0.5)
base:set("spawn_multiplier_elite",1)
assert(D.get_session_scaling().elite.quantity==5,"Running missions retain their multiplier snapshot")
advance(1); assert(#minions.units==10 and emissions[1]==4,"Fivefold elite batch is preserved across bounded chunks")
setup("elite",1,"quantity","timer"); advance(1.5); assert(emissions[1]==2)
-- Native per-minion scaling is still bypassed under the director, avoiding 25x.
local native_wrapper
for _,hook in ipairs(hooks) do if hook.owner==base and hook.target==MS and hook.name=="spawn_minion" then native_wrapper=hook.fn end end
base:set("spawn_multiplier_elite",5)
local calls=0
native_wrapper(function() calls=calls+1; return {} end,minions,"chaos_ogryn_executor",nil,nil,2,{})
assert(calls==1)
-- Triggered reinforcements scale their incoming quota once; speed only drains
-- it faster and never invents additional event triggers.
for _,mode in ipairs({"quantity","speed","mixed"}) do
    setup("common",5,mode,"event")
    advance(1); assert(#minions.units==0)
    local warp=setmetatable({},{__index=NW})
    for _=1,5 do warp:spawn_group({breeds={{name="chaos_poxwalker",amount={2,2}}}},{}) end
    advance(20)
    local expected=10*D.get_session_scaling().common.quantity
    assert(math.abs(#minions.units-math.floor(expected))<1.001,"Event quota was scaled twice or not scaled")
end
-- Map quantity changes create native tracked slots, not unowned spawn calls.
local generate_hook,activate_hook
for _,hook in ipairs(hooks) do
    if hook.owner==D and hook.target==RP then
        if hook.name=="_generate_roamers" then generate_hook=hook.fn end
        if hook.name=="_try_activate_roamer" then activate_hook=hook.fn end
    end
end
for _,mode in ipairs({"quantity","speed","mixed"}) do
    setup("elite",5,mode,"ambient",3)
    local roamer_owner={_patrol_data={patrols={{1,2,3,4,5,6,7,8,9,10}}}}
    local roamers={}
    local pos={unbox=function() return {} end}
    generate_hook(function(_,_,list)
        for i=1,10 do list[i]={breed_name="chaos_ogryn_executor",group_id=17,patrol_id=1,position=pos,side_id=2,roamer_id=i} end
    end,roamer_owner,{},roamers)
    assert(#roamers==math.floor(10*D.get_session_scaling().elite.quantity+0.000001))
    assert(#roamer_owner._patrol_data.patrols[1]==#roamers)
    roamer_owner._roamers=roamers
    advance(0.5)
    for _,roamer in ipairs(roamers) do
        assert(roamer.group_id==17 and roamer.position.unbox==pos.unbox)
        activate_hook(function(_,entry) minions:spawn_minion(entry.breed_name,nil,nil,2,{}); return true end,roamer_owner,roamer,2)
    end
    assert(#minions.units==3,"Tracked map copies must pass the same capacity checks")
end
-- Reproduce the real 15:11:32 crash in the original patrol update function.
local saved_blackboards,saved_astar=BLACKBOARDS,GwNavAStar
BLACKBOARDS={}
GwNavAStar={processing_finished=function() return true end,path_found=function() return true end}
local box={store=function() end,unbox=function() return {} end}
local unit_a,unit_b={},{}
HEALTH_ALIVE[unit_a]=true; HEALTH_ALIVE[unit_b]=true
BLACKBOARDS[unit_a]={patrol={patrol_id=1,walk_position=box}}
BLACKBOARDS[unit_b]={} -- same missing component as the crash locals
local patrol_data={patrols={{1,2}},active_patrols={[1]=true},claimed_patrol_zone_indexes={},
    astar_roamer_unit=unit_a,astar_roamer_position=box,astar_roamer={}}
local ok,err=pcall(NativePatrols.update_roamer_patrols,patrol_data,{{spawned_unit=unit_a},{spawned_unit=unit_b}},{},{})
assert(not ok and err:find("other_patrol_component",1,true),"Must reproduce the exact native crash before testing the fix")
setup("common",1,"quantity","ambient",512)
local safe,bad="renegade_melee","chaos_mutated_poxwalker"
assert(registry[safe].can_patrol and not registry[bad].can_patrol)
D.collect_sources=function() return {{id="patrol_regression",kind="ambient",pool={[safe]=1,[bad]=100},interval=60}} end
advance(0.5)
local roamers={{breed_name=safe,patrol_id=1},{breed_name=safe,patrol_id=1},{breed_name=safe}}
local owner={_roamers=roamers,_patrol_data={patrols={{1,2}}}}
local original_pick=P.pick_prepared
P.pick_prepared=function(pool) return pool.weights[bad] and bad or next(pool.weights) end
local function native_activate(_,entry)
    local unit=minions:spawn_minion(entry.breed_name,nil,nil,2,{})
    entry.spawned_unit=unit
    BLACKBOARDS[unit]=registry[entry.breed_name].can_patrol and {patrol={patrol_id=1,walk_position=box}} or {}
    return true
end
assert(activate_hook(native_activate,owner,roamers[1],2))
assert(activate_hook(native_activate,owner,roamers[2],2))
assert(roamers[1].breed_name==safe and roamers[2].breed_name==safe)
assert(activate_hook(native_activate,owner,roamers[3],2) and roamers[3].breed_name==bad,
    "Non-patrol map slots must retain the player's full pool")
patrol_data.astar_roamer_unit=roamers[1].spawned_unit
patrol_data.astar_roamer=roamers[1]
assert(pcall(NativePatrols.update_roamer_patrols,patrol_data,roamers,{},{}),"Fixed replacements must pass the exact crashing native function")
-- An incompatible-only pool must skip a patrol slot, never ignore the pool.
setup("common",1,"quantity","ambient",512)
D.collect_sources=function() return {{id="patrol_regression",kind="ambient",pool={[bad]=1},interval=60}} end
advance(0.5)
assert(not activate_hook(native_activate,owner,roamers[1],2))
-- A native slot can carry a patrol_id without being a member (e.g. a mixed pack).
setup("common",5,"quantity","ambient",512)
local owner2={_patrol_data={patrols={{1}}}}
local mixed={}
generate_hook(function(_,_,list)
    list[1]={breed_name=safe,patrol_id=1,roamer_id=1}
    list[2]={breed_name=bad,patrol_id=1,roamer_id=2}
end,owner2,{},mixed)
assert(#mixed==10 and #owner2._patrol_data.patrols[1]==5)
for i=7,10 do assert(mixed[i].patrol_id==nil) end
P.pick_prepared=original_pick; BLACKBOARDS=saved_blackboards; GwNavAStar=saved_astar
local phase_hook
for _,hook in ipairs(hooks) do
    if hook.owner==D and hook.target==PM and hook.name=="update" then
        assert(hook.safe,"The director runs after native pacing has updated the frame state")
        phase_hook=hook.fn
    end
end
assert(phase_hook and D.update==nil,"DMF's outer frame update must not also run the director")
local saved_update=D.update_director
local phase_calls=0
D.update_director=function(dt) assert(dt==0.25); phase_calls=phase_calls+1 end
phase_hook({},0.25); assert(phase_calls==0)
phase_hook(pacing,0.25); assert(phase_calls==1)
D.update_director=saved_update
D.collect_sources=original_sources; D.reset_runtime(); Managers.state=old_state
base.has_local_gameplay_authority=old_authority
for _,c in ipairs(P.categories) do base:set("spawn_multiplier_"..c,1); base:set("spawn_mode_"..c,"quantity") end
solo:set("havoc_faction","mixed")
''')
print('Crusher faction/union probability regression; all 4 categories x 5 multipliers x 3 modes; live timer/travel/event/map scheduling, fractional carry, caps, pauses, UI base edits, next-mission snapshot and no double scaling: PASS')
print('Reproduced native other_patrol_component=nil crash; fixed replacements pass original patrol update; incompatible-only pools and nonmember map copies: PASS')
print('Director scheduling moved to current native pacing instance after its update; no duplicate DMF-frame invocation: PASS')
