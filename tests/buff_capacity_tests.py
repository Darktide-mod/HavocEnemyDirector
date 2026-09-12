# Execute real native initialization, dispatch and reclamation with HED's fixed ring.
buff_path='scripts/extension_systems/buff/buff_extension_base.lua'
prefix='''local MAX_PROC_EVENTS=require("scripts/settings/buff/buff_settings").max_proc_events
local PROC_EVENTS_STRIDE=2; local MIN_PROC_EVENTS_SIZE=0
local PortableRandom={new=function() return {} end}; local _stat_buff_lazy_mt={}; local RPCS={}
local FixedFrame={get_latest_fixed_time=function() return 0 end}'''
L.globals().NativeProc=tbl({name:native_method(buff_path,'BuffExtensionBase',name,prefix)
    for name in ('init','destroy','request_proc_event_param_table','add_proc_event','_update_proc_events','_clear_param_tables')})
L.globals().BuffOptions=load_mod('HavocEnemyDirector/scripts/mods/HavocEnemyDirector/HavocEnemyDirector_data')
L.execute('''
local B,D=mods.HavocConditionManager,mods.HavocEnemyDirector
local old_bvalues,old_dvalues=table.clone_instance(B.values),table.clone_instance(D.values)
local old_config=D.get_config()
local old_authority,old_active,old_state=B.has_local_gameplay_authority,D.is_active,Managers.state
local old_log,old_params,old_time=Log,GameParameters,Managers.time
local old_info,old_solo_authority=D.info,mods.SoloPlay.has_local_gameplay_authority
table.clear=table.clear or function(t) for key in pairs(t) do t[key]=nil end end
table.clear_array=table.clear_array or table.clear
-- The capacity is edited in the Advanced page; DMF has no duplicate widget.
for _,w in ipairs(BuffOptions.options.widgets) do assert(w.setting_id~="buff_proc_capacity") end
D:set("buff_proc_capacity",nil)
D:set("buff_proc_linked_multiplier",5) -- A legacy saved key must have no effect.
assert(D.get_buff_proc_capacity()==300)
for _,capacity in ipairs({300,750,3000}) do
    D:set("buff_proc_capacity",capacity)
    for _,category in ipairs({"common","elite","special","boss"}) do
        for _,multiplier in ipairs({1,2,5}) do
            B:set("spawn_multiplier_"..category,multiplier)
            D.apply_capacity_presets(category)
            assert(D.get_buff_proc_capacity()==capacity,"Enemy multipliers must not change the Buff cap")
        end
    end
    D.restore_defaults()
    assert(D:get("buff_proc_capacity")==capacity,"Generator reset must preserve the separate Buff setting")
end
for _,case in ipairs({{20,300},{9999,3000},{751.9,751}}) do
    D:set("buff_proc_capacity",case[1]); assert(D.get_buff_proc_capacity()==case[2])
end

local first=#hooks+1
for _,h in ipairs(hooks) do
    if h.owner==D and h.require_hook and h.path=="scripts/extension_systems/buff/buff_extension_base" then h.fn(NativeProc) end
end
local installed=0
for i=first,#hooks do
    local h=hooks[i]
    if h.target==NativeProc then
        local fn,previous=h.fn,NativeProc[h.name]
        if h.safe then NativeProc[h.name]=function(self,...) previous(self,...); fn(self,...) end
        else NativeProc[h.name]=function(self,...) return fn(previous,self,...) end end
        installed=installed+1
    end
end
assert(installed==4)
for i=first,#hooks do assert(hooks[i].name~="_update_proc_events","No per-frame Buff update hook") end
local native_warnings=0
Log={warning=function() native_warnings=native_warnings+1 end}; GameParameters={}
Managers.state={extension={system=function() return {} end},game_session={fixed_time_step=1/60}}
local time=100
Managers.time={time=function() return time end}
B.has_local_gameplay_authority=function() return true end
mods.SoloPlay.has_local_gameplay_authority=function() return true end
D.is_active=function() return false end -- Native spawn mode still uses HED's independent Buff setting.
assert(D.is_gameplay_enabled())
local function queue(e,count,offset)
    local refs={}
    for i=1,count do
        local p=e:request_proc_event_param_table(); assert(p,"Unexpected drop at "..i)
        p.sequence=(offset or 0)+i; e:add_proc_event("hit",p); refs[i]=p
    end
    return refs
end
local function extension(capacity,preallocate,client,initial_count)
    if capacity then D:set("buff_proc_capacity",capacity); D.reset_buff_proc_capacity() end
    local e=setmetatable({},{__index=NativeProc})
    e.add_internally_controlled_buff=function(self) queue(self,initial_count or 0) end
    e:init({is_server=not client,network_event_delegate={register_session_unit_events=function() end,
        unregister_unit_events=function() end}}, {}, {player={},initial_buffs=initial_count and {"test"}},nil,nil,preallocate)
    e._buffs[1]={is_predicted=function() return false end,force_predicted_proc=function() return false end,
        skip_send_active_time_rpc=function() return false end,update_proc_events=function() return false end}
    return e
end
local native=extension(300)
queue(native,300); assert(native:request_proc_event_param_table()==nil and native._hed_proc_pool==nil)
native:_update_proc_events(0); assert(native._num_params_table_in_use==0 and native_warnings==1)
-- The cap is established before native init adds any initial Buffs.
local initial=extension(600,true,false,301)
assert(initial._hed_proc_pool.capacity==600 and initial._num_params_table_in_use==301)
initial:_update_proc_events(0); assert(initial._num_params_table_in_use==0)
for _,capacity in ipairs({600,750,1500,2400,3000}) do
    for _,preallocate in ipairs({false,true}) do
        local e=extension(capacity,preallocate)
        assert(e._hed_proc_pool.capacity==capacity and e._hed_proc_pool.peak==0)
        for cycle=1,3 do
            local count=cycle==1 and 100 or capacity
            local refs,seen=queue(e,count),{}
            for i,p in ipairs(refs) do assert(not seen[p] and p.sequence==i); seen[p]=true end
            if count==capacity then
                for j=1,715 do assert(e:request_proc_event_param_table()==nil) end
                assert(e._hed_proc_pool.capacity==capacity and e._num_params_table_in_use==capacity)
            end
            local consumed=0
            e._buffs[1].update_proc_events=function(_,t,events,n)
                for i=1,n do assert(events[i*2]==refs[i] and events[i*2].sequence==i); consumed=consumed+1 end
                return false
            end
            e:_update_proc_events(0)
            assert(consumed==count and e._num_params_table_in_use==0 and e._num_proc_events==0)
            for _,p in ipairs(refs) do assert(next(p)==nil) end
        end
        assert(e._hed_proc_pool.dropped==1430 and e._hed_proc_pool.capacity==capacity)
        e:destroy()
    end
end
assert(native_warnings==1,"Expanded pools reject directly without native overflow warnings")
-- Nested events must not overwrite the currently dispatched batch, even at capacity.
local e=extension(750,true)
queue(e,100); e:_update_proc_events(0)
local initial_refs=queue(e,250)
local nested_refs,injected,observed=nil,false,0
e._buffs[1].update_proc_events=function(_,t,events,n)
    if not injected then
        injected=true; nested_refs=queue(e,500,250)
        assert(e:request_proc_event_param_table()==nil and e._hed_proc_pool.capacity==750)
        for i=1,n do assert(events[2*i]==initial_refs[i] and initial_refs[i].sequence==i) end
    end
    return false
end
local observer=table.clone(e._buffs[1])
observer.update_proc_events=function(_,t,events,n)
    for i=1,n do assert(events[2*i].sequence==observed+i) end
    observed=observed+n; return false
end
e._buffs[2]=observer
e:_update_proc_events(1)
assert(e._num_params_table_in_use==500 and e._num_proc_events==500)
for _,p in ipairs(initial_refs) do assert(next(p)==nil) end
for i,p in ipairs(nested_refs) do assert(p.sequence==250+i) end
e:_update_proc_events(2); assert(observed==750 and e._num_params_table_in_use==0)
-- Manual edits apply to the next mission; later units share this mission's fixed cap.
D:set("buff_proc_capacity",1500)
local same_mission=extension(); assert(same_mission._hed_proc_pool.capacity==750)
assert(e._hed_proc_pool.capacity==750)
D.on_game_state_changed("exit","GameplayStateRun")
D.on_game_state_changed("enter","GameplayStateRun")
local next_mission=extension(); assert(next_mission._hed_proc_pool.capacity==1500)
B.has_local_gameplay_authority=function() return false end
queue(e,750); e._buffs={}; e:_update_proc_events(3)
assert(e._num_params_table_in_use==0 and e._hed_proc_pool.capacity==750)
local remote=extension(); queue(remote,300)
assert(remote:request_proc_event_param_table()==nil and remote._hed_proc_pool==nil)
B.has_local_gameplay_authority=function() return true end
local client=extension(nil,false,true); queue(client,300)
assert(client:request_proc_event_param_table()==nil and client._hed_proc_pool==nil)
local old_enabled=D.is_gameplay_enabled
D.is_gameplay_enabled=function() return false end
local disabled=extension(); queue(disabled,300)
assert(disabled:request_proc_event_param_table()==nil and disabled._hed_proc_pool==nil)
D.is_gameplay_enabled=old_enabled
-- Workload logging is sampled and overflow is aggregated.
local logs={}; D.info=function(_,fmt,...) logs[#logs+1]=string.format(fmt,...) end
local sampled=extension(600)
queue(sampled,330); sampled:_update_proc_events(time)
assert(#logs==2 and logs[2]:find("hit=330",1,true))
time=101; queue(sampled,330); sampled:_update_proc_events(time); assert(#logs==2)
time=130; queue(sampled,1); sampled:_update_proc_events(time); assert(#logs==4)
local before=#warnings; time=160; queue(sampled,600)
for i=1,10 do assert(sampled:request_proc_event_param_table()==nil) end
sampled:_update_proc_events(time); assert(#warnings==before+1)
D.info=old_info; B.values=old_bvalues; D.save_config(old_config); D.values=old_dvalues
B.has_local_gameplay_authority=old_authority; D.is_active=old_active
mods.SoloPlay.has_local_gameplay_authority=old_solo_authority
Managers.state=old_state; Managers.time=old_time; Log=old_log; GameParameters=old_params
D.reset_buff_proc_capacity()
''')
print('HED Buff setting: native 300 default, manual 300-3000 range, multiplier/reset independence, fixed mission cap in native spawn mode: PASS')
print('Native Buff init/dispatch: 600/750/1500/2400/3000 boundaries, overflow rejection, wrapped and nested event identity/order/reuse, remote/client pass-through, sampled diagnostics: PASS')
