local mod=get_mod("HavocEnemyDirector")
local base=get_mod("HavocConditionManager")
local S=base.template_schema
local M={}
function M.loc(key,...) return mod:localize("director_"..key,...) end
local function translated(key)
    local id="director_"..key;local value=mod:localize(id)
    if value~=id then return value end
end
function M.key(key,index)
    if type(key)=="number" then return M.loc("branch",tostring(key)) end
    local breed=base.template_registry.breeds[key]
    if breed then
        local value=breed.display_name and Localize(breed.display_name)
        if value and value~=key and not value:find("^loc_") then return value end
        local name=translated("breed_"..key);if name then return name end
    end
    local name=translated("group_"..key)
    if name then return name end
    local d=S.fields[key]
    if d then return S.text(d,base:localize("native_language")) end
    return index and M.loc("group_fallback",tostring(index)) or tostring(key):gsub("_"," ")
end
function M.master(id)
    local exact=translated("native_"..id);if exact then return exact end
    local mode=id:match("^(default)_") or id:match("^(havoc)_") or id:match("^(expedition)_")
    if mode then return M.loc("native_"..mode)..(id:match("_(%d+)$") and " · "..id:match("_(%d+)$") or "") end
    return id:gsub("_"," ")
end
function M.path(path,raw)
    if raw then return S.path_key(path) end
    local text={}
    if #path>3 then text[1]="…" end
    for i=math.max(1,#path-2),#path do text[#text+1]=M.key(path[i]) end
    return table.concat(text,"  ›  ")
end
local common={}
for _,key in ipairs({"max_tension","tension_threshold","duration","decay_tension_rate","allowed_spawn_types","challenge_rating_thresholds",
    "num_roamers_range","zone_length","zone_range","empty_zone_range","num_slots","breed_limit","tag_limits","num_encampments",
    "horde_timer_range","travel_distance_required_for_horde","travel_distance_spawning","num_waves","time_between_waves",
    "max_active_minions","pre_stinger_delays","chance","high_chance","total_num_allowed","trickle_horde_cooldown",
    "trickle_horde_travel_distance_range","breeds","max_alive_specials","max_of_same","timer_range","min_timer_diff_range",
    "coordinated_strike_timer_range","coordinated_strike_num_breeds","num_coordinated_surges_range","num_monsters","num_witches",
    "num_captains","num_boss_patrols","points","max_breed_amount","max_points","weight","weights","time_between_waves",
    "spawn_distance","spawners_min_range","spawners_max_range","points_base","resistance_multiplier","event_size"}) do common[key]=true end
function M.items(view,entry,tab)
    if tab~="parameters" then return entry.items end
    local filter=view._hed_field_filter or "common"
    if filter=="all" then return entry.items end
    local out={}
    local cfg=mod.peek_config()
    local fixed=cfg.patches[entry.id] or {};local relative=cfg.relative[entry.id] or {}
    for _,item in ipairs(entry.items) do
        if filter=="changed" and (fixed[item.id]~=nil or relative[item.id]~=nil) or
            filter=="common" and common[item.definition.key] then out[#out+1]=item end
    end
    return out
end
function M.help(entry,item)
    if item and item.definition.key=="max_active_hordes" then return M.loc("legacy_field") end
    return M.loc("scope_"..entry.family)
end
return M
