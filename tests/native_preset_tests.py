"""Validate native presets using real Windows Unicode and atomic file operations."""
from pathlib import Path
import sys,os,tempfile,shutil,json
HED_PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HED_PROJECT.parent/"HavocConditionManager/tests"))
from native_harness import *

def plain(value):
    if hasattr(value,"items"):
        items=dict(value.items())
        if items and all(isinstance(k,int) for k in items) and set(items)==set(range(1,len(items)+1)):
            return [plain(items[k]) for k in range(1,len(items)+1)]
        return {k:plain(v) for k,v in items.items()}
    return value
L.globals().json_encode=lambda v:json.dumps(plain(v),ensure_ascii=False,allow_nan=False,sort_keys=True)
L.globals().json_decode=lambda s:tbl(json.loads(s,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v))))
L.globals().native_test_ffi=L.eval("package.loaded.ffi or package.preload.ffi()")
L.execute('new_test_mod("HavocEnemyDirector"); Mods={lua={ffi=native_test_ffi}}; cjson={encode=json_encode,decode=json_decode}; mods.SoloPlay.has_local_gameplay_authority=function() return host end')
D=L.globals().mods.HavocEnemyDirector
D.localization=load_mod("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/HavocEnemyDirector_localization")
load_mod("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/HavocEnemyDirector")
test_parent=(HED_PROJECT/"build/native-template-tests").resolve()
test_parent.mkdir(parents=True,exist_ok=True)
test_appdata=Path(tempfile.mkdtemp(prefix="unicode-",dir=test_parent)).resolve()
(test_appdata/"Fatshark/Darktide").mkdir(parents=True)
previous_appdata=os.environ.get("APPDATA")
os.environ["APPDATA"]=str(test_appdata)
try:
    L.execute("""
local D=mods.HavocEnemyDirector
local P,C=D.presets,D.presets.codec
local id="specials/default_specials/1"
assert(D.set_patch(id,"max_alive_specials",8))
assert(D.set_rule(id,"encounter",{mode="append",match="all",clauses={{condition="load_max",value=42},{condition="monster_idle"}}}))
B:set("native_configuration_v3",S.coarse_config({special_slots=1.75,event_budget=1.5}))
local cfg=D.get_config(); cfg.seed=987654321; cfg.seed_enabled=true; assert(D.save_config(cfg))
B:set('diy_seed_v1',{enabled=false,value=2147483646})
local doc=assert(P.capture("欧格林 測試 01"))
assert(doc.condition_seed.enabled==false and doc.condition_seed.value==2147483646)
local seeds=S.copy(doc);seeds.condition_seed.enabled=true
assert(P.apply(seeds) and B:get('diy_seed_v1').enabled)
assert(P.apply(doc) and not B:get('diy_seed_v1').enabled and B:get('diy_seed_v1').value==2147483646)
local old_without_seeds=S.copy(doc);old_without_seeds.version=3;old_without_seeds.condition_seed=nil
B:set('diy_seed_v1',{enabled=true,value=42})
assert(P.apply(old_without_seeds) and B:get('diy_seed_v1').value==42,'older preset preserves current condition seed')
assert(P.apply(doc))
local legacy=S.copy(doc);legacy.version=2
legacy.config={version=2,patches=S.copy(doc.config.patches),rules=S.copy(doc.config.rules),seed=doc.config.seed}
local migrated=assert(C.validate(legacy))
assert(migrated.version==4 and migrated.config.version==3 and #migrated.config.formations==0 and not migrated.config.director.enabled)
assert(legacy.version==2 and legacy.config.version==2)
assert(doc.config.seed==987654321 and doc.coarse.special_slots==1.75 and not doc.context)
local file=assert(P.save_document(doc,doc.name))
assert(file=="欧格林 測試 01.json")
local loaded=assert(P.read(file))
assert(json_encode(loaded)==json_encode(doc))
local imported=assert(P.decode(assert(P.export(file))))
assert(json_encode(imported)==json_encode(doc))
assert(#P.list()==1)
local saved,err=P.save_document(doc,doc.name); assert(not saved and err=="template_exists")
local next_doc=S.copy(doc); next_doc.config.patches[id].max_alive_specials=9
assert(P.save_document(next_doc,next_doc.name,true))
assert(P.read(file).config.patches[id].max_alive_specials==9)
-- Lock the existing file against replacement. Failure retains complete content.
local ffi=native_test_ffi; local win=ffi.load("kernel32")
local path=assert(P.directory()).."/"..file
local n=win.MultiByteToWideChar(65001,8,path,#path,nil,0)
local wide=ffi.new("unsigned short[?]",n+1); win.MultiByteToWideChar(65001,8,path,#path,wide,n)
local handle=win.CreateFileW(wide,2147483648,1,nil,3,128,nil)
assert(handle~=ffi.cast("void*",-1))
saved=P.save_document(doc,doc.name,true); win.CloseHandle(handle)
assert(not saved and P.read(file).config.patches[id].max_alive_specials==9)
local Files=D:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/preset_files")
local fs=assert(Files.new(ffi)); assert(fs.write("broken.json","{broken",false))
local good,bad=0,0
for _,entry in ipairs(P.list()) do if entry.document then good=good+1 else bad=bad+1 end end
assert(good==1 and bad==1)
for _,name in ipairs({"","../evil","a/b","CON","NUL.txt","LPT1","tail.",string.rep("x",65)}) do assert(not C.name(name)) end
assert(C.name("中文 範本 α") and C.name("LPT10") and C.name(".template"))
assert(not P.read("../bad.json") and not P.delete("../bad.json"))
for _,text in ipairs({"return os.execute('bad')","null","[]","{}","{bad",string.rep("x",262145)}) do assert(not P.decode(text)) end
local old,why=C.validate({format=C.format,version=1,name="Legacy",context={},config={}})
assert(not old and why=="template_version")
local function reject(change)
    local copy=S.copy(doc); change(copy); assert(not C.validate(copy))
end
reject(function(x) x.callback="return true" end)
reject(function(x) x.config.seed=0 end)
reject(function(x) x.config.seed=math.huge end)
reject(function(x) x.config.seed=1.5 end)
reject(function(x) x.coarse.special_slots=11 end)
reject(function(x) x.config.patches[id].max_alive_specials=0 end)
reject(function(x) x.config.patches[id].max_alive_specials=0/0 end)
reject(function(x) x.config.patches[id].bad_field=10 end)
reject(function(x) x.config.patches.no_such_template={} end)
reject(function(x) x.config.rules[id].encounter.mode="replace" end)
reject(function(x) x.config.rules[id].encounter.clauses[1].condition="lua" end)
reject(function(x) x.config.rules[id].encounter.clauses[1].value="42" end)
reject(function(x) x.config.rules[id].encounter.clauses[1].callback="return true" end)
-- New HCM ceilings are shared by the unchanged HED codec and file round-trip.
local extreme=S.copy(doc); extreme.name="10x boundary"
for _,d in ipairs(S.coarse) do
    assert(d.max==10); extreme.coarse[d.id]=10
    reject(function(x) x.coarse[d.id]=d.max+0.25 end)
end
local extreme_file=assert(P.save_document(extreme,extreme.name))
local extreme_loaded=assert(P.read(extreme_file)); assert(P.apply(extreme_loaded))
for _,d in ipairs(S.coarse) do assert(B:get("native_configuration_v3")[d.id]==10) end
assert(P.apply(doc)); assert(P.delete(extreme_file))
-- Applying and repeatedly loading keep exact patch IDs, values and rule data.
mods.SoloPlay:set("hcm_condition_selection_v3","unchanged-native-selection")
Managers.state.game_session={}; E.reset()
local root=A.by_id[id].root
local frozen=E.prepare(root,"specials")
assert(frozen.max_alive_specials==8)
assert(P.apply(next_doc)); assert(P.apply(next_doc))
assert(D.peek_config().patches[id].max_alive_specials==9 and D.peek_config().seed==987654321)
assert(mods.SoloPlay:get("hcm_condition_selection_v3")=="unchanged-native-selection")
assert(E.prepare(root,"specials")==frozen and frozen.max_alive_specials==8)
Managers.state.game_session={}
assert(E.prepare(root,"specials").max_alive_specials==9)
-- A failed assignment restores both saved configurations.
local before=json_encode(D.get_config()); local coarse_before=json_encode(B:get("native_configuration_v3"))
local save=D.save_config; local fail=true
D.save_config=function(v) if fail then fail=false; error("injected persistence failure") end; return save(v) end
assert(not P.apply(doc))
D.save_config=save
assert(json_encode(D.get_config())==before and json_encode(B:get("native_configuration_v3"))==coarse_before)
assert(P.delete(file)); assert(not P.read(file))
""")
finally:
    if previous_appdata is None: os.environ.pop("APPDATA",None)
    else: os.environ["APPDATA"]=previous_appdata
    assert test_appdata.is_relative_to(test_parent) and test_parent.is_relative_to(HED_PROJECT.resolve()/"build")
    shutil.rmtree(test_appdata)
print("Native presets: real Unicode paths, atomic overwrite failure, JSON round-trip, legacy rejection, strict validation, rollback and mission isolation: PASS")

