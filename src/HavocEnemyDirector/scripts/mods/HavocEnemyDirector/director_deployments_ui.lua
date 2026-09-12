local mod=get_mod("HavocEnemyDirector")
local base=get_mod("HavocConditionManager")
local S,R=base.template_schema,base.template_conditions
return function(view,ui,U)
    local cfg=mod.peek_config();local C=mod.director_config
    local selected=U.find(cfg.deployments,view._hed_deployment_id) or cfg.deployments[1]
    if selected then view._hed_deployment_id=selected.id end
    ui:panel("hed_deploy_list_panel",105,282,475,680)
    ui:panel("hed_deploy_detail_panel",595,282,1220,680)
    local formations={};for _,f in ipairs(cfg.formations) do formations[#formations+1]={f.id,f.name} end
    local chosen=U.find(cfg.formations,view._hed_new_deployment_form) or cfg.formations[1]
    ui:text("hed_deploy_new_label",125,299,435,34,U.loc("formation_ref"),21,"muted")
    if chosen then
        ui:choice("hed_deploy_new_form",125,340,435,48,chosen.id,formations,function(id) view._hed_new_deployment_form=id end)
    end
    ui:button("hed_deploy_add",125,402,435,48,U.loc("add_deployment"),chosen and #cfg.deployments<64 and function()
        U.save(view,function(next_cfg)
            local rule=C.new_deployment(next_cfg,U.loc("new_deployment",next_cfg.next_id),chosen.id)
            view._hed_deployment_id=rule.id
        end)
    end)
    U.list(view,ui,"hed_deploy_list",cfg.deployments,selected and selected.id,function(id) view._hed_deployment_id=id;view._hed_delete_deployment=nil end,474,7)
    if not selected then
        ui:text("hed_deploy_empty",625,369,1160,160,U.loc("no_deployments"),27,"muted")
        ui:button("hed_deploy_open_formations",625,571,1160,56,U.loc("formations"),function() view._hed_section="formations" end)
        return
    end
    local d=selected
    local function change(fn) return U.record(view,"deployments",d.id,fn) end
    local function set(key,value) return change(function(v) v[key]=value end) end
    ui:button("hed_deploy_name",615,302,704,52,d.name,function() U.rename(view,"deployments",d) end)
    ui:checkbox("hed_deploy_enabled",1335,302,460,52,U.loc("rule_enabled"),function() set("enabled",not d.enabled) end,d.enabled)
    U.choice(ui,"hed_deploy_formation",615,368,1180,U.loc("formation_ref"),d.formation_id,formations,function(id) set("formation_id",id) end)
    local tab=view._hed_deployment_tab or "timing"
    U.tabs(view,ui,"hed_deploy_tab",{"timing","conditions","quotas","inheritance"},tab,438,function(id) view._hed_deployment_tab=id end,615,1180)
    local function number(key,x,y,w,minimum,maximum,step,integer)
        U.number(ui,"hed_deploy_"..key,x,y,w,U.loc(key),d[key],minimum,maximum,step,integer,function(v) set(key,v) end)
    end
    if tab=="timing" then
        U.choice(ui,"hed_deploy_trigger",615,509,1180,U.loc("trigger"),d.trigger,U.options({"timer","progress","condition"}),function(v)
            change(function(rule)
                rule.trigger=v
                if v=="condition" and #rule.conditions.clauses==0 then
                    rule.conditions.clauses={R.default_clause("load_max")}
                    view._hed_deployment_tab="conditions"
                end
            end)
        end)
        number("first_delay",615,580,1180,0,7200,5,false)
        if d.trigger=="timer" then
            for bound=1,2 do
                U.number(ui,"hed_deploy_interval_"..bound,615+(bound-1)*602,648,578,U.loc(bound==1 and "interval_min" or "interval_max"),
                    d.interval[bound],1,7200,5,false,function(n)
                    change(function(v)
                        v.interval[bound]=n
                        if bound==1 then v.interval[2]=math.max(n,v.interval[2]) else v.interval[1]=math.min(n,v.interval[1]) end
                    end)
                end)
            end
        elseif d.trigger=="progress" then
            number("progress_start",615,648,578,0,10000,10,true)
            number("progress_step",1217,648,578,1,10000,10,true)
        else ui:text("hed_deploy_edge_help",615,646,1180,54,U.loc("timing_help"),18,"muted") end
        number("start_time",615,716,578,0,d.end_time>0 and d.end_time or 14400,5,false)
        U.number(ui,"hed_deploy_end_time",1217,716,578,U.loc("end_time"),d.end_time,0,14400,5,false,function(v)
            if v>0 then v=math.max(d.start_time,v) end;set("end_time",v)
        end)
        number("waves",615,784,578,1,12,1,true)
        number("wave_gap",1217,784,578,0.5,120,0.5,false)
        ui:text("hed_deploy_timing_help",615,847,1180,48,U.loc("timing_help"),18,"muted")
    elseif tab=="conditions" then
        local conditions={}
        for _,def in ipairs(R.order) do if def.id~="always" then conditions[#conditions+1]={def.id,U.condition_label(def)} end end
        local rule=d.conditions
        U.choice(ui,"hed_deploy_match",615,509,1180,U.loc("match"),rule.match,{{"all",U.loc("all")},{"any",U.loc("any_match")}},function(v)
            change(function(value) value.conditions.match=v end)
        end)
        ui:checkbox("hed_deploy_recheck_conditions",615,575,1180,52,U.loc("recheck_conditions"),function() set("recheck_conditions",not d.recheck_conditions) end,d.recheck_conditions).font=19
        local offset=ui:window("hed_deploy_conditions_"..d.id,#rule.clauses,3,1,1255,824,540)
        if #rule.clauses==0 then ui:text("hed_deploy_no_conditions",615,665,1180,102,U.loc("no_conditions"),23,"muted") end
        for row=1,math.min(3,#rule.clauses-offset) do
            local i=offset+row;local clause=rule.clauses[i];local def=R.definitions[clause.condition];local y=641+(row-1)*60
            ui:choice("hed_deploy_condition_"..i,615,y,682,52,clause.condition,conditions,function(id)
                change(function(v) v.conditions.clauses[i]=R.default_clause(id) end)
            end)
            if def.kind=="number" then
                ui:number("hed_deploy_condition_value_"..i,1313,y,346,52,U.value(clause.value),{
                    label=S.text(def,base:localize("native_language")),value=clause.value,min=def.min,max=def.max,integer=true,
                    set=function(n) change(function(v) v.conditions.clauses[i].value=n end) end})
            elseif def.kind=="choice" then
                local choices={};for _,value in ipairs(def.options) do choices[#choices+1]={value,base:localize("native_choice_"..value)} end
                ui:choice("hed_deploy_condition_value_"..i,1313,y,346,52,clause.value,choices,function(value)
                    change(function(v) v.conditions.clauses[i].value=value end)
                end)
            elseif def.kind=="text" then
                ui:button("hed_deploy_condition_value_"..i,1313,y,346,52,clause.value,function()
                    local value=Clipboard and Clipboard.get and Clipboard.get()
                    value=type(value)=="string" and value:match("^%s*(.-)%s*$")
                    if value and #value<=64 and value:match("^[%w_%-]+$") then change(function(v) v.conditions.clauses[i].value=value end)
                    else base:notify(base:localize("diy_identifier_invalid")) end
                end,false,base:localize("diy_paste_identifier"))
            end
            ui:button("hed_deploy_condition_remove_"..i,1675,y,120,52,"−",(#rule.clauses>1 or d.trigger~="condition") and function()
                change(function(v) table.remove(v.conditions.clauses,i) end)
            end)
        end
        ui:button("hed_deploy_condition_add",615,824,620,42,U.loc("add_condition"),#rule.clauses<8 and function()
            change(function(v) v.conditions.clauses[#v.conditions.clauses+1]=R.default_clause("load_max") end)
        end)
        ui:text("hed_deploy_conditions_help",615,873,1180,36,U.loc("condition_help"),17,"muted")
    elseif tab=="quotas" then
        number("cooldown",615,510,1180,0.5,3600,1,false)
        number("max_occurrences",615,574,578,0,100,1,true)
        number("max_alive",1217,574,578,1,16,1,true)
        U.number(ui,"hed_deploy_priority",615,638,578,U.loc("rule_priority"),d.priority,0,100,1,true,function(v) set("priority",v) end)
        number("weight",1217,638,578,0.01,100,1,false)
        U.choice(ui,"hed_deploy_phase",615,705,1180,U.loc("phase"),d.phase,{{"any",U.loc("any")},{"build",U.loc("build")},{"pressure",U.loc("pressure_phase")},{"recovery",U.loc("recovery")}},function(v) set("phase",v) end)
        ui:text("hed_deploy_quota_help",615,782,1180,107,U.loc("quota_help"),20,"muted")
    else
        ui:checkbox("hed_deploy_inherit_size",615,510,1180,52,U.loc("inherit_size"),function() set("inherit_size",not d.inherit_size) end,d.inherit_size)
        number("size_multiplier",615,574,1180,0.1,10,0.1,false)
        ui:text("hed_deploy_size_help",615,638,1180,97,U.loc("inherit_help"),19,"muted")
        ui:checkbox("hed_deploy_inherit_frequency",615,748,1180,52,U.loc("inherit_frequency"),function() set("inherit_frequency",not d.inherit_frequency) end,d.inherit_frequency)
        number("frequency_multiplier",615,812,1180,0.1,10,0.1,false)
        ui:text("hed_deploy_frequency_help",615,866,1180,44,U.loc("frequency_help"),17,"muted")
    end
    ui:button("hed_deploy_copy",615,914,566,36,U.loc("copy"),#cfg.deployments<64 and function()
        U.save(view,function(next_cfg)
            local copy=S.copy(d);copy.id=C.allocate(next_cfg,"d");copy.name=U.copy_name(d.name)
            next_cfg.deployments[#next_cfg.deployments+1]=copy;view._hed_deployment_id=copy.id
        end)
    end)
    ui:button("hed_deploy_delete",1197,914,598,36,U.loc(view._hed_delete_deployment==d.id and "confirm_delete" or "delete"),function()
        if view._hed_delete_deployment==d.id then
            U.save(view,function(next_cfg)
                for i,v in ipairs(next_cfg.deployments) do if v.id==d.id then table.remove(next_cfg.deployments,i);break end end
            end);view._hed_deployment_id=nil;view._hed_delete_deployment=nil
        else view._hed_delete_deployment=d.id end
    end,false,nil,true)
end
