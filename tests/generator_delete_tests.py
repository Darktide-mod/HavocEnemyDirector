L.execute('''
local D,B=mods.HavocEnemyDirector,mods.HavocConditionManager
local P=D.planner
local old_cfg,old_sources,old_scaling=D.get_config(),D.collect_sources,D.get_spawn_scaling()
local selection=P.conditions_signature(B.get_selected_conditions())
local sources={{id="common",kind="timer",pool={chaos_poxwalker=2},interval=60},
    {id="special",kind="timer",pool={renegade_netgunner=2},interval=60,cap=8},
    {id="travel",kind="travel",pool={chaos_poxwalker=2},interval=60,distance=120},
    {id="ambient",kind="ambient",pool={chaos_poxwalker=2}}}
D.collect_sources=function() return sources end
for _,category in ipairs(P.categories) do B:set("spawn_multiplier_"..category,1); B:set("spawn_mode_"..category,"mixed") end
D.restore_defaults()
test_view._hcm_page=4; test_view._hcm_choice=nil; test_view._hcm_step=10
test_view._hed_generator_id="timer_common"; test_view._hed_pool_filter="all"
test_view._hcm_offsets.generators=0; test_view._hcm_offsets.pool=0
local function refresh() Paging.refresh(test_view,test_settings) end
local function find(id)
    for _,g in ipairs(D.preview_generators()) do if g.id==id then return g end end
end
local function input(key,value)
    click_control(key)
    test_view._widgets_by_name.hcm_number_input.content.input_text=tostring(value)
    click_control("number_confirm")
end
refresh()
local original_count=#D.preview_generators()
assert(original_count==4 and not find_control("step_1") and not find_control("step_5") and not find_control("step_10") and not find_control("step_label"))
input("generator_interval_value",12.75)
click_control("generator_interval_plus")
assert(find("timer_common").interval==13.75,"Fixed increment preserves typed decimal precision")
click_control("generator_interval_minus"); assert(find("timer_common").interval==12.75)
-- Pause stays in the list; delete leaves both the UI and the compiled collection.
click_control("generator_enabled")
assert(find_control("generator_timer_common") and not find("timer_common").enabled)
assert(#D.preview_generators()==original_count and find("timer_common").interval==12.75)
click_control("generator_enabled"); assert(find("timer_common").enabled)
click_control("delete_generator")
assert(not find_control("generator_timer_common") and not find("timer_common"))
assert(test_view._hed_generator_id=="timer_special" and #D.preview_generators()==original_count-1)
assert(D.get_config().generators.timer_common.deleted and not D.get_config().generators.timer_common.interval)
refresh(); assert(not find_control("generator_timer_common"))
-- Persisted settings, page entry and capacity presets cannot resurrect deleted defaults.
D.save_config(P.config(D:get("director_config_v1")))
click_control("tab_3"); click_control("multiplier_common5"); click_control("multiplier_special5"); click_control("tab_4")
assert(not find("timer_common") and not find_control("generator_timer_common"))
assert(D.get_config().generators.timer_common.deleted)
click_control("restore_all_generators")
assert(find("timer_common") and #D.preview_generators()==original_count)
assert(find("timer_common").interval~=12.75 and find("timer_common").enabled)
assert(find("timer_common").cap==600 and find("timer_special").cap==40)
-- Custom generators leave both definition and override tables.
test_view._hed_add_category=1; click_control("add_generator")
local custom=test_view._hed_generator_id
input("generator_count_value",9)
assert(find(custom) and D.get_config().generators[custom].count==9)
click_control("delete_generator")
assert(not find(custom) and not find_control("generator_"..custom))
assert(#D.get_config().custom==0 and D.get_config().generators[custom]==nil)
-- Reuse the lowest free custom number, without renumbering surviving definitions.
assert(D.get_config().next_id==1,"Deleting the only custom generator must release #1")
click_control("add_generator")
assert(test_view._hed_generator_id==custom and find(custom).count~=9)
click_control("add_generator"); local second=test_view._hed_generator_id
click_control("add_generator"); local third=test_view._hed_generator_id
assert(custom=="custom_1" and second=="custom_2" and third=="custom_3")
input("generator_count_value",17)
click_control("generator_enabled") -- Paused generators still own their number.
test_view._hed_generator_id=second; refresh()
input("generator_interval_value",777)
click_control("delete_generator")
assert(D.get_config().next_id==2)
assert(find(third).count==17 and not find(third).enabled)
-- Old saved counters are ignored on load, even when much higher than the surviving IDs.
local saved=P.copy(D:get("director_config_v1")); saved.next_id=999999
assert(P.config(saved).next_id==2 and saved.next_id==999999)
D.save_config(saved); refresh()
click_control("add_generator")
assert(test_view._hed_generator_id==second and D.get_config().generators[second]==nil)
assert(find(second).interval~=777 and find(third).count==17 and not find(third).enabled)
assert(D.get_config().next_id==4)
test_view._hed_generator_id=third; refresh(); click_control("delete_generator")
click_control("add_generator"); assert(test_view._hed_generator_id==third)
for _=1,3 do click_control("delete_generator"); click_control("add_generator"); assert(test_view._hed_generator_id==third) end
-- Definitions with an empty pool still reserve their ID; orphan overrides do not.
local raw={next_id=1,custom={{id="custom_1",category="common",kind="timer",pool={}}},
    generators={custom_2={deleted=true,count=99,interval=777}}}
assert(P.config(raw).next_id==2)
D.save_config(raw); refresh(); click_control("add_generator")
assert(test_view._hed_generator_id==second and find(second) and D.get_config().generators[second]==nil)
assert(#D.get_config().custom==2 and D.get_config().custom[1].id==custom)
-- An empty list still offers add and global reset.
while #D.preview_generators()>0 do click_control("delete_generator") end
assert(test_view._hed_generator_id==nil and find_control("no_generator"))
assert(not find_control("delete_generator") and not find_control("generator_count_value"))
assert(find_control("restore_all_generators").action and find_control("add_generator").action)
generator_delete_snapshots={empty=P.copy(test_view._hcm_ui.items)}
click_control("add_generator"); assert(#D.get_config().custom==1 and find(test_view._hed_generator_id))
-- Reset uses current conditions and multipliers for generators, pools, bans and all caps.
local cfg=D.get_config()
cfg.enabled=true; cfg.total_cap=1; cfg.category_caps.special=1
cfg.banned.renegade_netgunner=true; cfg.generators.scripted_encounters={deleted=true}
cfg.generators.timer_special={deleted=true,interval=777,pool={renegade_netgunner=0}}
D.save_config(cfg)
test_view._hed_pool_filter="banned"
click_control("restore_all_generators")
cfg=D.get_config()
assert(cfg.enabled and #cfg.custom==0 and next(cfg.banned)==nil and cfg.next_id==1)
assert(cfg.generators.scripted_encounters.deleted,"Reset generators must retain the map-event switch")
assert(cfg.total_cap==600 and cfg.category_caps.common==600 and cfg.category_caps.special==80)
assert(find("timer_special").pool.renegade_netgunner>0 and find("timer_special").cap==40)
assert(test_view._hed_pool_filter=="all" and test_view._hcm_offsets.generators==0 and test_view._hcm_offsets.pool==0)
assert(#D.preview_generators()==original_count and P.conditions_signature(B.get_selected_conditions())==selection)
assert(B:get("spawn_multiplier_common")==5 and B:get("spawn_mode_common")=="mixed")
for _,g in ipairs(D.preview_generators()) do assert(g.enabled) end
local revision=cfg.revision
click_control("restore_all_generators")
assert(D.get_config().revision==revision+1 and #D.preview_generators()==original_count)
generator_delete_snapshots.restored=P.copy(test_view._hcm_ui.items)
-- Deleting the final row of a long list keeps its neighbour visible.
for i=1,10 do click_control("add_generator") end
custom=test_view._hed_generator_id
click_control("delete_generator")
assert(not find(custom) and #D.get_config().custom==9)
assert(find_control("generator_"..test_view._hed_generator_id))
assert(test_view._hcm_offsets.generators==#D.preview_generators()-8)
for _,items in pairs(generator_delete_snapshots) do
    local actions={}
    for _,item in ipairs(items) do
        assert(item.x>=100 and item.x+item.w<=1820 and item.y>=130 and item.y+item.h<=1025,item.key)
        if item.action then actions[#actions+1]=item end
    end
    for i,a in ipairs(actions) do for j=i+1,#actions do
        local b=actions[j]
        assert(a.x+a.w<=b.x or b.x+b.w<=a.x or a.y+a.h<=b.y or b.y+b.h<=a.y,a.key.." overlaps "..b.key)
    end end
end
D.collect_sources=old_sources
for _,category in ipairs(P.categories) do B:set("spawn_multiplier_"..category,old_scaling[category].multiplier); B:set("spawn_mode_"..category,old_scaling[category].mode) end
D.save_config(old_cfg)
''')
layouts=json.loads((CHECKS/'ui-layout.json').read_text(encoding='utf-8'))
for key,items in L.globals().generator_delete_snapshots.items():
    layouts['generators_'+key]=plain_items({'items':items})
    for width,height in ratios:
        vp=paging.viewport(width,height)
        for item in layouts['generators_'+key]:
            x,y=(item['x']+vp.x)*vp.scale,(item['y']+vp.y)*vp.scale
            assert x>=0 and y>=0 and x+item['w']*vp.scale<=width and y+item['h']*vp.scale<=height
(CHECKS/'ui-layout.json').write_text(json.dumps(layouts,ensure_ascii=False,indent=2),encoding='utf-8')
print('Delete/pause UI -> compiled generators; lowest free custom IDs, old saved counters, surviving/paused/empty-pool IDs and clean reused overrides; persistent deletion, empty-list/add/reset, fixed increments, scroll and 11 resolutions: PASS')
