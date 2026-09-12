local mod=get_mod("HavocEnemyDirector")
local A=mod.presets
local active_view
local function short(text,limit)
    local chars={}; for c in text:gmatch(".[\128-\191]*") do chars[#chars+1]=c; if #chars==limit then break end end
    local prefix=table.concat(chars); return #prefix<#text and prefix.."…" or text
end
local function message(state,key)
    local id,detail=tostring(key or "template_io_failed"):match("^([^:]+):?%s*(.*)$")
    state.status=mod:localize(id)..(detail~="" and " · "..detail or "")
end
local function input(view,text)
    local s=view._hed_library
    s.name=text; s.pending=nil
    local w=view._hed_name_widget
    if w then
        local c=w.content
        c.input_text=text; c.display_text=text; c._input_text=text
        local length=Utf8.string_length(text)
        c.caret_position=length+1; c._caret_position=length+1; c.selected_text=nil
        c._selection_start=nil; c._selection_end=nil; c.force_caret_update=true
    end
end
local function refresh(view)
    local s=view._hed_library
    local entries,err=A.list(); s.entries=entries or {}
    if err then message(s,err) end
    if not s.selected and s.entries[1] then s.selected=s.entries[1].file end
    view._hcm_refresh=true
end
function mod.open_template_library(view)
    view._hed_templates_open=true; view._hcm_choice=nil; view._hcm_hold=nil
    view._hed_library={entries={},name=""}
    refresh(view); active_view=view
end
local function cleanup(view)
    if not view then return end
    local w=view._hed_name_widget
    if w then w.content.is_writing=false; w.content.hotspot.disabled=true end
    if not view._hcm_number then view.is_text_input_focused=false end
    view._hed_templates_open=nil; view._hed_name_widget=nil; view._hed_delete_backdrop=nil; view._hed_library=nil
    view._hcm_refresh=true
    if active_view==view then active_view=nil end
end
mod.cleanup_template_ui=function() cleanup(active_view) end
local function visible(view)
    return mod:is_enabled() and get_mod("HavocConditionManager"):is_enabled()
        and view._hcm_page==4 and view._hed_templates_open and view._hed_library
end
local function field(view)
    if view._hed_name_widget then return view._hed_name_widget end
    local Widget=require("scripts/managers/ui/ui_widget")
    local Input=require("scripts/ui/pass_templates/text_input_pass_templates")
    local passes=table.clone_instance(Input.simple_input_field)
    for _,p in ipairs(passes) do
        if p.pass_type=="hotspot" then
            p.change_function=function(h) if h.on_pressed then h.parent.is_writing=true end; h.double_click_timer=0 end
        elseif p.style_id=="limit_text" then p.visibility_function=function() return false end
        elseif p.style_id=="focused" then p.visibility_function=function(c) return c.is_writing end
        elseif p.style_id=="display_text" then p.style.font_type="proxima_nova_bold"; p.style.font_size=24 end
    end
    local def=Widget.create_definition(passes,"hcm_layout",{input_text="",max_length=64,close_on_backspace=false},{1140,50})
    local w=Widget.init("hed_template_name",def); w.offset={637,374,20}
    view._hed_name_widget=w; input(view,view._hed_library.name)
    return w
end
local function chosen(s)
    for _,entry in ipairs(s.entries) do if entry.file==s.selected then return entry end end
end
local function delete_backdrop(view)
    if view._hed_delete_backdrop then return view._hed_delete_backdrop end
    local Widget=require("scripts/managers/ui/ui_widget")
    local def=Widget.create_definition({
        {pass_type="rect",style_id="shade",style={size={1920,1080},offset={0,0,36},color={180,0,0,0}}},
        {pass_type="rect",style_id="border",style={size={1004,448},offset={458,306,44},color={255,151,139,92}}},
        {pass_type="rect",style_id="body",style={size={1000,444},offset={460,308,44.5},color={255,15,23,19}}},
    },"hcm_layout",{}, {1920,1080})
    view._hed_delete_backdrop=Widget.init("hed_template_delete_backdrop",def)
    return view._hed_delete_backdrop
end
local function clipboard(s,text)
    if not Clipboard or not Clipboard.put then message(s,"template_clipboard_unavailable"); return end
    local ok,value=pcall(Clipboard.put,text)
    message(s,ok and value~=false and "template_copied" or "template_clipboard_unavailable")
end
local function save(view,doc,overwrite)
    local s=view._hed_library
    local filename,err=A.save_document(doc,s.name,overwrite)
    if filename then
        s.selected=filename; s.pending=nil; refresh(view); message(s,"template_saved")
    elseif err=="template_exists" then
        s.pending={kind="overwrite",doc=doc,name=s.name}; message(s,"template_overwrite_hint")
    else message(s,err) end
end
function mod.build_template_library(view,ui)
    local s=view._hed_library
    active_view=view
    local selected=chosen(s)
    ui:panel("template_toolbar",105,220,1710,70)
    ui:button("template_back",125,233,290,44,mod:localize("template_back"),function() cleanup(view); view._hed_tab="parameters" end)
    ui:text("template_heading",440,233,830,44,mod:localize("template_heading"),28,"gold")
    ui:button("hed_reset_all",1300,233,490,44,mod:localize(s.reset_pending and "template_reset_confirm" or "template_reset"),function()
        if not s.reset_pending then s.reset_pending=true; return end
        mod.restore_defaults(); s.reset_pending=nil; message(s,"template_reset_done")
    end,false,nil,s.reset_pending)
    ui:panel("template_list_panel",105,310,480,652)
    ui:text("template_list_title",120,320,440,42,mod:localize("template_list_title"),24)
    local offset=ui:window("templates",#s.entries,8,1,120,824,440)
    for i=1,math.min(8,#s.entries-offset) do
        local e=s.entries[offset+i]
        local text=short(e.name,20)
        local b=ui:button("template_file_"..i,120,374+(i-1)*54,440,50,text,function()
            s.selected=e.file; input(view,e.document and e.name or ""); message(s,e.error or "template_selected")
        end,e.file==s.selected,e.error and mod:localize("template_file_invalid") or nil,e.error~=nil)
        b.font=20; b.center=false; b.scroll="templates"
    end
    if #s.entries==0 then ui:text("template_empty",125,390,430,170,mod:localize("template_empty"),21,"muted") end
    ui:button("template_refresh",120,884,212,44,mod:localize("template_refresh"),function() s.pending=nil; refresh(view) end)
    ui:button("template_delete",344,884,216,44,mod:localize("template_delete"),selected and function()
        field(view).content.is_writing=false; s.editing=nil; view.is_text_input_focused=false
        s.pending=nil; s.deleting={file=selected.file,name=selected.name}
    end,false,nil,true)
    ui:panel("template_details_panel",605,310,1210,652)
    ui:text("template_name_label",625,324,1160,38,mod:localize("template_name_label"),22)
    -- The native text field is drawn separately and retains its caret across refreshes.
    ui:panel("template_name_background",625,368,1160,62)
    local w=field(view)
    local function finish_name() w.content.is_writing=false; s.editing=nil; view.is_text_input_focused=false end
    ui:button("template_save",625,444,275,48,mod:localize("template_save"),function()
        finish_name(); s.pending=nil
        local doc,err=A.capture(s.name); if doc then save(view,doc,false) else message(s,err) end
    end)
    ui:button("template_load",920,444,275,48,mod:localize("template_load"),selected and selected.document and function()
        finish_name()
        local doc,err=A.read(selected.file)
        if doc then local ok,why=A.compatible(doc); if not ok then doc=nil; err=why end end
        if doc then s.pending={kind="load",doc=doc}; message(s,"template_load_hint") else message(s,err) end
    end)
    ui:button("template_export",1215,444,275,48,mod:localize("template_export"),selected and selected.document and function()
        finish_name(); local text,err=A.export(selected.file); if text then clipboard(s,text) else message(s,err) end
    end)
    ui:button("template_import",1510,444,275,48,mod:localize("template_import"),function()
        finish_name()
        local ok,text=pcall(function() return Clipboard.get() end)
        local doc,err
        if ok then doc,err=A.decode(text) else err="template_clipboard_unavailable" end
        if doc then input(view,doc.name); s.pending={kind="import",doc=doc}; message(s,"template_import_hint") else message(s,err) end
    end)
    local doc=s.pending and s.pending.doc or selected and selected.document
    ui:panel("template_summary_panel",625,512,1160,164)
    if doc then
        local fields,rules,relative=0,0,0
        for _,patch in pairs(doc.config.patches) do for _ in pairs(patch) do fields=fields+1 end end
        for _,patch in pairs(doc.config.relative or {}) do for _ in pairs(patch) do relative=relative+1 end end
        for _,targets in pairs(doc.config.rules) do for _ in pairs(targets) do rules=rules+1 end end
        ui:text("template_summary_name",637,518,1136,50,short(doc.name,40),24,"gold")
        local summary=mod:localize("director_counts",#(doc.config.formations or {}),#(doc.config.deployments or {})).."\n"..
            mod:localize("director_overrides",fields,relative,rules)
        ui:text("template_summary",637,570,1136,94,summary,20,"muted")
    else ui:text("template_summary",637,532,1136,114,mod:localize("template_scope"),22,"muted") end
    ui:text("template_status",625,690,1160,70,s.status or mod:localize("template_scope"),20,"gold")
    if s.pending then
        local pending=s.pending
        ui:button("template_confirm",625,772,565,48,mod:localize(pending.kind=="load" and "template_confirm_load" or pending.kind=="overwrite" and "template_confirm_overwrite" or "template_confirm_import"),function()
            finish_name()
            if pending.kind=="load" then
                local ok,err=A.apply(pending.doc,view); s.pending=nil
                message(s,ok and "template_loaded" or err)
            elseif pending.kind=="overwrite" and s.name==pending.name then save(view,pending.doc,true)
            else save(view,pending.doc,false) end
        end,false,nil,pending.kind=="overwrite")
        ui:button("template_cancel",1210,772,575,48,mod:localize("template_cancel"),function() s.pending=nil; s.status=nil end)
    end
    ui:text("template_folder_hint",625,840,1160,72,mod:localize("template_folder_hint"),19,"muted")
    ui:button("template_folder",625,916,1160,38,mod:localize("template_folder"),function()
        local path,err=A.directory(); if path then clipboard(s,path:gsub("/","\\")) else message(s,err) end
    end)
    w.content.hotspot.disabled=s.deleting~=nil
    if s.deleting then
        delete_backdrop(view)
        local deleting=s.deleting
        w.content.is_writing=false; view.is_text_input_focused=false
        for _,item in ipairs(ui.items) do item.blocked=true end
        ui.scrolls={}
        ui.popup={key="template_delete",x=460,y=308,w=1000,h=444}
        local first=#ui.items+1
        ui:panel("template_delete_panel",460,308,1000,444)
        ui:text("template_delete_title",484,326,952,44,mod:localize("template_delete_title"),28,"gold")
        ui:text("template_delete_name",484,380,952,104,deleting.name,26,"gold")
        ui:text("template_delete_file",484,486,952,58,mod:localize("template_delete_file",deleting.file),20,"muted")
        ui:text("template_delete_hint",484,556,952,76,mod:localize("template_delete_hint"),22)
        ui:button("template_delete_cancel",484,668,462,52,mod:localize("template_cancel"),function()
            if s.deleting==deleting then s.deleting=nil end
        end)
        ui:button("template_delete_confirm",970,668,466,52,mod:localize("template_delete_confirm"),function()
            if s.deleting~=deleting then return end
            local ok,err=A.delete(deleting.file); s.deleting=nil
            if ok then s.selected=nil; input(view,""); refresh(view) end
            message(s,ok and "template_deleted" or err)
        end,false,nil,true)
        for i=first,#ui.items do ui.items[i].overlay=true end
    end
end
mod:hook("HavocConditionManagerView","_handle_input",function(func,view,service,...)
    if mod.handle_director_text then mod.handle_director_text(view,service) end
    if visible(view) then
        local s=view._hed_library; local c=field(view).content
        if service.is_null_service and service:is_null_service() or view._input_disabled then c.is_writing=false end
        if c.is_writing and not s.editing then s.editing=true; s.original=s.name end
        if c.input_text~=s.name then s.name=c.input_text; view._hcm_refresh=true end
        if service:get("confirm_pressed") or service:get("left_pressed") and not c.hotspot.is_hover then c.is_writing=false end
        view.is_text_input_focused=c.is_writing==true
        if not c.is_writing then s.editing=nil end
    elseif view._hed_library then cleanup(view) end
    return func(view,service,...)
end)
mod:hook("HavocConditionManagerView","_on_back_pressed",function(func,view,...)
    if mod.back_director_text and mod.back_director_text(view) then return end
    if visible(view) then
        local s=view._hed_library; local c=field(view).content
        if s.deleting then s.deleting=nil; view._hcm_refresh=true
        elseif c.is_writing then input(view,s.original or s.name); c.is_writing=false; s.editing=nil; view.is_text_input_focused=false
        elseif view._hcm_choice then return func(view,...) else cleanup(view); view._hed_tab="parameters";view._hed_section=view._hed_library_from or "native" end
        return
    end
    return func(view,...)
end)
mod:hook_safe("HavocConditionManagerView","_draw_widgets",function(view,dt,t,service,renderer)
    if visible(view) then
        local Widget=require("scripts/managers/ui/ui_widget")
        Widget.draw(field(view),renderer)
        if view._hed_library.deleting then Widget.draw(delete_backdrop(view),renderer) end
    end
    if mod.draw_director_text then mod.draw_director_text(view,renderer) end
end)
mod:hook_safe("HavocConditionManagerView","on_exit",function(view)
    cleanup(view)
    if mod.cleanup_director_text then mod.cleanup_director_text(view) end
end)
