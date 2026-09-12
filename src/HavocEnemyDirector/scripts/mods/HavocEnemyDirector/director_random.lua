-- Park-Miller with Schrage reduction: exact integer arithmetic in LuaJIT
-- doubles. Purpose-specific streams never touch math.random or math.randomseed.
local M={}
function M.seed(value)
    value=tonumber(value) or 1
    if value~=value or value==math.huge or value==-math.huge then value=1 end
    return math.floor(math.abs(value))%2147483646+1
end
function M.derive(seed,key)
    local n=M.seed(seed)
    for i=1,#key do n=(n*31+key:byte(i))%2147483646 end
    return n+1
end
function M.new(seed,key)
    local state=M.derive(seed,key or "")
    local r={}
    function r.next()
        local high=math.floor(state/127773);local low=state-high*127773
        local n=16807*low-2836*high
        state=n>0 and n or n+2147483647
        return (state-1)/2147483646
    end
    function r.range(a,b) return a+(b-a)*r.next() end
    function r.integer(a,b) return a+math.floor(r.next()*(b-a+1)) end
    function r.weighted(list)
        local total=0;for _,v in ipairs(list) do total=total+v.weight end
        local draw=r.next()*total
        for i,v in ipairs(list) do draw=draw-v.weight;if draw<0 then return i end end
        return #list
    end
    return r
end
return M
