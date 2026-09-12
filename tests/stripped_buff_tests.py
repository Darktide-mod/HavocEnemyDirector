"""Execute real native Buff dispatch with the completely stripped allocator."""
import sys
from project_env import PROJECT,GAME
from lupa.luajit21 import LuaRuntime
sys.path.insert(0,str(PROJECT/'tools'))
from strip_debug import strip_lua
L=LuaRuntime(unpack_returned_tuples=True)
L.execute('''
function table.clear(t) for k in pairs(t) do t[k]=nil end end
table.clear_array=table.clear
Script={new_map=function() return {} end,new_array=function() return {} end}
GameParameters={};native_warnings=0
Log={warning=function() native_warnings=native_warnings+1 end}
Managers={state={extension={system=function() return {} end},game_session={fixed_time_step=1/60}},
 time={time=function() error("Stripped allocator read a diagnostic clock") end}}
D={cap=750};B={};hooks={}
function get_mod(name) return name=="HavocEnemyDirector" and D or B end
function D:get() return self.cap end
function D:set(_,v) self.cap=v end
D.planner={number=function(v,default,low,high) return math.max(low,math.min(high,v or default)) end}
function D.is_gameplay_enabled() return D.active~=false end
function B.has_local_gameplay_authority() return B.authority~=false end
function D:info() error("Stripped allocator logged diagnostics") end
D.warning=D.info
function require() return {max_proc_events=300} end
function D:hook_require(_,fn) self.install=fn end
function D:hook(object,name,fn)
 hooks[#hooks+1]=name
 local previous=object[name];object[name]=function(...) return fn(previous,...) end
end
function D:hook_safe() error("Stripped allocator retained a diagnostic destroy hook") end
''')
source=(GAME/'scripts/extension_systems/buff/buff_extension_base.lua').read_text(encoding='utf-8-sig')
prefix='''local MAX_PROC_EVENTS=300;local PROC_EVENTS_STRIDE=2;local MIN_PROC_EVENTS_SIZE=0
local PortableRandom={new=function() return {} end};local _stat_buff_lazy_mt={};local RPCS={}
local FixedFrame={get_latest_fixed_time=function() return 0 end}'''
methods={}
for name in ['init','destroy','request_proc_event_param_table','add_proc_event','_update_proc_events','_clear_param_tables']:
    body=source.split('BuffExtensionBase.'+name+' = function',1)[1].split('\nend',1)[0]
    methods[name]=L.execute(prefix+'\nreturn function'+body+'\nend')
L.globals().Native=L.table_from(methods)
path=PROJECT/'src/HavocEnemyDirector/scripts/mods/HavocEnemyDirector/buff_capacity.lua'
L.execute(strip_lua(path.read_text(encoding='utf-8-sig')))
L.execute('''
D.install(Native);assert(#hooks==3)
local function queue(e,n,offset)
 local refs={}
 for i=1,n do local p=e:request_proc_event_param_table();assert(p);p.sequence=(offset or 0)+i;e:add_proc_event("hit",p);refs[i]=p end
 return refs
end
local function ext(capacity,client,initial)
 D.cap=capacity;D.reset_buff_proc_capacity()
 local e=setmetatable({},{__index=Native})
 e.add_internally_controlled_buff=function(self) queue(self,initial or 0) end
 e:init({is_server=not client,network_event_delegate={register_session_unit_events=function() end,unregister_unit_events=function() end}}, {},
 {player={},initial_buffs=initial and {"initial"}},nil,nil,true)
 e._buffs[1]={is_predicted=function() return false end,force_predicted_proc=function() return false end,
 skip_send_active_time_rpc=function() return false end,update_proc_events=function() return false end}
 return e
end
for _,cap in ipairs({300,600,750,1500,2400,3000}) do
 local e=ext(cap)
 if cap==300 then assert(e._hed_proc_pool==nil)
 else for key in pairs(e._hed_proc_pool) do assert(key=="capacity","Diagnostic field survived stripping") end end
 for cycle=1,4 do
  local n=cycle==1 and 97 or cap;local refs=queue(e,n);local received=0
  e._buffs[1].update_proc_events=function(_,t,events,count)
   for i=1,count do assert(events[i*2]==refs[i] and refs[i].sequence==i);received=received+1 end
   return false
  end
  if n==cap then assert(e:request_proc_event_param_table()==nil) end
  e:_update_proc_events(cycle);assert(received==n and e._num_params_table_in_use==0)
  for _,p in ipairs(refs) do assert(next(p)==nil) end
 end
 e:destroy()
end
local initial=ext(600,false,301);assert(initial._num_params_table_in_use==301);initial:_update_proc_events(0)
local e=ext(750);queue(e,100);e:_update_proc_events(0)
local first=queue(e,250);local second,observed,injected=nil,0,false
e._buffs[1].update_proc_events=function(_,t,events,n)
 if not injected then injected=true;second=queue(e,500,250);assert(e:request_proc_event_param_table()==nil) end
 for i=1,n do observed=observed+1;assert(events[2*i].sequence==observed) end
 return false
end
e:_update_proc_events(1);assert(e._num_params_table_in_use==500)
for _,p in ipairs(first) do assert(next(p)==nil) end
for i,p in ipairs(second) do assert(p.sequence==250+i) end
e:_update_proc_events(2);assert(observed==750 and e._num_params_table_in_use==0)
for _,kind in ipairs({"remote","disabled","client"}) do
 B.authority=kind~="remote";D.active=kind~="disabled"
 local other=ext(750,kind=="client");assert(other._hed_proc_pool==nil)
 queue(other,300);assert(other:request_proc_event_param_table()==nil)
end
''')
print('Fully stripped real Buff dispatch: no diagnostic fields/clocks/logs/destroy hook; fixed capacities, overflow, exact event identity/order, wrap, nested events, native init and pass-through: PASS')
