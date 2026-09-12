"""Native lifecycle methods execute unchanged; navigation/engine are boundaries."""
from pathlib import Path
import sys
PROJECT_HED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT_HED.parent/"HavocConditionManager/tests"))
from native_harness import *
L.execute('new_test_mod("HavocEnemyDirector"); mods.SoloPlay.has_local_gameplay_authority=function() return host end')
load_mod("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_director")

def method(path,owner,name):
    text=(game/path).read_text(encoding="utf-8-sig")
    start=text.index(owner+"."+name+" = function")
    return text[start:text.index("\nend",start)+4]
special="scripts/managers/pacing/specials_pacing/specials_pacing.lua"
monster="scripts/managers/pacing/monster_pacing/monster_pacing.lua"
L.execute("""
table.clear=function(t) for k in pairs(t) do t[k]=nil end end
local SpecialsPacing,MonsterPacing={},{}
local USED_BREEDS={}
local DEFAULT_MIN_TIMER_DIFF_RANGE={3,5}
local Breeds=A.breeds
local perception_aggro_states={aggroed="aggroed",passive="passive"}
local pacing_types={default=1,timer_based=2}
"""+"\n".join(method(special,"SpecialsPacing",name) for name in
    ("_setup_specials_slot","try_inject_special","get_num_specials_owned_by_auto_event"))+
"\n"+method(monster,"MonsterPacing","_spawn_monster")+
"\nNativeSpecials=SpecialsPacing;NativeMonsters=MonsterPacing")
L.execute("""
local D=mods.HavocEnemyDirector
local Adapter=D:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_spawning")
local Spawn=require("scripts/managers/pacing/pacing_manager")
local boxes=function(value) return {unbox=function() return value end} end
Vector3Box=boxes;Quaternion={identity=function() return "rotation" end}
HEALTH_ALIVE={};BLACKBOARDS={}
local t=100
local position={x=100,y=2,z=0};local player="player"
local context={side_id=2,target=player,reachable_target=position}
local groups={next_id=1,locked={},unlocked=0}
function groups:generate_group_id() local id=self.next_id;self.next_id=id+1;return id end
function groups:lock_group_id(id) assert(not self.locked[id]);self.locked[id]=true end
function groups:unlock_group_id(id) assert(self.locked[id]);self.locked[id]=nil;self.unlocked=self.unlocked+1 end
local spawned={}
local minions={_spawn_queue_size=0,allocated=0}
function minions:request_param_table() return {} end
function minions:total_allocated_num_enemies() return self.allocated end
function minions:spawn_minion(name,pos,rotation,side,params)
    assert(pos==position and side==2 and rotation=="rotation")
    local unit="unit"..(#spawned+1)
    spawned[#spawned+1]={unit=unit,name=name,params=params}
    HEALTH_ALIVE[unit]=true
    BLACKBOARDS[unit]={patrol={walk_position={store=function(_,value) assert(value==position) end}}}
    return unit
end
local specials={_max_alive_specials=2,_specials_slots={{spawned=false},{spawned=false}},
    _template=A.by_id["specials/default_specials/1"].root,_timer_modifier=1}
setmetatable(specials,{__index=NativeSpecials})
local monsters={_template=A.by_id["monsters/default_monsters/1"].root,
    _health_modifier=1,_pacing_type=1,_aggroed_monster_units={},_alive_monsters={}}
setmetatable(monsters,{__index=NativeMonsters})
local native={_side_id=2,_target_side_id=1,_nav_world={},_level_seed=111,_specials_pacing=specials,
    _monster_pacing=monsters,permission=true,forced=0,pauses={}}
function native:get_in_safe_zone() return self.safe==true end
function native:spawn_type_enabled(kind) return self.permission end
function native:spawn_type_allowed(kind) return self.permission end
function native:force_horde_pacing_spawn() self.forced=self.forced+1 end
function native:pause_spawn_type(...) self.pauses[#self.pauses+1]={...} end
function native:state() return "build_up_tension" end
function native:total_challenge_rating() return 0 end
function native:num_aggroed_monsters() return 0 end
function native:get_mission_progression() return 100 end
local side={valid_player_units={player}}
Managers.state={pacing=native,minion_spawn=minions,game_session={},
    terror_event={num_active_events=function() return 0 end},
    extension={system=function(_,name)
        if name=="group_system" then return groups
        elseif name=="side_system" then return {get_side=function() return side end} end
    end}}
Managers.time={time=function() return t end}
local monster_events=0
Managers.event={trigger=function(_,name) assert(name=="monster_spawned");monster_events=monster_events+1 end}
local route=true;local validations=0
B.spawn_placement={
    context=function(side_id,target_side_id,now) assert(side_id==2 and target_side_id==1);return context end,
    anchor=function() return route and position end,
    valid=function(_,pos) validations=validations+1;assert(pos==position);return route end,
}
GwNavQueries={flood_fill_from_position=function(nav,anchor,above,below,n,output)
    for i=1,n do output[i]=position end;return n
end}
B.new_spawn_batch=function(source,side_id,target_side_id,event) return {source=source,side_id=side_id,target_side_id=target_side_id,event=event} end
local a=Adapter.new(native,S.coarse_config())
local function job(family,members,id)
    return {family=family,id=id or "hed:test:1",members=members,units={},index=1,wave=1,waves=1,wave_gap=1,next_at=0}
end
local j=job("hordes",{"chaos_poxwalker","chaos_poxwalker"})
route=false;a.update(j,{},0);assert(#spawned==0)
route=true;minions.allocated=145;a.update(j,{},1);assert(#spawned==0)
minions.allocated=0;minions._spawn_queue_size=16;a.update(j,{},2);assert(#spawned==0)
minions._spawn_queue_size=0;native.permission=false;a.update(j,{},3);assert(#spawned==0)
native.permission=true;a.update(j,{},4)
assert(#spawned==1 and j.started and not j.done and groups.locked[j.group_id])
assert(spawned[1].params._hcm_batch.source=="hed_director" and spawned[1].params.optional_aggro_state=="aggroed")
assert(spawned[1].params._hcm_batch.event==j.id,"HCM must retain independent encounter ownership")
a.update(j,{},4.1);assert(#spawned==1)
a.update(j,{},4.3);assert(#spawned==2 and j.done and groups.unlocked==1 and a.alive(j)==2 and validations==2)
HEALTH_ALIVE[j.units[1]]=false;assert(a.alive(j)==1)

local patrol=job("patrols",{"renegade_melee","renegade_melee"},"hed:patrol")
a.update(patrol,{},5);a.update(patrol,{},5.3)
assert(patrol.done and #patrol.units==2 and spawned[3].params.optional_aggro_state=="passive")
local leader=BLACKBOARDS[patrol.units[1]].patrol
local follower=BLACKBOARDS[patrol.units[2]].patrol
assert(leader.auto_patrol and leader.patrol_index==1 and follower.patrol_leader_unit==patrol.units[1])
local unfinished=job("hordes",{"chaos_poxwalker","chaos_poxwalker"},"hed:cancel")
a.update(unfinished,{},6);assert(groups.locked[unfinished.group_id])
a.cancel(unfinished);assert(unfinished.done and not groups.locked[unfinished.group_id] and HEALTH_ALIVE[unfinished.units[1]])

local boss=job("monsters",{"chaos_plague_ogryn"},"hed:boss")
a.update(boss,{},7)
assert(boss.done and #boss.units==1 and monster_events==1 and #monsters._alive_monsters==1)
assert(monsters._alive_monsters[1].spawned_unit==boss.units[1])
assert(spawned[#spawned].params.optional_health_modifier==1)

local specialist=job("specials",{"renegade_netgunner"},"hed:special")
specials._frozen=true;a.update(specialist,{},7.5);assert(not specialist.started)
specials._frozen=false
a.update(specialist,{},8)
assert(specialist.done and specialist.started and a.alive(specialist)==1)
assert(specials._specials_slots[1].breed_name=="renegade_netgunner" and specials._specials_slots[1].injected)
assert(specials._specials_slots[1].optional_auto_event_id=="hed:special")
assert(specials._specials_slots[2].optional_auto_event_id==nil)
-- Admission preserves native same-breed limits and does not overwrite busy slots.
specials._optional_max_of_same_override={renegade_netgunner=1}
local second=job("specials",{"renegade_netgunner"},"hed:second")
a.update(second,{},9);assert(not second.started and a.alive(specialist)==1)
a.cancel(specialist);assert(a.alive(specialist)==1)
specials:_setup_specials_slot(specials._specials_slots,specials._specials_slots[1],specials._template,1,"renegade_netgunner",0)
assert(a.alive(specialist)==0)

-- The actual runtime hook is host-only and freezes settings for this pacing
-- owner. Disabling the saved director affects the next mission, not mid-fight.
local cfg=D.director_config.validate({})
cfg.director.enabled=true
local f=D.director_config.new_formation(cfg,"Runtime","hordes","chaos_poxwalker")
local d=D.director_config.new_deployment(cfg,"Runtime rule",f.id)
d.first_delay=0;d.interval={1,1};d.cooldown=0.5;d.max_occurrences=0;d.max_alive=4
assert(D.save_config(cfg))
local update,remove
for _,h in ipairs(hooks) do
    if h.owner==D and h.target==Spawn and h.name=="update" then update=h.fn end
    if h.owner==D and h.target==Spawn and h.name=="delete" then remove=h.fn end
end
assert(update and remove)
require("scripts/utilities/attack/player_unit_status").requires_help=function() return false end
ScriptUnit={has_extension=function(unit,name)
    if name=="unit_data_system" then return {read_component=function() return {} end} end
end}
local previous=#spawned
host=false;update(native,0.5);update(native,0.5);assert(#spawned==previous)
host=true;update(native,0.5);update(native,0.5);assert(#spawned==previous+1)
cfg.director.enabled=false;assert(D.save_config(cfg))
for _=1,8 do update(native,0.5) end
assert(#spawned>previous+1)
remove(native);previous=#spawned
Managers.state.game_session={};B.template_runtime.reset()
update(native,0.5);update(native,0.5);assert(#spawned==previous)
print("Director native adapter: route/capacity gates, paced groups, patrol leaders, native monster registration, specialist slot ownership, cleanup, host authority and mission snapshots: PASS")
""")
