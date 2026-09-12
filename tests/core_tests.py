from project_env import SOURCES
from lupa.luajit21 import LuaRuntime
lua=LuaRuntime(unpack_returned_tuples=True)
def module(mod,path):
    return lua.execute((SOURCES/mod/'scripts/mods'/mod/path).read_text(encoding='utf-8-sig'))
lua.globals().M=module('HavocConditionManager','spawn_scaling.lua')
lua.globals().P=module('HavocEnemyDirector','planner.lua')
lua.execute('''local breeds={grunt={tags={}},elite={tags={elite=true}},netter={tags={special=true}},boss={tags={monster=true}},witch={tags={witch=true}}}
local source={{id="a",composition={breeds={{name="grunt",amount={10,10}},{name="elite",amount={2,2}}}},interval=10},
    {id="b",composition={breeds={{name="grunt",amount={20,20}},{name="netter",amount={2,2}}}},interval=20},
    {id="death",kind="event",composition={"grunt","grunt"},interval=1}}
local generators=P.compile(source,P.defaults(),breeds,M.category_for_breed)
assert(#generators==4)
local g=generators[1]
assert(g.id=="timer_common" and math.abs(g.interval-15)<0.001)
assert(g.sources.a and g.sources.b)
local cfg=P.defaults(); cfg.generators.timer_common={deleted=true}; cfg.banned.netter=true
local deleted=P.compile(source,cfg,breeds,M.category_for_breed)
for _,entry in ipairs(deleted) do assert(entry.id~="timer_common" and not entry.pool.netter) end
local pool=P.filter_pool({grunt=4,elite=1},{grunt=0},{},breeds,M.category_for_breed,"common")
assert(next(pool)==nil and P.pick(pool)==nil)
pool=P.filter_pool({grunt=4},nil,{elite=true},breeds,M.category_for_breed,"elite",function() return "elite" end)
assert(next(pool)==nil)
cfg=P.defaults(); cfg.custom={{id="custom_1",category="boss",pool={boss=2}}}
assert(#P.compile({},cfg,breeds,M.category_for_breed)==1)
assert(P.budget({count=20,category="special",cap=5},cfg,239,15,4)==1)
assert(P.budget({count=20,category="special",cap=5},cfg,241,15,4)==0)
-- Tier selection and duplicate table references must not multiply source pressure.
local comp={breeds={{name="grunt",amount={10,10}}}}
local ladder={{breeds={{name="grunt",amount={1,1}}}},comp}
assert(P.collect(ladder,breeds,nil,2).grunt==10)
assert(P.collect({x=comp,y=comp},breeds).grunt==10)
assert(P.pick({boss=1},function() return 0.999 end)=="boss")
''')
print('Core behavior: PASS')
