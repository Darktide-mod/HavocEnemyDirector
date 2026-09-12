"""Regression: changing a batch must change throughput, not its timer/distance."""
from pathlib import Path
import sys


def run():
    from project_env import PROJECT, GAME, SOURCES
    root = PROJECT
    
    from lupa.luajit21 import LuaRuntime
    lua = LuaRuntime(unpack_returned_tuples=True)
    mods = SOURCES
    lua.globals().P = lua.execute((mods / 'HavocEnemyDirector/scripts/mods/HavocEnemyDirector/planner.lua').read_text(encoding='utf-8'))
    lua.globals().M = lua.execute((mods / 'HavocConditionManager/scripts/mods/HavocConditionManager/spawn_scaling.lua').read_text(encoding='utf-8'))
    lua.execute('''
local breeds={grunt={tags={}},special={tags={special=true}}}
local sources={{id="native",kind="timer",pool={grunt=30},interval=60},
    {id="travel",kind="travel",pool={grunt=30},interval=60,distance=120}}
local cfg=P.defaults()
cfg.custom={{id="custom_1",category="special",kind="timer",pool={special=10}}}
local function find(id)
    for _,g in ipairs(P.compile(sources,cfg,breeds,M.category_for_breed)) do if g.id==id then return g end end
    error(id)
end
for _,id in ipairs({"timer_common","travel_common","custom_1"}) do
    local before=find(id)
    cfg.generators[id]={count=before.count*2}
    local after=find(id)
    assert(after.count==before.count*2)
    assert(after.interval==before.interval,id..": editing count changed interval")
    assert(after.distance==before.distance,id..": editing count changed distance")
    for _,mode in ipairs({"speed","quantity","mixed"}) do
        for multiplier=1,5 do
            local speed,quantity=M.factors(multiplier,mode)
            local factors={[before.category]={speed=speed,quantity=quantity}}
            local a,b=P.effective(before,factors),P.effective(after,factors)
            assert(a.interval==b.interval and a.distance==b.distance)
            assert(math.abs(b.count/b.interval-2*a.count/a.interval)<0.000001)
        end
    end
    cfg.generators[id].interval=17.25
    cfg.generators[id].distance=91.5
    cfg.generators[id].count=1
    after=find(id)
    assert(after.count==1 and after.interval==17.25 and after.distance==91.5)
    cfg.generators[id]=nil
    after=find(id)
    assert(after.count==before.count and after.interval==before.interval and after.distance==before.distance)
end
''')
    print('Generator parameter independence: native/custom, timer/travel, explicit values, reset and all 15 multiplier/mode combinations: PASS')


run()
