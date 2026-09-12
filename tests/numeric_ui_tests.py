L.execute('''
local D,B,N=mods.HavocEnemyDirector,mods.HavocConditionManager,Paging.numeric
local P=D.planner
local old_log_info=Log.info; Log.info=function() end
local old_cfg,old_sources,old_scaling=D.get_config(),D.collect_sources,D.get_spawn_scaling()
local old_buff_capacity=D:get("buff_proc_capacity")
local sources={{id="common",kind="timer",pool={chaos_poxwalker=2},interval=60},
    {id="travel",kind="travel",pool={chaos_poxwalker=2},interval=60,distance=120},
    {id="ambient",kind="ambient",pool={chaos_poxwalker=2}},
    {id="special",kind="timer",pool={renegade_netgunner=2},interval=60}}
D.collect_sources=function() return sources end
local cfg=P.defaults(); cfg.generators.timer_common={count=2,interval=60,cap=100}
D.save_config(cfg)
for _,category in ipairs(P.categories) do B:set("spawn_multiplier_"..category,1); B:set("spawn_mode_"..category,"quantity") end
test_view._hcm_page=4; test_view._hcm_choice=nil; test_view._hcm_step=1
test_view._hed_generator_id="timer_common"; test_view._hed_pool_filter="all"; test_view._hcm_offsets.pool=0
Paging.refresh(test_view,test_settings)
local input=test_view._widgets_by_name.hcm_number_input
local function service(actions,null)
    return {get=function(_,key) return key=="scroll_axis" and {0,0,0} or actions and actions[key] or false end,
        is_null_service=function() return null or false end}
end
local function native_text(strokes,actions)
    test_keystrokes=strokes or {}
    for _,pass in ipairs(input.passes) do
        if pass.pass_type=="logic" and (not pass.visibility_function or pass.visibility_function(input.content,input.style)) then
            pass.value(pass,{input_service=service(actions),scale=1},{parent=input.style},input.content,{0,0,0},{236,50})
        end
    end
    test_keystrokes=nil
end
local function refresh() Paging.refresh(test_view,test_settings) end
local function enter()
    Paging.update(test_view,service({confirm_pressed=true})); refresh()
end
local function type_number(key,text)
    click_control(key); native_text({text})
end
-- Real native selection/keyboard/paste logic; save only once after confirmation.
local revision=D.get_config().revision
type_number("total_cap_value","500")
assert(input.content.input_text=="500" and D.get_config().total_cap==240)
assert(input.visible and test_view.is_text_input_focused and find_control("number_confirm"))
for _,item in ipairs(test_view._hcm_ui.items) do if item.action and not item.overlay then assert(item.blocked) end end
enter()
assert(D.get_config().total_cap==500 and D.get_config().revision==revision+1)
assert(find_control("total_cap_value").text=="500" and not input.visible and not input.content.is_writing)
enter(); assert(D.get_config().revision==revision+1,"Enter must not write twice")
-- Decimal, empty, invalid, out-of-range and non-finite inputs leave the value untouched.
for _,text in ipairs({"1.5","601","-1","abc","1e309","0/0","0x10"}) do
    type_number("total_cap_value",text); enter()
    assert(test_view._hcm_number and test_view._hcm_number.error and D.get_config().total_cap==500,text)
    click_control("number_cancel")
end
click_control("total_cap_value"); native_text({Keyboard.BACKSPACE}); enter()
assert(input.content.input_text=="" and test_view._hcm_number.error and D.get_config().total_cap==500)
native_text({"420"}); enter(); assert(D.get_config().total_cap==420)
-- Corrections, selection and paste go through the shipped game's native input passes.
click_control("cap_elite_value"); test_clipboard=" 125 "
native_text({}, {clipboard_paste=true}); enter()
assert(D.get_config().category_caps.elite==125)
type_number("generator_interval_value","12.75")
native_text({Keyboard.BACKSPACE}); assert(input.content.input_text=="12.7")
native_text({}, {navigate_beginning=true}); native_text({Keyboard.DELETE})
assert(input.content.input_text=="2.7")
native_text({}, {select_all_text=true}); native_text({"12.75"}); enter()
assert(D.get_config().generators.timer_common.interval==12.75)
-- Enter / button / outside-click all run the same refresh and derived-value computation.
click_control("tab_3"); click_control("multiplier_common5"); click_control("mode_commonmixed"); click_control("tab_4")
assert(find_control("total_cap_value").text=="600" and find_control("cap_common_value").text=="600")
type_number("generator_count_value","7"); click_control("number_confirm")
assert(D.get_config().generators.timer_common.count==7)
assert(find_control("generator_count_effective").text==string.format("%.2f",7*math.sqrt(5)))
assert(find_control("generator_interval_effective").text==string.format("%.2f",12.75/math.sqrt(5)))
assert(find_control("generator_explanation").text:find(string.format("%.2f",7*5*60/12.75),1,true))
type_number("generator_interval_value","20")
test_view._widgets_by_name.hcm_popup_blocker.content.hotspot.pressed_callback(); refresh()
assert(D.get_config().generators.timer_common.interval==20)
assert(find_control("generator_interval_effective").text==string.format("%.2f",20/math.sqrt(5)))
type_number("generator_cap_value","321"); enter()
assert(find_control("generator_cap_effective").text=="321" and D.get_config().generators.timer_common.cap==321)
-- Cancel, unedited confirmation and fraction precision never overwrite defaults.
type_number("total_cap_value","300"); assert(N.cancel(test_view)); refresh()
assert(D.get_config().total_cap==600)
local precise=120.123456789
cfg=D.get_config(); cfg.generators.travel_common={distance=precise}; D.save_config(cfg)
test_view._hed_generator_id="travel_common"; refresh()
click_control("generator_distance_value"); enter()
assert(D.get_config().generators.travel_common.distance==precise)
type_number("generator_distance_value","25.125"); enter()
assert(D.get_config().generators.travel_common.distance==25.125)
assert(find_control("generator_distance_effective").text==string.format("%.2f",25.125/math.sqrt(5)))
local weight_key="weight_chaos_poxwalker"
assert(find_control(weight_key))
type_number(weight_key,"0.025"); enter()
assert(D.get_config().generators.travel_common.pool.chaos_poxwalker==0.025)
assert(find_control(weight_key).text=="<0.1")
click_control(weight_key); assert(input.content.input_text=="0.025"); enter()
assert(D.get_config().generators.travel_common.pool.chaos_poxwalker==0.025)
type_number(weight_key,"0"); enter(); assert(find_control(weight_key).text=="0")
test_view._hed_generator_id="ambient_common"; refresh()
for _,key in ipairs({"count","interval","distance"}) do assert(not find_control("generator_"..key.."_value").action) end
test_view._hed_generator_id="timer_common"; refresh()
assert(not find_control("generator_distance_value").action)
-- Exercise the exact post-hotspot logic pass, with current-frame native hotspot state.
local function hold_frame(key,dt,hover,pressed,held)
    Paging.update(test_view,service({left_hold=held})); refresh()
    local _,widget=find_control(key); local hotspot=widget.content.hotspot
    hotspot.is_hover=hover; hotspot._input_pressed=held; hotspot.on_pressed=pressed; hotspot.on_double_click=false
    assert(widget.passes[1].pass_type=="hotspot" and widget.passes[2].pass_type=="logic")
    widget.passes[2].value(nil,{dt=dt},nil,widget.content)
    refresh()
end
-- The relocated Buff input persists independently and stays usable in native mode.
D:set("buff_proc_capacity",nil); refresh()
assert(find_control("buff_proc_capacity_value").text=="300")
local spec=find_control("buff_proc_capacity_value").number
assert(spec.min==300 and spec.max==3000 and spec.integer)
type_number("buff_proc_capacity_value","750"); enter()
D.reset_buff_proc_capacity(); assert(D.get_session_buff_proc_capacity()==750)
for _,text in ipairs({"299","3001","750.5"}) do
    type_number("buff_proc_capacity_value",text); enter()
    assert(test_view._hcm_number.error and D:get("buff_proc_capacity")==750)
    click_control("number_cancel")
end
click_control("director_enabled"); click_control("choice_director_enabled_native")
revision=D.get_config().revision
click_control("buff_proc_capacity_plus")
hold_frame("buff_proc_capacity_plus",0.01,true,true,true)
for i=1,4 do hold_frame("buff_proc_capacity_plus",0.1,true,false,true) end
hold_frame("buff_proc_capacity_plus",0.08,true,false,false)
assert(D:get("buff_proc_capacity")==752 and not test_view._hcm_hold)
assert(D.get_config().revision==revision and D.get_session_buff_proc_capacity()==750)
type_number("buff_proc_capacity_value","3000"); enter()
click_control("buff_proc_capacity_plus"); assert(D:get("buff_proc_capacity")==3000)
type_number("buff_proc_capacity_value","300"); enter()
click_control("buff_proc_capacity_minus"); assert(D:get("buff_proc_capacity")==300)
click_control("director_enabled"); click_control("choice_director_enabled_advanced")
D:set("buff_proc_capacity",old_buff_capacity); D.reset_buff_proc_capacity(); refresh()
type_number("generator_count_value","10"); enter()
click_control("generator_count_plus")
assert(D.get_config().generators.timer_common.count==11)
hold_frame("generator_count_plus",0.01,true,true,true)
for i=1,3 do hold_frame("generator_count_plus",0.1,true,false,true) end
hold_frame("generator_count_plus",0.09,true,false,true)
assert(D.get_config().generators.timer_common.count==11,"No repeat before 400 ms")
hold_frame("generator_count_plus",0.01,true,false,true)
assert(D.get_config().generators.timer_common.count==12)
hold_frame("generator_count_plus",0.08,true,false,true)
assert(D.get_config().generators.timer_common.count==13,"Repeat must use fresh values after UI refresh")
hold_frame("generator_count_plus",0.08,true,false,false)
assert(D.get_config().generators.timer_common.count==13 and not test_view._hcm_hold)
-- Leaving, returning without a new press, rapid taps, context changes and focus loss.
click_control("generator_count_minus"); hold_frame("generator_count_minus",0.1,false,false,true)
assert(not test_view._hcm_hold)
hold_frame("generator_count_minus",0.1,true,false,true)
assert(D.get_config().generators.timer_common.count==12)
local _,button=find_control("generator_count_plus")
button.content.hotspot.double_click_callback(); refresh()
assert(D.get_config().generators.timer_common.count==13)
click_control("tab_3"); assert(not test_view._hcm_hold); click_control("tab_4")
click_control("generator_count_plus"); Paging.update(test_view,service(nil,true))
assert(not test_view._hcm_hold)
click_control("generator_count_plus"); test_view._hed_generator_id="travel_common"; refresh()
hold_frame("generator_count_plus",0.1,true,false,true); assert(not test_view._hcm_hold)
type_number("generator_count_value","9"); Paging.update(test_view,service(nil,true)); refresh()
assert(not test_view._hcm_number and not input.visible and not input.content.is_writing)
type_number("generator_count_value","9"); test_view._hcm_page=3; refresh()
assert(not test_view._hcm_number and not input.visible)
click_control("tab_4"); test_view._hed_generator_id="timer_common"; refresh()
test_view._hcm_step=10 -- A stale view must not change the fixed increment.
type_number("generator_count_value","99"); enter()
click_control("generator_count_plus"); hold_frame("generator_count_plus",0.1,true,false,true)
assert(D.get_config().generators.timer_common.count==100)
type_number("generator_count_value","1"); enter(); click_control("generator_count_minus")
for i=1,7 do hold_frame("generator_count_minus",0.1,true,false,true) end
assert(D.get_config().generators.timer_common.count==1)
N.cancel(test_view)
-- Save a native-coordinate popup preview and check popup bounds under every supported aspect ratio.
numeric_ui_snapshots={}
for _,key in ipairs({"total_cap_value","buff_proc_capacity_value","generator_interval_value",weight_key}) do
    click_control(key)
    local popup=test_view._hcm_ui.popup
    assert(popup.x>=100 and popup.x+popup.w<=1820 and popup.y>=130 and popup.y+popup.h<=964)
    numeric_ui_snapshots[key]=P.copy(test_view._hcm_ui.items)
    local edit=test_view._hcm_number
    table.insert(numeric_ui_snapshots[key],{key="native_input",x=edit.x+12,y=edit.y+48,w=236,h=50,
        fill=true,text=input.content.input_text,font=24,color="gold",overlay=true})
    for _,resolution in ipairs({{1280,720},{1920,1080},{2560,1440},{3840,2160},{1920,1200},{2560,1600},
        {2560,1080},{3440,1440},{1280,960},{1600,1200},{5120,1440}}) do
        local v=Paging.viewport(resolution[1],resolution[2])
        assert((popup.x+v.x)*v.scale>=0 and (popup.y+v.y)*v.scale>=0)
        assert((popup.x+popup.w+v.x)*v.scale<=resolution[1] and (popup.y+popup.h+v.y)*v.scale<=resolution[2])
    end
    click_control("number_cancel")
end
-- Previously the explicit interval fixture above masked a count-to-cadence bug.
cfg=P.defaults(); cfg.custom={{id="custom_1",category="special",kind="timer",pool={renegade_netgunner=10}}}
D.save_config(cfg)
for _,id in ipairs({"timer_common","travel_common","custom_1"}) do
    test_view._hed_generator_id=id; refresh()
    local interval=find_control("generator_interval_value").text
    local distance=find_control("generator_distance_value").text
    local scaled_interval=find_control("generator_interval_effective").text
    type_number("generator_count_value","7"); enter()
    click_control("generator_count_plus")
    for i=1,6 do hold_frame("generator_count_plus",0.1,true,false,true) end
    hold_frame("generator_count_plus",0.1,true,false,false)
    assert(find_control("generator_interval_value").text==interval)
    assert(find_control("generator_distance_value").text==distance)
    assert(find_control("generator_interval_effective").text==scaled_interval)
    assert(not D.get_config().generators[id].interval and not D.get_config().generators[id].distance)
end
D.collect_sources=old_sources; D.save_config(old_cfg); Log.info=old_log_info
for _,category in ipairs(P.categories) do B:set("spawn_multiplier_"..category,old_scaling[category].multiplier); B:set("spawn_mode_"..category,old_scaling[category].mode) end
''')
layouts=json.loads((CHECKS/'ui-layout.json').read_text(encoding='utf-8'))
for key,items in L.globals().numeric_ui_snapshots.items(): layouts['numeric_'+key]=plain_items({'items':items})
(CHECKS/'ui-layout.json').write_text(json.dumps(layouts,ensure_ascii=False,indent=2),encoding='utf-8')
print('Native keyboard/selection/paste, numeric commit/cancel/ranges/precision, derived values, 400 ms hold / 80 ms repeat, release/leave/focus/context, bounds and 11 popup resolutions: PASS')
