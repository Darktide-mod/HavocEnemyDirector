"""Compile fractional relative edits through the real HCM template runtime."""
from pathlib import Path
import sys
PROJECT_HED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT_HED.parent/"HavocConditionManager/tests"))
from native_harness import *
L.execute('new_test_mod("HavocEnemyDirector"); mods.SoloPlay.has_local_gameplay_authority=function() return host end')
load_mod("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_director")
L.execute("""
local D=mods.HavocEnemyDirector
-- Install just the compiler hooks as DMF does; the engine-facing hooks remain
-- explicit boundaries in the separate native spawn adapter tests.
for _,hook in ipairs(hooks) do
    if hook.owner==D and (hook.target==S or hook.target==E) then
        local fn,original=hook.fn,hook.target[hook.name]
        hook.target[hook.name]=function(...) return fn(original,...) end
    end
end
local entry,item
for _,e in ipairs(A.entries) do
    for _,field in ipairs(e.items) do
        if field.definition.key=="trickle_horde_cooldown" and type(field.value)=="number" and
            field.value>0 and field.value<field.definition.min then entry=e;item=field;break end
    end
    if item then break end
end
assert(item,"real native sub-minimum cooldown fixture")
local original=item.value
local coarse=S.coarse_config({trickle_frequency=10})
B:set("native_configuration_v3",coarse)
local raw=D.get_saved_config();raw.relative[entry.id]={[item.id]=1}
assert(D.save_config(raw))
Managers.state.game_session={};E.reset()
local expected=S.scaled(item,entry.family,coarse)
local prepared=E.prepare(entry.root,entry.family)
assert(S.get(prepared,item.path)==expected and expected<item.definition.min)
assert(E.prepare(entry.root,entry.family)==prepared)
assert(S.get(entry.root,item.path)==original)
raw.relative[entry.id][item.id]=0.5;assert(D.save_config(raw))
assert(E.prepare(entry.root,entry.family)==prepared,"mission configuration must remain frozen")
Managers.state.game_session={};E.reset()
local lowered=E.prepare(entry.root,entry.family)
assert(S.get(lowered,item.path)==math.max(0.001,expected*0.5))
assert(E.prepare(lowered,entry.family)==lowered,"compiled templates must not be scaled twice")

-- Slot capacity stays fractional until the native slot owner applies its own
-- runtime multiplier and ceil; 1x does not silently pin a rounded field.
local id="specials/default_specials/1"
local cfg=D.get_saved_config();cfg.relative={[id]={max_alive_specials=1}}
cfg.rules={[id]={encounter={mode="append",match="all",clauses={{condition="monster_idle"}}}}}
assert(D.save_config(cfg))
B:set("native_configuration_v3",S.coarse_config({special_slots=1.25}))
Managers.state.game_session={};E.reset()
local result=E.prepare(A.by_id[id].root,"specials")
local baseline=A.by_id[id].root.max_alive_specials
assert(result.max_alive_specials==baseline*1.25)
assert(E.has_gate(result),"native rule binding must see the final relative table")
Managers.state.pacing={num_aggroed_monsters=function() return 1 end}
E.clear_context();assert(not E.allowed(result,1))
cfg.relative[id].max_alive_specials=1.5;assert(D.save_config(cfg))
assert(E.prepare(A.by_id[id].root,"specials")==result)
Managers.state.game_session={};E.reset()
local next_result=E.prepare(A.by_id[id].root,"specials")
assert(next_result.max_alive_specials==baseline*1.25*1.5)
assert(E.has_gate(next_result))

-- Pure validation has no dependency on a previous mission's relative edits.
local valid,fault=A.validate_config({patches={[id]={max_alive_specials=8}},rules={}})
assert(#fault==0 and valid.patches[id].max_alive_specials==8)
local native=A.by_id[id].root
local standalone=S.apply(native,"specials",S.coarse_config(),{max_alive_specials=8},A.breeds,A.by_table)
assert(standalone.max_alive_specials==8)
host=false;Managers.state.game_session={};E.reset()
assert(E.prepare(native,"specials")==native,"clients must not compile host overrides")
print("Native relative compiler: subsecond heat coefficients, exact 1x inheritance, fractional slots, rule binding, cache identity, immutable sources, mission snapshots, pure validation and client isolation: PASS")
""")
