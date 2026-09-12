-- Persisted data only. All editors, imports and the mission snapshot share this
-- validator; no saved expression is ever compiled or evaluated as source code.
local base=get_mod("HavocConditionManager")
local S,A,R=base.template_schema,base.template_registry,base.template_conditions
local C={version=3,families={"hordes","trickle","specials","monsters","patrols"}}
C.director_defaults={enabled=false,mode="rules",seed=0,seed_enabled=false,selection="priority",admission_interval=2,
    max_active_groups=4,load_ceiling=100,capable_min=1,allow_events=false,
    low_load=25,high_load=65,build_duration={40,80},pressure_duration={25,45},recovery_duration={20,40},
    build_size=1,pressure_size=1.25,recovery_size=0.5,
    build_frequency=1,pressure_frequency=1.5,recovery_frequency=0}
C.deployment_defaults={enabled=true,trigger="timer",interval={60,90},first_delay=30,
    progress_start=100,progress_step=100,start_time=0,end_time=0,cooldown=20,
    max_occurrences=5,max_alive=1,priority=1,weight=1,phase="any",
    inherit_size=true,inherit_frequency=true,size_multiplier=1,frequency_multiplier=1,
    waves=1,wave_gap=5,recheck_conditions=false,conditions={mode="append",match="all",clauses={}}}
local function fields(t,keys)
    if type(t)~="table" or getmetatable(t) then return false end
    for k in pairs(t) do if not keys[k] then return false end end
    return true
end
local function keys(t,extra) local r=extra or {};for k in pairs(t) do r[k]=true end;return r end
local function array(t,minimum,maximum)
    if type(t)~="table" or getmetatable(t) or #t<minimum or #t>maximum then return false end
    local n=0
    for k in pairs(t) do
        if type(k)~="number" or k%1~=0 or k<1 or k>#t then return false end;n=n+1
    end
    return n==#t
end
local function num(n,lo,hi,integer) return S.finite(n) and n>=lo and n<=hi and (not integer or n%1==0) end
local function pair(v,lo,hi,integer) return array(v,2,2) and num(v[1],lo,hi,integer) and num(v[2],lo,hi,integer) and v[1]<=v[2] end
local function one(v,options) for _,x in ipairs(options) do if x==v then return true end end;return false end
local function id(s) return type(s)=="string" and #s<=48 and s:match("^[a-zA-Z0-9_%-]+$")~=nil end
function C.name(s)
    if type(s)~="string" or #s>192 or s:find("[%z\1-\31]") or not s:find("%S") then return false end
    local n=0;for _ in s:gmatch(".[\128-\191]*") do n=n+1 end
    return n<=48
end
local monster_names={chaos_spawn=true,chaos_beast_of_nurgle=true,chaos_plague_ogryn=true}
function C.breed_allowed(family,name)
    local b=A.breeds[name];if not b or b.breed_type~="minion" or b.airbound then return false end
    local tags=b.tags or {}
    if family=="monsters" then return monster_names[name]==true end
    if family=="specials" then
        -- Native slot setup needs breed-specific timers, distances and sounds.
        if not tags.special then return false end
        for _,entry in ipairs(A.entries) do
            if entry.family=="specials" and entry.root.foreshadow_stinger_timers and
                entry.root.foreshadow_stinger_timers[name]~=nil then return true end
        end
        return false
    end
    if tags.special or tags.monster or tags.captain or tags.cultist_captain or tags.ritualist or
        not (tags.horde or tags.roamer or tags.elite) then return false end
    return family~="patrols" or b.can_patrol==true
end
local director_numbers={seed={0,2147483646,true},admission_interval={0.5,60},max_active_groups={1,16,true},
    load_ceiling={1,2000},capable_min={1,4,true},low_load={0,2000},high_load={1,2000},
    build_size={0.1,5},pressure_size={0.1,5},recovery_size={0.1,5},
    build_frequency={0,5},pressure_frequency={0,5},recovery_frequency={0,5}}
local deployment_numbers={first_delay={0,7200},progress_start={0,10000},progress_step={1,10000},
    start_time={0,14400},end_time={0,14400},cooldown={0.5,3600},max_occurrences={0,100,true},
    max_alive={1,16,true},priority={0,100,true},weight={0.01,100},size_multiplier={0.1,10},
    frequency_multiplier={0.1,10},waves={1,12,true},wave_gap={0.5,120}}
local function fill(raw,defaults)
    local out=S.copy(defaults);for k,v in pairs(raw) do out[k]=S.copy(v) end;return out
end
local function numbers(value,definitions)
    for k,d in pairs(definitions) do if not num(value[k],d[1],d[2],d[3]) then return false,k end end
    return true
end
function C.validate(raw)
    if raw==nil then raw={} end
    local clean={version=3,patches={},relative={},rules={},director=S.copy(C.director_defaults),formations={},deployments={},next_id=1}
    local bad={}
    local function fail(why) bad[#bad+1]=why;return clean,bad end
    if not fields(raw,{version=true,patches=true,relative=true,rules=true,seed=true,seed_enabled=true,director=true,formations=true,deployments=true,next_id=true}) then return fail("config fields") end
    if raw.version~=nil and raw.version~=2 and raw.version~=3 then return fail("config version") end
    if raw.seed~=nil and not num(raw.seed,1,2147483646,true) then return fail("map seed") end
    if raw.seed_enabled~=nil and type(raw.seed_enabled)~="boolean" then return fail("map seed switch") end
    if raw.patches~=nil and type(raw.patches)~="table" or raw.rules~=nil and type(raw.rules)~="table" then return fail("native config") end
    local native,rejected=A.validate_config(raw)
    if #rejected>0 then return fail(rejected[1]) end
    clean.patches=native.patches;clean.rules=native.rules;clean.seed=native.seed
    clean.seed_enabled=raw.seed_enabled==true or raw.seed_enabled==nil and raw.seed~=nil
    if clean.seed_enabled and not clean.seed then return fail("map seed value") end
    local relative=raw.relative or {}
    if type(relative)~="table" or getmetatable(relative) then return fail("relative") end
    local count=0
    for entry_id,patch in pairs(relative) do
        local entry=A.by_id[entry_id]
        if not entry or type(patch)~="table" or getmetatable(patch) then return fail("relative template") end
        local values={}
        for key,factor in pairs(patch) do
            count=count+1;local item=entry.fields[key]
            if count>4096 or not item or item.kind~="number" and item.kind~="range" or not num(factor,0.1,10) or
                clean.patches[entry_id] and clean.patches[entry_id][key]~=nil then return fail("relative field") end
            values[key]=factor
        end
        if next(values) then clean.relative[entry_id]=values end
    end
    local d=raw.director or {}
    if not fields(d,keys(C.director_defaults)) then return fail("director fields") end
    local legacy_seed=d.seed_enabled==nil and d.seed~=nil and d.seed~=0
    d=fill(d,C.director_defaults);clean.director=d
    if legacy_seed then d.seed_enabled=true end
    if not numbers(d,director_numbers) or type(d.enabled)~="boolean" or type(d.allow_events)~="boolean" or type(d.seed_enabled)~="boolean" or d.seed_enabled and d.seed<1 or
        not one(d.mode,{"rules","adaptive"}) or not one(d.selection,{"priority","weighted"}) or d.low_load>=d.high_load then return fail("director values") end
    for _,phase in ipairs({"build","pressure","recovery"}) do
        if not pair(d[phase.."_duration"],1,1200) then return fail("phase duration") end
    end
    clean.next_id=raw.next_id or 1
    if not num(clean.next_id,1,1000000000,true) then return fail("next id") end
    local formations=raw.formations or {}
    if not array(formations,0,32) then return fail("formations") end
    local ids={}
    for _,f in ipairs(formations) do
        if not fields(f,{id=true,name=true,family=true,variants=true}) or not id(f.id) or ids[f.id] or not C.name(f.name) or
            not one(f.family,C.families) or not array(f.variants,1,8) then return fail("formation") end
        ids[f.id]=f
        for _,variant in ipairs(f.variants) do
            if not fields(variant,{weight=true,members=true}) or not num(variant.weight,0.01,100) or not array(variant.members,1,16) then return fail("variant") end
            local total=0
            for _,m in ipairs(variant.members) do
                if not fields(m,{name=true,amount=true}) or not C.breed_allowed(f.family,m.name) or not pair(m.amount,0,300,true) then return fail("formation member") end
                total=total+m.amount[2]
            end
            local limit=f.family=="monsters" and 3 or f.family=="specials" and 16 or 300
            if total<1 or total>limit then return fail("formation size") end
        end
        clean.formations[#clean.formations+1]=S.copy(f)
    end
    local deployments=raw.deployments or {}
    if not array(deployments,0,64) then return fail("deployments") end
    local used={}
    for _,value in ipairs(deployments) do
        if not fields(value,keys(C.deployment_defaults,{id=true,name=true,formation_id=true})) or not id(value.id) or used[value.id] or
            not C.name(value.name) or not ids[value.formation_id] then return fail("deployment") end
        used[value.id]=true
        local rule=fill(value,C.deployment_defaults)
        if not numbers(rule,deployment_numbers) or not pair(rule.interval,1,7200) or
            type(rule.enabled)~="boolean" or type(rule.inherit_size)~="boolean" or type(rule.inherit_frequency)~="boolean" or type(rule.recheck_conditions)~="boolean" or
            not one(rule.trigger,{"timer","progress","condition"}) or not one(rule.phase,{"any","build","pressure","recovery"}) or
            rule.end_time~=0 and rule.end_time<rule.start_time or not R.validate(rule.conditions) or rule.conditions.mode~="append" then return fail("deployment values") end
        if rule.trigger=="condition" and #rule.conditions.clauses==0 then return fail("condition trigger needs a condition") end
        clean.deployments[#clean.deployments+1]=rule
    end
    return clean,bad
end
function C.relative_value(item,coarse,factor)
    local value=S.scaled(item,item.family,coarse)
    if factor==1 then return value end
    local d=item.definition
    local function scale(v,native)
        if v==0 then return 0 end
        local minimum=d.min
        if v<minimum or native<minimum then minimum=math.min(0.001,v,native>0 and native or v) end
        local maximum=math.max(d.max,native)
        local result=S.clamp(v*factor,minimum,maximum)
        -- Native specialist capacity is multiplied again and only then rounded
        -- up by the slot owner. Preserve that order for relative settings.
        if d.integer and d.key~="max_alive_specials" and native%1==0 then result=math.floor(result+0.5) end
        return result
    end
    if type(value)=="table" then return {scale(value[1],item.value[1]),scale(value[2],item.value[2])} end
    return scale(value,item.value)
end
function C.apply_relative(root,entry,patch,coarse)
    local result=root;local changed=0
    for key,factor in pairs(patch or {}) do
        local item=entry.fields[key]
        if item then
            local value=C.relative_value(item,coarse,factor)
            if not S.equal(value,S.get(result,item.path)) then
                if result==root then result={};for k,v in pairs(root) do result[k]=v end end
                S.set(result,item.path,value);changed=changed+1
            end
        end
    end
    return result,changed
end
function C.validate_relative_result(raw,coarse)
    for id,patch in pairs(raw.relative or {}) do
        local entry=A.by_id[id]
        local prepared=S.apply(entry.root,entry.family,coarse,raw.patches[id],A.breeds,A.by_table)
        local result=C.apply_relative(prepared,entry,patch,coarse)
        local near,far=result.spawners_min_range,result.spawners_max_range
        if type(near)=="table" and type(far)=="table" then
            for breed,n in pairs(near) do
                if type(n)=="number" and type(far[breed])=="number" and n>far[breed] then return false,"spawner distance order" end
            end
        end
    end
    return true
end
function C.resolve(raw,coarse)
    local out={version=2,patches=S.copy(raw.patches),rules=S.copy(raw.rules),seed=raw.seed_enabled~=false and raw.seed or nil}
    for id,patch in pairs(raw.relative or {}) do
        local entry=A.by_id[id];out.patches[id]=out.patches[id] or {}
        for key,factor in pairs(patch) do
            out.patches[id][key]=C.relative_value(entry.fields[key],coarse,factor)
        end
    end
    return out
end
function C.allocate(config,prefix)
    local used={};for _,list in ipairs({config.formations,config.deployments}) do for _,v in ipairs(list) do used[v.id]=true end end
    local n=config.next_id
    while used[prefix..n] do n=n+1 end
    config.next_id=n+1;return prefix..n
end
function C.new_formation(config,name,family,breed)
    local f={id=C.allocate(config,"f"),name=name,family=family,
        variants={{weight=1,members={{name=breed,amount={1,1}}}}}}
    config.formations[#config.formations+1]=f;return f
end
function C.new_deployment(config,name,formation)
    local d=S.copy(C.deployment_defaults)
    d.id=C.allocate(config,"d");d.name=name;d.formation_id=formation
    config.deployments[#config.deployments+1]=d;return d
end
return C
