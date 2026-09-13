-- Windows Unicode filesystem access, on explicit library actions only.
-- No shell, extra DLL, Lua evaluation, or polling during gameplay.
local F={}
function F.new(ffi)
    if not ffi then return nil,"template_io_unavailable" end
    if not pcall(ffi.typeof,"HED_TEMPLATE_FIND_DATA") then
        ffi.cdef[[
        typedef struct { unsigned long attributes; unsigned long times[6]; unsigned long size_high, size_low, reserved[2]; unsigned short name[260], alternate[14]; } HED_TEMPLATE_FIND_DATA;
        ]]
    end
    -- FFI symbols are shared by every mod. Private symbol aliases keep our
    -- pointer types independent of load order and previously loaded versions.
    ffi.cdef[[
        int __stdcall HED_TEMPLATE_IO_MultiByteToWideChar(unsigned int,unsigned long,const char*,int,unsigned short*,int) __asm__("MultiByteToWideChar");
        int __stdcall HED_TEMPLATE_IO_WideCharToMultiByte(unsigned int,unsigned long,const unsigned short*,int,char*,int,const char*,int*) __asm__("WideCharToMultiByte");
        unsigned long __stdcall HED_TEMPLATE_IO_GetEnvironmentVariableW(const unsigned short*,unsigned short*,unsigned long) __asm__("GetEnvironmentVariableW");
        int __stdcall HED_TEMPLATE_IO_CreateDirectoryW(const unsigned short*,void*) __asm__("CreateDirectoryW");
        unsigned long __stdcall HED_TEMPLATE_IO_GetFileAttributesW(const unsigned short*) __asm__("GetFileAttributesW");
        void* __stdcall HED_TEMPLATE_IO_FindFirstFileW(const unsigned short*,HED_TEMPLATE_FIND_DATA*) __asm__("FindFirstFileW");
        int __stdcall HED_TEMPLATE_IO_FindNextFileW(void*,HED_TEMPLATE_FIND_DATA*) __asm__("FindNextFileW");
        int __stdcall HED_TEMPLATE_IO_FindClose(void*) __asm__("FindClose");
        void* __stdcall HED_TEMPLATE_IO_CreateFileW(const unsigned short*,unsigned long,unsigned long,void*,unsigned long,unsigned long,void*) __asm__("CreateFileW");
        int __stdcall HED_TEMPLATE_IO_ReadFile(void*,void*,unsigned long,unsigned long*,void*) __asm__("ReadFile");
        int __stdcall HED_TEMPLATE_IO_WriteFile(void*,const void*,unsigned long,unsigned long*,void*) __asm__("WriteFile");
        int __stdcall HED_TEMPLATE_IO_FlushFileBuffers(void*) __asm__("FlushFileBuffers");
        int __stdcall HED_TEMPLATE_IO_CloseHandle(void*) __asm__("CloseHandle");
        int __stdcall HED_TEMPLATE_IO_MoveFileExW(const unsigned short*,const unsigned short*,unsigned long) __asm__("MoveFileExW");
        int __stdcall HED_TEMPLATE_IO_DeleteFileW(const unsigned short*) __asm__("DeleteFileW");
        unsigned long __stdcall HED_TEMPLATE_IO_GetLastError(void) __asm__("GetLastError");
    ]]
    local win=ffi.load("kernel32")
    local invalid=ffi.cast("void*",-1)
    local function wide(s)
        local n=win.HED_TEMPLATE_IO_MultiByteToWideChar(65001,8,s,#s,nil,0)
        if n==0 then error("template_name_invalid",0) end
        local out=ffi.new("unsigned short[?]",n+1); win.HED_TEMPLATE_IO_MultiByteToWideChar(65001,8,s,#s,out,n); return out
    end
    local function utf8(s)
        local n=win.HED_TEMPLATE_IO_WideCharToMultiByte(65001,0,s,-1,nil,0,nil,nil)
        local out=ffi.new("char[?]",n); win.HED_TEMPLATE_IO_WideCharToMultiByte(65001,0,s,-1,out,n,nil,nil); return ffi.string(out)
    end
    local env=ffi.new("unsigned short[32768]")
    local n=win.HED_TEMPLATE_IO_GetEnvironmentVariableW(wide("APPDATA"),env,32768)
    if n==0 or n>=32768 then return nil,"template_io_unavailable" end
    local parent=utf8(env).."/Fatshark/Darktide"
    local root=parent.."/HavocEnemyDirector"
    local directory=root.."/templates"
    local store={directory=directory}
    local function exists(path) return tonumber(win.HED_TEMPLATE_IO_GetFileAttributesW(wide(path)))~=4294967295 end
    function store.ensure()
        for _,p in ipairs({root,directory}) do
            if win.HED_TEMPLATE_IO_CreateDirectoryW(wide(p),nil)==0 and not exists(p) then return nil,"template_io_failed" end
        end
        return true
    end
    function store.list()
        local ok,err=store.ensure(); if not ok then return nil,err end
        local data=ffi.new("HED_TEMPLATE_FIND_DATA[1]")
        local handle=win.HED_TEMPLATE_IO_FindFirstFileW(wide(directory.."/*.json"),data)
        if handle==invalid then if win.HED_TEMPLATE_IO_GetLastError()==2 then return {} end; return nil,"template_io_failed" end
        local names={}
        repeat
            if math.floor(tonumber(data[0].attributes)/16)%2==0 then names[#names+1]=utf8(data[0].name) end
            if #names>256 then win.HED_TEMPLATE_IO_FindClose(handle); return nil,"template_library_full" end
        until win.HED_TEMPLATE_IO_FindNextFileW(handle,data)==0
        local errcode=win.HED_TEMPLATE_IO_GetLastError(); win.HED_TEMPLATE_IO_FindClose(handle)
        if errcode~=18 then return nil,"template_io_failed" end
        table.sort(names); return names
    end
    function store.read(filename)
        local handle=win.HED_TEMPLATE_IO_CreateFileW(wide(directory.."/"..filename),2147483648,1,nil,3,128,nil)
        if handle==invalid then return nil,"template_io_failed" end
        local buffer,nread=ffi.new("char[262145]"),ffi.new("unsigned long[1]")
        local ok=win.HED_TEMPLATE_IO_ReadFile(handle,buffer,262145,nread,nil); win.HED_TEMPLATE_IO_CloseHandle(handle)
        if ok==0 then return nil,"template_io_failed" end
        if nread[0]>262144 then return nil,"template_too_large" end
        return ffi.string(buffer,nread[0])
    end
    function store.remove(filename)
        if win.HED_TEMPLATE_IO_DeleteFileW(wide(directory.."/"..filename))==0 then return nil,"template_io_failed" end
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
            handle=win.HED_TEMPLATE_IO_CreateFileW(wide(tmp),1073741824,0,nil,1,128,nil)
            if handle~=invalid then break end
        end
        if handle==invalid then return nil,"template_io_failed" end
        local written=ffi.new("unsigned long[1]")
        local good=win.HED_TEMPLATE_IO_WriteFile(handle,text,#text,written,nil)~=0 and tonumber(written[0])==#text and win.HED_TEMPLATE_IO_FlushFileBuffers(handle)~=0
        win.HED_TEMPLATE_IO_CloseHandle(handle)
        if good then good=win.HED_TEMPLATE_IO_MoveFileExW(wide(tmp),wide(dest),overwrite and 9 or 8)~=0 end
        if not good then win.HED_TEMPLATE_IO_DeleteFileW(wide(tmp)); return nil,not overwrite and exists(dest) and "template_exists" or "template_io_failed" end
        return true
    end
    return store
end
return F
