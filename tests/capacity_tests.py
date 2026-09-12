L.execute('''
local D,B=mods.HavocEnemyDirector,mods.HavocConditionManager
local P,S=D.planner,D.capacity_stats
local old_cfg,old_sources,old_state,old_authority,old_info=D.get_config(),D.collect_sources,Managers.state,B.has_local_gameplay_authority,D.info
local old_scaling=D.get_spawn_scaling()
Managers.state={}; D.reset_runtime(); B.has_local_gameplay_authority=function() return true end
for _,category in ipairs(P.categories) do B:set("spawn_multiplier_"..category,1); B:set("spawn_mode_"..category,"mixed") end
local sources={{id="common",kind="timer",pool={chaos_poxwalker=2},interval=1},
    {id="special",kind="timer",pool={renegade_netgunner=2},interval=1,cap=8,breed_caps={renegade_netgunner=3}}}
D.collect_sources=function() return sources end
local cfg=P.defaults(); cfg.generators.timer_common={count=7,interval=12,pool={chaos_poxwalker=3}}
D.save_config(cfg); D.apply_capacity_presets()
test_view._hcm_page=4; test_view._hed_generator_id="timer_common"; test_view._hcm_choice=nil
test_view._hcm_step=1; test_view._hcm_offsets.pool=0; test_view._hed_pool_filter="all"
Paging.refresh(test_view,test_settings)
assert(not find_control("capacity_mode") and not find_control("total_cap_effective"))
assert(find_control("total_cap_value").text=="240")
capacity_ui_snapshots={}
for n=1,5 do
    click_control("tab_3")
    for _,category in ipairs(P.categories) do click_control("multiplier_"..category..n) end
    click_control("tab_4")
    local saved=D:get("director_config_v1")
    assert(saved.total_cap==P.total_capacity_presets[n] and find_control("total_cap_value").text==tostring(saved.total_cap))
    for _,category in ipairs(P.categories) do
        assert(saved.category_caps[category]==P.default_capacity(category)*n)
        assert(find_control("cap_"..category.."_value").text==tostring(saved.category_caps[category]))
    end
    assert(saved.generators.timer_common.cap==120*n and find_control("generator_cap_value").text==tostring(120*n))
    assert(saved.generators.timer_special.cap==8*n,"Use the generator's native source cap")
    assert(saved.generators.timer_common.count==7 and saved.generators.timer_common.interval==12 and saved.generators.timer_common.pool.chaos_poxwalker==3)
    if n==5 then capacity_ui_snapshots.five=P.copy(test_view._hcm_ui.items) end
end
assert(P.config({total_cap=600}).total_cap==600 and P.config({total_cap=99999}).total_cap==600)
local saved=D.get_config()
local special
for _,g in ipairs(D.preview_generators()) do if g.category=="special" then special=g end end
assert(special.cap==40 and special.breed_caps.renegade_netgunner==3)
assert(P.effective(special,D.get_spawn_scaling()).cap==40,"Do not scale saved caps in runtime")
-- Deployment may already contain the requested numeric caps before the first game load.
local upgrading=D.get_config(); upgrading.capacity_preset_version=nil
for _,category in ipairs(P.categories) do upgrading.capacity_multipliers[category]=1 end
D.save_config(upgrading); D.apply_capacity_presets()
assert(D.get_config().total_cap==600 and D.get_config().generators.timer_special.cap==40)
saved=D.get_config()
local revision=saved.revision
D.apply_capacity_presets(); assert(D.get_config().revision==revision)
click_control("total_cap_minus"); assert(D.get_config().total_cap==599)
click_control("cap_elite_minus"); assert(D.get_config().category_caps.elite==224)
click_control("tab_3"); click_control("multiplier_common4"); click_control("tab_4")
assert(D.get_config().total_cap==600 and D.get_config().category_caps.elite==224)
assert(D.get_config().category_caps.common==480 and D.get_config().generators.timer_common.cap==480)
click_control("tab_3")
for _,category in ipairs(P.categories) do click_control("multiplier_"..category.."1") end
click_control("tab_4")
assert(D.get_config().total_cap==240 and D.get_config().category_caps.elite==45 and D.get_config().generators.timer_common.cap==120)
capacity_ui_snapshots.one=P.copy(test_view._hcm_ui.items)
click_control("tab_3")
for _,category in ipairs(P.categories) do click_control("multiplier_"..category.."5") end
click_control("tab_4")
assert(D.get_config().total_cap==600 and D.get_config().generators.timer_common.cap==600)
local stats=S.new(); local g={id="timer_common",category="common",cap=120,enabled=true}
S.observe(stats,1,100,{common=100},{timer_common=100},P.defaults(),{g})
S.budget(stats,g,P.defaults(),100,100,100,67)
assert(stats.entries["category:common"].limited_checks==1 and stats.entries["category:common"].full_seconds==0)
S.observe(stats,2,120,{common=120},{timer_common=120},P.defaults(),{g})
assert(stats.entries["category:common"].full_seconds==2 and stats.entries["category:common"].peak==120)
local MS=game_classes["scripts/managers/minion/minion_spawn_manager"]
local PM=game_classes["scripts/managers/pacing/pacing_manager"]
local SP=game_classes["scripts/managers/pacing/specials_pacing/specials_pacing"]
local minions=setmetatable({units={}},{__index=MS})
local template=test_templates.havoc
local pacing=setmetatable({_template=template,_horde_pacing={_template=template.horde_pacing_template.resistance_templates[5]},
    _specials_pacing=setmetatable({_template=template.specials_pacing_template.resistance_templates[5]},{__index=SP}),
    _paused_spawn_types={},_frozen_spawn_types={},_allowed_spawn_types={trickle_hordes=true,hordes=true,specials=true,monsters=true,roamers=true,terror_events=true},
    _heat_pacing={active=function() return false end},get_mission_progression=function() return 10000 end},{__index=PM})
local horde={horde=function(_,_,_,side,_,composition)
    for _,entry in ipairs(composition.breeds) do for _=1,entry.amount[1] do minions:spawn_minion(entry.name,nil,nil,side,{}) end end
    return true
end}
Managers.state={pacing=pacing,minion_spawn=minions,horde=horde,difficulty={get_parsed_havoc_data=function() return {} end},
    main_path={is_main_path_available=function() return true end,ahead_unit=function() return {} end}}
local logs={}; D.info=function(_,fmt,...) logs[#logs+1]=string.format(fmt,... ) end
D.collect_sources=function() return {sources[1]} end
cfg=D.get_config(); cfg.generators.timer_common.count=100; cfg.generators.timer_common.interval=1; D.save_config(cfg)
for _=1,700 do D.update_director(0.05) end
assert(#minions.units==600 and D.get_session_config().total_cap==600)
local enabled,reason=pacing:spawn_type_enabled("trickle_hordes")
assert(not enabled and reason=="Hard_allocated_limit_reached")
assert(table.concat(logs,"\\n"):find("total peak=600/600",1,true))
local performance_logs=0
for _,line in ipairs(logs) do if line:find("Director performance",1,true) then performance_logs=performance_logs+1 end end
assert(performance_logs==1 and #logs-performance_logs<=4,"Only one 30-second timing summary; do not log every retry")
for _,category in ipairs(P.categories) do B:set("spawn_multiplier_"..category,1) end
D.apply_capacity_presets()
assert(D.get_config().total_cap==240 and D.get_session_config().total_cap==600,"Preserve current mission snapshot")
D.reset_runtime(); minions.units={}
for _=1,60 do D.update_director(0.05) end
assert(#minions.units==120 and D.get_session_config().total_cap==240)
D.reset_runtime(); minions.units={}
cfg=D.get_config(); cfg.generators.timer_common.cap=3; D.save_config(cfg)
for _=1,60 do D.update_director(0.05) end
assert(#minions.units==3)
D.reset_runtime(); minions.units={}; cfg.category_caps.common=0; D.save_config(cfg)
for _=1,60 do D.update_director(0.05) end
assert(#minions.units==0)
D.reset_runtime(); assert(table.concat(logs,"\\n"):find("mission_end",1,true))
D.info=old_info; D.collect_sources=old_sources; Managers.state=old_state; B.has_local_gameplay_authority=old_authority
for _,category in ipairs(P.categories) do
    B:set("spawn_multiplier_"..category,old_scaling[category].multiplier)
    B:set("spawn_mode_"..category,old_scaling[category].mode)
end
D.save_config(old_cfg)
''')
layouts=json.loads((CHECKS/'ui-layout.json').read_text(encoding='utf-8'))
for key,items in L.globals().capacity_ui_snapshots.items():
    layouts['capacity_'+key]=plain_items({'items':items})
    for width,height in ratios:
        vp=paging.viewport(width,height)
        for item in layouts['capacity_'+key]:
            x,y=(item['x']+vp.x)*vp.scale,(item['y']+vp.y)*vp.scale
            assert x>=0 and y>=0 and x+item['w']*vp.scale<=width and y+item['h']*vp.scale<=height
(CHECKS/'ui-layout.json').write_text(json.dumps(layouts,ensure_ascii=False,indent=2),encoding='utf-8')
print('Fixed presets saved through multiplier buttons: 240/330/420/510/600; class/native-source caps, repeated 1x/5x/reloads, manual values, live 600/120/3/0 limits, mission snapshots and aggregated capacity diagnostics: PASS')
