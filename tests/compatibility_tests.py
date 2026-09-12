# Runs inside integration_tests.py against real condition and mission-override data.
import subprocess
def native_source(path):
    target=game/path
    if not target.exists():
        data=subprocess.run(['git','-C',str(game),'show','HEAD:'+path],capture_output=True,check=True).stdout
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
    return target.read_text(encoding='utf-8-sig')

def native_method(path,cls,name,prefix=''):
    source=native_source(path)
    body=source.split(cls+'.'+name+' = function',1)[1].split('\nend',1)[0]
    return L.execute(prefix+'\nreturn function'+body+'\nend')

L.globals().native_load_one=native_method('scripts/managers/mutator/mutator_manager.lua','MutatorManager','load_mutator_from_name',
    'local MutatorTemplates=require("scripts/settings/mutator/mutator_templates")')
L.globals().native_havoc_pickups=native_method('scripts/managers/game_mode/game_mode_extensions/game_mode_extension_havoc.lua',
    'GameModeExtensionHavoc','get_havoc_pickup_overrides','local MissionOverrides=require("scripts/settings/circumstance/mission_overrides")')
pickup_path='scripts/extension_systems/pickups/pickup_system.lua'
for method in ('_get_pickup_pool_from_difficulty','_add_to_table','_remove_table_negative'):
    L.globals()['native'+method]=native_method(pickup_path,'PickupSystem',method)

L.execute('''
local base=mods.HavocConditionManager
local templates=require("scripts/settings/circumstance/circumstance_templates")
local mutators=require("scripts/settings/mutator/mutator_templates")
local overrides=require("scripts/settings/circumstance/mission_overrides")
local MM=require("scripts/managers/mutator/mutator_manager")
local HM=require("scripts/managers/game_mode/game_mode_extensions/game_mode_extension_havoc")
local HS=require("scripts/extension_systems/hazard_prop/hazard_prop_system")
local loader,pickups,barrels
for _,hook in ipairs(hooks) do
    if hook.owner==base then
        if hook.target==MM and hook.name=="_load_mutators" then loader=hook.fn end
        if hook.target==HM and hook.name=="get_havoc_pickup_overrides" then pickups=hook.fn end
        if hook.target==HS and hook.name=="_populate_hazard_props" then barrels=hook.fn end
    end
end
assert(loader and pickups and barrels)
local saved_state=Managers.state
local saved_authority=base.has_local_gameplay_authority
local data={circumstances={"darkness_hunting_grounds_01","hcm_auric_hounds","hcm_auric_hounds"}}
Managers.state={difficulty={get_parsed_havoc_data=function() return data end},
    circumstance={circumstance_name=function() return "default" end},
    mutator={mutator=function() return nil end}}
base.has_local_gameplay_authority=function() return true end
local created,activated,current_id={},{},nil
Log={warning=function(_,format,...) error(string.format(format,...)) end}
local original_require=require
require=function(path)
    if path:find("scripts/managers/mutator/mutators/",1,true)==1 then
        return {new=function(_,is_server,delegate,template)
            local id=current_id
            created[id]=(created[id] or 0)+1
            return {activate=function() activated[id]=(activated[id] or 0)+1 end}
        end}
    end
    return original_require(path)
end
local function execute_loader()
    local instance={_mutators={},_is_server=true,load_mutator_from_name=function(self,id)
            current_id=id; return native_load_one(self,id) end,
        activate_mutator=function(self,id) self._mutators[id]:activate() end}
    loader(function() error("Unexpected unfiltered loader") end,instance,"default")
    return instance
end
local expected={}
for _,id in ipairs(data.circumstances) do
    for _,name in ipairs(templates[id].mutators) do expected[name]=true end
end
local instance=execute_loader()
for name in pairs(expected) do
    assert(created[name]==1,name.." was initialized more than once")
    if mutators[name].activate_on_load then assert(activated[name]==1) end
    assert(instance._mutators[name])
end
assert(#templates.darkness_hunting_grounds_01.mutators>1)
-- Test the new gold conditions with every environment, including shared mutators.
for _,environment in ipairs(test_settings.order.havoc_theme_circumstances) do
    data.circumstances={environment}
    for id in pairs(base.auric_conditions.entries) do
        data.circumstances[#data.circumstances+1]=id
    end
    created,activated={},{}
    execute_loader()
    for name,count in pairs(created) do assert(count==1,name) end
end
-- Every source-backed catalogue entry under every environment; engine-only templates are reported separately.
for _,environment in ipairs(test_settings.order.havoc_theme_circumstances) do
 data.circumstances={environment}
 for _,id in ipairs(test_settings.order.havoc_circumstances) do
  local known=true
  for _,name in ipairs(templates[id].mutators) do if not mutators[name] or mutators[name].class=="native_odin_gameplay" then known=false end end
  if known then data.circumstances[#data.circumstances+1]=id end
 end
 created,activated={},{}
 execute_loader()
 for name,count in pairs(created) do assert(count==1,name) end
end
require=original_require

data.circumstances={"toxic_gas_01","hcm_auric_no_ammo","hcm_auric_no_ammo"}
local result=pickups(native_havoc_pickups,{})
assert(result.primary.ammo.small_clip[1]==-97)
assert(result.primary.grenade.small_grenade[1]==4)
assert(result.primary.wounds.syringe_corruption_pocketable[1]==10)
assert(result.primary.forge_material.small_metal[1]==-99)
assert(overrides.havoc_pickups.pickup_settings.primary.ammo.small_clip[1]==2)
assert(templates.hcm_auric_no_ammo.mission_overrides.pickup_settings.primary.ammo.small_clip[1]==-99)
-- Exercise the actual native difficulty projection, additive merge and negative removal.
local system={_get_pickup_pool_from_difficulty=native_get_pickup_pool_from_difficulty,
    _add_to_table=native_add_to_table,_remove_table_negative=native_remove_table_negative}
for difficulty=1,5 do
    local pool={primary={ammo={small_clip=20,large_clip=20,ammo_cache_pocketable=3},
        grenade={small_grenade=1},wounds={syringe_corruption_pocketable=1}}}
    local adjustment=system:_get_pickup_pool_from_difficulty(result,difficulty)
    system:_add_to_table(pool,adjustment)
    system:_remove_table_negative(pool)
    assert(pool.primary.ammo.small_clip==0 and pool.primary.ammo.large_clip==0 and pool.primary.ammo.ammo_cache_pocketable==0)
    assert(pool.primary.grenade.small_grenade==5 and pool.primary.wounds.syringe_corruption_pocketable==11)
end
-- Main circumstance pickup overrides are already applied by PickupSystem.
Managers.state.circumstance.circumstance_name=function() return "toxic_gas_01" end
assert(not pickups(native_havoc_pickups,{}).primary.wounds)

data.circumstances={"hcm_auric_barrels"}
local hazard={_hazard_prop_settings={none=1}}
barrels(function(self) assert(self._hazard_prop_settings.none==0 and self._hazard_prop_settings.fire==1) end,hazard)
Managers.state.mutator.mutator=function() return {} end
barrels(function(self) assert(self._hazard_prop_settings.none==0 and self._hazard_prop_settings.fire==0) end,hazard)
-- Remote sessions and non-Havoc missions remain native.
base.has_local_gameplay_authority=function() return false end
assert(loader(function() return "native" end,{},"default")=="native")
assert(pickups(native_havoc_pickups,{})==overrides.havoc_pickups.pickup_settings)
assert(base.get_havoc_hazard_settings()==nil)
base.has_local_gameplay_authority=function() return true end
data=nil
assert(loader(function() return "native" end,{},"default")=="native")
assert(pickups(native_havoc_pickups,{})==overrides.havoc_pickups.pickup_settings)
Managers.state=saved_state
base.has_local_gameplay_authority=saved_authority
''')
print('Native mutator initialization deduplicated; gold/environment loads; toxic-gas/no-ammo pickup application at 5 tiers; barrel precedence; remote/non-Havoc pass-through: PASS')

# Catalogue audit records actual template fields, not assumed additive semantics.
rows=[]
for id in settings.order.havoc_circumstances.values():
    t=templates[id]
    effects=[]
    for name in t.mutators.values():
        m=mutators[name]
        if m is None or m['class']=='native_odin_gameplay':
            effects.append(dict(id=name,public_source='unavailable'))
            continue
        fields={key for key in m.keys()}
        effects.append(dict(id=name,engine_class=m['class'],fields=sorted(str(k) for k in fields),
            faction=(m.init_modify_pacing and m.init_modify_pacing.override_faction) or
                    (m.modify_pacing and m.modify_pacing.override_faction),
            native_horde_override=m.pacing_override))
    rows.append(dict(id=id,category=catalog.category(id),effects=effects,
        mission_override_fields=sorted(str(k) for k in (t.mission_overrides or {}).keys())))
(CHECKS/'condition-native-audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(rows)} catalogue entries audited; source-backed entries load once under every environment; missing engine-only implementations recorded separately: PASS')
