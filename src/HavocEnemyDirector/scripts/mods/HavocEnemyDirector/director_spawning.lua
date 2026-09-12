-- Native objects keep their own health, AI, slot, boss and group lifecycles.
-- HED only schedules bounded requests and remembers ownership for admission.
local base=get_mod("HavocConditionManager")
local Blackboard=require("scripts/extension_systems/blackboard/utilities/blackboard")
local Patrols=require("scripts/utilities/minion_patrols")
local M={}
local pacing_types={hordes="hordes",trickle="hordes",specials="specials",monsters="monsters",patrols="monsters"}
function M.new(pacing,coarse)
    local out={};local next_member=0
    local function group_system() return Managers.state.extension and Managers.state.extension:system("group_system") end
    local function unlock(job)
        if job.locked then
            local system=group_system();if system then system:unlock_group_id(job.group_id) end
            job.locked=nil
        end
    end
    function out.allowed(family)
        if base.diy_api and (base.diy_api.paused("hed") or base.diy_api.paused(family=="trickle" and "trickle_hordes" or family)) then return false end
        local child=family=="specials" and pacing._specials_pacing or
            (family=="monsters" or family=="patrols") and pacing._monster_pacing or pacing._horde_pacing
        if child and (child._disabled or child._frozen) then return false end
        return not pacing._disabled and not pacing:get_in_safe_zone() and pacing:spawn_type_enabled(pacing_types[family])
    end
    function out.alive(job)
        local n=0
        for i=#job.units,1,-1 do
            if HEALTH_ALIVE[job.units[i]] then n=n+1 end
        end
        if job.family=="specials" and pacing._specials_pacing then
            n=n+pacing._specials_pacing:get_num_specials_owned_by_auto_event(job.id)
        end
        return n
    end
    function out.cancel(job)
        -- Already accepted native specials remain owned until native slot
        -- completion. Never delete living enemies or interrupt their attacks.
        unlock(job);job.done=true;job.positions=nil
    end
    local function advance(job,now)
        job.started=true;job.index=job.index+1;job.next_at=now+0.25
        if job.index>#job.members then
            if job.wave>=job.waves then job.done=true;unlock(job)
            else job.wave=job.wave+1;job.index=1;job.next_at=now+job.wave_gap end
        end
    end
    local function position_for(job,context)
        local placement=base.spawn_placement
        local anchor=placement.anchor(context,job)
        if not anchor then return end
        if not job.positions then
            local positions={}
            local count=GwNavQueries.flood_fill_from_position(pacing._nav_world,anchor,2,2,math.min(16,#job.members),positions)
            job.positions={};job.position_index=1
            for i=1,count or 0 do job.positions[i]=Vector3Box(positions[i]) end
            if #job.positions==0 then job.positions=nil;return end
        end
        local position=job.positions[job.position_index]:unbox()
        job.position_index=job.position_index+1
        if job.position_index>#job.positions then job.positions=nil end
        if placement.valid(context,position) then return position end
        job.positions=nil
    end
    local function special(job,name,context)
        local manager=pacing._specials_pacing;local template=manager and manager._template
        if not template or not template.foreshadow_stinger_timers or template.foreshadow_stinger_timers[name]==nil then return end
        local maximum=manager._optional_max_of_same_override and manager._optional_max_of_same_override[name] or template.max_of_same[name]
        local count=0
        for _,slot in ipairs(manager._specials_slots) do
            if slot.breed_name==name and (slot.spawned or slot.foreshadow_triggered or slot.injected or slot.spawner_queue_id) then count=count+1 end
        end
        if maximum and count>=maximum then return end
        return manager:try_inject_special(name,"ahead",context.target,nil,false,nil,nil,job.id)
    end
    local function ordinary(job,name,position,context,manager)
        local system=group_system()
        if not job.group_id then
            job.group_id=system:generate_group_id();system:lock_group_id(job.group_id);job.locked=true
        end
        local params=manager:request_param_table()
        params.optional_group_id=job.group_id;params.spawn_source=job.state and job.state.external and "hed_diy" or "hed_director"
        params.optional_aggro_state=job.family=="patrols" and "passive" or "aggroed"
        params.optional_target_unit=job.family~="patrols" and context.target or nil
        if base.new_spawn_batch then
            -- This is an independently owned encounter. HCM's external-event
            -- ownership keeps its recovery pool from replacing these members
            -- outside HED's per-rule active-encounter accounting.
            job.batch=job.batch or base.new_spawn_batch(params.spawn_source,context.side_id,pacing._target_side_id,job.id)
            params._hcm_batch=job.batch
        end
        local unit=manager:spawn_minion(name,position,Quaternion.identity(),context.side_id,params)
        if unit and job.family=="patrols" then
            local board=Blackboard.write_component(BLACKBOARDS[unit],"patrol")
            local index=#job.units+1
            local follow=index>1 and job.units[Patrols.get_follow_index(index)]
            if not HEALTH_ALIVE[follow] then
                follow=nil;for i=#job.units,1,-1 do if HEALTH_ALIVE[job.units[i]] then follow=job.units[i];break end end
            end
            board.should_patrol=true;board.patrol_index=follow and index or 1
            if follow then board.patrol_leader_unit=follow
            else board.walk_position:store(context.reachable_target);board.auto_patrol=true end
        end
        return unit
    end
    function out.update(job,_,now)
        if now<job.next_at or now<next_member or not out.allowed(job.family) then return false end
        job.next_at=now+0.25;next_member=now+0.25
        local manager=Managers.state.minion_spawn
        if not manager or (manager._spawn_queue_size or 0)>=16 or
            manager:total_allocated_num_enemies()>=math.floor(145*(coarse.combat_tolerance or 1)+0.5)-4 then return true end
        local placement=base.spawn_placement
        if not placement then return true end
        local t=Managers.time:time("gameplay")
        local context=placement.context(pacing._side_id or 2,pacing._target_side_id or 1,t)
        if not context then return true end
        local name=job.members[job.index]
        if job.family=="specials" then
            if special(job,name,context) then advance(job,now) else job.next_at=now+2 end
            return true
        end
        local position=position_for(job,context)
        if not position then job.next_at=now+0.5;return true end
        local unit
        if job.family=="monsters" then
            local monster={breed_name=name,position=Vector3Box(position)}
            pacing._monster_pacing:_spawn_monster(monster,context.target,context.side_id)
            unit=monster.spawned_unit
        else unit=ordinary(job,name,position,context,manager) end
        if unit then job.units[#job.units+1]=unit;advance(job,now)
        else job.next_at=now+2 end
        return true
    end
    return out
end
return M
