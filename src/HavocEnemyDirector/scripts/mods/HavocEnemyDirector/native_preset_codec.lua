-- Data only. Imported files are never evaluated as Lua.
local C={format="HavocEnemyDirector.Template",version=4,max_bytes=262144,max_files=256}
local base=get_mod("HavocConditionManager")
local S,A=base.template_schema,base.template_registry
local Director=get_mod("HavocEnemyDirector").director_config
local Seed=base:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_seed")
function C.name(s)
    if type(s)~="string" then return nil end
    s=s:match("^%s*(.-)%s*$")
    if s=="" or #s>256 or s:find('[%z\1-\31<>:"/\\|?*]') or s:match("[%. ]$") then return nil end
    local n=0; for _ in s:gmatch(".[\128-\191]*") do n=n+1 end
    local stem=(s:match("^([^%.]+)") or ""):upper()
    if n>64 or stem=="CON" or stem=="PRN" or stem=="AUX" or stem=="NUL" or stem:match("^COM[1-9]$") or stem:match("^LPT[1-9]$") then return nil end
    return s
end
function C.filename(s) return type(s)=="string" and s:sub(-5):lower()==".json" and C.name(s:sub(1,-6))~=nil end
local function fields(value,allowed)
    if type(value)~="table" or getmetatable(value) then return false end
    for key in pairs(value) do if not allowed[key] then return false end end
    return true
end
function C.validate(value)
    if type(value)~="table" then return nil,"template_invalid" end
    if value.format~=C.format or value.version~=2 and value.version~=3 and value.version~=C.version then return nil,"template_version" end
    if not fields(value,{format=true,version=true,name=true,config=true,coarse=true,condition_seed=true}) then return nil,"template_invalid" end
    local condition_seed=value.condition_seed and Seed.validate(value.condition_seed)
    if value.condition_seed~=nil and not condition_seed then return nil,"template_invalid" end
    local name=C.name(value.name); if not name then return nil,"template_name_invalid" end
    local raw=value.config
    if type(raw)~="table" or raw.version~=2 and raw.version~=3 or type(raw.patches)~="table" or type(raw.rules)~="table" then return nil,"template_invalid" end
    if raw.seed~=nil and (not S.finite(raw.seed) or raw.seed<1 or raw.seed>2147483646 or raw.seed%1~=0) then return nil,"template_invalid" end
    local count=0
    for _,section in ipairs({raw.patches,raw.rules}) do
        for _,entry in pairs(section) do
            if type(entry)~="table" then return nil,"template_invalid" end
            for _ in pairs(entry) do count=count+1 end
            if count>4096 then return nil,"template_too_large" end
        end
    end
    local config,rejected=Director.validate(raw)
    if #rejected>0 then return nil,"template_invalid: "..rejected[1] end
    local allowed={}; for _,d in ipairs(S.coarse) do allowed[d.id]=true end
    if not fields(value.coarse,allowed) then return nil,"template_invalid" end
    for _,d in ipairs(S.coarse) do
        local v=value.coarse[d.id]
        if not S.finite(v) or v<d.min or v>d.max then return nil,"template_invalid" end
    end
    local valid,why=Director.validate_relative_result(config,value.coarse)
    if not valid then return nil,"template_invalid: "..tostring(why) end
    return {format=C.format,version=C.version,name=name,config=config,coarse=S.copy(value.coarse),condition_seed=condition_seed}
end
function C.decode(text,json)
    if type(text)~="string" or #text>C.max_bytes then return nil,"template_too_large" end
    text=text:gsub("^\239\187\191","")
    local ok,value=pcall(json.decode,text)
    if not ok then return nil,"template_json_invalid" end
    local checked,doc,err=pcall(C.validate,value)
    if not checked then return nil,"template_invalid" end
    return doc,err
end
return C
