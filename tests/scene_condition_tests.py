# Run inside the integration harness, including the current runtime's actual hooks.
native_mutator=(game/'scripts/managers/mutator/mutators/mutator_spawner.lua').read_text(encoding='utf-8')
native_trigger=native_mutator.split('MutatorSpawner._trigger_runtime_spawn = function',1)[1].split('\nend',1)[0]
L.globals().native_condition_trigger=L.execute('return function'+native_trigger+'\nend')
L.execute('''
local D,B=mods.HavocEnemyDirector,mods.HavocConditionManager
local P=D.planner
local old_cfg,old_selected,old_active=D.get_config(),B.get_selected_conditions,D.is_active
local selected={"mutator_havoc_rotten_armor"}
B.get_selected_conditions=function() return selected end
D.is_active=function() return true end
D.reset_runtime()
local before=D.preview_generators()
local cfg=D.get_config(); cfg.native_extras_enabled=false; cfg.generators.scripted_encounters={deleted=true}
D.save_config(cfg)
local after=D.preview_generators()
assert(#before==#after)
local armor=false
for i,g in ipairs(before) do
    assert(g.id==after[i].id and g.interval==after[i].interval and g.distance==after[i].distance and g.count==after[i].count)
    for name,weight in pairs(g.pool) do assert(after[i].pool[name]==weight) end
    for id in pairs(g.sources) do if id:find("rotten_armor",1,true) then armor=true end end
end
assert(armor,"Rotten Armour source must still be compiled")
-- Exercise the native ritual/twin runtime trigger through any director hook.
local trigger=native_condition_trigger
for _,h in ipairs(hooks) do
    if h.owner==D and h.name=="_trigger_runtime_spawn" then
        local original=trigger; trigger=function(...) return h.fn(original,...) end
    end
end
local called=0
local location={position={unbox=function() return "position" end},rotation="rotation",level_size="size"}
local function actor(runtime)
    return {is_runtime=function() return runtime end,trigger_spawn=function(_,ray,pos,target,rotation,size)
        assert(ray=="ray" and pos=="position" and target=="player" and rotation=="rotation" and size=="size")
        called=called+1
    end}
end
local owner={_template={name="mutator_monster_spawner"},_raycast_object="ray",_spawners={actor(true),actor(false),actor(true)}}
trigger(owner,location,"player")
assert(called==2,"Scene switch must not suppress native condition actors")
assert(P.defaults().havoc_twins_enabled and P.config({}).havoc_twins_enabled,"Twin ambush is on by default, including existing settings")
for _,scenes in ipairs({false,true}) do for _,extras in ipairs({false,true}) do for _,twins in ipairs({false,true}) do
    cfg=D.get_config(); cfg.generators.scripted_encounters={deleted=not scenes}
    cfg.native_extras_enabled=extras; cfg.havoc_twins_enabled=twins; D.save_config(cfg)
    local n=called
    owner._template.name="mutator_monster_spawner"; trigger(owner,location,"player")
    assert(called==n+2,"Ritual must be independent of all three switches")
    owner._template.name="mutator_monster_havoc_twins"; trigger(owner,location,"player")
    assert(called==n+2+(twins and 2 or 0),"Only the twin switch controls the difficulty ambush")
    owner._template.name="other_named_actor"; trigger(owner,location,"player")
    assert(called==n+4+(twins and 2 or 0))
end end end
cfg=D.get_config(); cfg.native_extras_enabled=false; cfg.havoc_twins_enabled=false
cfg.generators.scripted_encounters={deleted=true}; D.save_config(cfg)
test_view._hcm_page=4; test_view._hcm_choice=nil; test_view._hcm_number=nil
Paging.refresh(test_view,test_settings)
assert(find_control("havoc_twins"))
click_control("havoc_twins"); assert(D.get_config().havoc_twins_enabled)
assert(D.get_config().generators.scripted_encounters.deleted and not D.get_config().native_extras_enabled)
click_control("havoc_twins"); assert(not D.get_config().havoc_twins_enabled)
selected={"mutator_havoc_rotten_armor","mutator_havoc_chaos_rituals"}
D.synchronize_conditions()
assert(D.get_config().generators.scripted_encounters.deleted and not D.get_config().native_extras_enabled)
assert(not D.get_config().havoc_twins_enabled)
D.restore_defaults()
assert(D.get_config().generators.scripted_encounters.deleted and not D.get_config().native_extras_enabled)
assert(not D.get_config().havoc_twins_enabled)
D.is_active=function() return false end
owner._template.name="mutator_monster_havoc_twins"
local n=called; trigger(owner,location,"player"); assert(called==n+2)
B.get_selected_conditions=old_selected; D.is_active=old_active; D.reset_runtime(); D.save_config(old_cfg)
''')
print('Three independent switches: all 8 combinations, Rotten Armour/rituals retained, default-on Havoc twin toggle, UI/save/reset and inactive pass-through: PASS')
