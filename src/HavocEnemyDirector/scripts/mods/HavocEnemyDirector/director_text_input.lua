local mod=get_mod("HavocEnemyDirector")
local active
local function clear(view)
    if not view then return end
    if view._hed_text_widget then view._hed_text_widget.content.is_writing=false end
    view._hed_text=nil;view._hed_text_widget=nil;view.is_text_input_focused=false;view._hcm_refresh=true
    if active==view then active=nil end
end
function mod.open_director_text(view,title,value,save)
    clear(active);active=view
    view._hcm_choice=nil;view._hcm_hold=nil
    view._hed_text={title=title,value=value,save=save}
    view._hcm_refresh=true
end
local function widget(view)
    if view._hed_text_widget then return view._hed_text_widget end
    local Widget=require("scripts/managers/ui/ui_widget")
    local Input=require("scripts/ui/pass_templates/text_input_pass_templates")
    local passes=table.clone_instance(Input.simple_input_field)
    for _,p in ipairs(passes) do
        if p.pass_type=="hotspot" then p.change_function=function(h) if h.on_pressed then h.parent.is_writing=true end;h.double_click_timer=0 end
        elseif p.style_id=="limit_text" then p.visibility_function=function() return false end
        elseif p.style_id=="focused" then p.visibility_function=function(c) return c.is_writing end
        elseif p.style_id=="display_text" then p.style.font_type="proxima_nova_bold";p.style.font_size=24 end
    end
    local text=view._hed_text.value
    local def=Widget.create_definition(passes,"hcm_layout",{input_text=text,max_length=48,close_on_backspace=false},{820,56})
    local w=Widget.init("hed_director_text",def);w.offset={550,465,65}
    local c=w.content
    c.input_text=text;c.display_text=text;c._input_text=text;c.is_writing=true
    local n=Utf8.string_length(text)
    c.caret_position=n+1;c._caret_position=n+1;c.force_caret_update=true
    view._hed_text_widget=w;return w
end
local function commit(view)
    local state=view._hed_text;if not state then return end
    local value=widget(view).content.input_text
    local ok,why=state.save(value)
    if ok==false then state.error=why or mod:localize("director_invalid_name")
    else clear(view) end
end
function mod.build_director_text(view,ui)
    local state=view._hed_text;if not state then return end
    for _,item in ipairs(ui.items) do item.blocked=true end
    ui.scrolls={};ui.popup={key="hed_text",x=510,y=354,w=900,h=344}
    local start=#ui.items+1
    ui:panel("hed_text_panel",510,354,900,344)
    ui:text("hed_text_title",538,377,844,56,state.title,27,"gold")
    ui:panel("hed_text_input_panel",538,453,844,76)
    ui:text("hed_text_error",538,537,844,56,state.error or mod:localize("director_name_hint"),20,"muted")
    ui:button("hed_text_cancel",538,615,412,52,mod:localize("template_cancel"),function() clear(view) end)
    ui:button("hed_text_save",970,615,412,52,mod:localize("director_save"),function() commit(view) end)
    for i=start,#ui.items do ui.items[i].overlay=true end
    widget(view)
end
function mod.handle_director_text(view,service)
    if not view._hed_text then return end
    if view._hcm_page~=4 or not mod:is_enabled() then clear(view);return end
    local c=widget(view).content
    if view._input_disabled or service.is_null_service and service:is_null_service() then c.is_writing=false end
    if service:get("confirm_pressed") then commit(view) end
    view.is_text_input_focused=view._hed_text~=nil
end
function mod.back_director_text(view)
    if view._hed_text then clear(view);return true end
end
function mod.draw_director_text(view,renderer)
    if view._hed_text then require("scripts/managers/ui/ui_widget").draw(widget(view),renderer) end
end
mod.cleanup_director_text=function(view) clear(view or active) end
return true
