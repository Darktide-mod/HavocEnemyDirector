"""Compile only this mod and validate its declared local imports."""
from project_env import PROJECT, SOURCES
from lupa.luajit21 import LuaRuntime
import re
lua=LuaRuntime(unpack_returned_tuples=True)
compile_lua=lua.eval('function(s,n) local f,e=loadstring(s,n); return f~=nil,e end')
files=[p for p in (PROJECT/'src').rglob('*') if p.suffix in ('.lua','.mod')]
for path in files:
    text=path.read_text(encoding='utf-8-sig')
    ok,error=compile_lua(text,str(path))
    assert ok,(path,error)
    for target in re.findall(r'io_dofile\(\s*"([^"]+)"',text):
        if target.split('/')[0]==PROJECT.name:
            assert (SOURCES/(target+'.lua')).is_file(),(path,target)
print(f'{PROJECT.name}: {len(files)} Lua/mod files; syntax and local imports: PASS')
