-- Windows Unicode filesystem access, on explicit library actions only.
-- No shell, extra DLL, Lua evaluation, or polling during gameplay.
local F={}
function F.new(ffi)
    if not ffi then return nil,"template_io_unavailable" end
    if not pcall(ffi.typeof,"HED_TEMPLATE_FIND_DATA") then
        ffi.cdef[[
        typedef struct { unsigned long attributes; unsigned long times[6]; unsigned long size_high, size_low, reserved[2]; unsigned short name[260], alternate[14]; } HED_TEMPLATE_FIND_DATA;
        int __stdcall MultiByteToWideChar(unsigned int,unsigned long,const char*,int,unsigned short*,int);
        int __stdcall WideCharToMultiByte(unsigned int,unsigned long,const unsigned short*,int,char*,int,const char*,int*);
        unsigned long __stdcall GetEnvironmentVariableW(const unsigned short*,unsigned short*,unsigned long);
        int __stdcall CreateDirectoryW(const unsigned short*,void*);
        unsigned long __stdcall GetFileAttributesW(const unsigned short*);
        void* __stdcall FindFirstFileW(const unsigned short*,HED_TEMPLATE_FIND_DATA*);
        int __stdcall FindNextFileW(void*,HED_TEMPLATE_FIND_DATA*);
        int __stdcall FindClose(void*);
        void* __stdcall CreateFileW(const unsigned short*,unsigned long,unsigned long,void*,unsigned long,unsigned long,void*);
        int __stdcall ReadFile(void*,void*,unsigned long,unsigned long*,void*);
        int __stdcall WriteFile(void*,const void*,unsigned long,unsigned long*,void*);
        int __stdcall FlushFileBuffers(void*);
        int __stdcall CloseHandle(void*);
        int __stdcall MoveFileExW(const unsigned short*,const unsigned short*,unsigned long);
        int __stdcall DeleteFileW(const unsigned short*);
        unsigned long __stdcall GetLastError(void);
        ]]
    end
    local win=ffi.load("kernel32")
    local invalid=ffi.cast("void*",-1)
    local function wide(s)
        local n=win.MultiByteToWideChar(65001,8,s,#s,nil,0)
        if n==0 then error("template_name_invalid",0) end
        local out=ffi.new("unsigned short[?]",n+1); win.MultiByteToWideChar(65001,8,s,#s,out,n); return out
    end
    local function utf8(s)
        local n=win.WideCharToMultiByte(65001,0,s,-1,nil,0,nil,nil)
        local out=ffi.new("char[?]",n); win.WideCharToMultiByte(65001,0,s,-1,out,n,nil,nil); return ffi.string(out)
    end
    local env=ffi.new("unsigned short[32768]")
    local n=win.GetEnvironmentVariableW(wide("APPDATA"),env,32768)
    if n==0 or n>=32768 then return nil,"template_io_unavailable" end
    local parent=utf8(env).."/Fatshark/Darktide"
    local root=parent.."/HavocEnemyDirector"
    local directory=root.."/templates"
    local store={directory=directory}
    local function exists(path) return tonumber(win.GetFileAttributesW(wide(path)))~=4294967295 end
    function store.ensure()
        for _,p in ipairs({root,directory}) do
            if win.CreateDirectoryW(wide(p),nil)==0 and not exists(p) then return nil,"template_io_failed" end
        end
        return true
    end
    function store.list()
        local ok,err=store.ensure(); if not ok then return nil,err end
        local data=ffi.new("HED_TEMPLATE_FIND_DATA[1]")
        local handle=win.FindFirstFileW(wide(directory.."/*.json"),data)
        if handle==invalid then if win.GetLastError()==2 then return {} end; return nil,"template_io_failed" end
        local names={}
        repeat
            if math.floor(tonumber(data[0].attributes)/16)%2==0 then names[#names+1]=utf8(data[0].name) end
            if #names>256 then win.FindClose(handle); return nil,"template_library_full" end
        until win.FindNextFileW(handle,data)==0
        local errcode=win.GetLastError(); win.FindClose(handle)
        if errcode~=18 then return nil,"template_io_failed" end
        table.sort(names); return names
    end
    function store.read(filename)
        local handle=win.CreateFileW(wide(directory.."/"..filename),2147483648,1,nil,3,128,nil)
        if handle==invalid then return nil,"template_io_failed" end
        local buffer,nread=ffi.new("char[262145]"),ffi.new("unsigned long[1]")
        local ok=win.ReadFile(handle,buffer,262145,nread,nil); win.CloseHandle(handle)
        if ok==0 then return nil,"template_io_failed" end
        if nread[0]>262144 then return nil,"template_too_large" end
        return ffi.string(buffer,nread[0])
    end
    function store.remove(filename)
        if win.DeleteFileW(wide(directory.."/"..filename))==0 then return nil,"template_io_failed" end
        return true
    end
    function store.write(filename,text,overwrite)
        local ok,err=store.ensure(); if not ok then return nil,err end
        local dest=directory.."/"..filename
        if not overwrite and exists(dest) then return nil,"template_exists" end
        if not exists(dest) then
            local entries,e=store.list(); if not entries then return nil,e end
            if #entries>=256 then return nil,"template_library_full" end
        end
        local tmp,handle
        for i=1,100 do
            tmp=dest..".writing-"..i
            handle=win.CreateFileW(wide(tmp),1073741824,0,nil,1,128,nil)
            if handle~=invalid then break end
        end
        if handle==invalid then return nil,"template_io_failed" end
        local written=ffi.new("unsigned long[1]")
        local good=win.WriteFile(handle,text,#text,written,nil)~=0 and tonumber(written[0])==#text and win.FlushFileBuffers(handle)~=0
        win.CloseHandle(handle)
        if good then good=win.MoveFileExW(wide(tmp),wide(dest),overwrite and 9 or 8)~=0 end
        if not good then win.DeleteFileW(wide(tmp)); return nil,not overwrite and exists(dest) and "template_exists" or "template_io_failed" end
        return true
    end
    return store
end
return F
