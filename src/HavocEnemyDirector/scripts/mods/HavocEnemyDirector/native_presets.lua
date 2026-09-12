local mod=get_mod("HavocEnemyDirector")
local base=get_mod("HavocConditionManager")
local S=base.template_schema
local C=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_preset_codec")
local Files=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/preset_files")
local A={codec=C}; local store
local Seed=base:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_seed")
local condition_seeds=Seed.new(base)
local function protect(fn,...)
    local ok,value,err=pcall(fn,...)
    if not ok then return nil,"template_io_failed" end
    return value,err
end
local function storage()
    if not store then
        local ok,value,err=pcall(Files.new,Mods and Mods.lua and Mods.lua.ffi)
        if not ok or not value then return nil,err or "template_io_unavailable" end
        store=value
    end
    return store
end
function A.directory()
    local fs,err=storage(); if not fs then return nil,err end
    local ok,e=protect(fs.ensure); if not ok then return nil,e end
    return fs.directory
end
function A.compatible(doc) local checked,err=C.validate(doc); return checked and true or nil,err end
function A.capture(name)
    return C.validate({format=C.format,version=C.version,name=name,config=mod.get_saved_config(),coarse=S.coarse_config(base:get("native_configuration_v3")),condition_seed=condition_seeds.get()})
end
function A.decode(text) return C.decode(text,cjson) end
function A.read(filename)
    if not C.filename(filename) then return nil,"template_name_invalid" end
    local fs,err=storage(); if not fs then return nil,err end
    local text,e=protect(fs.read,filename); if not text then return nil,e end
    return A.decode(text)
end
function A.list()
    local fs,err=storage(); if not fs then return nil,err end
    local filenames,e=protect(fs.list); if not filenames then return nil,e end
    local result={}
    for _,filename in ipairs(filenames) do
        if C.filename(filename) then
            local doc,why=A.read(filename)
            result[#result+1]={file=filename,name=doc and doc.name or filename,document=doc,error=why}
        end
    end
    table.sort(result,function(a,b) return a.name==b.name and a.file<b.file or a.name<b.name end)
    return result
end
function A.save_document(doc,name,overwrite)
    name=C.name(name); if not name then return nil,"template_name_invalid" end
    local copy=S.copy(doc); copy.name=name
    local checked,err=C.validate(copy); if not checked then return nil,err end
    local ok,text=pcall(cjson.encode,checked)
    if not ok or #text>C.max_bytes then return nil,"template_too_large" end
    local fs,e=storage(); if not fs then return nil,e end
    local saved,why=protect(fs.write,name..".json",text,overwrite==true)
    if not saved then return nil,why end
    return name..".json"
end
function A.save(name,overwrite) local doc,err=A.capture(name); if not doc then return nil,err end; return A.save_document(doc,name,overwrite) end
function A.delete(filename)
    if not C.filename(filename) then return nil,"template_name_invalid" end
    local fs,err=storage(); if not fs then return nil,err end
    return protect(fs.remove,filename)
end
function A.export(filename)
    local doc,err=A.read(filename); if not doc then return nil,err end
    local ok,text=pcall(cjson.encode,doc); if not ok then return nil,"template_json_invalid" end
    return text
end
function A.apply(doc,view)
    if not mod:is_enabled() or not base:is_enabled() then return nil,"template_disabled" end
    local checked,err=C.validate(doc); if not checked then return nil,err end
    local previous=A.capture("rollback")
    local function assign(value)
        base:set("native_configuration_v3",value.coarse)
        local ok,why=mod.save_config(value.config); if not ok then error(why) end
        if value.condition_seed and not condition_seeds.set(value.condition_seed) then error("condition seed") end
    end
    local applied=pcall(assign,checked)
    if not applied then if previous then pcall(assign,previous) end; return nil,"template_apply_failed" end
    if view then view._hed_path={}; view._hed_item=nil; view._hed_rule_target=nil; view._hcm_offsets={}; view._hcm_refresh=true end
    return true
end
mod.presets=A
return A
