"""Actual add/remove controls, with native faction and replacement constraints."""
L.execute('''
local D=mods.HavocEnemyDirector
local P=D.planner
local old_cfg,old_sources,old_resolve=D.get_config(),D.collect_sources,D.preview_resolve
local sources={{id="common",kind="timer",pool={chaos_newly_infected=1,chaos_poxwalker=1},interval=60},
    {id="travel",kind="travel",pool={chaos_poxwalker=1},interval=60,distance=100}}
sources.faction="renegade"
D.collect_sources=function() return sources end
D.preview_resolve=function(name) return name=="chaos_newly_infected" and "chaos_poxwalker" or name end
D.restore_defaults()
test_view._hcm_page=4; test_view._hcm_choice=nil; test_view._hcm_number=nil
test_view._hed_generator_id="timer_common"; test_view._hed_pool_filter="included"
test_view._hcm_offsets.pool=0
local function refresh() Paging.refresh(test_view,test_settings) end
local function find(id)
    for _,g in ipairs(D.preview_generators()) do if g.id==id then return g end end
end
local function offered(name)
    for _,option in ipairs(test_view._hcm_ui.choices.add_pool_unit.options) do if option[1]==name then return true end end
    return false
end
refresh()
local travel_weight=find("travel_common").pool.chaos_poxwalker
click_control("remove_unit_chaos_poxwalker")
assert(not find_control("unit_chaos_poxwalker") and not find("timer_common").pool.chaos_poxwalker)
assert(find("travel_common").pool.chaos_poxwalker==travel_weight)
local pool=D.get_config().generators.timer_common.pool
assert(pool.chaos_poxwalker==0 and pool.chaos_newly_infected==0,"Removed replacements must not return via their source aliases")
assert(not D.get_config().banned.chaos_poxwalker)
assert(offered("chaos_poxwalker") and offered("renegade_melee"))
assert(not offered("chaos_newly_infected") and not offered("cultist_melee"))
assert(not offered("renegade_gunner") and not offered("attack_valkyrie"))
click_control("add_pool_unit")
assert(test_view._hcm_ui.popup.upwards and test_view._hcm_ui.popup.y+test_view._hcm_ui.popup.h<921)
local _,blocked=find_control("clear_pool"); assert(blocked.content.hotspot.disabled)
pool_membership_snapshots={add_menu=P.copy(test_view._hcm_ui.items)}
Paging.close_choice(test_view); refresh()
assert(not find("timer_common").pool.chaos_poxwalker,"Opening/cancelling the menu must not add a unit")
click_control("add_pool_unit"); click_control("choice_add_pool_unit_chaos_poxwalker")
assert(not test_view._hcm_ui.popup and find("timer_common").pool.chaos_poxwalker==1)
assert(not offered("chaos_poxwalker"))
D.save_config(P.config(D:get("director_config_v1"))); refresh()
assert(find("timer_common").pool.chaos_poxwalker==1)
-- Per-row add/remove works from All and keeps global bans separate.
click_control("pool_filter_all")
click_control("remove_unit_chaos_poxwalker")
assert(find_control("add_unit_chaos_poxwalker") and not find_control("remove_unit_chaos_poxwalker"))
click_control("add_unit_chaos_poxwalker")
click_control("ban_chaos_poxwalker")
assert(not find("timer_common").pool.chaos_poxwalker and not find("travel_common").pool.chaos_poxwalker)
assert(find_control("remove_unit_chaos_poxwalker"),"Banned units keep visible saved weights")
click_control("remove_unit_chaos_poxwalker")
assert(D.get_config().banned.chaos_poxwalker and not offered("chaos_poxwalker"))
assert(not find_control("add_unit_chaos_poxwalker").action)
click_control("ban_chaos_poxwalker")
assert(offered("chaos_poxwalker") and not find("timer_common").pool.chaos_poxwalker)
assert(find("travel_common").pool.chaos_poxwalker==travel_weight)
click_control("add_unit_chaos_poxwalker")
-- The same controls can populate a new, initially empty custom pool.
test_view._hed_add_category=1; click_control("add_generator")
local custom=test_view._hed_generator_id
click_control("clear_pool")
assert(next(find(custom).pool)==nil and offered("chaos_poxwalker"))
click_control("add_pool_unit"); click_control("choice_add_pool_unit_chaos_poxwalker")
assert(find(custom).pool.chaos_poxwalker==1 and find("timer_common").pool.chaos_poxwalker==1)
click_control("remove_unit_chaos_poxwalker")
assert(next(find(custom).pool)==nil and find("timer_common").pool.chaos_poxwalker==1)
-- A full eligible pool offers no additional choices and disables the add menu.
for name,breed in pairs(D.breeds) do
    if not breed.airbound and name~="attack_valkyrie" and D.category_for(breed)=="common"
        and D.preview_resolve(name)==name and P.faction_allowed(breed,sources.faction) then
        local cfg=D.get_config(); cfg.generators[custom].pool[name]=1; D.save_config(cfg)
    end
end
refresh()
assert(not find_control("add_pool_unit").action and not test_view._hcm_ui.choices.add_pool_unit)
D.collect_sources=old_sources; D.preview_resolve=old_resolve; D.save_config(old_cfg)
''')
for items in L.globals().pool_membership_snapshots.values():
    specs=plain_items({'items':items})
    for width,height in ratios:
        vp=paging.viewport(width,height)
        for item in specs:
            x,y=(item['x']+vp.x)*vp.scale,(item['y']+vp.y)*vp.scale
            assert x>=0 and y>=0 and x+item['w']*vp.scale<=width and y+item['h']*vp.scale<=height
    active=[item for item in items.values() if item.action and not item.blocked]
    for i,a in enumerate(active):
        for b in active[i+1:]:
            assert a.x+a.w<=b.x or b.x+b.w<=a.x or a.y+a.h<=b.y or b.y+b.h<=a.y,(a.key,b.key)
print('Pool add/remove: menu and row actions, native/custom isolation, saved reload, replacements, category/faction/bans, empty/full pools and popup bounds at 11 resolutions: PASS')
