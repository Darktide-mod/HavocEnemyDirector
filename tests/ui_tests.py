# Run within integration_tests.py using the existing real-template Lua harness.
L.execute('Color=setmetatable({}, {__index=function() return function() return {255,200,200,200} end end})')
cache['scripts/managers/ui/ui_font_settings']=tbl({f'header_{i}':{'font_size':24,'font_type':'proxima_nova_bold'} for i in range(1,6)})
cache['scripts/settings/difficulty/danger_settings']=tbl([{'color':[255,200,200,200]} for _ in range(5)])
cache['scripts/settings/ui/ui_sound_events']=tbl({})
cache['scripts/utilities/ui/colors']=tbl({})
cache['scripts/ui/pass_templates/button_pass_templates']=L.eval('{default_button={{pass_type="hotspot",content_id="hotspot"},size={347,76}},terminal_button={{pass_type="hotspot",content_id="hotspot"}}}')
cache['scripts/ui/views/mission_board_view/mission_board_view_styles']=tbl({'difficulty_stepper_style':{}})
exec((work/'numeric_ui_support.py').read_text(encoding='utf-8'),globals())
paging=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging')
definitions=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/condition_manager_view_definitions')
L.globals().Paging=paging
L.globals().full_definitions=definitions
L.execute('''
local D=mods.HavocEnemyDirector
D.save_config(D.planner.defaults())
test_view={_widgets_by_name=table.clone_instance(full_definitions.widget_definitions),
    _options={havoc_theme_circumstance={{id="default",display_name="无特殊环境"},{id="darkness_01",display_name="停电"},
        {id="ventilation_purge_01",display_name="通风净化"},{id="toxic_gas_01",display_name="毒气"}}},
    _dropdown_widgets={},
    _spawn_multiplier_widgets={},_current={havoc_circumstances={}},_positions={}}
function test_view:_set_exclusive_focus_on_setting() end
function test_view:_persist_havoc_circumstances() mods.HavocConditionManager:set("havoc_circumstances_serialized",table.concat(self._current.havoc_circumstances,":")) end
function test_view:_condition_display_name(id) return test_settings.loc.havoc_circumstances[id] or id end
function test_view:_set_scenegraph_position(id,x,y,z) self._positions[id]={x,y,z} end
function test_view:_set_scenegraph_size(id,w,h) self._positions[id]=self._positions[id] or {}; self._positions[id].w=w; self._positions[id].h=h end
function find_control(key)
    for i,item in ipairs(test_view._hcm_ui.items) do if item.key==key then return item,test_view._widgets_by_name["hcm_control_"..i] end end
end
function click_control(key)
    local item,widget=find_control(key)
    assert(item and item.action and not widget.content.hotspot.disabled,"Unavailable control "..key)
    widget.content.hotspot.pressed_callback()
    Paging.refresh(test_view,test_settings)
end
test_view._current.havoc_theme_circumstance="default"
test_view._dropdown_widgets.havoc_theme_circumstance={content={hotspot={},entry={on_activated=function(value)
    test_view._current.havoc_theme_circumstance=value
    mods.SoloPlay:set("havoc_theme_circumstance",value)
end}}}
Paging.enter(test_view,test_settings)
assert(not test_view._dropdown_widgets.havoc_theme_circumstance.visible)
assert(not test_view._widgets_by_name.havoc_theme_circumstance_label.visible)
assert(not find_control("environment"))
assert(test_view._hcm_ui.page_count==4 and test_view._widgets_by_name.hcm_previous.content.hotspot.disabled)
test_view._widgets_by_name.hcm_next.content.hotspot.pressed_callback()
Paging.refresh(test_view,test_settings)
assert(test_view._hcm_page==2 and test_view._widgets_by_name.normal_start.visible==false)
local shown=0
for _,item in ipairs(test_view._hcm_ui.items) do if item.key:find("^condition_") then shown=shown+1 end end
assert(shown==math.min(27,#test_settings.order.havoc_circumstances),"Condition list capacity accounts for environment row")
assert(find_control("environment") and find_control("environment_label"))
click_control("environment")
assert(test_view._hcm_ui.popup and not test_view._hcm_ui.popup.upwards)
assert(test_view._current.havoc_theme_circumstance=="default")
click_control("choice_environment_darkness_01")
assert(test_view._current.havoc_theme_circumstance=="darkness_01" and mods.SoloPlay:get("havoc_theme_circumstance")=="darkness_01")
local environment=test_view._current.havoc_theme_circumstance
click_control("select_all")
assert(#test_view._current.havoc_circumstances==#test_settings.order.havoc_circumstances)
click_control("filter_selected")
assert(find_control("condition_"..test_settings.order.havoc_circumstances[1]))
click_control("clear_all")
assert(#test_view._current.havoc_circumstances==0 and find_control("empty"))
click_control("filter_maelstrom")
for _,item in ipairs(test_view._hcm_ui.items) do
    if item.key:find("^condition_") then assert(test_catalog.category(item.key:sub(11))=="maelstrom") end
end
-- Scoped batch edits preserve other categories and never include difficulty.
click_control("select_all")
assert(#test_view._current.havoc_circumstances==23)
click_control("filter_event"); click_control("select_all")
local event_count=0
for _,id in ipairs(test_settings.order.havoc_circumstances) do if test_catalog.category(id)=="event" then event_count=event_count+1 end end
assert(#test_view._current.havoc_circumstances==23+event_count)
click_control("clear_all")
assert(#test_view._current.havoc_circumstances==23)
assert(test_view._current.havoc_theme_circumstance==environment)
click_control("environment")
assert(Paging.close_choice(test_view))
Paging.refresh(test_view,test_settings)
assert(test_view._current.havoc_theme_circumstance==environment)
-- Simulate the native map change callback rebuilding its compatible environment list.
local native_options=test_view._options.havoc_theme_circumstance
test_view._options.havoc_theme_circumstance={{id="default",display_name="无特殊环境"}}
test_view._current.havoc_theme_circumstance="default"; mods.SoloPlay:set("havoc_theme_circumstance","default")
Paging.refresh(test_view,test_settings)
click_control("environment")
assert(not find_control("choice_environment_darkness_01"))
click_control("choice_environment_default")
test_view._options.havoc_theme_circumstance=native_options
-- Long environment lists scroll inside a bounded menu.
for i=1,25 do native_options[#native_options+1]={id="theme_"..i,display_name="测试环境 "..i} end
click_control("environment")
assert(test_view._hcm_ui.popup.y>=130 and test_view._hcm_ui.popup.y+test_view._hcm_ui.popup.h<=964)
assert(find_control("choice_list_environment_down"))
click_control("choice_list_environment_down")
assert(test_view._hcm_offsets.choice_list_environment==1)
click_control("environment")
assert(not test_view._hcm_ui.popup)
while #native_options>4 do table.remove(native_options) end
test_view._hcm_offsets.choice_list_environment=0
click_control("filter_havoc")
assert(not find_control("condition_mutator_highest_difficulty"))
assert(not find_control("condition_more_havoc_monster_specials"))
click_control("filter_faction")
assert(find_control("condition_more_faction_switch"))
click_control("tab_3")
click_control("multiplier_special5")
click_control("mode_specialmixed")
assert(mods.HavocConditionManager:get("spawn_multiplier_special")==5)
assert(mods.HavocConditionManager:get("spawn_mode_special")=="mixed")
click_control("tab_4")
assert(test_view._widgets_by_name.hcm_next.content.hotspot.disabled)
assert(find_control("generator_count_plus") and find_control("pool_heading"))
assert(not find_control("step_10") and not find_control("step_label"))
local cap=D.get_config().total_cap
click_control("total_cap_plus")
assert(D.get_config().total_cap==math.min(D.planner.capacity_limit,cap+1))
click_control("total_cap_minus")
assert(D.get_config().total_cap==math.min(D.planner.capacity_limit,cap+1)-1)
local selected=test_view._hed_generator_id
click_control("delete_generator")
assert(D.get_config().generators[selected].deleted)
assert(not find_control("generator_"..selected) and test_view._hed_generator_id~=selected)
Paging.refresh(test_view,test_settings)
assert(D.get_config().generators[selected].deleted)
click_control("restore_all_generators")
assert(not D.get_config().generators[selected].deleted)
-- Category selection opens upwards; opening/cancelling never changes values.
local initial=test_view._hed_add_category
click_control("new_category")
local popup=test_view._hcm_ui.popup
assert(popup and popup.upwards and popup.y+popup.h<879)
assert(test_view._hed_add_category==initial)
local _,blocked=find_control("add_generator")
assert(blocked.content.hotspot.disabled)
for i,item in ipairs(test_view._hcm_ui.items) do
    if item.action and not item.overlay then assert(test_view._widgets_by_name["hcm_control_"..i].content.hotspot.disabled) end
end
assert(Paging.close_choice(test_view))
Paging.refresh(test_view,test_settings)
assert(not test_view._hcm_ui.popup and test_view._hed_add_category==initial)
click_control("new_category")
test_view._widgets_by_name.hcm_popup_blocker.content.hotspot.pressed_callback()
Paging.refresh(test_view,test_settings)
assert(not test_view._hcm_ui.popup)
click_control("new_category"); click_control("choice_new_category_2")
assert(test_view._hed_add_category==2 and not test_view._hcm_ui.popup)
click_control("director_enabled")
assert(test_view._hcm_ui.popup and not test_view._hcm_ui.popup.upwards)
assert(D.get_config().enabled)
click_control("choice_director_enabled_native")
assert(not D.get_config().enabled)
click_control("director_enabled"); click_control("choice_director_enabled_advanced")
click_control("add_generator")
assert(D.get_config().custom[1].category=="elite")
click_control("generator_trigger")
assert(D.get_config().custom[1].kind=="timer")
assert(find_control("choice_generator_trigger_travel") and not find_control("choice_generator_trigger_ambient"))
click_control("choice_generator_trigger_travel")
assert(D.get_config().custom[1].kind=="travel")
-- Page changes close any open menu, and leave no invisible active overlay.
click_control("new_category")
test_view._widgets_by_name.hcm_previous.content.hotspot.pressed_callback()
Paging.refresh(test_view,test_settings)
assert(not test_view._hcm_ui.popup and not test_view._widgets_by_name.hcm_popup_blocker.visible)
click_control("tab_4")
assert(test_view._hed_generator_id:find("^custom_") and #D.get_config().custom==1)
local chosen_name
for _,item in ipairs(test_view._hcm_ui.items) do
    if item.key:find("^weight_plus_") then chosen_name=item.key:sub(13); break end
end
assert(chosen_name)
click_control("weight_plus_"..chosen_name)
local weight=D.get_config().generators[test_view._hed_generator_id].pool[chosen_name]
click_control("ban_"..chosen_name)
assert(D.get_config().banned[chosen_name])
local value=find_control("weight_"..chosen_name)
assert(math.abs(tonumber(value.text)-weight)<0.051,"Bans must preserve visible configured weights to display precision")
assert(D.get_config().generators[test_view._hed_generator_id].pool[chosen_name]==weight,"Display rounding must not change saved probabilities")
click_control("ban_"..chosen_name)
assert(not D.get_config().banned[chosen_name])
click_control("clear_pool")
for _,weight in pairs(D.get_config().generators[test_view._hed_generator_id].pool) do assert(weight==0) end
assert(not find_control("unit_attack_valkyrie"))
local old_localize=Localize
Localize=function() return '<unlocalized "missing": string not found>' end
assert(not D.unit_display_name("test_enemy",{display_name="missing"}):find("unlocalized",1,true))
Localize=old_localize
-- Large modded catalogs/custom lists use local scrolling without adding global pages.
local original_ids=test_settings.order.havoc_circumstances
test_settings.order.havoc_circumstances=table.clone_instance(original_ids)
for i=1,80 do
    local id="test_large_"..i
    test_settings.order.havoc_circumstances[#test_settings.order.havoc_circumstances+1]=id
    test_settings.lookup.havoc_circumstances[id]=true
end
test_view._hcm_condition_filter="all"; click_control("tab_2")
assert(test_view._hcm_ui.page_count==4 and find_control("conditions_down"))
local hovered
for i,item in ipairs(test_view._hcm_ui.items) do if item.scroll=="conditions" then
    test_view._widgets_by_name["hcm_control_"..i].content.hotspot.is_hover=true; hovered=i; break
end end
Paging.update(test_view,{get=function() return {0,-1,0} end})
assert(test_view._hcm_offsets.conditions==3)
test_view._widgets_by_name["hcm_control_"..hovered].content.hotspot.is_hover=false
test_settings.order.havoc_circumstances=original_ids
test_view._hcm_offsets.conditions=0
D.save_config(D.planner.defaults())
test_view._hed_generator_id=nil
''')
print('Four sections, native side arrows, all conditions, direct multipliers, generator editing, pool bans and local scroll: PASS')
# Check geometry of all four layouts and every click target against other click targets.
L.execute('''
for page=1,4 do
    test_view._hcm_page=page
    Paging.refresh(test_view,test_settings)
    local actions={}
    for _,item in ipairs(test_view._hcm_ui.items) do
        assert(item.x>=100 and item.x+item.w<=1820 and item.y>=130 and item.y+item.h<=1025,item.key.." outside safe area")
        if item.action then actions[#actions+1]=item end
    end
    for i,a in ipairs(actions) do for j=i+1,#actions do
        local b=actions[j]
        assert(a.x+a.w<=b.x or b.x+b.w<=a.x or a.y+a.h<=b.y or b.y+b.h<=a.y,a.key.." overlaps "..b.key)
    end end
    for i=#test_view._hcm_ui.items+1,Paging.control_count do
        local w=test_view._widgets_by_name["hcm_control_"..i]
        assert(w.visible==false and w.content.hotspot.disabled)
    end
end
local nodes=full_definitions.scenegraph_definition
for _,id in ipairs({"normal_mission","normal_side_mission","normal_circumstance","normal_mission_giver",
    "havoc_mission","havoc_faction","havoc_mission_giver","havoc_theme_circumstance","havoc_difficulty_circumstance"}) do
    assert(nodes[id].size[1]==510 and nodes[id].size[2]==52,id)
end
local native={"normal_start","havoc_start","havoc_randomize","normal_difficulty","havoc_modifiers_grid",
    "havoc_modifier_lock","havoc_mission_giver","havoc_difficulty_badge","havoc_difficulty"}
for i,a in ipairs(native) do for j=i+1,#native do
    local an,bn=nodes[a],nodes[native[j]]
    assert(an.parent=="hcm_layout" and bn.parent=="hcm_layout")
    local ax,ay=an.position[1],an.position[2]; local bx,by=bn.position[1],bn.position[2]
    assert(ax+an.size[1]<=bx or bx+bn.size[1]<=ax or ay+an.size[2]<=by or by+bn.size[2]<=ay,a.." overlaps "..native[j])
end end
for _,id in ipairs({"hcm_previous","hcm_next"}) do
    assert(nodes[id].size[1]==80 and nodes[id].position[2]==500)
    assert(full_definitions.widget_definitions[id].style.arrow.size[1]==64)
end
''')
print('All dashboard hitboxes, hidden controls, native mission controls and uniform dropdown dimensions: PASS')
# Export the real declarative UI for a layout preview, using game-independent sample labels.
def plain_items(ui):
    fields=('key','x','y','w','h','text','font','fill','panel','selected','center','danger','color','checkbox','choice','expanded','upwards','overlay','blocked','text_right_padding')
    return [{key:item[key] for key in fields if item[key] is not None} for _,item in ui['items'].items()]
snapshots={}
for page in range(1,5):
    L.globals().test_view._hcm_page=page
    paging.refresh(L.globals().test_view,settings)
    snapshots[str(page)]=plain_items(L.globals().test_view._hcm_ui)
for key in ('new_category','director_enabled','environment'):
    L.globals().test_view._hcm_page=2 if key=='environment' else 4
    L.globals().test_view._hcm_choice=key
    paging.refresh(L.globals().test_view,settings)
    snapshots[key]=plain_items(L.globals().test_view._hcm_ui)
    popup=L.globals().test_view._hcm_ui.popup
    assert popup.y>=130 and popup.y+popup.h<=964
    active=[item for _,item in L.globals().test_view._hcm_ui['items'].items() if item.action and not item.blocked]
    for i,a in enumerate(active):
        for b in active[i+1:]:
            assert a.x+a.w<=b.x or b.x+b.w<=a.x or a.y+a.h<=b.y or b.y+b.h<=a.y,(a.key,b.key)
L.globals().test_view._hcm_choice=None
(CHECKS/'ui-layout.json').write_text(json.dumps(snapshots,ensure_ascii=False,indent=2),encoding='utf-8')

for key,angle in (('hcm_previous',3.141592653589793),('hcm_next',0)):
    definition=definitions.widget_definitions[key]
    assert definition.passes[1].pass_type=='rotated_texture'
    assert abs(definition.style.arrow.angle-angle)<1e-8
    assert definition.style.arrow.pivot[1]==32 and definition.style.arrow.pivot[2]==32
print('Native rotated-arrow parameters, semantic filters, scoped batches and popup input isolation: PASS')

# Use the production viewport transform for standard and ultrawide resolutions.
ratios=[(1280,720),(1920,1080),(2560,1440),(3840,2160),(1920,1200),(2560,1600),(2560,1080),(3440,1440),(1280,960),(1600,1200),(5120,1440)]
results=[]
for width,height in ratios:
    vp=paging.viewport(width,height)
    assert abs(vp.scale-min(width/1920,height/1080))<1e-8
    assert abs((vp.x*2+1920)*vp.scale-width)<1e-6
    assert abs((vp.y*2+1080)*vp.scale-height)<1e-6
    rectangles=[]
    for items in snapshots.values():
        rectangles.extend((i['x'],i['y'],i['w'],i['h'],i['key']) for i in items)
    rectangles.extend((x,500,80,80,'side_arrow') for x in (12,1828))
    for key,node in definitions.scenegraph_definition.items():
        if node.parent=='hcm_layout':
            assert node.size[1]>=0 and node.size[2]>=0
            if key.startswith('hcm_control_'): continue
            x,y=node.position[1],node.position[2]
            if node.horizontal_alignment=='right': x+=1920-node.size[1]
            if node.horizontal_alignment=='center': x+=(1920-node.size[1])/2
            if node.vertical_alignment=='bottom': y+=1080-node.size[2]
            if node.vertical_alignment=='center': y+=(1080-node.size[2])/2
            if key!='canvas': rectangles.append((x,y,node.size[1],node.size[2],key))
    for x,y,w,h,key in rectangles:
        px,py=(x+vp.x)*vp.scale,(y+vp.y)*vp.scale
        assert px>=-0.01 and py>=-0.01 and px+w*vp.scale<=width+.01 and py+h*vp.scale<=height+.01,(width,height,key)
        # Drawing and hotspot inverse transformation share the same scale and scenegraph.
        cx,cy=px+w*vp.scale/2,py+h*vp.scale/2
        assert abs(cx/vp.scale-vp.x-(x+w/2))<1e-6
        assert abs(cy/vp.scale-vp.y-(y+h/2))<1e-6
    results.append({'width':width,'height':height,'scale':vp.scale,'canvas_x':vp.x,'canvas_y':vp.y,'checked_rectangles':len(rectangles)})
L.execute('''
local v=test_view
v._ui_scenegraph={}
function v:set_render_scale(scale) self._render_scale=scale end
function v:trigger_resolution_update() self.resolution_updates=(self.resolution_updates or 0)+1 end
for _,resolution in ipairs({{1920,1080},{3440,1440},{1280,960},{1920,1200},{1920,1080}}) do
    RESOLUTION_LOOKUP={width=resolution[1],height=resolution[2]}
    local expected=Paging.viewport(resolution[1],resolution[2])
    Paging.fit(v)
    assert(v._render_scale==expected.scale)
    assert(v._widgets_by_name.hcm_popup_blocker.style.hotspot.size[1]*expected.scale==resolution[1])
    local count=v.resolution_updates
    Paging.fit(v)
    assert(v.resolution_updates==count)
end
v._ui_scenegraph=nil; RESOLUTION_LOOKUP=nil
''')
(CHECKS/'aspect-ratio-checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('11 resolutions: 16:9, 16:10, 21:9, 4:3, 32:9; full bounds, inverse hit coordinates, live resize: PASS')
