# Uses the actual catalog and breed metadata loaded by integration_tests.py.
L.execute('''
local D,B,S=mods.HavocEnemyDirector,mods.HavocConditionManager,mods.SoloPlay
local P=D.planner
local saved_state,saved_selection=Managers.state,B.get_selected_conditions
local selected={}
Managers.state={}
B.get_selected_conditions=function() return selected end
S:set("havoc_faction","mixed")
local function choose(ids) selected=ids; return D.collect_sources(true) end
local function find(sources,id) for _,s in ipairs(sources) do if s.id==id then return s end end end
local forced_count=0
for _,id in ipairs(test_settings.order.havoc_circumstances) do
    local sources=choose({id})
    local cfg=P.defaults()
    for i,category in ipairs(P.categories) do
        local pool={}
        for name,breed in pairs(D.breeds) do if D.category_for(breed)==category then pool[name]=10 end end
        cfg.custom[#cfg.custom+1]={id="custom_"..i,category=category,pool=pool}
    end
    local gs=P.compile(sources,cfg,D.breeds,D.category_for,D.preview_resolve)
    if sources.faction then forced_count=forced_count+1 end
    for _,g in ipairs(gs) do
        for name in pairs(g.pool) do
            local breed=D.breeds[name]
            assert(P.faction_allowed(breed,sources.faction),id..":"..name)
            assert(not sources.faction or breed.name=="cultist_vanguard" and sources.faction=="cultist" or breed.can_be_used_for_all_factions or
                (breed.sub_faction_name~="renegade" and breed.sub_faction_name~="cultist") or breed.sub_faction_name==sources.faction)
        end
    end
end
assert(forced_count>=10)
assert(P.faction_allowed(D.breeds.cultist_mutant,"renegade"))
assert(P.faction_allowed(D.breeds.renegade_netgunner,"cultist"))
assert(P.faction_allowed(D.breeds.chaos_ogryn_executor,"cultist"))
assert(not P.faction_allowed(D.breeds.cultist_gunner,"renegade"))
assert(not P.faction_allowed(D.breeds.renegade_gunner,"cultist"))
assert(not P.faction_allowed(D.breeds.cultist_vanguard,"renegade"))
assert(P.faction_allowed(D.breeds.cultist_vanguard,"cultist"))
local cultist_compositions=require("scripts/managers/pacing/horde_pacing/compositions/havoc/havoc_cultist_horde_compositions")
assert(P.collect(cultist_compositions,D.breeds).cultist_vanguard)
for _,ids in ipairs({{"mutator_havoc_rotten_armor","hcm_auric_cultists"},{"hcm_auric_cultists","mutator_havoc_rotten_armor"}}) do
    local preview=choose(ids)
    local live={}
    for _,id in ipairs(ids) do
        for _,name in ipairs(require("scripts/settings/circumstance/circumstance_templates")[id].mutators) do
            live[name]={_template=require("scripts/settings/mutator/mutator_templates")[name]}
        end
    end
    Managers.state={mutator={_mutators=live},difficulty={
        get_parsed_havoc_data=function() return {circumstances=ids,faction="mixed"} end,
        get_table_entry_by_resistance=function(_,t) return t[math.min(5,#t)] end,
        get_table_entry_by_challenge=function(_,t) return t[math.min(5,#t)] end}}
    local actual=D.collect_sources(false)
    assert(preview.faction==actual.faction)
    assert(actual.faction==(ids[2]=="hcm_auric_cultists" and "cultist" or "renegade"))
    Managers.state={}
end
local sources=choose({"mutator_havoc_rotten_armor"})
local cfg=P.defaults()
cfg.custom={{id="custom_1",category="elite",pool={renegade_gunner=1}}}
cfg.generators.custom_1={pool={cultist_gunner=100,renegade_gunner=5}}
local gs=P.compile(sources,cfg,D.breeds,D.category_for,function(name)
    return name=="renegade_gunner" and "cultist_gunner" or name
end)
for _,g in ipairs(gs) do assert(not g.pool.cultist_gunner) end
-- Candidate alternatives produce one monster, and native refill replaces the same lane.
local monsters=find(choose({}),"native_monsters")
local total=0; for _,weight in pairs(monsters.pool) do total=total+weight end
assert(math.abs(total-1)<1e-9)
local abhuman=choose({"abhuman_01"})
assert(not find(abhuman,"native_monsters"))
local extra=find(abhuman,"mutator_live_abhuman_monster")
assert(extra.pool.chaos_plague_ogryn==1 and extra.distance==125)
-- Actual native max/chance/health and independent reference pool/options.
local native=require("scripts/settings/mutator/mutator_templates").mutator_monster_specials.init_modify_pacing.specials_monster_spawn_config
local weak=find(choose({"hcm_auric_monsters"}),"native_monster_specials")
assert(weak.cap==native.max_monsters)
for name,health in pairs(native.health_modifiers) do assert(weak.health_modifiers[name]==health) end
B:set("monster_specials_houndmaster",true)
local combined=choose({"hcm_auric_monsters","more_havoc_monster_specials"})
local ref=find(combined,"more_havoc_monster_specials")
assert(ref.pool.chaos_ogryn_houndmaster and ref.profile=="weak_reference")
assert(ref.health_modifiers.chaos_ogryn_houndmaster==0.4)
assert(find(combined,"native_monster_specials").profile~=ref.profile)
local elite=choose({"elite_army"})
assert(not find(elite,"native_hordes"))
local special=find(elite,"native_specials")
assert(special.kind=="travel" and special.rules.required_challenge==5 and special.rules.move_timer_for_monster)
local rations=find(choose({"rations_destroy"}),"native_hordes")
assert(rations.rules.horde_travel==40)
local saints=find(choose({"saints_core"}),"native_hordes")
assert(saints.rules.horde_travel==25)
-- Mixed-faction reference hooks cannot re-add the excluded faction later.
local RP=require("scripts/managers/pacing/roamer_pacing/roamer_pacing")
local forced={_override_faction="renegade"}
Managers.state={pacing={_roamer_pacing=forced}}
S:set("havoc_faction","combined")
local checked=false
for _,hook in ipairs(hooks) do
    if hook.owner==B and hook.target==RP and hook.name=="current_faction" then
        assert(hook.fn(function() return "cultist" end,forced)=="renegade")
        checked=true
    end
end
assert(checked)
Managers.state={};S:set("havoc_faction","mixed")
-- Only unit effects are not interpreted as missing spawn streams.
local baseline=choose({})
for _,id in ipairs({"mutator_havoc_duplicating_enemies","mutator_havoc_thorny_armor","mutator_encroaching_garden"}) do
    local effects=choose({id})
    assert(#effects==#baseline)
    for i,source in ipairs(effects) do assert(source.id==baseline[i].id) end
end
choose({"mutator_havoc_rotten_armor"})
D.save_config(P.defaults())
test_view._hcm_page=4;test_view._hcm_choice=nil;test_view._hed_generator_id="ambient_common"
test_view._hed_pool_filter="all";test_view._hcm_offsets.pool=0
Paging.refresh(test_view,test_settings)
local locked=find_control("ban_cultist_melee")
assert(locked and locked.text=="阵营" and not locked.action)
assert(not find_control("weight_plus_cultist_melee").action)
assert(not find_control("weight_plus_cultist_vanguard").action)
assert(find_control("preview_summary").text:find("血痂",1,true))
-- Difficulty ladders use the selected tier rather than flattening all tiers.
local real=require("scripts/managers/pacing/pacing_templates").havoc.roamer_pacing_template
local saved_density=real.density_settings
real.density_settings={
    {low={packs={breeds={{name="cultist_melee",amount=1}}}},high={packs={breeds={{name="cultist_melee",amount=1}}}}},
    {low={packs={breeds={{name="renegade_melee",amount=1}}}},high={packs={breeds={{name="renegade_melee",amount=1}}}}}}
Managers.state={difficulty={get_table_entry_by_resistance=function(_,t) return t[1] end,get_table_entry_by_challenge=function(_,t) return t[1] end}}
local low=find(choose({}),"native_roamers").pool
assert(low.cultist_melee and not low.renegade_melee)
real.density_settings=saved_density
Managers.state=saved_state; B.get_selected_conditions=saved_selection; D.reset_runtime()
''')
print('All 64 catalog entries: faction-safe defaults/custom overrides; native shared units, replacement results, conflict order, monster alternatives/refills, weak presets, event pacing and selected-tier pools: PASS')
layouts=json.loads((CHECKS/'ui-layout.json').read_text(encoding='utf-8'))
layouts['4']=plain_items(L.globals().test_view._hcm_ui)
(CHECKS/'ui-layout.json').write_text(json.dumps(layouts,ensure_ascii=False,indent=2),encoding='utf-8')
