"""Real Windows Unicode files, schema validation, atomic load and native text controls."""
import os, tempfile, shutil

def json_plain(value):
    if hasattr(value,'items'):
        items=dict(value.items())
        if items and all(isinstance(k,int) and not isinstance(k,bool) for k in items) and set(items)==set(range(1,len(items)+1)):
            return [json_plain(items[k]) for k in range(1,len(items)+1)]
        return {k:json_plain(v) for k,v in items.items()}
    return value
def encode_json(v):return json.dumps(json_plain(v),ensure_ascii=False,allow_nan=False,sort_keys=True)
def decode_json(s):return tbl(json.loads(s,parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v))))
L.globals().json_encode=encode_json; L.globals().json_decode=decode_json
L.globals().native_test_ffi=L.eval('package.loaded.ffi or package.preload.ffi()')
old_appdata=os.environ.get('APPDATA')
test_parent=(PROJECT/'build/template-tests').resolve();test_parent.mkdir(exist_ok=True)
test_appdata=Path(tempfile.mkdtemp(prefix='unicode-',dir=test_parent)).resolve()
(test_appdata/'Fatshark/Darktide').mkdir(parents=True)
os.environ['APPDATA']=str(test_appdata)
try:
    L.execute('''
old_mods_globals=Mods
local old_log_info=Log.info;Log.info=function() end
Mods={lua={ffi=native_test_ffi}}
cjson={encode=json_encode,decode=json_decode}
local W=require("scripts/managers/ui/ui_widget")
W.init=function(name,definition) return definition end
W.draw=function(w,r) test_drawn_template_field=w end
local D,B=mods.HavocEnemyDirector,mods.HavocConditionManager
local A,P=D.presets,D.planner
saved_template_cfg=D.get_config()
saved_template_conditions=B:get("havoc_circumstances_serialized")
saved_template_environment=mods.SoloPlay:get("havoc_theme_circumstance")
saved_template_faction=mods.SoloPlay:get("havoc_faction")
saved_template_scaling=D.get_spawn_scaling()
-- Match SoloPlay's native faction order in the fixture.
saved_template_faction_order=test_settings.order.havoc_factions
test_settings.order.havoc_factions={"mixed","renegade","cultist"}
mods.SoloPlay:set("havoc_faction","renegade"); mods.SoloPlay:set("havoc_theme_circumstance","default")
B:set("havoc_circumstances_serialized","hcm_auric_hounds")
for _,cat in ipairs(P.categories) do B:set("spawn_multiplier_"..cat,5); B:set("spawn_mode_"..cat,"mixed") end
local cfg=P.defaults(); cfg.total_cap=600; cfg.custom={{id="custom_1",kind="timer",category="common",pool={chaos_poxwalker=1}}}
cfg.generators.custom_1={count=13,interval=27.5,cap=66,pool={chaos_poxwalker=0,chaos_newly_infected=3}}
cfg.generators.timer_common={deleted=true}; cfg.generators.scripted_encounters={deleted=true}
cfg.banned.renegade_netgunner=true; cfg.native_extras_enabled=false; cfg.havoc_twins_enabled=false
-- Rule-derived IDs from the reported live setup contain decimal cooldowns.
-- Generate them through the production planner rather than a simplified fixture ID.
local rule_sources={
 {id="native_trickles",kind="travel",interval=30,distance=80,pool={chaos_poxwalker=1,renegade_executor=1},
  rules={active_limit=4,cooldown=27.5}},
 {id="armor_reinforcement",kind="travel",interval=60,distance=100,pool={renegade_executor=1},
  rules={min_players=2,active_limit=2,cooldown=42.5,pause={hordes=40,specials=50,trickle_hordes=40}}},
}
for _,source in ipairs(rule_sources) do source.profile=P.rules_key(source.rules) end
local rule_ids={}
for _,g in ipairs(P.compile(rule_sources,P.defaults(),D.breeds,D.category_for)) do
 rule_ids[g.id]=true
 cfg.generators[g.id]={count=7,interval=27.5,distance=80,cap=g.cap,pool=P.copy(g.pool)}
end
assert(rule_ids["travel_common_rules_0_0_4_27.5_0_0_0_0_0"])
assert(rule_ids["travel_elite_rules_0_0_4_27.5_0_0_0_0_0"])
assert(rule_ids["travel_elite_rules_2_0_2_42.5_40_0_50_0_40"])
D.save_config(cfg)
template_doc=assert(A.capture("欧格林 测试 01"))
local filename=assert(A.save_document(template_doc,template_doc.name))
assert(filename=="欧格林 测试 01.json")
local doc=assert(A.read(filename))
for id in pairs(rule_ids) do assert(json_encode(doc.config.generators[id])==json_encode(cfg.generators[id]),id) end
local shared=assert(A.decode(assert(A.export(filename))))
for id in pairs(rule_ids) do assert(json_encode(shared.config.generators[id])==json_encode(cfg.generators[id]),id) end
assert(doc.config.custom[1].id=="custom_1" and doc.config.generators.custom_1.interval==27.5)
assert(doc.config.generators.timer_common.deleted and doc.config.banned.renegade_netgunner)
assert(doc.context.scaling.common.multiplier==5 and doc.context.scaling.common.mode=="mixed")
assert(#A.list()==1 and A.list()[1].name==template_doc.name)
local _,why=A.save_document(template_doc,template_doc.name); assert(why=="template_exists")
local updated=P.copy(template_doc); updated.config.total_cap=510
assert(A.save_document(updated,updated.name,true)); assert(A.read(filename).config.total_cap==510)
assert(A.save_document(template_doc,template_doc.name,true))
-- A failed Windows replacement must retain the previous complete file.
local ffi=native_test_ffi; local win=ffi.load("kernel32")
local path=assert(A.directory()).."/"..filename
local len=win.HED_TEMPLATE_IO_MultiByteToWideChar(65001,8,path,#path,nil,0)
local wide=ffi.new("unsigned short[?]",len+1);win.HED_TEMPLATE_IO_MultiByteToWideChar(65001,8,path,#path,wide,len)
local lock=win.HED_TEMPLATE_IO_CreateFileW(wide,2147483648,1,nil,3,128,nil)
assert(lock~=ffi.cast("void*",-1))
local saved=A.save_document(updated,updated.name,true)
win.HED_TEMPLATE_IO_CloseHandle(lock)
assert(not saved and A.read(filename).config.total_cap==600)
local Files=D:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/preset_files")
local fs=assert(Files.new(ffi)); assert(fs.write("broken.json","{broken",false))
local entries=assert(A.list());local good,bad=0,0
for _,e in ipairs(entries) do if e.document then good=good+1 else bad=bad+1 end end
assert(good==1 and bad==1,"one broken file must not prevent loading valid templates")
assert(not A.read("../bad.json") and not A.read("C:\\bad.json") and not A.delete("../bad.json"))
for _,name in ipairs({"", "../evil", "a/b", "CON", "NUL.txt", "LPT1", "tail.",string.rep("x",65)}) do assert(not A.codec.name(name),name) end
assert(A.codec.name("中文 範本 α") and A.codec.name("LPT10") and A.codec.name(".template"))
mods.SoloPlay:set("havoc_faction",nil)
assert(A.capture("Default faction").context.faction=="mixed")
mods.SoloPlay:set("havoc_faction","renegade")
for _,text in ipairs({"return os.execute('bad')","null","[]","{}","{bad",string.rep("x",262145)}) do assert(not A.decode(text)) end
local function rejects(fn)
 local d=P.copy(template_doc);fn(d);assert(not A.codec.validate(d,P,D.breeds))
end
rejects(function(d) d.version=99 end)
rejects(function(d) d.config.total_cap=601 end)
rejects(function(d) d.config.generators.custom_1.count="13" end)
rejects(function(d) d.config.custom[2]=P.copy(d.config.custom[1]) end)
rejects(function(d) d.config.custom[1].category="invalid" end)
rejects(function(d) d.config.banned.not_a_real_unit=true end)
rejects(function(d) d.config.generators.custom_1.pool.not_a_real_unit=1 end)
rejects(function(d) d.context.scaling.common.multiplier=6 end)
rejects(function(d) d.config.custom[1].pool.chaos_poxwalker=0/0 end)
rejects(function(d) d.config.custom[1].pool.chaos_poxwalker=math.huge end)
rejects(function(d) d.config.custom[1].callback="return true" end)
for _,id in ipairs({"bad/id","bad\\\\id","bad:id","bad id"}) do
 rejects(function(d) d.config.generators[id]={cap=1} end)
end
rejects(function(d) d.config.custom[1].id="custom_1.5" end)
rejects(function(d) d.context.conditions={"condition.with.dot"} end)
-- Lua tostring may also use exponent signs in rule profiles.
for _,cooldown in ipairs({0.0000001,1e20}) do
 local d=P.copy(template_doc)
 d.config.generators["travel_common_"..P.rules_key({cooldown=cooldown})]={cap=120}
 assert(A.codec.validate(d,P,D.breeds))
end
-- Set callbacks behave as DMF does; loading must suspend midpoint rebuilds.
local original_set=B.set
B.set=function(self,key,v) original_set(self,key,v); B.on_setting_changed(key) end
D.save_config(P.defaults()); B:set("havoc_circumstances_serialized","")
for _,cat in ipairs(P.categories) do B:set("spawn_multiplier_"..cat,1) end
D:set("buff_proc_capacity",750)
for i=1,3 do
 assert(A.apply(template_doc,test_view))
 assert(D:get("buff_proc_capacity")==750,"Template loading must preserve the separate Buff cap even when multipliers change")
 assert(not D.synchronize_conditions(),"load must survive the next condition sync")
 local got=D.get_config()
 assert(got.total_cap==600 and got.custom[1].id=="custom_1" and got.generators.custom_1.count==13)
 assert(got.generators.custom_1.interval==27.5 and got.generators.custom_1.cap==66)
 assert(D.get_spawn_scaling().common.multiplier==5 and not got.native_extras_enabled and not got.havoc_twins_enabled)
 for id in pairs(rule_ids) do assert(json_encode(got.generators[id])==json_encode(cfg.generators[id]),id) end
 for _,g in ipairs(P.compile(rule_sources,got,D.breeds,D.category_for)) do
  if rule_ids[g.id] then assert(g.count==7 and g.interval==27.5 and g.distance==80,"loaded override must still match its original ID") end
 end
end
local before=json_encode(D.get_config())
local incompatible=P.copy(template_doc); incompatible.context.conditions={"missing_condition"}
assert(not A.apply(incompatible)); assert(json_encode(D.get_config())==before)
local fail_once=true
B.set=function(self,key,v)
 if key=="spawn_mode_special" and fail_once then fail_once=false;error("simulated settings failure") end
 original_set(self,key,v);B.on_setting_changed(key)
end
local failed_doc=P.copy(template_doc); failed_doc.config.total_cap=330
failed_doc.context.scaling.elite.multiplier=1; failed_doc.context.scaling.special.multiplier=1
assert(not A.apply(failed_doc));assert(D.get_config().total_cap==600 and not D._loading_template)
assert(D:get("buff_proc_capacity")==750,"Failed template load must retain the previous manual Buff cap")
B.set=function(self,key,v) original_set(self,key,v); B.on_setting_changed(key) end
incompatible=P.copy(template_doc); incompatible.context.environment="missing_environment"
assert(not A.apply(incompatible)); assert(json_encode(D.get_config())==before)
-- Existing mission snapshots are never reset by importing another saved setup.
local old_state,old_authority,old_enabled=Managers.state,B.has_local_gameplay_authority,D.is_gameplay_enabled
Managers.state={difficulty={get_parsed_havoc_data=function() return {} end},pacing={_horde_pacing={_template={}},_specials_pacing={_template={}}}}
B.has_local_gameplay_authority=function() return true end;D.is_gameplay_enabled=function() return true end
local native_cfg=D.get_config();native_cfg.enabled=false;D.save_config(native_cfg)
D.reset_runtime();D.update_director(0); local live=D.get_session_config(); local previous_cap=live.total_cap
assert(A.apply(updated)); assert(D.get_session_config()==live and live.total_cap==previous_cap)
D.reset_runtime()
Managers.state=old_state; B.has_local_gameplay_authority=old_authority;D.is_gameplay_enabled=old_enabled
B.set=original_set
test_view._hcm_page=4; test_view._hcm_choice=nil; test_view._hcm_number=nil
Paging.refresh(test_view,test_settings); click_control("template_library")
assert(test_view._hed_templates_open and find_control("template_save") and test_view._hed_name_widget)
-- Library and independent native name field share the fitted canvas and input transform.
local function template_geometry()
local rectangles={}
for _,item in ipairs(test_view._hcm_ui.items) do rectangles[#rectangles+1]=item end
local w=test_view._hed_name_widget
assert(w.scenegraph_id=="hcm_layout")
rectangles[#rectangles+1]={key="native_name",x=w.offset[1],y=w.offset[2],w=1140,h=50,action=not w.content.hotspot.disabled}
for _,r in ipairs({{1280,720},{1920,1080},{2560,1440},{3840,2160},{1920,1200},{2560,1600},
    {2560,1080},{3440,1440},{1280,960},{1600,1200},{5120,1440}}) do
 local vp=Paging.viewport(r[1],r[2])
 for i,a in ipairs(rectangles) do
  local x,y=(a.x+vp.x)*vp.scale,(a.y+vp.y)*vp.scale
  assert(x>=0 and y>=0 and x+a.w*vp.scale<=r[1]+0.01 and y+a.h*vp.scale<=r[2]+0.01,a.key)
  assert(math.abs((x+a.w*vp.scale/2)/vp.scale-vp.x-(a.x+a.w/2))<1e-6)
  if a.action and not a.blocked then for j=i+1,#rectangles do local b=rectangles[j]
   if b.action and not b.blocked then assert(a.x+a.w<=b.x or b.x+b.w<=a.x or a.y+a.h<=b.y or b.y+b.h<=a.y,a.key.." / "..b.key) end
  end end
 end
end
end
template_geometry()
function template_hook(name)
 for _,h in ipairs(hooks) do if h.owner==D and h.target=="HavocConditionManagerView" and h.name==name then return h.fn end end
 error(name)
end
function template_service(actions) return {get=function(_,k) return actions and actions[k] or false end,is_null_service=function() return false end} end
function template_update(actions) template_hook("_handle_input")(function() end,test_view,template_service(actions)) end
function template_type(text)
 local c=test_view._hed_name_widget.content;c.is_writing=true; template_update()
 c.input_text=text;template_update({confirm_pressed=true})
end
template_type("第二模板"); click_control("template_save")
assert(A.read("第二模板.json") and not test_view._hed_library.pending)
click_control("template_save"); assert(test_view._hed_library.pending.kind=="overwrite")
click_control("template_cancel"); assert(not test_view._hed_library.pending)
click_control("template_load"); assert(test_view._hed_library.pending.kind=="load")
click_control("template_confirm"); assert(not test_view._hed_library.pending)
click_control("template_export"); assert(A.decode(test_clipboard))
click_control("template_import"); assert(test_view._hed_library.pending.kind=="import")
template_type("分享导入"); click_control("template_confirm"); assert(A.read("分享导入.json"))
-- Run the shipped game's text-editing logic, including paste and blur.
local w=test_view._hed_name_widget;local c=w.content
c.is_writing=true;c.input_text="";c.display_text="";c._input_text="";c.caret_position=1;c._caret_position=1
c.selected_text=nil;c._selection_start=nil;c._selection_end=nil
test_keystrokes={"Native Input"}
for _,pass in ipairs(w.passes) do
 if pass.pass_type=="logic" and (not pass.visibility_function or pass.visibility_function(c,w.style)) then
  pass.value(pass,{input_service=template_service(),scale=1},{parent=w.style},c,{0,0,0},{1140,50})
 end
end
test_keystrokes=nil;template_update({left_pressed=true})
assert(c.input_text=="Native Input" and test_view._hed_library.name=="Native Input" and not c.is_writing)
-- Select-all and paste Chinese through the actual native text-input logic.
c.is_writing=true;template_update();test_clipboard="中文粘贴名称"
for _,actions in ipairs({{select_all_text=true},{clipboard_paste=true}}) do
 test_keystrokes={}
 for _,pass in ipairs(w.passes) do
  if pass.pass_type=="logic" and (not pass.visibility_function or pass.visibility_function(c,w.style)) then
   pass.value(pass,{input_service=template_service(actions),scale=1},{parent=w.style},c,{0,0,0},{1140,50})
  end
 end
end
test_keystrokes=nil;template_update({confirm_pressed=true})
assert(c.input_text=="中文粘贴名称" and not c.is_writing)
-- Deletion is modal, names the exact file, and never mutates active settings.
local current_cfg=json_encode(D.get_config());local delete_file=test_view._hed_library.selected
local delete_doc=assert(A.read(delete_file));local stale_save=find_control("template_save").action
click_control("template_delete")
assert(test_view._hcm_ui.popup.key=="template_delete")
assert(find_control("template_delete_name").text==delete_doc.name)
assert(find_control("template_delete_file").text:find(delete_file,1,true))
assert(find_control("tab_1").blocked and find_control("template_save").blocked)
assert(test_view._widgets_by_name.hcm_previous.content.hotspot.disabled and test_view._hed_name_widget.content.hotspot.disabled)
template_geometry();stale_save();assert(not A.read("中文粘贴名称.json"))
template_hook("_on_back_pressed")(function() error("must cancel deletion") end,test_view)
Paging.refresh(test_view,test_settings);assert(A.read(delete_file) and not test_view._hed_library.deleting)
click_control("template_delete");click_control("template_delete_cancel");assert(A.read(delete_file))
click_control("template_delete");local stale_delete=find_control("template_delete_confirm").action
click_control("template_delete_confirm")
assert(not A.read(delete_file) and A.read(filename) and json_encode(D.get_config())==current_cfg)
assert(A.save_document(delete_doc,delete_doc.name));stale_delete();assert(A.read(delete_file))
-- Broken files can also be selected and removed after the same confirmation.
test_view._hed_library.selected="broken.json";Paging.refresh(test_view,test_settings)
click_control("template_delete");assert(find_control("template_delete_name").text=="broken.json")
click_control("template_delete_confirm");assert(not A.read("broken.json") and json_encode(D.get_config())==current_cfg)
template_type("分享导入")
-- Escape restores the edit, then exits the library; stale actions cannot persist.
local c=test_view._hed_name_widget.content;c.is_writing=true;template_update();c.input_text="cancel";template_update()
template_hook("_on_back_pressed")(function() error("must consume back") end,test_view)
assert(test_view._hed_library.name=="分享导入" and not c.is_writing)
local stale=find_control("template_save").action
D.cleanup_template_ui();stale();assert(not test_view._hed_templates_open and not test_view.is_text_input_focused)
for i=1,3 do D.open_template_library(test_view);Paging.refresh(test_view,test_settings);template_hook("on_exit")(test_view);assert(not test_view._hed_name_widget) end
D.open_template_library(test_view);Paging.refresh(test_view,test_settings)
local retained=test_view._hed_library.selected
click_control("template_delete")
local stale=find_control("template_delete_confirm").action
D._enabled=false;stale();D.on_disabled(false)
assert(not test_view._hed_library and not test_view._hed_delete_backdrop and not test_view.is_text_input_focused and A.read(retained))
D._enabled=true;D.on_enabled(false)
D.open_template_library(test_view);Paging.refresh(test_view,test_settings);click_control("template_delete")
D.on_unload();assert(not test_view._hed_library and not test_view._hed_delete_backdrop and A.read(retained))
-- Return to the normal dashboard for the remaining checks/export tools.
Mods=old_mods_globals
Log.info=old_log_info
test_settings.order.havoc_factions=saved_template_faction_order
B:set("havoc_circumstances_serialized",saved_template_conditions)
mods.SoloPlay:set("havoc_theme_circumstance",saved_template_environment)
mods.SoloPlay:set("havoc_faction",saved_template_faction)
for c,f in pairs(saved_template_scaling) do B:set("spawn_multiplier_"..c,f.multiplier);B:set("spawn_mode_"..c,f.mode) end
D.save_config(saved_template_cfg); Paging.refresh(test_view,test_settings)
''')
finally:
    if old_appdata is None:os.environ.pop('APPDATA',None)
    else:os.environ['APPDATA']=old_appdata
    assert test_appdata.is_relative_to(test_parent) and test_appdata!=test_parent
    shutil.rmtree(test_appdata)
print('Templates: native Windows Unicode files and failed replacement; real rule-derived IDs with decimal cooldowns and exponent signs; unchanged IDs/overrides through save, share and repeated load; strict validation; mission isolation; library and modal deletion, exact names/cancel/Escape/stale callbacks; native Chinese paste, focus cleanup and 11 resolutions: PASS')
