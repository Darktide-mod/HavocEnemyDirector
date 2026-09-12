local mod=get_mod("HavocEnemyDirector")
local base=get_mod("HavocConditionManager")
local Pacing=require("scripts/managers/pacing/pacing_manager")
local Status=require("scripts/utilities/attack/player_unit_status")
local Engine=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_engine")
local Spawning=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_spawning")
local Config=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_config")
local owner,engine,elapsed
mod.diy_api={version=1}
function mod.diy_api.status()
    return {ready=engine~=nil,phase=engine and engine.phase,elapsed=engine and engine.elapsed or 0,
        pending=engine and #engine.jobs or 0,seed=engine and engine.seed}
end
function mod.diy_api.request(request)
    if not engine or not base.has_local_gameplay_authority() or not mod.is_gameplay_enabled() then return false,"director_not_ready" end
    if type(request)~="table" then return false,"request" end
    for key in pairs(request) do if key~="formation" and key~="breed" and key~="count" and key~="seed" and key~="source" then return false,"request_field" end end
    if type(request.source)~="string" or #request.source>192 or not request.source:match("^[%w_:/%-]+$") then return false,"request_source" end
    if request.seed~=nil and (type(request.seed)~="number" or request.seed~=request.seed or request.seed%1~=0 or request.seed<1 or request.seed>2147483646) then return false,"request_seed" end
    local formation
    if request.formation and not request.breed then
        for _,f in ipairs(engine.config.formations) do if f.id==request.formation then formation=f;break end end
        if not formation then return false,"formation_missing" end
        if request.count~=nil and request.count~=1 then return false,"formation_count" end
    elseif request.breed and not request.formation then
        local count=request.count or 1
        if type(count)~="number" or count~=count or count%1~=0 or count<1 or count>16 then return false,"request_count" end
        local family
        for _,candidate in ipairs({"monsters","specials","trickle"}) do if Config.breed_allowed(candidate,request.breed) then family=candidate;break end end
        if not family or family=="monsters" and count>3 then return false,"request_breed" end
        formation={id="external",family=family,variants={{weight=1,members={{name=request.breed,amount={count,count}}}}}}
    else return false,"request_target" end
    return engine.submit(request,formation)
end
function mod.finish_director()
    if engine then engine.finish() end
    owner=nil;engine=nil;elapsed=0
end
mod:hook_safe(Pacing,"update",function(self,dt)
    if not base.has_local_gameplay_authority() or not mod.is_gameplay_enabled() then return end
    if owner~=self then
        mod.finish_director();owner=self
        -- One immutable configuration snapshot per mission, like HCM.
        local cfg=mod.get_saved_config()
        if not cfg.director.enabled then return end
        if not base.spawn_placement then mod:notify(mod:localize("director_navigation_required"));return end
        local coarse=base.template_runtime.config().coarse
        engine=Engine.new(cfg,self._level_seed,coarse,base.template_conditions,Spawning.new(self,coarse))
    end
    if not engine then return end
    elapsed=elapsed+dt
    if elapsed<0.1 then return end
    local step=elapsed;elapsed=0
    local context=base.template_conditions.capture(Managers,Status,ScriptUnit,self._target_side_id)
    context.safe=self._disabled or self:get_in_safe_zone()
    if base.diy_api then
        base.diy_api.context(context)
        context.diy_paused=base.diy_api.paused("hed")
    end
    local mortis=get_mod("MortisBuffManager")
    if mortis and mortis.diy_api then
        mortis.diy_api.context(context);context.diy_paused=context.diy_paused or mortis.diy_api.paused("hed")
    end
    engine.tick(step,context)
end)
mod:hook_safe(Pacing,"delete",function(self) if owner==self then mod.finish_director() end end)
return true
