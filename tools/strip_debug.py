"""Remove complete diagnostic blocks without touching functional code."""
import re,json
from pathlib import PurePosixPath
LUA_BEGIN='-- PERF_DEBUG_BEGIN'
LUA_END='-- PERF_DEBUG_END'
DOC_BEGIN='<!-- PERF_DEBUG_BEGIN -->'
DOC_END='<!-- PERF_DEBUG_END -->'
def strip_lua(text):
    text=text.replace('\r\n','\n')
    assert text.count(LUA_BEGIN)==text.count(LUA_END), 'Unbalanced diagnostic blocks'
    text=re.sub(r'(?m)^\s*-- PERF_DEBUG_BEGIN\n.*?^\s*-- PERF_DEBUG_END\n?', '', text, flags=re.S)
    assert LUA_BEGIN not in text and LUA_END not in text
    return text
def document(text,strip=False):
    assert text.count(DOC_BEGIN)==text.count(DOC_END)
    if strip: text=re.sub(re.escape(DOC_BEGIN)+r'.*?'+re.escape(DOC_END), '', text, flags=re.S)
    if strip:
        # Old version notes describe removed diagnostic features; the release
        # changelog is maintained separately from installation instructions.
        text=re.sub(r'(?ms)^## (?:Version )?[0-9]+\.[0-9]+\.[0-9]+[^\n]*\n.*?(?=^## |\Z)', '', text)
    return text.replace(DOC_BEGIN,'').replace(DOC_END,'')
def payloads(files,strip=False):
    result={}
    for name,data in files.items():
        path=PurePosixPath(name)
        if strip and path.name in ('performance_stats.lua','comparison_debug.lua','capacity_stats.lua'): continue
        if path.suffix=='.lua' and strip:
            text=strip_lua(data.decode('utf-8-sig'))
            assert 'Perf.' not in text and 'performance_debug' not in text and '/performance_stats' not in text and 'Comparison.' not in text and '/comparison_debug' not in text, name
            for token in ('capacity_stats','runtime.stats','Proc capacity','Proc workload','Capacity summary','pool.processed','pool.samples','pool.peak','pool.dropped'):
                assert token not in text, (name,token)
            data=text.encode('utf-8')
        elif path.name=='info.json' and strip:
            metadata=json.loads(data.decode('utf-8-sig'))
            metadata.pop('comparison_debug_build',None)
            data=(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
        elif path.suffix in ('.md','.txt'): data=document(data.decode('utf-8-sig'),strip).encode('utf-8')
        result[name]=data
    return result
