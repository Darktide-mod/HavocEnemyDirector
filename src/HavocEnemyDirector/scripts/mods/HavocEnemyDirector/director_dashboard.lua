local mod=get_mod("HavocEnemyDirector")
local U=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_ui_helpers")
local Overview=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_overview_ui")
local Formations=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_formations_ui")
local Deployments=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_deployments_ui")
local native=mod.build_dashboard
local function legacy(view,ui)
    local add=ui.add
    function ui:add(key,x,y,w,h,text,options)
        local modal=key:find("^template_delete_") and key~="template_delete_back"
        if not modal then y=282+(y-220)*0.91;h=h*0.91 end
        return add(self,key,x,y,w,h,text,options)
    end
    native(view,ui)
    ui.add=add
    local field=view._hed_name_widget
    if field then field.offset={637,282+(374-220)*0.91,20} end
end
mod.build_dashboard=function(view,ui)
    -- The shared HCM builder creates dropdown rows after this function returns.
    -- Change this builder instance only; normal HCM checkbox controls keep
    -- their existing behavior.
    local checkbox=ui.checkbox
    function ui:checkbox(key,...)
        local item=checkbox(self,key,...)
        if key:find("^choice_") then item.checkbox=item.selected==true end
        return item
    end
    local section=view._hed_section or (view._hed_family or view._hed_tab or view._hed_entry) and "native" or "overview"
    if view._hed_tab=="presets" and (section=="native" or section=="presets") then section="presets" end
    U.tabs(view,ui,"hed_section",{"overview","formations","deployments","native","presets"},section,220,function(id)
        if mod.cleanup_director_text then mod.cleanup_director_text(view) end
        mod.cleanup_template_ui()
        view._hed_section=id;view._hed_status=nil;view._hcm_choice=nil
        if id=="presets" then view._hed_library_from=section;view._hed_tab="presets"
        elseif view._hed_tab=="presets" then view._hed_tab="parameters" end
    end)
    if section=="overview" then Overview(view,ui,U)
    elseif section=="formations" then Formations(view,ui,U)
    elseif section=="deployments" then Deployments(view,ui,U)
    else
        legacy(view,ui)
        if section=="presets" then
            for _,item in ipairs(ui.items) do
                if item.key=="template_back" then
                    local action=item.action
                    item.action=function() action();view._hed_section=view._hed_library_from or "native" end
                end
            end
        end
    end
    if view._hed_status then ui:text("hed_director_status",120,963,1680,28,view._hed_status,18,"danger") end
    mod.build_director_text(view,ui)
end
return true
