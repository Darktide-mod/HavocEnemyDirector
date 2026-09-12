# Native event preset tables; engine-owned callbacks are not executed by this harness.
L.execute('''
table.clone=table.clone_instance
function table.append(a,b) for _,v in ipairs(b) do a[#a+1]=v end return a end
function table.add_missing(a,b) for k,v in pairs(b) do if a[k]==nil then a[k]=v end end return a end
function table.reduce(a,fn,result) for _,v in ipairs(a) do result=fn(result,v) end return result end
''')
cache['scripts/settings/ui/ui_sound_events']=tbl({})
cache['scripts/managers/mutator/mutators/mutator_spawner/mutator_spawner_location_sources'].main_path_locations=L.eval('function() return {} end')
cache['scripts/managers/mutator/mutators/mutator_stat_trigger/mutator_stat_trigger_utilities']=L.eval('''{
    on_trigger_spawn_event_enemies_as_horde=function() return function() end end,
    on_trigger_send_live_event_notification=function() return function() end end
}''')
cache['scripts/managers/mutator/mutators/mutator_gameplay/mutator_gameplay_live_event_leftover']=tbl({})
cache['scripts/managers/mutator/mutators/mutator_gameplay/mutator_gameplay_live_event_saints']=L.eval('{on_global_stat_trigger_apply_player_buff_stacks=function() return function() end end}')
cache['scripts/settings/level_prop/level_props']=tbl({})
for path in ('stolen_rations_enemy_compositions','live_event_broker_stimms_enemy_composition'):
    cache['scripts/settings/live_event/live_event_enemy_compositions/'+path]=tbl({})
event_mutator_paths=['mutator_live_event_templates','mutator_monster_spawner_templates']
event_mutator_paths += ['live_event_mutator_templates/'+p.stem for p in
    sorted((game/'scripts/settings/mutator/templates/live_event_mutator_templates').glob('*.lua'))
    if any(word in p.stem for word in ('saints','broker_stimms','abhuman_explosions','elite_army','skulls_guns','barren','leftover','endless_hordes'))]
for path in event_mutator_paths:
    for key,value in require('scripts/settings/mutator/templates/'+path).items(): mutators[key]=value
# Odin's native implementation is not part of the Lua source checkout; registration-only fixture.
mutators['mutator_gameplay_barren_odin']=tbl({'class':'native_odin_gameplay'})
for path in sorted((game/'scripts/settings/circumstance/templates').glob('live_event_*_circumstance_template.lua')):
    entries=require('scripts/settings/circumstance/templates/'+path.stem)
    for key,value in entries.items(): cache['scripts/settings/circumstance/circumstance_templates'][key]=value
