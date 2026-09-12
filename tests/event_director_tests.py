# Run after the full HCM entry point is available.
events=list(catalog.event_ids.keys())
assert len(events)==20
assert all(catalog.category(id)=='event' for id in events)
assert sum(catalog.category(id)=='event' for id in settings.order.havoc_circumstances.values())==24
assert not catalog.category('rations_destroy_embers')
assert not catalog.category('saints_core_gas')
assert not catalog.category('communication_hack_02')
lookup=cache['scripts/network_lookup/network_lookup'].circumstance_templates
before=len(list(lookup.keys()))
catalog.extend(settings)
assert len(list(lookup.keys()))==before,'Native event IDs must not be appended to the network lookup'
missing='mutator_communication_hack_event'
original=mutators[missing]; mutators[missing]=None
assert not catalog.category('communication_hack_01')
mutators[missing]=original

view_source=(stage/'HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/condition_manager_view.lua').read_text(encoding='utf-8')
persist=view_source.split('HavocConditionManagerView._persist_havoc_circumstances = function',1)[1].split('\nend',1)[0]
L.globals().persist_selected=L.execute('''
local mod=mods.HavocConditionManager
local HavocConditions=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/havoc_conditions")
local SoloPlaySettings=test_settings
local function set_setting(key,value) mod:set(key,value) end
local function get_setting(key) return mod:get(key) end
return function'''+persist+'\nend')
L.execute('''
local D,base,solo=mods.HavocEnemyDirector,mods.HavocConditionManager,mods.SoloPlay
local P=D.planner
local saved_state=Managers.state
Managers.state={}
solo:set("havoc_theme_circumstance","default")
solo:set("havoc_difficulty_circumstance","default")
local view={_current={havoc_circumstances={}}}
persist_selected(view)
local function select(ids)
    view._current.havoc_circumstances=ids; persist_selected(view)
end
local function dirty()
    local cfg=D.get_config()
    cfg.generators.travel_special={deleted=true,pool={chaos_hound=0},interval=900}
    cfg.custom={{id="custom_999",category="boss",pool={chaos_spawn=1}}}
    cfg.banned.chaos_hound=true
    cfg.total_cap=2; cfg.category_caps.special=1
    D.save_config(cfg)
    return D.get_config().revision
end
local function sources()
    local ids={}
    for _,source in ipairs(D.collect_sources(true)) do ids[source.id]=source end
    return ids
end
local function generator(id)
    for _,g in ipairs(D.preview_generators()) do if g.id==id or g.id:sub(1,#id+1)==id.."_" then return g end end
end
local baseline=generator("timer_special")
assert(baseline.pool.cultist_flamer and baseline.pool.renegade_flamer)
assert(baseline.pool.cultist_grenadier and baseline.pool.renegade_grenadier)
dirty(); select({"hcm_auric_hounds"})
local fresh=D.get_config()
assert(next(fresh.banned)==nil and #fresh.custom==0)
for _,g in pairs(fresh.generators) do for key in pairs(g) do assert(key=="cap") end end
local scaling=D.get_spawn_scaling()
local highest=1; for _,c in ipairs(P.categories) do highest=math.max(highest,scaling[c].multiplier) end
assert(fresh.total_cap==P.total_capacity_presets[highest] and fresh.category_caps.special==P.default_capacity("special")*scaling.special.multiplier)
assert(generator("travel_special").pool.chaos_hound)
local revision=dirty()
select({"hcm_auric_hounds"})
assert(D.get_config().revision==revision and D.get_config().banned.chaos_hound,"Saving the same selection must preserve manual edits")
select({"hcm_auric_hounds","hcm_auric_mutants"})
assert(not D.get_config().banned.chaos_hound)
local found_hounds,found_mutants=false,false
for id in pairs(sources()) do
    found_hounds=found_hounds or id:find("mutator_chaos_hounds",1,true)~=nil
    found_mutants=found_mutants or id:find("mutator_mutants",1,true)~=nil
end
assert(found_hounds and found_mutants)
local travel=generator("travel_special")
local has_mutant,has_hound=false,false
for _,g in ipairs(D.preview_generators()) do
    if g.kind=="travel" and g.category=="special" then
        has_hound=has_hound or g.pool.chaos_hound~=nil
        for name in pairs(g.pool) do if name:find("cultist_mutant",1,true) then has_mutant=true end end
    end
end
assert(has_hound and has_mutant,"Sources with different native gates may use separate categorized generators")
dirty(); select({"hcm_auric_mutants"})
for id in pairs(sources()) do assert(not id:find("mutator_chaos_hounds",1,true)) end
assert(not generator("travel_special").pool.chaos_hound)
select({"hcm_auric_waves"})
assert(generator("timer_special").interval<baseline.interval,"Shock troops must change the inferred specialist pressure")
select({"abhuman_01"})
assert(sources().mutator_live_abhuman_monster,"Activation-time monster reinforcements must be included")
local roamers=sources().native_roamers.pool
assert(not roamers.renegade_executor and roamers.chaos_ogryn_executor)
select({"hcm_auric_melee"})
assert(not sources().native_roamers.pool.renegade_rifleman)
select({"hcm_auric_ranged"})
assert(sources().native_roamers.pool.renegade_rifleman)
select({}); dirty()
solo:set("havoc_theme_circumstance","darkness_hunting_grounds_01")
base.refresh_condition_generators()
assert(not D.get_config().banned.chaos_hound and generator("travel_special").pool.chaos_hound)
local cfg=D.get_config(); cfg.enabled=false; D.save_config(cfg)
select({"hcm_auric_cooldown"})
assert(not D.get_config().enabled,"Rebuilding must preserve native/advanced mode")
cfg=D.get_config(); cfg.enabled=true; D.save_config(cfg)
local current=D.get_config()
assert(P.config(D:get("director_config_v1")).conditions_signature==current.conditions_signature)
-- A previous mission's replacements must not leak into the new selection preview.
Managers.state={minion_spawn={replacement_breed=function() return "chaos_spawn" end}}
solo:set("havoc_theme_circumstance","default"); select({})
assert(generator("timer_special").pool.renegade_netgunner)
Managers.state=saved_state
''')

# Check native resource rules of barren events reach Havoc's additional conditions.
L.execute('''
local base=mods.HavocConditionManager
local saved=Managers.state
local saved_authority=base.has_local_gameplay_authority
base.has_local_gameplay_authority=function() return true end
Managers.state={difficulty={get_parsed_havoc_data=function() return {circumstances={"barren"}} end}}
local health,stats
local Health=require("scripts/extension_systems/health_station/health_station_system")
local Circumstance=require("scripts/managers/circumstance/circumstance_manager")
for _,hook in ipairs(hooks) do
    if hook.owner==base then
        if hook.target==Health and hook.name=="_fetch_settings" then health=hook.fn end
        if hook.target==Circumstance and hook.name=="mission_overrides" then stats=hook.fn end
    end
end
local original={charges_to_distribute=5}
local settings=health(function() return original end,{},{},"default")
assert(settings.charges_to_distribute==0 and settings.remove_plugged_charges and settings.skip_battery_spawning)
assert(original.charges_to_distribute==5)
assert(stats(function() return {} end,{}).stat_settings)
Managers.state=saved; base.has_local_gameplay_authority=saved_authority
''')
print('20 native events + 4 adaptations; actual UI persistence rebuilds defaults; add/remove/unchanged/environment/mode cases; combined pools, pacing modifiers, preview isolation and event health/stat overrides: PASS')
