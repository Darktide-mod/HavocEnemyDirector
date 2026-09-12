"""Formal source and stripped payload contain no retired diagnostic/generator code."""
import sys,re,json
from pathlib import Path
from project_env import PROJECT
from lupa.luajit21 import LuaRuntime
sys.path.insert(0,str(PROJECT/'tools'))
from strip_debug import payloads
from release import collect_sources
files={p.relative_to(PROJECT/'src').as_posix():p.read_bytes() for p in (PROJECT/'src').rglob('*') if p.is_file()}
normal=payloads(files); clean=payloads(files,True)
assert set(normal)==set(clean), "Formal source already excludes diagnostic modules"
retired={"performance_stats.lua","comparison_debug.lua","capacity_stats.lua","reference_conditions.lua","auric_conditions.lua","native_spawn.lua","native_scaling.lua","spawn_queue.lua","planner.lua","runtime.lua","buff_capacity.lua","population.lua","native_specials.lua"}
for name in clean: assert Path(name).name not in retired,name
lua=LuaRuntime(unpack_returned_tuples=True)
compile_lua=lua.eval('function(s,n) local f,e=loadstring(s,n);return f~=nil,e end')
for name,data in clean.items():
    if not name.endswith(('.lua','.mod')): continue
    text=data.decode('utf-8-sig');ok,error=compile_lua(text,name);assert ok,(name,error)
    for token in ('PERF_DEBUG','performance_debug','comparison_debug','ComparePerf','Perf.','capacity_stats','spawn_generation_mode','buff_capacity'):
        assert token not in text,(name,token)
    for target in re.findall(r'io_dofile\(\s*"([^"]+)"',text):
        if target.split('/')[0]==PROJECT.name: assert target+'.lua' in clean,(name,target)
config,version,documents,built=collect_sources()
assert config['file_category']=='Main Files' and config['diagnostics_stripped']
assert config['release_id']==version and '-test.' not in version
assert built==clean and not documents['changelog.en.txt'].startswith('Packaging variant:')
assert 'comparison_debug_build' not in json.loads(clean[PROJECT.name+'/info.json'])
print('Formal source and payload: no retired modules or diagnostics; all Lua compiles, imports resolve, Main Files metadata and changelog are consistent: PASS')
