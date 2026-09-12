-- Deterministic scheduling with an injected native-spawn boundary. This module
-- owns HED encounters only; original mission events and pacing remain native.
local mod=get_mod("HavocEnemyDirector")
local breeds=get_mod("HavocConditionManager").template_registry.breeds
local RNG=mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_random")
local E={}
local size_keys={hordes="horde_size",trickle="trickle_size",specials="special_slots",monsters="monster_encounters"}
local frequency_keys={hordes="horde_frequency",trickle="trickle_frequency",specials="special_frequency"}
function E.new(config,level_seed,coarse,rules,adapter)
    local settings=config.director
    local fixed=settings.seed_enabled
    if fixed==nil then fixed=settings.seed~=0 end
    local seed=fixed and settings.seed or level_seed or 1
    local self={config=config,seed=seed,coarse=coarse,adapter=adapter,elapsed=0,phase="build",
        states={},jobs={},next_admission=0,serial=0,phase_random=RNG.new(seed,"director/phase"),
        selection_random=RNG.new(seed,"director/selection")}
    local formations={}
    for _,f in ipairs(config.formations) do formations[f.id]=f end
    for _,d in ipairs(config.deployments) do
        self.states[#self.states+1]={definition=d,formation=formations[d.formation_id],remaining=0,next_progress=d.progress_start,
            cooldown_until=0,occurrences=0,active=0,armed=true,edge=false,last_condition=false,
            timer_random=RNG.new(seed,d.id.."/timer"),variant_random=RNG.new(seed,d.id.."/variant"),
            amount_random=RNG.new(seed,d.id.."/amount")}
    end
    -- Reordering the editor list does not change tie-breaking or random draws.
    table.sort(self.states,function(a,b) return a.definition.id<b.definition.id end)
    local function enter(phase)
        self.phase=phase
        local duration=settings[phase.."_duration"]
        self.phase_until=self.elapsed+self.phase_random.range(duration[1],duration[2])
    end
    enter("build")
    function self.factors(state)
        local d,f=state.definition,state.formation
        local size=d.size_multiplier*(d.inherit_size and (coarse[size_keys[f.family]] or 1) or 1)
        local frequency=d.frequency_multiplier*(d.inherit_frequency and (coarse[frequency_keys[f.family]] or 1) or 1)
        if settings.mode=="adaptive" then
            size=size*settings[self.phase.."_size"];frequency=frequency*settings[self.phase.."_frequency"]
        end
        return size,frequency
    end
    local function phase(context)
        if settings.mode~="adaptive" then return end
        local distressed=context.players~=nil and context.players<settings.capable_min or context.load~=nil and context.load>=settings.high_load
        if self.phase~="recovery" and distressed then enter("recovery")
        elseif self.phase=="recovery" then
            if self.elapsed>=self.phase_until and context.load~=nil and context.load<=settings.low_load and
                context.players~=nil and context.players>=settings.capable_min then enter("build") end
        elseif self.elapsed>=self.phase_until then enter(self.phase=="build" and "pressure" or "recovery") end
    end
    local function admitted(context)
        return context.safe~=true and context.diy_paused~=true and context.load~=nil and context.load<settings.load_ceiling and
            context.players~=nil and context.players>=settings.capable_min and
            (settings.allow_events or context.events==0)
    end
    local function phase_allowed(d)
        return d.phase=="any" or settings.mode=="adaptive" and d.phase==self.phase
    end
    local function reset_timer(s)
        local d=s.definition;s.remaining=s.timer_random.range(d.interval[1],d.interval[2])
    end
    local function started(s,job,context)
        if job.counted then return end
        job.counted=true;s.occurrences=s.occurrences+1
        s.cooldown_until=self.elapsed+s.definition.cooldown
        reset_timer(s)
        local _,frequency=self.factors(s)
        s.next_progress=math.max(s.next_progress,context.progress or 0)+s.definition.progress_step/math.max(0.1,frequency)
        s.edge=false
    end
    local function service(context)
        local active=0
        local serviced
        for _,s in ipairs(self.states) do s.active=0 end
        for index=#self.jobs,1,-1 do
            local job=self.jobs[index];local s=job.state;local d=s.definition
            local _,frequency=self.factors(s)
            local requirements=job.counted and not d.recheck_conditions or phase_allowed(d) and rules.evaluate(d.conditions,context)
            local allowed=admitted(context) and frequency>0 and requirements
            if not job.done then
                if self.elapsed>=job.expires or d.end_time>0 and self.elapsed>d.end_time then
                    adapter.cancel(job);job.done=true
                elseif allowed and adapter.allowed(s.formation.family,context) then
                    if adapter.update(job,context,self.elapsed) then serviced=job end
                end
                if job.started then started(s,job,context) end
                if job.done then
                    s.pending=nil
                    if not job.counted then
                        s.cooldown_until=self.elapsed+math.max(5,d.cooldown);reset_timer(s);s.edge=false
                        s.next_progress=math.max(s.next_progress,context.progress or 0)+d.progress_step
                    end
                end
            end
            local alive=adapter.alive(job)
            if not job.done or alive>0 then s.active=s.active+1;active=active+1
            else table.remove(self.jobs,index) end
        end
        -- Native submission is globally paced. Move its latest turn behind
        -- other pending encounters so one large group cannot monopolize it.
        if serviced and #self.jobs>1 then
            for i,job in ipairs(self.jobs) do
                if job==serviced then table.remove(self.jobs,i);table.insert(self.jobs,1,job);break end
            end
        end
        return active
    end
    local function prepare(s)
        local f,d=s.formation,s.definition
        local size=self.factors(s)
        if size<=0 then return end
        local variant=f.variants[s.variant_random.weighted(f.variants)]
        local limit=f.family=="monsters" and 3 or f.family=="specials" and 16 or 256
        local waves=math.min(d.waves,limit)
        local wave_limit=math.floor(limit/waves)
        local counts,total={},0
        for index,m in ipairs(variant.members) do
            local factor=size
            if d.inherit_size and breeds[m.name] and breeds[m.name].tags.elite then
                factor=factor/(coarse[size_keys[f.family]] or 1)*(coarse.elite_density or 1)
            end
            local n=math.floor(s.amount_random.integer(m.amount[1],m.amount[2])*factor+0.5)
            counts[#counts+1]={name=m.name,count=n,index=index};total=total+n
        end
        if total>wave_limit then
            local assigned=0;local fractions={}
            for _,member in ipairs(counts) do
                local amount=member.count*wave_limit/total
                member.count=math.floor(amount);assigned=assigned+member.count
                fractions[#fractions+1]={member=member,remainder=amount-member.count}
            end
            table.sort(fractions,function(a,b)
                return a.remainder==b.remainder and a.member.index<b.member.index or a.remainder>b.remainder
            end)
            for i=1,wave_limit-assigned do fractions[i].member.count=fractions[i].member.count+1 end
        end
        local members={}
        for _,member in ipairs(counts) do for _=1,member.count do members[#members+1]=member.name end end
        if #members==0 then
            reset_timer(s);s.cooldown_until=self.elapsed+d.cooldown
            s.next_progress=s.next_progress+d.progress_step;s.edge=false
            return
        end
        -- One encounter budget spans every wave; no unbounded queue expansion.
        self.serial=self.serial+1
        return {id="hed:"..d.id..":"..self.serial,state=s,family=f.family,members=members,
            index=1,wave=1,waves=waves,wave_gap=d.wave_gap,next_at=self.elapsed,units={},slots={},
            expires=self.elapsed+math.min(600,120+waves*d.wave_gap),done=false}
    end
    function self.tick(dt,context)
        if self.finished or not settings.enabled or not dt or dt<=0 then return end
        self.elapsed=self.elapsed+dt;phase(context)
        for i=#self.states,1,-1 do
            local s=self.states[i]
            if s.external and not s.pending and s.active==0 and (s.occurrences>0 or self.elapsed>s.definition.end_time) then table.remove(self.states,i) end
        end
        for _,s in ipairs(self.states) do
            local d=s.definition;local _,frequency=self.factors(s)
            if not s.pending or s.pending.counted then s.remaining=math.max(0,s.remaining-dt*frequency) end
            local condition=rules.evaluate(d.conditions,context)
            if condition and not s.last_condition then s.edge=true end
            if not condition then s.edge=false end
            s.last_condition=condition
        end
        local active=service(context)
        if self.elapsed<self.next_admission or active>=settings.max_active_groups or not admitted(context) then return end
        local eligible={}
        for _,s in ipairs(self.states) do
            local d=s.definition;local size,frequency=self.factors(s)
            local within=self.elapsed>=math.max(d.start_time,d.first_delay) and (d.end_time==0 or self.elapsed<=d.end_time)
            local ready=d.trigger=="timer" and s.remaining<=0 or
                d.trigger=="progress" and context.progress~=nil and context.progress>=s.next_progress or
                d.trigger=="condition" and s.edge
            if d.enabled and within and ready and size>0 and frequency>0 and not s.pending and
                self.elapsed>=s.cooldown_until and s.active<d.max_alive and (d.max_occurrences==0 or s.occurrences<d.max_occurrences) and
                phase_allowed(d) and rules.evaluate(d.conditions,context) and adapter.allowed(s.formation.family,context) then
                eligible[#eligible+1]={state=s,weight=d.weight}
            end
        end
        if #eligible==0 then return end
        if settings.selection=="priority" then
            local maximum=-1
            for _,e in ipairs(eligible) do maximum=math.max(maximum,e.state.definition.priority) end
            for i=#eligible,1,-1 do if eligible[i].state.definition.priority<maximum then table.remove(eligible,i) end end
        end
        local s=eligible[self.selection_random.weighted(eligible)].state
        self.next_admission=self.elapsed+settings.admission_interval
        local job=prepare(s)
        if job then s.pending=job;self.jobs[#self.jobs+1]=job end
    end
    -- Requests enter the same admission, navigation and population budget as
    -- authored encounters. They never call native spawn systems directly.
    function self.submit(request,formation)
        if not settings.enabled or self.finished then return false,"director_disabled" end
        if (self.request_serial or 0)>=128 then return false,"mission_request_budget" end
        local count=0;for _,s in ipairs(self.states) do if s.external then count=count+1 end end
        if count>=32 then return false,"request_capacity" end
        self.request_serial=(self.request_serial or 0)+1
        local id="diy-"..self.request_serial
        local d={id=id,enabled=true,trigger="timer",interval={600,600},first_delay=0,start_time=0,end_time=self.elapsed+120,
            progress_start=0,progress_step=1,cooldown=1,max_occurrences=1,max_alive=1,priority=1,weight=1,phase="any",
            inherit_size=false,inherit_frequency=false,size_multiplier=1,frequency_multiplier=1,waves=1,wave_gap=1,
            recheck_conditions=true,conditions={mode="append",match="all",clauses={}}}
        local stream=tostring(request.source).."/"..id
        self.states[#self.states+1]={external=true,source=request.source,definition=d,formation=formation,remaining=0,next_progress=0,
            cooldown_until=0,occurrences=0,active=0,armed=true,edge=false,last_condition=false,
            timer_random=RNG.new(request.seed or seed,stream.."/timer"),variant_random=RNG.new(request.seed or seed,stream.."/variant"),
            amount_random=RNG.new(request.seed or seed,stream.."/amount")}
        return true,id
    end
    function self.finish()
        self.finished=true
        for _,job in ipairs(self.jobs) do adapter.cancel(job) end
        self.jobs={}
    end
    return self
end
return E
