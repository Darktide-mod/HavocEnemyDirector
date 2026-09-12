local mod=get_mod("HavocEnemyDirector")
local base=get_mod("HavocConditionManager")
local S=base.template_schema
local U={}
function U.loc(key,...) return mod:localize("director_"..key,...) end
function U.value(value) return string.format("%.4g",value) end
function U.condition_label(def)
    if def.id=="horde_active" or def.id=="horde_idle" then return U.loc("condition_"..def.id) end
    return S.text(def,base:localize("native_language"))
end
function U.save(view,change)
    local cfg=mod.get_saved_config();change(cfg)
    local ok,why=mod.save_config(cfg)
    view._hcm_refresh=true
    view._hed_status=not ok and U.loc("save_failed",tostring(why)) or nil
    return ok,why
end
function U.record(view,collection,id,change)
    return U.save(view,function(cfg)
        for _,v in ipairs(cfg[collection]) do if v.id==id then change(v,cfg);return end end
    end)
end
function U.find(list,id) for _,v in ipairs(list) do if v.id==id then return v end end end
function U.options(ids)
    local out={};for _,id in ipairs(ids) do out[#out+1]={id,U.loc(id)} end;return out
end
function U.number(ui,key,x,y,w,title,value,minimum,maximum,step,integer,set)
    local function change(n)
        n=S.clamp(n,minimum,maximum);if integer then n=math.floor(n+0.5) end
        return set(n)
    end
    ui:text(key.."_label",x,y,w-218,52,title,18)
    ui:repeat_button(key.."_minus",x+w-210,y,34,52,"−",function() change(value-(step or 1)) end)
    ui:number(key.."_value",x+w-172,y,134,52,U.value(value),
        {label=title,value=value,min=minimum,max=maximum,integer=integer,set=change},20)
    ui:repeat_button(key.."_plus",x+w-34,y,34,52,"+",function() change(value+(step or 1)) end)
end
function U.choice(ui,key,x,y,w,title,value,options,set)
    ui:text(key.."_label",x,y,math.min(340,w*0.36),52,title,19)
    ui:choice(key,x+math.min(350,w*0.38),y,w-math.min(350,w*0.38),52,value,options,set)
end
function U.rename(view,collection,record)
    mod.open_director_text(view,U.loc("name"),record.name,function(value)
        if not mod.director_config.name(value) then return false,U.loc("invalid_name") end
        return U.record(view,collection,record.id,function(v) v.name=value end)
    end)
end
function U.copy_name(name)
    local out={};for c in name:gmatch(".[\128-\191]*") do if #out==38 then break end;out[#out+1]=c end
    return table.concat(out)..U.loc("copy_suffix")
end
local breed_cache={}
function U.breed_name(name)
    local breed=base.template_registry.breeds[name]
    local display=breed and breed.display_name and Localize(breed.display_name)
    if display and display~=name and not display:find("^loc_") then return display end
    local key="director_breed_"..name
    local translated=mod:localize(key)
    return translated~=key and translated or name:gsub("_"," ")
end
function U.breeds(family)
    local language=base:localize("native_language")
    local key=family..language
    if breed_cache[key] then return breed_cache[key] end
    local out={}
    for name in pairs(base.template_registry.breeds) do
        if mod.director_config.breed_allowed(family,name) then out[#out+1]={name,U.breed_name(name)} end
    end
    table.sort(out,function(a,b) return a[2]==b[2] and a[1]<b[1] or a[2]<b[2] end)
    breed_cache[key]=out;return out
end
function U.list(view,ui,key,list,selected,choose,y,capacity)
    local offset=ui:window(key,#list,capacity,1,125,906,435)
    for row=1,math.min(capacity,#list-offset) do
        local v=list[offset+row]
        local item=ui:button(key.."_"..v.id,125,y+(row-1)*60,435,52,v.name,function() choose(v.id) end,v.id==selected)
        item.center=false;item.font=19;item.scroll=key
    end
end
function U.tabs(view,ui,key,values,current,y,choose,x,w)
    x=x or 105;w=w or 1710
    local width=(w-(#values-1)*12)/#values
    for i,id in ipairs(values) do
        ui:button(key.."_"..id,x+(i-1)*(width+12),y,width,48,U.loc(id),function() choose(id) end,current==id)
    end
end
return U
