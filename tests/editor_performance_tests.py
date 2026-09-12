# Run in the real-template integration harness, after lifecycle/template cases.
L.execute('''
local D,B,S=mods.HavocEnemyDirector,mods.HavocConditionManager,mods.SoloPlay
local saved_state,saved_selection,saved_cfg=Managers.state,B.get_selected_conditions,D.get_config()
local saved_faction=S:get("havoc_faction")
local selected={}
Managers.state={};B.get_selected_conditions=function() return selected end
S:set("havoc_faction","mixed")
D.save_config(D.planner.defaults())
local view=test_view
view._hcm_page=4;view._hcm_choice=nil;view._hcm_number=nil;view._hed_templates_open=nil
view._hed_preview=nil;view._hed_generator_id=nil;view._hed_pool_filter="all";view._hcm_offsets={}
local collect,compile=D.collect_sources,D.planner.compile
local scans,compiles=0,0
D.collect_sources=function(...) scans=scans+1;return collect(...) end
D.planner.compile=function(...) compiles=compiles+1;return compile(...) end
Paging.refresh(view,test_settings)
assert(scans==1 and compiles==1)
local preview=view._hed_preview
local pools=preview.pools
for i=1,120 do
 view._hcm_offsets.pool=i%3
 Paging.refresh(view,test_settings)
 assert(view._hed_preview==preview and preview.pools==pools)
end
click_control("new_category");click_control("new_category")
click_control("pool_filter_included");click_control("pool_filter_all")
assert(scans==1 and compiles==1,"Scrolling, filters and dropdowns must not recompile native compositions")
-- UI edits invalidate immediately, including pooled weights and caps.
click_control("total_cap_plus")
assert(scans==2 and compiles==2 and view._hed_preview~=preview)
preview=view._hed_preview
local raw=S:get("havoc_faction");S:set("havoc_faction","renegade")
Paging.refresh(view,test_settings)
assert(view._hed_preview~=preview and view._hed_preview.sources.faction=="renegade")
local function equivalent()
 local fresh_sources=collect(true)
 local cfg=D.get_config();cfg.banned={}
 local fresh=compile(fresh_sources,cfg,D.breeds,D.category_for,D.preview_resolve)
 local cached=view._hed_preview.generators
 assert(#fresh==#cached)
 for i,g in ipairs(fresh) do
  local c=cached[i];assert(g.id==c.id and g.kind==c.kind and g.interval==c.interval and g.cap==c.cap)
  for name,weight in pairs(g.pool) do assert(c.pool[name]==weight) end
  for name,weight in pairs(c.pool) do assert(g.pool[name]==weight) end
 end
end
-- Same set, different override order: native faction precedence must change.
selected={"mutator_havoc_rotten_armor","hcm_auric_cultists"}
Paging.refresh(view,test_settings);assert(view._hed_preview.sources.faction=="cultist");equivalent()
selected={"hcm_auric_cultists","mutator_havoc_rotten_armor"}
Paging.refresh(view,test_settings);assert(view._hed_preview.sources.faction=="renegade");equivalent()
-- Tiers can change in place on the same manager.
local level=2
Managers.state.difficulty={get_table_entry_by_resistance=function(_,t) return t[math.min(level,#t)] end,
 get_table_entry_by_challenge=function(_,t) return t[math.min(level,#t)] end}
Paging.refresh(view,test_settings);equivalent();preview=view._hed_preview
level=5;Paging.refresh(view,test_settings);assert(view._hed_preview~=preview);equivalent()
selected={"more_havoc_monster_specials"};Paging.refresh(view,test_settings)
local previous=B:get("monster_specials_melee_twin_captain")
preview=view._hed_preview;B:set("monster_specials_melee_twin_captain",not previous)
Paging.refresh(view,test_settings);assert(view._hed_preview~=preview);equivalent()
B:set("monster_specials_melee_twin_captain",previous)
-- Scaling-only mode changes need new displayed numbers, not new source pools.
local mode=B:get("spawn_mode_common")
preview=view._hed_preview;B:set("spawn_mode_common",mode=="speed" and "quantity" or "speed")
Paging.refresh(view,test_settings) -- reference option restoration invalidates once
preview=view._hed_preview
B:set("spawn_mode_common",mode);Paging.refresh(view,test_settings)
assert(view._hed_preview==preview)
D.collect_sources=collect;D.planner.compile=compile
Managers.state=saved_state;B.get_selected_conditions=saved_selection
S:set("havoc_faction",saved_faction);D.save_config(saved_cfg)
''')
print('Editor preview: 120 scroll rebuilds plus filters/dropdowns reuse one source collection and compilation; caps, faction, condition order, tier and weak-Boss options invalidate; cached pools match fresh native compilation: PASS')
