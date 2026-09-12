from pathlib import Path
import sys,re,json
work=Path(__file__).resolve().parent
sys.excepthook=lambda typ,value,tb: print(typ.__name__+': '+str(value))
from project_env import PROJECT, GAME, FIXTURES, CHECKS, SOURCES
from lupa.luajit21 import LuaRuntime
L=LuaRuntime(unpack_returned_tuples=True)
stage=SOURCES; game=GAME
L.execute('''
function settings(_,value) return value end
function table.clone(t) local r={} for k,v in pairs(t or {}) do r[k]=v end return r end
function table.clone_instance(t)
    if type(t)~="table" then return t end
    local r={} for k,v in pairs(t) do r[k]=table.clone_instance(v) end return r
end
function table.merge(a,b) for k,v in pairs(b) do a[k]=v end return a end
function table.merge_recursive(a,b)
    for k,v in pairs(b) do
        if type(v)=="table" and type(a[k])=="table" then table.merge_recursive(a[k],v) else a[k]=table.clone_instance(v) end
    end
    return a
end
function table.merge_recursive_advanced(a,b) return table.merge_recursive(a,b),{} end\nfunction table.enum(...) local r={} for _,s in ipairs({...}) do r[s]=s end return r end
function table.keys(t) local r={} for k in pairs(t) do r[#r+1]=k end return r end
table.enum_id=table.enum
function table.array_contains(t,v) for _,x in ipairs(t) do if x==v then return true end end return false end
function math.clamp(n,a,b) return math.max(a,math.min(n,b)) end
function math.lerp(a,b,t) return a+(b-a)*t end
function math.round(n) return math.floor(n+0.5) end
function math.random_range(a,b) return (a+b)/2 end
function Localize(s)
    local strings=mods and mods.HavocConditionManager and mods.HavocConditionManager.global_localization
    return strings and strings[s] and (strings[s][test_language or "zh-cn"] or strings[s].en) or s
end
Managers={state={}}
Script={new_map=function() return {} end,new_array=function() return {} end}
CLASS={HudElementBossHealth={}}
Application={user_setting=function() return {} end}
mods={}; hooks={}; classes={}; warnings={}
function get_mod(name) return mods[name] end
function new_test_mod(name)
    local m={_settings={},values={},localization={}}
    function m:get(k) return self.values[k] end
    function m:set(k,v) self.values[k]=table.clone_instance(v) end
    function m:is_enabled() return self._enabled~=false end
    function m:enable_all_hooks() self._hooks_enabled=true end
    function m:disable_all_hooks() self._hooks_enabled=false end
    -- DMF always formats translated text, including calls without arguments.
    function m:localize(k,...) local v=self.localization[k]; local s=v and (v[test_language or "zh-cn"] or v.en) or k; return string.format(s,...) end
    function m:io_dofile(p) return load_mod_file(p) end
    function m:add_global_localize_strings(t) self.global_localization=self.global_localization or {}; for k,v in pairs(t) do self.global_localization[k]=v end end
    function m:hook(target,name,fn) hooks[#hooks+1]={target=target,name=name,fn=fn,owner=self,safe=false} end
    function m:hook_safe(target,name,fn) hooks[#hooks+1]={target=target,name=name,fn=fn,owner=self,safe=true} end
    function m:hook_require(path,fn) hooks[#hooks+1]={path=path,fn=fn,owner=self,require_hook=true} end
    function m:info(...) end
    function m:warning(...) warnings[#warnings+1]={...} end
    function m:error(...) error(string.format(...)) end
    function m:add_require_path(...) end
    function m:register_view(...) end
    function m:notify(...) end
    mods[name]=m
    return m
end
''')
def lua_file(path): return L.execute(path.read_text(encoding='utf-8-sig'),name='@'+str(path))
def load_mod(p): return lua_file(stage/(p+'.lua'))
L.globals().load_mod_file=load_mod
cache={}
def tbl(x):
    if isinstance(x,dict): return L.table_from({k:tbl(v) for k,v in x.items()})
    if isinstance(x,list): return L.table_from([tbl(v) for v in x])
    return x
breeds={}
for p in (game/'scripts/settings/breed/breeds').rglob('*_breed.lua'):
    s=p.read_text(encoding='utf-8'); tags=re.search(r'\btags\s*=\s*\{(.*?)\}',s,re.S)
    if not tags: continue
    name=p.stem.removesuffix('_breed')
    kind=re.search(r'breed_type\s*=\s*breed_types\.(\w+)',s)
    breeds[name]={'name':name,'breed_type':kind.group(1) if kind else 'minion',
        'airbound':bool(re.search(r'airbound\s*=\s*true',s)),
        'can_patrol':bool(re.search(r'can_patrol\s*=\s*true',s)),
        'sub_faction_name':(re.search(r'sub_faction_name\s*=\s*"(\w+)"',s).group(1) if re.search(r'sub_faction_name\s*=\s*"(\w+)"',s) else None),
        'can_be_used_for_all_factions':bool(re.search(r'can_be_used_for_all_factions\s*=\s*true',s)),
        'tags':{k:True for k in re.findall(r'(\w+)\s*=\s*true',tags.group(1))},'display_name':name}
cache['scripts/settings/breed/breeds']=tbl(breeds)
cache['scripts/managers/horde/horde_templates']=tbl({n:{'name':n} for n in ('trickle_horde','ambush_horde','far_vector_horde','flood_horde','far_distance_horde')})
cache['scripts/utilities/attack/player_unit_status']=tbl({})
cache['scripts/utilities/breed_queries']=L.eval('{minion_breeds_by_name=function() return require("scripts/settings/breed/breeds") end}')
cache['scripts/settings/perception/perception_settings']=tbl({'aggro_states':{'aggroed':'aggroed','passive':'passive'}})
cache['scripts/managers/mutator/mutators/mutator_spawner/mutator_spawner_node']=tbl({'SINGLE_PLACEMENT':1,'CIRCLE_PLACEMENT':2})
cache['scripts/managers/mutator/mutators/mutator_spawner/mutator_spawner_location_sources']=L.eval('{prebaked_mission_locations=function() return {} end, mission_provided_gizmo=function() return {} end}')
cache['scripts/settings/components/enemy_event_spawner_settings']=tbl({'nurgle_totem':{}})
cache['scripts/network_lookup/network_lookup']=tbl({'buff_templates':{},'circumstance_templates':{}})
# Reproduce the engine's missing-key error instead of using permissive plain tables.
network_source=(game/'scripts/network_lookup/network_lookup.lua').read_text(encoding='utf-8-sig')
lookup_init=network_source.split('local function _init(name, lookup_table)',1)[1].split('\nend',1)[0]
L.execute('table.dump=function() end')
init_lookup=L.execute('return function(name,lookup_table)'+lookup_init+'\nend')
for lookup_name,lookup_table in cache['scripts/network_lookup/network_lookup'].items():
    init_lookup(lookup_name,lookup_table)

cache['scripts/settings/buff/buff_templates']=tbl({'NON_PREDICTED':{},'mutator_minion_nurgle_blessing_tougher':{'name':'mutator_minion_nurgle_blessing_tougher'}})
cache['scripts/utilities/loaded_dice']=L.eval('{create=function() return {},{} end}')
cache['scripts/managers/ui/ui_widget']=L.eval('''{create_definition=function(passes,node,content,size)
    local d={passes=passes,scenegraph_id=node,content=table.clone_instance(content or {}),style={},size=size}
    for _,p in ipairs(passes) do
        if p.style_id then d.style[p.style_id]=table.clone_instance(p.style or {}) end
        if p.value_id and p.value then d.content[p.value_id]=p.value end
        if p.content_id then d.content[p.content_id]={} end
    end
    return d
end}''')
real_roots=('scripts/managers/pacing/utilities/','scripts/managers/pacing/templates/','scripts/managers/pacing/roamer_pacing/templates/',
    'scripts/managers/pacing/specials_pacing/templates/','scripts/managers/pacing/monster_pacing/templates/',
    'scripts/managers/pacing/horde_pacing/templates/','scripts/managers/pacing/horde_pacing/compositions/',
    'scripts/settings/roamer/','scripts/settings/mutator/templates/','scripts/settings/havoc/','scripts/settings/circumstance/')
real_files={'scripts/managers/pacing/pacing_templates','scripts/managers/pacing/horde_pacing/horde_compositions',
    'scripts/managers/pacing/monster_pacing/boss_patrols','scripts/settings/horde/horde_settings','scripts/settings/buff/buff_settings',
    'scripts/settings/havoc_settings','scripts/settings/circumstance/templates/havoc_circumstance_template'}
class_paths={}
def require(path):
    if path in cache: return cache[path]
    f=game/(path+'.lua')
    if (path in real_files or path.startswith(real_roots) or path.endswith('_pacing_templates')) and f.exists():
        value=lua_file(f); cache[path]=value; return value
    if path in ['scripts/managers/pacing/pacing_manager','scripts/managers/pacing/roamer_pacing/roamer_pacing',
        'scripts/managers/pacing/horde_pacing/horde_pacing','scripts/managers/pacing/specials_pacing/specials_pacing','scripts/managers/pacing/heat_pacing/heat_pacing',
        'scripts/managers/pacing/monster_pacing/monster_pacing','scripts/managers/minion/minion_spawn_manager',
        'scripts/managers/mutator/mutators/mutator_spawner','scripts/managers/mutator/mutators/mutator_nurgle_warp',
        'scripts/managers/horde/horde_manager','scripts/managers/mutator/mutators/mutator_modify_havoc',
        'scripts/managers/mutator/mutator_manager','scripts/managers/game_mode/game_mode_extensions/game_mode_extension_havoc',
        'scripts/managers/circumstance/circumstance_manager','scripts/extension_systems/health_station/health_station_system',
        'scripts/extension_systems/hazard_prop/hazard_prop_system']:
        value=tbl({});cache[path]=value;class_paths[path]=value;return value
    raise RuntimeError('Missing harness dependency: '+path)
L.globals().require=require
# Load authoritative data, then register all ten reference words with their actual source code.
pacing=require('scripts/managers/pacing/pacing_templates')
circ=require('scripts/settings/circumstance/templates/havoc_circumstance_template')
cache['scripts/settings/circumstance/circumstance_templates']=L.eval('table.clone')(circ)
mutators=tbl({})
for path in ['scripts/settings/mutator/templates/mutator_havoc_templates','scripts/settings/mutator/templates/mutator_minion_nurgle_blessing_templates',
             'scripts/settings/mutator/templates/mutator_extra_trickle_templates',
             'scripts/settings/mutator/templates/mutator_modify_pacing_templates','scripts/settings/mutator/templates/mutator_positive_templates']:
    for key,value in require(path).items(): mutators[key]=value
cache['scripts/settings/mutator/mutator_templates']=mutators
L.execute('new_test_mod("SoloPlay"); new_test_mod("HavocConditionManager"); mods.HavocConditionManager.has_local_gameplay_authority=function() return true end')
loc=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/HavocConditionManager_localization')
L.globals().mods.HavocConditionManager.localization=loc
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/reference_conditions')
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/native_spawn')
exec((work/'load_event_test_data.py').read_text(encoding='utf-8'),globals())
catalog=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_catalog')
settings=tbl({'order':{'havoc_circumstances':[]},'lookup':{'havoc_circumstances':{}},'loc':{'havoc_circumstances':{},'circumstances':{}}})
# Stale SoloPlay difficulty rows must be removed from both order and lookup.
settings.lookup.havoc_circumstances.mutator_increased_difficulty=True
settings.lookup.havoc_circumstances.mutator_highest_difficulty=True
catalog.extend(settings)
assert not settings.lookup.havoc_circumstances.mutator_highest_difficulty
assert not catalog.category('mutator_increased_difficulty')
assert catalog.category('mutator_havoc_rotten_armor')=='havoc'
assert catalog.category('more_old_rotten_armor')=='havoc'
assert catalog.category('more_havoc_monster_specials')=='maelstrom'
assert catalog.category('more_havoc_nurgle_blessing')=='maelstrom'
assert catalog.category('more_havoc_assault_force')=='maelstrom'
assert catalog.category('more_havoc_abhuman')=='event'
assert catalog.category('more_havoc_elite_army')=='event'
assert catalog.category('more_havoc_endless_hordes')=='event'
assert catalog.category('more_havoc_barrel_grounds')=='event'
assert catalog.category('more_faction_combined')=='faction'
assert not catalog.category('unknown_havoc_event')
auric=L.globals().mods.HavocConditionManager.auric_conditions
assert len(list(auric.entries.keys()))==20
assert sum(catalog.category(id)=='maelstrom' for id in settings.order.havoc_circumstances.values())==23
native_flash=require('scripts/settings/circumstance/templates/flash_mission_circumstance_template')
native_mutators={m for template in native_flash.values() for m in template.mutators.values()}
native_lookup=cache['scripts/network_lookup/network_lookup'].circumstance_templates
templates=cache['scripts/settings/circumstance/circumstance_templates']
for id,entry in auric.entries.items():
    template=templates[id]
    assert native_lookup[native_lookup[id]]==id
    assert template.theme_tag=='default'
    assert catalog.category(id)=='maelstrom'
    assert id in settings.lookup.havoc_circumstances
    assert not settings.loc.havoc_circumstances[id].startswith('hcm_auric_')
    for m in template.mutators.values():
        assert m in native_mutators and mutators[m] is not None,(id,m)
# Only environmental setup supplies these mutually exclusive map states.
assert all(m not in {'mutator_darkness_los','mutator_ventilation_purge_los','mutator_toxic_gas_volumes'}
           for id in auric.entries.keys() for m in templates[id].mutators.values())
assert templates.hcm_auric_no_ammo.mission_overrides.pickup_settings.primary.ammo.small_clip[1]==-99
assert templates.hcm_auric_barrels.mission_overrides.hazard_prop_settings.none==0
before=len(list(native_lookup.keys()))
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/auric_conditions')
assert len(list(native_lookup.keys()))==before
# A reload with the module cache cleared must reuse every protected lookup ID.
registered={id:native_lookup[id] for id in auric.entries.keys()}
L.globals().mods.HavocConditionManager.auric_conditions=None
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/auric_conditions')
assert len(list(native_lookup.keys()))==before
assert all(native_lookup[id]==number and native_lookup[number]==id for id,number in registered.items())
print('Protected native NetworkLookup: first registration, cached reload and uncached reload: PASS')

environment_families={
    'darkness':['darkness_01','darkness_hunting_grounds_01'],
    'ventilation_purge':['ventilation_purge_01','ventilation_purge_with_snipers_01'],
    'toxic_gas':['toxic_gas_01','toxic_gas_cultist_grenadier'],
    'ember':['ember_01_havoc'],
}
for family in environment_families:
    for id,template in require('scripts/settings/circumstance/templates/'+family+'_circumstance_template').items():
        templates[id]=template
havoc_settings=require('scripts/settings/havoc_settings')
settings.order.havoc_theme_circumstances=tbl([id for ids in environment_families.values() for id in ids])
settings.lookup.theme_of_circumstances=tbl({'default':'default',**{id:family for family,ids in environment_families.items() for id in ids}})
allowed={}
for family,missions in havoc_settings.missions.items():
    for mission in missions.values():
        allowed.setdefault(mission,{})
        for id in environment_families.get(family,[]): allowed[mission][id]=True
settings.lookup.theme_circumstances_of_havoc_missions=tbl(allowed)
for ids in environment_families.values():
    for id in ids:
        settings.loc.havoc_circumstances[id]=id
# Each selectable environment must have a matching map theme and real loaded mutators.
for mission in allowed:
    for family,ids in environment_families.items():
        expected=family in havoc_settings.missions and mission in list(havoc_settings.missions[family].values())
        for id in ids:
            assert bool(catalog.environment_available(settings,mission,id))==expected,(mission,id)
assert not catalog.environment_available(settings,'unknown_map','darkness_01')
assert not catalog.environment_available(settings,'cm_habs','missing_template')
for mission in allowed:
    assert catalog.environment_available(settings,mission,'default')
print('Environment allowlists: 19 native maps; darkness 13, fog 9, gas 6; unknown maps and unsupported ember excluded: PASS')

print('20 native Auric mechanisms, 23 gold entries, network registration, localization, resource overrides and taxonomy: PASS')
L.globals().test_settings=settings
L.globals().test_catalog=catalog
L.globals().test_templates=pacing
L.execute('''
mods.HavocConditionManager.condition_catalog=test_catalog
mods.HavocConditionManager.get_selected_conditions=function() return test_settings.order.havoc_circumstances end
mods.HavocConditionManager.open_condition_manager_view=function() end
new_test_mod("HavocEnemyDirector")
''')
L.globals().mods.HavocEnemyDirector.localization=load_mod('HavocEnemyDirector/scripts/mods/HavocEnemyDirector/HavocEnemyDirector_localization')
load_mod('HavocEnemyDirector/scripts/mods/HavocEnemyDirector/HavocEnemyDirector')
generators=L.globals().mods.HavocEnemyDirector.preview_generators()
print('Loaded actual Havoc templates and reference registrations:',len(settings.order.havoc_circumstances),'selectable conditions;',len(generators),'preview generators')
L.globals().preview_generators=generators
L.execute('''
local categories={}
for _,g in ipairs(preview_generators) do
    categories[g.category]=true
    assert(g.interval>=1 and g.interval<=3600)
end
assert(categories.common and categories.elite and categories.special and categories.boss)
assert(type(mods.HavocEnemyDirector.build_dashboard)=="function")
''')
print('Actual-template preview, four categories and advanced editor construction: PASS')
L.globals().game_classes=tbl(class_paths)
L.execute('''
mods.HavocConditionManager.get_selected_conditions=function() return {} end
local D=mods.HavocEnemyDirector
local MS=game_classes["scripts/managers/minion/minion_spawn_manager"]
local HM=game_classes["scripts/managers/horde/horde_manager"]
local PM=game_classes["scripts/managers/pacing/pacing_manager"]
local SP=game_classes["scripts/managers/pacing/specials_pacing/specials_pacing"]
local RP=game_classes["scripts/managers/pacing/roamer_pacing/roamer_pacing"]
local registry=require("scripts/settings/breed/breeds")
local minions={units={}}
setmetatable(minions,{__index=MS})
function MS:spawned_minions() return self.units end
function MS:total_allocated_num_enemies() return #self.units end
function MS:replacement_breed(name) return self._mutator_breed_data and self._mutator_breed_data.breed_replacement[name] end
function MS:mutator_breed_init(ctx) self._mutator_breed_data=ctx end
HEALTH_ALIVE={}
function MS:spawn_minion(name,position,rotation,side,params)
    local unit={breed=registry[name]}
    assert(unit.breed,"Unknown breed "..tostring(name))
    self.units[#self.units+1]=unit
    HEALTH_ALIVE[unit]=true
    return unit
end
ScriptUnit={extension=function(unit) return {breed=function() return unit.breed end} end}
function HM:horde(kind,template,side,target,composition)
    for _,entry in ipairs(composition.breeds) do
        for i=1,entry.amount[1] do minions:spawn_minion(entry.name,nil,nil,side,{}) end
    end
    return true,nil,nil,1
end
function PM:spawn_type_enabled() return true end
function SP:_get_breed_name(name)
    local factions=self._template.faction_bound_breeds
    return factions and factions[name] and (factions[name].renegade or next(factions[name])) or name
end
function SP:_spawn_special() return "native_special" end
function RP:_try_activate_roamer() return "native_roamer" end
function RP:_limit_roamer_breeds() return nil,false end
-- Install the director hooks in the same wrap/safe order used by DMF.
for _,hook in ipairs(hooks) do
    if hook.owner==D and not hook.require_hook and type(hook.target)=="table" then
        local target,key,fn=hook.target,hook.name,hook.fn
        local original=target[key] or function() end
        if hook.safe then
            target[key]=function(...) local result=original(...); fn(...); return result end
        else target[key]=function(...) return fn(original,...) end end
    end
end
local template=test_templates.havoc
local pacing=setmetatable({_template=template,_horde_pacing={_template=template.horde_pacing_template.resistance_templates[5]},
    _specials_pacing=setmetatable({_template=template.specials_pacing_template.resistance_templates[5],_max_alive_specials=8},{__index=SP}),
    _monster_pacing={_template=template.monster_pacing_template.challenge_templates[5]},
    _roamer_pacing={_roamer_template=template.roamer_pacing_template},
    _paused_spawn_types={},_frozen_spawn_types={},_allowed_spawn_types={trickle_hordes=true,hordes=true,specials=true,monsters=true,roamers=true,terror_events=true},
    _heat_pacing={active=function() return false end},get_mission_progression=function() return 1000 end},{__index=PM})
Managers.state={pacing=pacing,minion_spawn=minions,horde=setmetatable({},{__index=HM}),
    difficulty={get_parsed_havoc_data=function() return {} end,get_table_entry_by_resistance=function(_,t) return t[math.min(5,#t)] end,
        get_table_entry_by_challenge=function(_,t) return t[math.min(5,#t)] end},
    mutator={_mutators={}},main_path={is_main_path_available=function() return true end,ahead_unit=function() return {} end}}
local cfg=D.get_config()
for _,g in ipairs(D.preview_generators()) do cfg.generators[g.id]={deleted=true} end
cfg.custom={{id="custom_test",kind="timer",category="special",pool={renegade_netgunner=1}}}
cfg.generators.custom_test={count=3,interval=1,cap=4}
cfg.category_caps.special=4
cfg.total_cap=10
D.save_config(cfg)
for i=1,24 do D.update_director(0.25) end
assert(#minions.units==4,"Director must honor its own and category cap")
assert(pacing._specials_pacing:_spawn_special({breed_name="renegade_netgunner"})==false)
assert(pacing._specials_pacing:_spawn_special({breed_name="renegade_netgunner",injected=true})=="native_special")
pacing._paused_spawn_types.trickle_hordes=true
assert(not pacing:spawn_type_enabled("trickle_hordes"))
pacing._paused_spawn_types.trickle_hordes=nil
local roamer=setmetatable({},{__index=RP})
assert(roamer:_try_activate_roamer({breed_name="chaos_poxwalker"})==false,"Deleted ambient generator must not spawn")
cfg.enabled=false
D.save_config(cfg)
assert(D.is_active(),"Configuration changes must not switch half a live mission")
D.reset_runtime(); D.update_director(0.25)
assert(not D.is_active())
assert(pacing._specials_pacing:_spawn_special({breed_name="renegade_netgunner"})=="native_special")
D.reset_runtime()
Managers.state={}
''')
print('Director host scheduling, hard/category/generator caps, pause gates, deleted ambient and next-mission activation: PASS')
L.execute('''
local base=mods.HavocConditionManager
local MS=game_classes["scripts/managers/minion/minion_spawn_manager"]
local PM=game_classes["scripts/managers/pacing/pacing_manager"]
local wrapper
for _,hook in ipairs(hooks) do if hook.owner==base and hook.target==MS and hook.name=="spawn_minion" then wrapper=hook.fn end end
assert(wrapper)
local manager=setmetatable({units={}},{__index=MS})
Managers.state={minion_spawn=manager,pacing={spawn_type_enabled=function() return true end}}
local raw_spawn=function(self,name,position,rotation,side,params)
    local unit={breed=require("scripts/settings/breed/breeds")[name],params=params}
    self.units[#self.units+1]=unit; HEALTH_ALIVE[unit]=true; return unit
end
local params={sentinel="native"}
base:set("spawn_multiplier_common",1)
local unit=wrapper(raw_spawn,manager,"chaos_poxwalker",nil,nil,2,params)
assert(#manager.units==1 and unit.params==params)
base:set("spawn_multiplier_common",5)
manager.units={}
wrapper(raw_spawn,manager,"chaos_poxwalker",nil,nil,2,params)
assert(#manager.units==5)
for _,spawned in ipairs(manager.units) do assert(spawned.breed.name=="chaos_poxwalker") end
for i=6,143 do manager.units[i]={breed=require("scripts/settings/breed/breeds").chaos_poxwalker} end
wrapper(raw_spawn,manager,"chaos_poxwalker",nil,nil,2,params)
assert(#manager.units==145,"Basic multipliers must not expand native allocation capacity")
base:set("spawn_mode_common","speed")
local horde={_current_compositions={breeds={{name="chaos_poxwalker",amount={10,10}}}},_next_horde_at=100,_next_horde_pre_stinger_at=90}
base.scale_native_horde(horde)
assert(horde._next_horde_at==20 and horde._next_horde_pre_stinger_at==10)
base.has_local_gameplay_authority=function() return false end
manager.units={}
wrapper(raw_spawn,manager,"chaos_poxwalker",nil,nil,2,params)
assert(#manager.units==1)
''')
print('Native 1x transparency, exact breed reuse, quantity/cadence scaling and unchanged allocation ceiling: PASS')
# Reject duplicate DMF ownership even when one hook uses a class name and another a table.
for owner in ('HavocConditionManager','HavocEnemyDirector'):
    seen=set()
    for path in (stage/owner).rglob('*.lua'):
        source=path.read_text(encoding='utf-8')
        for obj,method in re.findall(r'mod:hook(?:_safe|_origin)?\(\s*([^,\n]+),\s*"([^"]+)"',source):
            if obj.strip() in ('template',): continue
            token=(obj.strip().strip('"'),method)
            assert token not in seen,(owner,'duplicate hook',token)
            seen.add(token)
print('DMF hook ownership uniqueness: PASS')
exec((work/'ui_tests.py').read_text(encoding='utf-8'),globals())
# Exercise the base entry point and its actual mission-context wrapper.
cache['scripts/settings/wwise_game_sync/wwise_game_sync_settings']=tbl({'state_groups':{'options':{'ingame_menu':'menu'}}})
for path in ('scripts/ui/hud/elements/tactical_overlay/hud_element_tactical_overlay','scripts/ui/views/lobby_view/lobby_view'):
    cache[path]=tbl({})
L.execute('''
function string.split(s,delimiter)
    local result,first={},1
    while true do
        local last=s:find(delimiter,first,true)
        result[#result+1]=s:sub(first,last and last-1 or #s)
        if not last then return result end
        first=last+#delimiter
    end
end
mods.SoloPlay.io_dofile=function() return test_settings end
mods.SoloPlay.has_local_gameplay_authority=function() return true end
mods.SoloPlay.gen_havoc_mission_context=function() return {havoc_data="a;;rank;faction;old;modifiers;seed;tail"} end
mods.SoloPlay.open_solo_view=function() return "native view" end
hcm_native_order=test_settings.order.havoc_circumstances
hcm_native_lookup=test_settings.lookup.havoc_circumstances
''')
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/HavocConditionManager')
L.execute('''
mods.HavocConditionManager:set("havoc_circumstances_serialized","")
mods.SoloPlay:set("havoc_theme_circumstance","default")
assert(mods.SoloPlay.gen_havoc_mission_context().havoc_data=="a;;rank;faction;;modifiers;seed;tail")
local saved_open=mods.HavocConditionManager.open_condition_manager_view
mods.HavocConditionManager.open_condition_manager_view=function() return "expanded view" end
assert(mods.SoloPlay.open_solo_view()=="expanded view")
mods.HavocConditionManager.open_condition_manager_view=saved_open
''')
print('Base entry point and SoloPlay mission-context/view wrappers: PASS')

L.execute('''
local base,solo=mods.HavocConditionManager,mods.SoloPlay
solo:set("havoc_difficulty_circumstance","mutator_increased_difficulty")
base:set("havoc_circumstances_serialized","mutator_highest_difficulty:more_havoc_monster_specials")
local selected=base.get_primary_havoc_conditions()
assert(#selected==1 and selected[1]=="more_havoc_monster_specials")
assert(solo:get("havoc_difficulty_circumstance")=="mutator_highest_difficulty")
local context=solo.gen_havoc_mission_context()
assert(context.havoc_data:find("more_havoc_monster_specials",1,true))
local _,count=context.havoc_data:gsub("mutator_highest_difficulty","")
assert(count==1)
-- Once removed from storage, changing difficulty must not remigrate it.
solo:set("havoc_difficulty_circumstance","mutator_increased_difficulty")
base.get_primary_havoc_conditions()
assert(solo:get("havoc_difficulty_circumstance")=="mutator_increased_difficulty")
''')
print('Stored difficulty migration, single mission application and later player choice: PASS')

L.execute('''
local base,solo=mods.HavocConditionManager,mods.SoloPlay
base:set("havoc_circumstances_serialized","hcm_auric_mutants:hcm_auric_cooldown")
solo:set("havoc_mission","cm_habs")
solo:set("havoc_theme_circumstance","darkness_01")
solo:set("havoc_difficulty_circumstance","mutator_increased_difficulty")
local context=solo.gen_havoc_mission_context()
assert(context.havoc_data:find("hcm_auric_mutants",1,true) and context.havoc_data:find("hcm_auric_cooldown",1,true))
local _,count=context.havoc_data:gsub("darkness_01","")
assert(count==1)
local sources=mods.HavocEnemyDirector.collect_sources(true)
local found=false
for _,source in ipairs(sources) do if source.id:find("mutator_mutants",1,true) then found=true end end
assert(found,"Advanced director must collect native Auric spawn sources")
''')
print('Environment and Auric mission composition, advanced director source collection: PASS')

options_module=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/make_options')
for mission in [*allowed.keys(),'unknown_map']:
    options=options_module.havoc_theme_circumstance(tbl({'havoc_mission':mission}))
    returned={option.id for option in options.values()}
    assert returned=={'default',*allowed.get(mission,{}).keys()},mission
L.execute('''
local solo=mods.SoloPlay
solo:set("havoc_mission","cm_raid")
solo:set("havoc_theme_circumstance","darkness_01")
solo.gen_havoc_mission_context()
assert(solo:get("havoc_theme_circumstance")=="default","A stale incompatible environment must be reset before mission construction")
solo:set("havoc_mission","cm_habs")
solo:set("havoc_theme_circumstance","darkness_hunting_grounds_01")
local context=solo.gen_havoc_mission_context()
assert(solo:get("havoc_theme_circumstance")=="darkness_hunting_grounds_01")
assert(context.havoc_data:find("darkness_hunting_grounds_01",1,true))
''')
print('Actual environment option builder, stale saved selection validation before mission creation: PASS')

# Execute SoloPlay's actual mission constructor with only external metadata helpers mocked.
solo_source=(FIXTURES/'mods/SoloPlay/scripts/mods/SoloPlay/SoloPlay.lua').read_text(encoding='utf-8')
constructor=solo_source.split('mod.gen_havoc_mission_context = function ()',1)[1].split('\nend',1)[0]
L.globals().test_settings.lookup.havoc_modifiers_max_level=tbl({})
L.execute('''
mods.SoloPlay:set("havoc_difficulty",40)
mods.SoloPlay:set("havoc_faction","mixed")
mods.SoloPlay:set("havoc_circumstance1","default")
mods.SoloPlay:set("havoc_circumstance2","default")
mods.SoloPlay.parse_mission_params=function(mission) return mission,{} end
''')
native_constructor=L.execute('''
local mod=mods.SoloPlay
local SoloPlaySettings=test_settings
local NetworkLookup={havoc_modifiers={}}
local function _mission_giver_vo_override() return nil end
return function()
'''+constructor+'\nend')
L.globals().mods.SoloPlay._havoc_condition_manager_context_wrapper=native_constructor
matrix=[]
for mission in allowed:
    for id in settings.order.havoc_theme_circumstances.values():
        solo=L.globals().mods.SoloPlay
        solo.set(solo,'havoc_mission',mission)
        solo.set(solo,'havoc_theme_circumstance',id)
        context=solo.gen_havoc_mission_context()
        fields=context.havoc_data.split(';')
        compatible=bool(allowed[mission].get(id))
        expected_theme=settings.lookup.theme_of_circumstances[id] if compatible else 'default'
        assert fields[0]==mission and fields[2]==expected_theme,(mission,id,fields)
        assert fields[4].split(':').count(id)==(1 if compatible else 0)
        matrix.append({'mission':mission,'environment':id,'compatible':compatible,'applied_theme':fields[2]})
L.execute('''
local solo,base,D=mods.SoloPlay,mods.HavocConditionManager,mods.HavocEnemyDirector
solo:set("havoc_mission","cm_habs")
solo:set("havoc_theme_circumstance","darkness_hunting_grounds_01")
base:set("havoc_circumstances_serialized","")
local before={}
for _,source in ipairs(D.collect_sources(true)) do before[source.id]=true end
base:set("havoc_circumstances_serialized","hcm_auric_hounds")
local after={}
for _,source in ipairs(D.collect_sources(true)) do after[source.id]=true; assert(before[source.id]) end
for id in pairs(before) do assert(after[id]) end
''')
(CHECKS/'environment-compatibility.json').write_text(json.dumps(matrix,ensure_ascii=False,indent=2),encoding='utf-8')
print('133 real SoloPlay mission constructions: correct map theme, automatic fallback, one environment; shared hound sources deduplicated: PASS')
exec((work/'compatibility_tests.py').read_text(encoding='utf-8'),globals())
# DMF io_dofile returns false on failure. The parent modules must stop without a second exception.
original_io=L.globals().mods.HavocConditionManager.io_dofile
L.execute('''
startup_failed_loads=0
mods.HavocConditionManager.io_dofile=function(self,path)
    if path:find("auric_conditions",1,true) then startup_failed_loads=startup_failed_loads+1; return false end
    error("Unexpected dependent module load: "..path)
end
''')
assert load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_catalog') is None
assert L.globals().startup_failed_loads==1
L.execute('''
mods.HavocConditionManager.io_dofile=function(self,path)
    if path:find("reference_conditions",1,true) then return end
    if path:find("condition_catalog",1,true) then return false end
    error("Unexpected load after catalog failure: "..path)
end
''')
assert load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/HavocConditionManager') is None
L.globals().mods.HavocConditionManager.io_dofile=original_io
print('DMF failed-module boolean: one load attempt, no Auric/Catalog cascade or dependent initialization: PASS')
exec((work/'event_director_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'advanced_scaling_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'native_rotten_audit_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'faction_condition_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'multiplier_ui_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'buff_capacity_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'capacity_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'numeric_ui_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'generator_delete_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'pool_membership_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'extra_spawns_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'three_language_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'dmf_localization_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'framework_toggle_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'generator_parameter_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'scene_condition_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'mission_event_tests.py').read_text(encoding='utf-8'),globals())

exec((work/'native_mode_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'preset_tests.py').read_text(encoding='utf-8'),globals())
exec((work/'editor_performance_tests.py').read_text(encoding='utf-8'),globals())
