# Exercise the real multiplier buttons and advanced-page controls with known bases.
L.execute('''
local D,B=mods.HavocEnemyDirector,mods.HavocConditionManager
local P=D.planner
local saved_sources,saved_cfg,saved_state=D.collect_sources,D.get_config(),Managers.state
local saved_scaling=D.get_spawn_scaling()
local breeds={common="chaos_poxwalker",elite="chaos_ogryn_executor",special="renegade_netgunner",boss="chaos_spawn"}
local sources={}
local cfg=P.defaults()
for _,category in ipairs(P.categories) do
    B:set("spawn_multiplier_"..category,1); B:set("spawn_mode_"..category,"quantity")
    for _,kind in ipairs({"timer","travel","event","ambient"}) do
        sources[#sources+1]={id=kind.."_"..category,kind=kind,pool={[breeds[category]]=2},interval=60,distance=120}
        cfg.generators[kind.."_"..category]={count=2,interval=60,distance=120,cap=45}
    end
end
Managers.state={}
D.collect_sources=function() return sources end
D.save_config(cfg)
local revision=D.get_config().revision
test_view._hcm_page=4; test_view._hcm_choice=nil; test_view._hcm_step=1
test_view._hed_pool_filter="all"; test_view._hcm_offsets.pool=0
Paging.refresh(test_view,test_settings)
multiplier_ui_snapshots={}
for _,category in ipairs(P.categories) do
    for _,mode in ipairs({"quantity","speed","mixed"}) do
        for _,n in ipairs({1,2,5}) do
            click_control("tab_3")
            click_control("multiplier_"..category..n)
            click_control("mode_"..category..mode)
            assert(B:get("spawn_multiplier_"..category)==n and B:get("spawn_mode_"..category)==mode)
            click_control("tab_4")
            local quantity=mode=="quantity" and n or mode=="mixed" and math.sqrt(n) or 1
            local speed=mode=="speed" and n or mode=="mixed" and math.sqrt(n) or 1
            for _,kind in ipairs({"timer","travel","event","ambient"}) do
                test_view._hed_generator_id=kind.."_"..category
                Paging.refresh(test_view,test_settings)
                assert(find_control("generator_effective_heading").text=="倍率后 · 预览")
                local function value(key) return find_control("generator_"..key.."_value").text end
                local function effective(key)
                    local item,widget=find_control("generator_"..key.."_effective")
                    assert(not item.action and widget.content.hotspot.disabled,"Effective values are read-only")
                    return item.text
                end
                local saved_cap=D.get_config().generators[kind.."_"..category].cap
                assert(value("cap")==tostring(saved_cap) and effective("cap")==tostring(saved_cap))
                assert(find_control("generator_explanation").text:find("任务内改动下局生效",1,true))
                if kind=="ambient" then
                    assert(value("count")=="—" and effective("count")==string.format("×%.2f",quantity))
                    assert(not find_control("generator_count_plus").action)
                    assert(value("interval")=="—" and effective("interval")=="—")
                else
                    assert(value("count")=="2" and value("interval")=="60.0")
                    assert(effective("count")==string.format("%.2f",2*quantity))
                    assert(effective("interval")==string.format("%.2f",60/speed))
                end
                assert(effective("distance")== (kind=="travel" and string.format("%.2f",120/speed) or "—"))
                if category=="common" and n==5 and (kind=="travel" or kind=="ambient" and mode=="mixed") then
                    multiplier_ui_snapshots[kind.."_"..mode]=P.copy(test_view._hcm_ui.items)
                end
            end
            local kept=D.get_config().generators["timer_"..category]
            assert(kept.count==2 and kept.interval==60 and kept.distance==120,"A multiplier change must preserve manual generation parameters")
        end
    end
end
-- Editing at 5x changes the base once and refreshes its effective neighbour immediately.
test_view._hed_generator_id="travel_common"
Paging.refresh(test_view,test_settings)
click_control("generator_count_plus")
assert(find_control("generator_count_value").text=="3")
assert(find_control("generator_count_effective").text==string.format("%.2f",3*math.sqrt(5)))
assert(D.get_config().generators.travel_common.count==3)
click_control("tab_3"); click_control("multiplier_common1"); click_control("tab_4")
assert(find_control("generator_count_value").text=="3" and find_control("generator_count_effective").text=="3.00")
click_control("tab_3"); click_control("multiplier_elite1"); click_control("tab_4")
assert(find_control("generator_count_effective").text=="3.00","Other enemy categories must not change the selected generator")
local fractional=D.get_config()
fractional.generators.travel_common.distance=120/7
D.save_config(fractional)
Paging.refresh(test_view,test_settings)
assert(find_control("generator_distance_value").text=="17.1")
assert(find_control("generator_distance_effective").text=="17.14")
assert(D.get_config().generators.travel_common.distance==120/7,"Display precision must not round the stored base")
-- Captured previews remain within the safe layout area and have no overlapping buttons.
for _,items in pairs(multiplier_ui_snapshots) do
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
D.collect_sources=saved_sources; Managers.state=saved_state
for _,category in ipairs(P.categories) do
    B:set("spawn_multiplier_"..category,saved_scaling[category].multiplier)
    B:set("spawn_mode_"..category,saved_scaling[category].mode)
end
D.save_config(saved_cfg)
''')
layouts=json.loads((CHECKS/'ui-layout.json').read_text(encoding='utf-8'))
for key,items in L.globals().multiplier_ui_snapshots.items():
    layouts['multiplier_'+key]=plain_items({'items':items})
(CHECKS/'ui-layout.json').write_text(json.dumps(layouts,ensure_ascii=False,indent=2),encoding='utf-8')
print('Actual multiplier page -> advanced page: 4 enemy categories x 3 modes x 1/2/5x x 4 generator types; effective values, stored capacity presets, preserved base parameters and non-overlapping layout: PASS')
