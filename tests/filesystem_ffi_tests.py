"""Real Windows file I/O across mod load orders and existing FFI declarations."""
from project_env import PROJECT, CHECKS
from itertools import permutations
from pathlib import Path
import os
import tempfile

from lupa.luajit21 import LuaRuntime

RELATIVE = {
    'HavocConditionManager': 'diy/diy_files.lua',
    'HavocEnemyDirector': 'preset_files.lua',
    'MortisBuffManager': 'modules/diy/diy_files.lua',
}
sources = {}
for name, relative in RELATIVE.items():
    path = PROJECT.parent / name / 'src' / name / 'scripts/mods' / name / relative
    if path.is_file():
        sources[name] = path.read_text(encoding='utf-8-sig')
assert PROJECT.name in sources

foreign = '''
    typedef struct {
        unsigned long flags, times[6], high, low, reserved[2];
        unsigned short filename[260], alternate[14];
    } OTHER_MOD_FIND_DATA;
    void* __stdcall FindFirstFileW(const unsigned short*, OTHER_MOD_FIND_DATA*);
    int __stdcall FindNextFileW(void*, OTHER_MOD_FIND_DATA*);
    int __stdcall FindClose(void*);
    int __stdcall ReadFile(void*,void*,unsigned int,unsigned int*,void*);
    int __stdcall WriteFile(void*,const void*,unsigned int,unsigned int*,void*);
'''
legacy = '''
    typedef struct { unsigned long attributes, times[6], size_high, size_low, reserved[2];
        unsigned short name[260], alternate[14]; } DT_DIY_FIND_DATA;
    typedef struct { unsigned long attributes, times[6], size_high, size_low, reserved[2];
        unsigned short name[260], alternate[14]; } HED_TEMPLATE_FIND_DATA;
'''

exercise = r'''
    local F=assert(assert(loadstring(source))())
    local fs=assert(F.new(ffi,mod_name))
    assert(#assert(fs.list())==0)
    local filename='欧格林 測試.json'
    assert(fs.write(filename,'{"name":"中文"}',false))
    assert(fs.write('second.json','{}',false))
    assert(#assert(fs.list())==2, 'FindNextFileW must work too')
    assert(fs.read(filename)=='{"name":"中文"}')
    assert(not fs.write(filename,'bad',false))
    assert(fs.write(filename,'{"updated":true}',true))
    assert(fs.read(filename)=='{"updated":true}')
    if fs.list_packages then
        local function id(s)return s=='test-package' end
        local function path(s)return s=='package.json' or s=='lua' or s=='lua/main.lua' end
        local files={['package.json']='{}',['lua/main.lua']='return {}'}
        assert(fs.write_package('test-package',files,id,path))
        assert(#assert(fs.list_packages(id))==1)
        assert(fs.read_package('test-package',id,path)['lua/main.lua']=='return {}')
        if mod_name=='HavocConditionManager' then
            files['lua/main.lua']='return {updated=true}'
            assert(fs.write_package('test-package',files,id,path,true))
            assert(fs.read_package('test-package',id,path)['lua/main.lua']==files['lua/main.lua'])
        end
        assert(fs.export_packages({['test-package']={files=files}},id,path))
        assert(fs.retire_package('test-package',id))
        assert(#assert(fs.list_packages(id))==0)
    end
    assert(fs.remove(filename));assert(fs.remove('second.json'))
    assert(#assert(fs.list())==0)
'''

previous = os.environ.get('APPDATA')
count = 0
try:
    with tempfile.TemporaryDirectory(prefix='ffi-中文-', dir=CHECKS) as temporary:
        for declarations in ('', foreign, legacy + foreign):
            for order in permutations(sources):
                directory = Path(temporary) / str(count)
                (directory / 'Fatshark/Darktide').mkdir(parents=True)
                os.environ['APPDATA'] = str(directory)
                lua = LuaRuntime(unpack_returned_tuples=True)
                lua.execute("ffi=require('ffi')")
                if declarations:
                    lua.globals().ffi.cdef(declarations)
                    original = lua.eval("tostring(ffi.typeof(ffi.load('kernel32').FindFirstFileW))")
                # Run twice in one VM: module refresh must work after its own
                # structs (or the older release's structs) already exist.
                for _ in range(2):
                    for name in order:
                        lua.globals().source = sources[name]
                        lua.globals().mod_name = name
                        try:
                            lua.execute(exercise)
                        except Exception as error:
                            raise AssertionError((order, 'existing declarations' if declarations else 'fresh', name, str(error))) from error
                if declarations:
                    assert lua.eval("tostring(ffi.typeof(ffi.load('kernel32').FindFirstFileW))") == original
                    lua.execute(r'''
                        local win=ffi.load('kernel32')
                        local rows=ffi.new('OTHER_MOD_FIND_DATA[1]')
                        local query=ffi.new('unsigned short[2]',{42,0})
                        local handle=win.FindFirstFileW(query,rows)
                        assert(handle~=ffi.cast('void*',-1))
                        win.FindNextFileW(handle,rows);assert(win.FindClose(handle)~=0)
                    ''')
                count += 1
finally:
    if previous is None:
        os.environ.pop('APPDATA', None)
    else:
        os.environ['APPDATA'] = previous

print(f'PASS: {count} load-order/declaration combinations, twice per VM; real Unicode scans, reads, writes, replacement, package backup/export and foreign binding preservation.')
