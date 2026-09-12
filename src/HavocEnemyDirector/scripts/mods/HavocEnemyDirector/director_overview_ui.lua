local mod=get_mod("HavocEnemyDirector")
local base=get_mod("HavocConditionManager")
local S=base.template_schema
return function(view,ui,U)
    local cfg=mod.peek_config();local d=cfg.director
    local tab=view._hed_overview_tab or "general"
    U.tabs(view,ui,"hed_overview",{"general","pressure","seeds","summary"},tab,282,function(id) view._hed_overview_tab=id end)
    local function set(key,value) U.save(view,function(next_cfg) next_cfg.director[key]=value end) end
    if tab=="general" then
        ui:panel("hed_director_panel",105,350,1100,612)
        ui:panel("hed_director_guide",1225,350,590,612)
        ui:checkbox("hed_director_enabled",125,370,1060,52,U.loc("enabled"),function() set("enabled",not d.enabled) end,d.enabled)
        U.choice(ui,"hed_director_mode",125,438,1060,U.loc("mode"),d.mode,U.options({"rules","adaptive"}),function(v) set("mode",v) end)
        U.choice(ui,"hed_director_selection",125,506,1060,U.loc("selection"),d.selection,U.options({"priority","weighted"}),function(v) set("selection",v) end)
        local rows={{"admission_interval",0.5,60,0.5},{"max_active_groups",1,16,1,true},
            {"load_ceiling",1,2000,5},{"capable_min",1,4,1,true}}
        for i,row in ipairs(rows) do
            local key=row[1]
            U.number(ui,"hed_director_"..key,125,574+(i-1)*64,1060,U.loc(key),d[key],row[2],row[3],row[4],row[5],function(v) set(key,v) end)
        end
        ui:checkbox("hed_director_allow_events",125,844,1060,52,U.loc("allow_events"),function() set("allow_events",not d.allow_events) end,d.allow_events)
        ui:text("hed_director_guide_title",1245,373,550,82,U.loc(d.enabled and "scope_on" or "scope_off"),25,"gold")
        ui:text("hed_director_guide_counts",1245,473,550,76,U.loc("counts",#cfg.formations,#cfg.deployments),22)
        ui:text("hed_director_guide_help",1245,565,550,148,U.loc("empty_help"),21,"muted")
        ui:text("hed_director_guide_limits",1245,735,550,190,U.loc("limits_help"),20,"muted")
    elseif tab=="pressure" then
        ui:panel("hed_pressure_main",105,350,1100,612)
        ui:panel("hed_pressure_guide",1225,350,590,612)
        ui:text("hed_pressure_mode",125,368,1060,54,U.loc("phase_only"),21,"gold")
        local phase=view._hed_pressure_phase or "build"
        local labels={{"build",U.loc("build")},{"pressure",U.loc("pressure_phase")},{"recovery",U.loc("recovery")}}
        for i,choice in ipairs(labels) do
            ui:button("hed_phase_"..choice[1],125+(i-1)*359,438,342,48,choice[2],function() view._hed_pressure_phase=choice[1] end,phase==choice[1])
        end
        local range=d[phase.."_duration"]
        for i=1,2 do
            U.number(ui,"hed_phase_duration_"..i,125,508+(i-1)*64,1060,U.loc(i==1 and "duration_min" or "duration_max"),range[i],1,1200,5,false,function(value)
                local next_range=S.copy(range);next_range[i]=value
                if i==1 then next_range[2]=math.max(value,next_range[2]) else next_range[1]=math.min(value,next_range[1]) end
                set(phase.."_duration",next_range)
            end)
        end
        U.number(ui,"hed_phase_size",125,652,1060,U.loc("phase_size"),d[phase.."_size"],0.1,5,0.1,false,function(v) set(phase.."_size",v) end)
        U.number(ui,"hed_phase_frequency",125,722,1060,U.loc("phase_frequency"),d[phase.."_frequency"],0,5,0.1,false,function(v) set(phase.."_frequency",v) end)
        ui:text("hed_phase_status_help",125,810,1060,118,U.loc("status_help"),20,"muted")
        U.number(ui,"hed_phase_low_load",1245,376,550,U.loc("low_load"),d.low_load,0,d.high_load-1,5,true,function(v) set("low_load",v) end)
        U.number(ui,"hed_phase_high_load",1245,451,550,U.loc("high_load"),d.high_load,d.low_load+1,2000,5,true,function(v) set("high_load",v) end)
        ui:text("hed_phase_help",1245,556,550,328,U.loc("phase_help"),22,"muted")
    elseif tab=="seeds" then
        ui:panel("hed_seed_panel",105,350,1710,612)
        ui:checkbox("hed_director_seed_enabled",125,372,960,52,U.loc("fixed_director_seed"),function()
            U.save(view,function(next_cfg)next_cfg.director.seed_enabled=not d.seed_enabled;next_cfg.director.seed=math.max(1,d.seed)end)
        end,d.seed_enabled)
        ui:number("hed_director_seed_value",1125,372,670,52,tostring(math.max(1,d.seed)),d.seed_enabled and {
            label=U.loc("director_seed"),value=math.max(1,d.seed),min=1,max=2147483646,integer=true,set=function(v)set("seed",v)end},24)
        ui:text("hed_director_seed_help",125,446,1650,98,U.loc("seed_help"),23,"muted")
        ui:checkbox("hed_layout_seed_enabled",125,578,960,52,U.loc("fixed_map_seed"),function()
            U.save(view,function(next_cfg)next_cfg.seed_enabled=not cfg.seed_enabled;next_cfg.seed=cfg.seed or 1 end)
        end,cfg.seed_enabled)
        ui:number("hed_layout_seed_value",1125,578,670,52,tostring(cfg.seed or 1),cfg.seed_enabled and {
            label=U.loc("map_seed"),value=cfg.seed or 1,min=1,max=2147483646,integer=true,
            set=function(v)U.save(view,function(next_cfg)next_cfg.seed=v end)end},24)
        ui:text("hed_layout_seed_help",125,652,1650,96,U.loc("map_seed_help"),23,"muted")
        ui:text("hed_seed_limit",125,799,1650,120,U.loc("seed_limit"),23,"gold")
    else
        ui:panel("hed_summary_panel",105,350,1710,612)
        local fixed,relative,rules,enabled,unused=0,0,0,0,0
        for _,patch in pairs(cfg.patches) do for _ in pairs(patch) do fixed=fixed+1 end end
        for _,patch in pairs(cfg.relative) do for _ in pairs(patch) do relative=relative+1 end end
        for _,targets in pairs(cfg.rules) do for _ in pairs(targets) do rules=rules+1 end end
        local used={}
        for _,rule in ipairs(cfg.deployments) do if rule.enabled then enabled=enabled+1 end;used[rule.formation_id]=true end
        for _,formation in ipairs(cfg.formations) do if not used[formation.id] then unused=unused+1 end end
        ui:text("hed_summary_counts",125,376,1670,58,U.loc("counts",#cfg.formations,#cfg.deployments),27,"gold")
        ui:text("hed_summary_enabled",125,451,1670,52,U.loc("enabled_rules",enabled,#cfg.deployments),23)
        ui:text("hed_summary_unused",125,520,1670,52,U.loc("unreferenced",unused),23,"muted")
        ui:text("hed_summary_overrides",125,590,1670,58,U.loc("overrides",fixed,relative,rules),23)
        ui:text("hed_summary_help",125,680,1670,105,U.loc("summary_help"),22,"muted")
        ui:button("hed_summary_presets",125,818,790,56,U.loc("presets"),function()
            view._hed_section="presets";view._hed_tab="presets";view._hed_library_from="overview"
        end)
        ui:button("hed_summary_native",935,818,860,56,U.loc(view._hed_clear_native and "reset_native_confirm" or "reset_native"),function()
            if view._hed_clear_native then
                U.save(view,function(next_cfg) next_cfg.patches={};next_cfg.relative={};next_cfg.rules={} end);view._hed_clear_native=nil
            else view._hed_clear_native=true end
        end,false,nil,true)
    end
end
