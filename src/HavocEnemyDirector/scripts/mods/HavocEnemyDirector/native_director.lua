local mod=get_mod("HavocEnemyDirector")
local base=get_mod("HavocConditionManager")
if not base or not base.template_registry then mod:error("HavocConditionManager 3.0.0 or newer must load before HavocEnemyDirector"); return end
local S,A=base.template_schema,base.template_registry
local Solo=get_mod("SoloPlay")
local Toggle=base:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/runtime_toggle")
local toggle=Toggle(mod,function() return Solo and Solo.has_local_gameplay_authority and Solo.has_local_gameplay_authority() or false end,base)
mod.is_gameplay_enabled=toggle.active
local C=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_config")
mod.director_config=C
local loaded,rejected=C.validate(mod:get("native_director_v3") or mod:get("native_director_v2"))
local cfg=#rejected==0 and loaded or C.validate({})
if #rejected>0 then mod:notify(mod:localize("director_saved_invalid")) end
mod.get_saved_config=function() return S.copy(cfg) end
mod.get_config=function() return {version=2,patches=S.copy(cfg.patches),rules=S.copy(cfg.rules),seed=cfg.seed_enabled and cfg.seed or nil} end
mod.preview_config=function() return C.resolve(cfg,S.coarse_config(base:get("native_configuration_v3"))) end
mod.peek_config=function() return cfg end
mod.save_config=function(raw)
    local clean,rejected=C.validate(raw)
    if #rejected>0 then return false,rejected[1] end
    local valid,why=C.validate_relative_result(clean,S.coarse_config(base:get("native_configuration_v3")))
    if not valid then return false,why end
    cfg=clean; mod:set("native_director_v3",cfg); return true
end
mod.restore_defaults=function() return mod.save_config({}) end
mod.set_patch=function(id,key,value)
    local next_cfg=S.copy(cfg); next_cfg.patches[id]=next_cfg.patches[id] or {}; next_cfg.patches[id][key]=S.copy(value)
    if next_cfg.relative[id] then next_cfg.relative[id][key]=nil end
    return mod.save_config(next_cfg)
end
mod.set_relative=function(id,key,factor)
    local next_cfg=S.copy(cfg);next_cfg.relative[id]=next_cfg.relative[id] or {};next_cfg.relative[id][key]=factor
    if next_cfg.patches[id] then next_cfg.patches[id][key]=nil end
    return mod.save_config(next_cfg)
end
mod.set_rule=function(id,target,rule)
    local next_cfg=S.copy(cfg); next_cfg.rules[id]=next_cfg.rules[id] or {}; next_cfg.rules[id][target]=S.copy(rule)
    return mod.save_config(next_cfg)
end
mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_relative")
mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_presets")
mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_text_input")
mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/preset_ui")
mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_editor")
mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_dashboard")
mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_runtime")
mod.open_settings=function()
    if mod:is_enabled() and base:is_enabled() then mod._open_settings_requested=true; base.open_condition_manager_view() end
end
local function changed(initial)
    toggle.changed(initial)
    mod._open_settings_requested=nil
    if mod.cleanup_template_ui then mod.cleanup_template_ui() end
    if mod.cleanup_director_text then mod.cleanup_director_text() end
    if not initial and base.close_condition_manager_view then base.close_condition_manager_view() end
end
mod.on_enabled=changed; mod.on_disabled=changed; mod.on_base_state_changed=changed
mod.on_unload=function()
    if mod.cleanup_template_ui then mod.cleanup_template_ui() end
    if mod.cleanup_director_text then mod.cleanup_director_text() end
    if mod.finish_director then mod.finish_director() end
end
mod.on_game_state_changed=function(status,state)
    if state=="GameplayStateRun" then
        if status=="exit" then mod.finish_director();toggle.finish()
        elseif status=="enter" then mod.finish_director();toggle.start() end
    end
end
