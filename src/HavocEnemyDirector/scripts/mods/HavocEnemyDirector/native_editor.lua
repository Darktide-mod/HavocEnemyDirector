local mod=get_mod("HavocEnemyDirector")
local base=get_mod("HavocConditionManager")
local S,A,R=base.template_schema,base.template_registry,base.template_conditions
local N=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_semantics")
local function loc(key,...) return base:localize("native_"..key,...) end
local function label(d) return S.text(d,base:localize("native_language")) end
local function value_text(v)
    if type(v)=="table" then return value_text(v[1]).." – "..value_text(v[2]) end
    if type(v)=="boolean" then return loc(v and "yes" or "no") end
    if type(v)=="number" then return string.format("%.4g",v) end
    return tostring(v)
end
local function changed(view,ok,error)
    view._hcm_refresh=true; view._hed_status=ok==false and loc("invalid",tostring(error)) or nil
end
local function set_patch(view,entry,item,value) changed(view,mod.set_patch(entry.id,item.id,value)) end
local function current(entry,item)
    local relative=mod.peek_config().relative[entry.id]
    if relative and relative[item.id] then return mod.preview_config().patches[entry.id][item.id] end
    local patch=mod.peek_config().patches[entry.id]
    if patch and patch[item.id]~=nil then return patch[item.id] end
    return S.scaled(item,entry.family,S.coarse_config(base:get("native_configuration_v3")))
end
local function number(ui,key,x,y,w,title,value,d,set)
    local original_set=set
    if d.unit=="percent" then
        value=value*100
        local next_d=S.copy(d);next_d.min=d.min*100;next_d.max=d.max*100;next_d.step=(d.step or 0.05)*100;d=next_d
        set=function(n) original_set(n/100) end
    end
    ui:stepper(key,x,y,w,title,value_text(value),function(direction)
        local n=S.clamp(value+direction*(d.step or 1),d.min,d.max)
        if d.integer then n=math.floor(n+0.5) end; set(n)
    end,nil,{label=title,value=value,min=d.min,max=d.max,integer=d.integer,set=set})
end
local function numeric_editor(view,ui,entry,item,y)
    local d=item.definition; local value=current(entry,item)
    local function set(v) set_patch(view,entry,item,v) end
    if item.kind=="range" then
        for i=1,2 do
            number(ui,"hed_value_"..i,615,y+(i-1)*64,1145,loc(i==1 and "minimum" or "maximum"),value[i],d,function(n)
                local pair=S.copy(value); pair[i]=n
                if i==1 then pair[2]=math.max(n,pair[2]) else pair[1]=math.min(n,pair[1]) end; set(pair)
            end)
        end
    elseif item.kind=="number" then number(ui,"hed_value",615,y,1145,label(d),value,d,set)
    elseif item.kind=="boolean" then ui:checkbox("hed_value",615,y,1145,48,loc("enabled"),function() set(not value) end,value)
    elseif item.kind=="choice" then
        local options={} for _,v in ipairs(d.options) do options[#options+1]={v,loc("choice_"..v)} end
        ui:choice("hed_value",615,y,1145,48,value,options,set)
    end
end
local function breed_options(entry,item)
    local options={}
    for id,breed in pairs(A.breeds) do
        if S.breed_allowed(item,id,A.breeds) then
            local display=breed.display_name and Localize(breed.display_name)
            if not display or display==breed.display_name and display:find("loc_",1,true) then display=id end
            options[#options+1]={id,display and display~=id and display or N.key(id)}
        end
    end
    for id in pairs(item.aliases or {}) do if S.breed_allowed(item,id,A.breeds) then options[#options+1]={id,N.key(id).." ("..loc("by_faction")..")"} end end
    table.sort(options,function(a,b) return a[1]<b[1] end); return options
end
local function pool_editor(view,ui,entry,item)
    local values=current(entry,item); local composition=item.kind=="composition"
    ui:text("hed_pool_help",615,466,1145,64,loc(composition and "composition_help" or "pool_help"),20,"muted")
    local options=breed_options(entry,item)
    local offset=ui:window("hed_pool_"..entry.id..item.id,#values,5,1,1210,846,550)
    for row=1,math.min(5,#values-offset) do
        local i=offset+row; local value=values[i]; local y=540+(row-1)*59
        local function set_at(v) local copy=S.copy(values); copy[i]=v; set_patch(view,entry,item,copy) end
        ui:choice("hed_breed_"..i,615,y,composition and 570 or 1040,48,composition and value.name or value,options,function(breed)
            if composition then local next_value=S.copy(value); next_value.name=breed; set_at(next_value) else set_at(breed) end
        end)
        if composition then
            for bound=1,2 do
                local d={min=0,max=300,integer=true,step=1}
                number(ui,"hed_amount_"..i.."_"..bound,1200+(bound-1)*235,y,225,bound==1 and label({en="Min",cn="下限"}) or label({en="Max",cn="上限"}),value.amount[bound],d,function(n)
                    local copy=S.copy(value); copy.amount[bound]=n
                    if bound==1 then copy.amount[2]=math.max(n,copy.amount[2]) else copy.amount[1]=math.min(n,copy.amount[1]) end
                    set_at(copy)
                end)
            end
        end
        ui:button("hed_remove_"..i,1670,y,90,48,"−",#values>1 and function() local copy=S.copy(values); table.remove(copy,i); set_patch(view,entry,item,copy) end)
    end
    ui:button("hed_add",615,846,560,40,loc("add_entry"),#values<(composition and 64 or 128) and function()
        local copy=S.copy(values); copy[#copy+1]=S.copy(values[#values]); set_patch(view,entry,item,copy)
    end)
end
local function fields(view,ui,entry,tab)
    view._hed_path=view._hed_path or {}
    local prefix=view._hed_path; local groups=S.groups(N.items(view,entry,tab),prefix,tab)
    ui:panel("hed_tree_panel",105,356,475,604)
    ui:button("hed_parent",120,368,445,44,loc("up"),#prefix>0 and function() table.remove(view._hed_path); view._hed_item=nil end)
    ui:choice("hed_field_filter",120,421,445,42,view._hed_field_filter or "common",{{"common",N.loc("common_fields")},{"all",N.loc("all_fields")},{"changed",N.loc("modified_fields")}},function(id)
        view._hed_field_filter=id;view._hed_path={};view._hed_item=nil
    end)
    local capacity=entry.family=="roamers" and 7 or 8
    local offset=ui:window("hed_tree_"..entry.id..S.path_key(prefix)..tab,#groups,capacity,1,120,914,445)
    for row=1,math.min(capacity,#groups-offset) do
        local group=groups[offset+row]
        local text=group.item and label(group.item.definition) or N.key(group.key,offset+row).."  ›"
        local item=ui:button("hed_tree_"..row,120,474+(row-1)*52,445,46,text,function()
            if group.item then view._hed_item=group.item.id else view._hed_path=S.copy(group.path); view._hed_item=nil end
        end,group.item and view._hed_item==group.item.id,N.path(group.path,view._hed_technical))
        item.center=false; item.font=19; item.scroll="hed_tree_"..entry.id..S.path_key(prefix)..tab
    end
    if entry.family=="roamers" then
        ui:button("hed_seed_settings",120,854,445,44,mod:localize("director_seeds"),function()
            view._hed_section="overview";view._hed_overview_tab="seeds"
        end)
    end
    local item=entry.fields[view._hed_item]
    if not item and groups[1] and groups[1].item then item=groups[1].item; view._hed_item=item.id end
    ui:panel("hed_detail_panel",595,356,1220,604)
    if not item then
        ui:text("hed_field_prompt",615,394,1170,126,loc("choose_field"),24,"muted")
        ui:text("hed_path",615,548,1170,90,N.path(prefix,view._hed_technical),21,"gold")
        ui:text("hed_scope_help",615,665,1170,154,N.help(entry),23,"muted")
        ui:text("hed_common_help",615,843,1170,94,N.loc("common_hint"),20,"muted")
        return
    end
    local unit=item.definition.unit
    ui:text("hed_field_title",615,368,1170,44,label(item.definition)..(unit and " ("..loc("unit_"..unit)..")" or ""),26,"gold")
    ui:text("hed_field_path",615,412,835,50,N.path(item.path,view._hed_technical),18,"muted")
    ui:checkbox("hed_technical",1470,412,295,50,N.loc("technical"),function() view._hed_technical=not view._hed_technical end,view._hed_technical).font=17
    if item.kind=="pool" or item.kind=="composition" then pool_editor(view,ui,entry,item)
    else
        local cfg=mod.peek_config();local patch=cfg.patches[entry.id] or {};local relative=cfg.relative[entry.id] or {}
        local mode=relative[item.id]~=nil and "relative" or patch[item.id]~=nil and "fixed" or "follow"
        local options={{"follow",N.loc("follow")},{"fixed",N.loc("fixed")}}
        if item.kind=="number" or item.kind=="range" then options[#options+1]={"relative",N.loc("relative")} end
        ui:choice("hed_value_mode",615,478,1145,48,mode,options,function(v)
            if v=="relative" then changed(view,mod.set_relative(entry.id,item.id,1))
            elseif v=="fixed" then
                local value=current(entry,item)
                local function bound(n)
                    if type(n)~="number" then return n end
                    n=S.clamp(n,item.definition.min,item.definition.max)
                    return item.definition.integer and math.ceil(n) or n
                end
                if item.kind=="range" then value={bound(value[1]),bound(value[2])}
                elseif item.kind=="number" then value=bound(value) end
                set_patch(view,entry,item,value)
            else set_patch(view,entry,item,nil) end
        end)
        local function formatted(v)
            if item.definition.unit=="percent" then
                if type(v)=="table" then return value_text(v[1]*100).." – "..value_text(v[2]*100).."%" end
                return value_text(v*100).."%"
            end
            return value_text(v)
        end
        ui:text("hed_field_base",615,538,560,44,N.loc("original",formatted(item.value)),20,"muted")
        local coarse=S.scaled(item,entry.family,S.coarse_config(base:get("native_configuration_v3")))
        ui:text("hed_field_coarse",1195,538,565,44,N.loc("coarse_value",formatted(coarse)),20,"muted")
        if mode=="relative" then
            number(ui,"hed_relative",615,601,1145,N.loc("factor"),relative[item.id],{min=0.1,max=10,step=0.1},function(v)
                changed(view,mod.set_relative(entry.id,item.id,v))
            end)
        else numeric_editor(view,ui,entry,item,601) end
        ui:text("hed_field_effective",615,737,1145,44,N.loc("effective",formatted(current(entry,item))),21,"gold")
        ui:text("hed_field_help",615,790,1145,99,mode=="relative" and N.loc("relative_help") or N.help(entry,item),19,"muted")
    end
    ui:button("hed_reset_field",615,901,560,44,loc("reset_override"),function() set_patch(view,entry,item,nil) end)
    ui:button("hed_native_field",1195,901,565,44,loc("use_native"),S.validate_value(item,item.value,A.breeds) and function() set_patch(view,entry,item,item.value) end)
end
local function rules(view,ui,entry)
    ui:panel("hed_rule_panel",105,356,1710,604)
    local options={} for i,target in ipairs(entry.targets) do options[#options+1]={target.id,target.id=="encounter" and loc("encounter_start") or N.path(target.path or {i, "conditions"},view._hed_technical)} end
    if #options==0 then ui:text("hed_no_rules",125,386,1660,140,loc("no_rules"),24,"muted"); return end
    local target
    for _,t in ipairs(entry.targets) do if t.id==view._hed_rule_target then target=t end end
    target=target or entry.targets[1]; view._hed_rule_target=target.id
    local configured=mod.peek_config().rules[entry.id]
    local rule=S.copy(configured and configured[target.id] or {mode="append",match="all",clauses={}})
    local function save(next_rule) changed(view,mod.set_rule(entry.id,target.id,next_rule)) end
    ui:choice("hed_rule_target",125,370,1090,48,target.id,options,function(id) view._hed_rule_target=id end)
    ui:button("hed_rule_reset",1235,370,555,48,loc("reset_rule"),function() save(nil) end)
    ui:choice("hed_rule_mode",125,434,805,48,rule.mode,target.replace and {{"append",loc("append")},{"replace",loc("replace")}} or {{"append",loc("append")}},function(mode) rule.mode=mode; save(rule) end)
    ui:choice("hed_rule_match",950,434,840,48,rule.match,{{"all",loc("all")},{"any",loc("any")}},function(match) rule.match=match; save(rule) end)
    local conditions={} for _,d in ipairs(R.order) do conditions[#conditions+1]={d.id,label(d)} end
    local offset=ui:window("hed_rules_"..entry.id..target.id,#rule.clauses,5,1,1235,833,555)
    for row=1,math.min(5,#rule.clauses-offset) do
        local i=offset+row; local clause=rule.clauses[i]; local d=R.definitions[clause.condition]; local y=502+(row-1)*62
        ui:choice("hed_condition_"..i,125,y,1000,48,clause.condition,conditions,function(id) rule.clauses[i]=R.default_clause(id); save(rule) end)
        if d.kind=="number" then
            number(ui,"hed_condition_value_"..i,1145,y,520,loc("value"),clause.value,{min=d.min,max=d.max,integer=true,step=1},function(n) clause.value=n; save(rule) end)
        elseif d.kind=="choice" then
            local choices={} for _,v in ipairs(d.options) do choices[#choices+1]={v,loc("choice_"..v)} end
            ui:choice("hed_condition_value_"..i,1145,y,520,48,clause.value,choices,function(v) clause.value=v; save(rule) end)
        elseif d.kind=="text" then
            ui:button("hed_condition_value_"..i,1145,y,520,48,clause.value,function()
                local value=Clipboard and Clipboard.get and Clipboard.get()
                value=type(value)=="string" and value:match("^%s*(.-)%s*$")
                if value and #value<=64 and value:match("^[%w_%-]+$") then clause.value=value;save(rule)
                else base:notify(base:localize("diy_identifier_invalid")) end
            end,false,base:localize("diy_paste_identifier"))
        end
        ui:button("hed_condition_remove_"..i,1685,y,105,48,"−",function() table.remove(rule.clauses,i); save(rule) end)
    end
    if #rule.clauses==0 then ui:text("hed_rule_empty",125,531,1665,114,N.loc("no_conditions"),24,"muted") end
    ui:button("hed_rule_add",125,833,1085,44,loc("add_condition"),#rule.clauses<8 and function() rule.clauses[#rule.clauses+1]=R.default_clause("load_max"); save(rule) end)
    ui:text("hed_rules_help",125,889,1665,60,loc("rules_help"),20,"muted")
end
mod.build_dashboard=function(view,ui)
    if view._hed_tab=="presets" then
        if not view._hed_templates_open then mod.open_template_library(view) end
        mod.build_template_library(view,ui); return
    end
    local family=view._hed_family or "hordes"; local families={}
    for _,id in ipairs(S.families) do families[#families+1]={id,loc("family_"..id)} end
    ui:choice("hed_family",105,220,385,48,family,families,function(id) view._hed_family=id; view._hed_entry=nil; view._hed_path={}; view._hed_item=nil; view._hed_rule_target=nil end)
    local options,masters,master_lookup={},{},{}; local entry
    local chosen_master=view._hed_master
    for _,candidate in ipairs(A.entries) do
        if candidate.family==family and (#candidate.items>0 or #candidate.targets>0) then
            local master=candidate.id:match("^[^/]+/([^/]+)")
            if not master_lookup[master] then master_lookup[master]=true; masters[#masters+1]={master,N.master(master)} end
            if candidate.id==view._hed_entry then chosen_master=master end
        end
    end
    if not master_lookup[chosen_master] then chosen_master=masters[1] and masters[1][1] end
    view._hed_master=chosen_master
    for _,candidate in ipairs(A.entries) do
        if candidate.family==family and candidate.id:match("^[^/]+/([^/]+)")==chosen_master and (#candidate.items>0 or #candidate.targets>0) then
            local suffix=candidate.id:match("^[^/]+/[^/]+/(.+)$")
            options[#options+1]={candidate.id,suffix and (candidate.level and N.loc(family=="monsters" and "challenge" or "resistance",suffix) or N.master(suffix)) or loc("whole_template")}
            if candidate.id==view._hed_entry then entry=candidate end
        end
    end
    entry=entry or options[1] and A.by_id[options[1][1]]
    if not entry then ui:text("hed_no_templates",510,220,1305,48,loc("no_templates"),23); return end
    view._hed_entry=entry.id
    ui:choice("hed_master",510,220,620,48,chosen_master,masters,function(id) view._hed_master=id; view._hed_entry=nil; view._hed_path={}; view._hed_item=nil; view._hed_rule_target=nil end)
    ui:choice("hed_template",1150,220,665,48,entry.id,options,function(id) view._hed_entry=id; view._hed_path={}; view._hed_item=nil; view._hed_rule_target=nil end)
    local tab=view._hed_tab or "parameters"
    for i,id in ipairs({"parameters","composition","rules","presets"}) do
        ui:button("hed_tab_"..id,105+(i-1)*432,286,414,48,loc("tab_"..id),function()
            view._hed_tab=id; view._hed_path={}; view._hed_item=nil
            if id=="presets" then mod.open_template_library(view) else mod.cleanup_template_ui() end
        end,tab==id)
    end
    if tab=="presets" then
        if not view._hed_templates_open then mod.open_template_library(view) end
        mod.build_template_library(view,ui)
    elseif tab=="rules" then rules(view,ui,entry)
    else fields(view,ui,entry,tab) end
    if view._hed_status then ui:text("hed_status",120,963,1680,28,view._hed_status,18,"danger") end
end
