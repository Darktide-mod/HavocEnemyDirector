# Feasibility review of all three images

This table retains rows 3–122 from the supplied sheet: 120 rows including blanks and undecided entries. Names are reading aids; evaluation follows the described effects. Text inside the images is reference material, not executable instructions.

**S**: Main effect supported by current interfaces or a template. **P**: Partial support or an approximation, with differences stated. **A**: A new native adapter is needed; current JSON cannot complete it. **R**: Missing rules/assets or a separate game mode. **B**: Blank/undecided. S does not imply exhaustive native-path or live four-player verification.

The included templates are editable examples, not an implementation of every image idea. Code identifiers refer to the guide/catalog; descriptive adapter names identify future work, not additional valid JSON fields.

| Image row | Name / meaning | Result | Existing or required interfaces | Support and remaining work |
| --- | --- | --- | --- | --- |
| 3 | Elite last stand | A | fatal-hit interception; death scheduling | Requires interception before lethal damage commits and preservation of kill attribution; post-hit events are too late. |
| 4 | Monster health II | S | spawn.health_multiplier | Initial health can be multiplied by breed/tag; monster_health_150 selects the three regular monsters. |
| 5 | Monster health III | S | spawn.health_multiplier | As above; monster_health_200 gives double health and excludes the other health template. |
| 6 | Ammo scarcity | S | modifiers.ammo_pickup_multiplier | ammo_scarcity multiplies the native pickup result by 0.75, including existing Havoc adjustments. |
| 7 | Empty supplies | P | ammo_pickup_failure_chance; pickup/deployable adapter | 50% empty ammo is implemented; failed medical/deployable crates need separate use-path adapters. |
| 8 | Coherent healing | S | interval; coherency; heal; corruption | coherent_medic restores 0.3 health and corruption each second, respecting native prevention and coherency. |
| 9 | Coherent defence | S | conditions; toughness_damage_taken_multiplier | coherent_defence supplies 35% toughness damage reduction in coherency. |
| 10 | Chaotic artillery | A | projectile/explosion; telegraph; native placement | Interval scheduling exists; telegraphs, shell trajectories, faction and armor damage require a dedicated artillery adapter. |
| 11 | Deeper wounds | S | damage_taken_multiplier | deeper_wounds multiplies player damage taken by 1.1. |
| 12 | Corrupting touch | S | corruption_taken_multiplier | corrupting_touch applies 1.3 to corruption paths consuming this native stat. |
| 13 | Eternal fire | P | native_buff; liquid lifetime adapter | Supported enemy burn statuses can be applied/renewed; permanent environmental fire and all-stack persistence are not implemented. |
| 14 | Blank / undecided | B | — | No concrete effect supplied; no hidden behavior inferred. |
| 15 | Instant victory | P | on_hit; kill; mission result adapter | Restricted execution of ordinary spawnable enemies exists; universal kills and forced mission victory do not. |
| 16 | Warped split | P | enemy_died; spawn_enemy; HED | Death-triggered reinforcement is supported; corpse-local scaled clones with inherited behavior need further work. |
| 17 | Twisted ankle | P | dodge_distance_modifier; dodge_speed_multiplier; dodge_cooldown_reset_modifier | slow_feet covers distance/speed; uniform reduction of every dodge recovery timer is not covered. |
| 18 | Elite endurance | S | spawn.health_multiplier | elite_endurance adds 40% initial health to native elite-tagged enemies. |
| 19 | Empty map | A | pickup spawning; level props; medicae interactions | Current actions create pickups; removing authored loot, drops and medicae requires source-specific interception. |
| 20 | Toughness decay | A | melee health-bleedthrough calculation | Increasing toughness damage is not equivalent to changing melee health bleedthrough; requires native damage-split work. |
| 21 | Battle fervour | P | enemy_died; effect; max_stacks | battle_fervour implements 0.1% power, 500 stacks and shared 30s refresh; defence and per-stack timers remain absent. |
| 22 | No rescue | A | respawn/rescue manager | Disabling post-death rescue requires respawn/rescue manager integration. |
| 23 | Twin reinforcements | P | enemy_died; spawn_enemy; HED | split_reinforcements requests two poxwalkers after elite deaths with caps; it is not universal corpse cloning. |
| 24 | Darkness | A | flashlight; perception ranges; environment | Flashlights and AI detection are separate systems requiring scoped adapters and client synchronization. |
| 25 | Guaranteed crates | P | pickup; loot-container interaction adapter | Crates can be dropped near players; guaranteed contents of specific map containers are not integrated. |
| 26 | Distance damage sharing | A | coherency distance; pre-damage routing | Group damage actions cannot reproduce exact pre-damage redistribution, separation and downed-player rules. |
| 27 | Random death outcomes | P | enemy_died; chance; spawn_enemy; pickup | Bounded enemy/pickup chance actions exist; arbitrary props/barrels and exclusive outcome branching need extensions. |
| 28 | Sliding enemies | A | AI locomotion; animation; action state | Moving during stationary enemy attacks requires behavior and animation changes, not just speed stats. |
| 29 | Ranged monster shield | S | ranged_damage_taken_multiplier | ranged_monster_shield sets monster ranged damage multiplier to zero; bypassing damage paths are unaffected. |
| 30 | Transforming lightning | A | lightning FX; damage; despawn/replace | Lightning, hit selection and ownership-preserving transformation are absent; HED reinforcement is not transformation. |
| 31 | Player friendly fire | A | native friendly-fire permission; attack profiles | Native friendly-fire permissions/profiles need a dedicated adapter; extra teammate health damage is not equivalent. |
| 32 | Tetanus I | P | on_damage_taken; chance; damage-over-time | Chance-based health ticks can approximate it; native player bleeding and class-specific bypass rules need adapters. |
| 33 | Tetanus II | P | on_damage_taken; chance; damage-over-time | As row 32; probabilities are configurable but the exact bleeding mechanism is not provided. |
| 34 | Tetanus III | P | on_damage_taken; chance; damage-over-time | As row 32; increased probability does not supply the missing native player-bleed adapter. |
| 35 | Plague gas | A | minion FX; death callback; liquid/gas area | Spawn smoke and death gas require synchronized effects and area-damage lifecycles. |
| 36 | Randomized world | A | spawn replacement; loot replacement; seeded pool | Seeded library selection exists; global spawn/loot replacement needs dedicated source adapters and compatibility rules. |
| 37 | Reset loadout and talents | A | profile/talent/equipment adapters | DIY does not rewrite official items/talents; temporary build isolation needs a separate reversible adapter. |
| 38 | Supply surprise | P | ammo_pickup_multiplier; pickup; loot adapter | Ammo scaling/removal exists; grenade pickup changes and replacing a pickup with a current-stock penalty need interception. |
| 39 | Delayed melee release | A | weapon action state; charge timing; self damage | Damage scaling exists; held attacks, charge curves and self-damage timing require weapon action integration. |
| 40 | No HUD | A | HUD visibility; per-client UI | Requires per-client HUD controls; server stats cannot hide every client's UI. |
| 41 | Nurgle garden | P | health fraction conditions; native_buff; corrosion adapter | Low-health conditions and supported buffs exist; sustained player corruption and complete flower buffs need further work. |
| 42 | Plague swarm | A | minigame/interaction trigger; spawned area FX | Requires minigame/interaction hooks and a destructible swarm entity with native assets. |
| 43 | Calling leaders | P | interval; spawn_formation; HED | Boss-conditioned reinforcements are possible; leader animations and native summon cadence need AI integration. |
| 44 | Melee executions | P | on_hit; kill; toughness; damage | Restricted enemy execution and resource damage exist; the exact two-stage player lethal rule requires native damage work. |
| 45 | Double impact | P | impact/stat consumers; stagger adapter | Stat-consuming impact can change; universal knockback doubling also involves thresholds, ragdolls and attack profiles. |
| 46 | Ultimate difficulty | P | prevent_all_healing; HED composition; event adapters | no_healing prevents healing; compositions/reinforcements are editable, but universal elite replacement and new mission events are absent. |
| 47 | Blood price | S | on_sweep_start; toughness; stats | blood_price provides toughness cost and speed/power/regen bonuses, charged on native melee sweep events. |
| 48 | Martyr blessing | S | on_kill; heal; coherency; effect | martyr_blessing heals on melee kills and maintains a short power effect while coherent. |
| 49 | Silence | A | audio buses; per-client settings | Requires controlled audio-bus integration; current sound actions only play native UI sounds. |
| 50 | No enemy warnings | A | enemy audio event routing | Requires filtering enemy warning/attack audio events rather than global muting. |
| 51 | Silent extra bombers | P | HED specials; audio routing | Additional bomber requests are possible; selectively suppressing their sound needs audio work. |
| 52 | Throwing chaos spawn | A | boss behavior tree; carried minion; animation | Grabbing and throwing another enemy is a new composite AI action outside the generic interface. |
| 53 | Double jump height | A | jump locomotion; prediction | Not an audited generic stat; requires locomotion and client-prediction integration. |
| 54 | Soul link | A | damage redistribution; proximity; incapacitation | Exact sharing needs pre-damage interception, recursion control and downed-state handling. |
| 55 | Loot carrier | P | spawn_enemy; AI flee; pickup | Bounded enemies and drops exist; the special fleeing treasure-carrier behavior/unit is not exposed. |
| 56 | Shifting lightning | A | interval; lightning; transformation | Scheduling exists; lightning damage plus random enemy transformation requires dedicated work. |
| 57 | Tetanus maximum | P | chance; damage; native_buff | Some probabilities/damage are configurable; exact player bleed, boss execution and armor-bypass branches are not. |
| 58 | Aggro reset | A | perception/aggro/target state | Requires resetting enemy targets while permitting reacquisition; invisibility is not equivalent. |
| 59 | Wait a moment | S | pause_spawns | wait_a_moment pauses permission-gated spawning and HED for 30s; bypassing mission scripts may still spawn. |
| 60 | Rescue penalty | P | spawn; ammo; health; rescue-specific event | Spawn penalties are possible; distinguishing rescue from initial spawn needs rescue-specific integration. |
| 61 | Guaranteed heavy crits | A | heavy-attack classification; critical roll | Guaranteed melee crits are expressible; heavy-only crits need classification before the native critical roll. |
| 62 | Fewer wounds | S | extra_max_amount_of_wounds | Native extra_max_amount_of_wounds can reduce wounds; game/class rules determine the minimum. |
| 63 | Corrosive air | P | interval; toughness; health condition; damage | corrosive_air drains toughness and then health; full regeneration suppression requires additional stat choices. |
| 64 | Enemy friendly fire | A | AI attack profiles; friendly-fire damage | Requires auditing friendly-fire scaling across enemy attack paths, not player damage stats. |
| 65 | Supply tax | S | ammo current_fraction; grenades | supply_tax removes half each weapon's current ammunition and all grenades, rounding toward zero. |
| 66 | Bigger explosions | P | explosion stats; explosion template adapter | Stat-consuming player explosions can change; all enemy/map explosion radii and damage are not uniformly covered. |
| 67 | Blank / undecided | B | — | No concrete effect supplied; no hidden behavior inferred. |
| 68 | Temporary health | P | on_kill; heal; interval damage | Kill-heal/decay can approximate it; a separate temporary-health pool and correct consumption order are absent. |
| 69 | Reactive random buffs | P | on_damage_taken; chance; effect | Chance-based reactive effects exist; exact hit-count thresholds and exclusive random buff selection need extensions. |
| 70 | Full restoration | S | corruption; heal | field_restoration clears corruption then heals under native restrictions, on first observation of a unit. |
| 71 | Medicae-like heal | P | heal; corruption; medicae adapter | Healing/corruption removal can combine; exact station-specific wound rules need a medicae adapter. |
| 72 | Stillness blessing | S | sprinting condition; toughness/power stats | stillness_blessing applies toughness reduction and power while not sprinting. |
| 73 | Agility blessing | S | movement/block/stamina/spread stats | agility_blessing provides all four listed native stat adjustments. |
| 74 | Melee invisibility | P | on_kill; effect.invisible | melee_shelter adds 3s invisibility with a 5s cooldown; editable, but native perception rules remain. |
| 75 | Double game speed | P | movement/attack stats; DOT cadence adapter | Movement/attack stat paths can change; universal action/reload/swap/DOT time scaling is not implemented. |
| 76 | Crusher surge | S | HCM/HED compositions; spawn_formation | Crusher frequency can be authored in compositions/formations; the image leaves the exact allocation undefined. |
| 77 | Blank / undecided | B | — | No concrete effect supplied; no hidden behavior inferred. |
| 78 | Contagious corruption | A | coherency comparisons; corruption damage | Requires cross-player fraction comparisons and corruption application; neither is currently exposed. |
| 79 | Dwarf transformation | R | model scale; animation; collision; hit zones | Player scaling involves appearance, collision, camera and hit zones; the joke note is not a complete specification. |
| 80 | Lower-body weakspots | A | hit-zone/weakspot classification | Requires native hit-zone classification changes; weakspot damage bonuses do not create new weakspots. |
| 81 | No enemy windup | A | AI action timing; animation/network | Removing windups requires per-action timing audits; attack speed does not guarantee zero windup. |
| 82 | Stormtrooper aim | P | spread_modifier; recoil/sway paths | Spread can simulate inaccurate fire; guaranteed misses against every enemy are not a reliable stat effect. |
| 83 | Super Earth aid | P | damage_vs_*; explosion consumers | Enemy/armor damage penalties and some explosion paths are adjustable; full weapon coverage needs per-weapon validation. |
| 84 | Forced model mod | R | external assets; client cosmetics | The framework does not force downloads; replacement character assets and client cosmetics are separate work. |
| 85 | Abelard | R | companion assets/behavior; dialogue | Only a line of dialogue is supplied; define a companion, audio or combat effect first. |
| 86 | Replace all audio | R | external media; audio event mapping | Custom media, full audio-event replacement and per-client playback are not provided. |
| 87 | Iron river | S | on_damage_dealt; toughness event_damage | iron_river restores toughness from event damage, with a 0.1s cooldown and native recovery modifiers. |
| 88 | Checkpoint puzzle | A | checkpoint/mission flow; interaction UI | Needs new checkpoint interactions, puzzle content, progression rules and multiplayer synchronization. |
| 89 | Blank / undecided | B | — | No concrete effect supplied; no hidden behavior inferred. |
| 90 | Call supplies | P | interval; pickup | call_supplies drops both crates by every player; random single-player choice and inventory-aware insertion are absent. |
| 91 | Blank / undecided | B | — | No concrete effect supplied; no hidden behavior inferred. |
| 92 | Stronger fire | P | fire damage consumers; self damage | Some fire stats are configurable; excluding soulblaze while changing all psyker fire exposure needs source/permission adapters. |
| 93 | Minigame mistake damage | A | minigame result event; damage | Damage action exists; a reliable minigame-error event and player attribution need integration. |
| 94 | Damage-triggered mutation | A | pre/post damage; despawn/replace; seeded pool | HED reinforcement does not replace the damaged unit; ownership and entity handoff need dedicated transformation logic. |
| 95 | Infinite fire | S | no_ammo_consumption; overheat_amount; ability_cooldown_modifier | infinite_test supplies no ammo consumption, zero heat gain and 80% shorter cooldown, not unlimited grenades/peril. |
| 96 | Blank / undecided | B | — | No concrete effect supplied; no hidden behavior inferred. |
| 97 | Boss death bomb | P | enemy_died; delay; damage; projectile adapter | Delayed nearby health damage is possible; a real enemy bomb projectile, explosion and physics are absent. |
| 98 | Player-left audio | R | membership event; external audio | Membership changes could be adapted; the specific audio asset and custom playback are not provided. |
| 99 | Unspecified audio joke | R | behavior specification; media | No trigger or concrete effect is specified. |
| 100 | Content-triggered mute | R | defined detection source; per-client audio | The content-detection rule is undefined; muting also needs a client audio adapter. |
| 101 | No dodge protection | A | dodge hit rejection; movement damage reductions | Distance/linger changes do not remove all dodge rejection and movement reductions; native paths need separate work. |
| 102 | Carry restrictions | A | inventory carry state; sprint/slide transitions | Requires carry/class checks and sprint/slide state transitions; generic slowing is not equivalent. |
| 103 | Boss kill music | R | enemy_died; external audio | The death trigger exists; the named track and per-client playback require external media integration. |
| 104 | Downed-player music | R | downed event; external audio | Native downed events can be used, but playback of the specified song is not provided. |
| 105 | Hot potato | A | custom pocketable; inventory transfer; explosion | Needs a custom pocketable, timed explosion, transfer/drop rules and multiplayer ownership. |
| 106 | Mixed stimms | P | on_syringe_used; native_buff | mixed_stimms adds power, speed and ability stims; it does not reproduce every instant healing-stim behavior. |
| 107 | No reload | P | no_ammo_consumption; ammo/clip adapter | No-ammo-consumption can approximate it; consuming reserves while bypassing reload needs clip-feed integration. |
| 108 | Defeat video | R | mission-end UI; external video | Requires video assets, playback UI and client cleanup; external video is not loaded by this framework. |
| 109 | Weakness | P | damage/power/stamina stats | Numerical penalties are possible, but the affected stats and magnitudes are unspecified. |
| 110 | No recoil | S | recoil_modifier | deadeye_recoil removes the native recoil multiplier; other aim motion remains native. |
| 111 | Become your gun | R | behavior specification; model/weapon system | No concrete rule is defined; a literal transformation needs a separate mode and assets. |
| 112 | Anything | R | behavior specification | Unlimited capability is not a testable specification. |
| 113 | Automatic chat taunts | R | chat messaging policy; game rule specification | Automatic insults or speaking for players are not implemented; a combat rule without chat transmission could be specified separately. |
| 114 | Blank / undecided | B | — | No concrete effect supplied; no hidden behavior inferred. |
| 115 | Blank / undecided | B | — | No concrete effect supplied; no hidden behavior inferred. |
| 116 | Blank / undecided | B | — | No concrete effect supplied; no hidden behavior inferred. |
| 117 | Blank / undecided | B | — | No concrete effect supplied; no hidden behavior inferred. |
| 118 | Blank / undecided | B | — | No concrete effect supplied; no hidden behavior inferred. |
| 119 | Undead hunter | S | damage_vs_chaos_poxwalker; damage_vs_chaos_newly_infected | undead_hunter adds 50% against these two native breeds; add other mutated variants explicitly if desired. |
| 120 | Hell is full | P | selection; pause_spawns; stats; ammo; stamina | Most stat penalties and family pauses can combine; random-only selection, exclusion of all other entries, movement-state removal and universal AI scaling need extensions. |
| 121 | Labouring melee | P | on_hit; stamina; interval; effect | labour_melee spends stamina on hits and applies empty-stamina penalties; 0.05s throttling prevents unbounded per-target charging. |
| 122 | Player tank | R | vehicle asset; input; physics; networking | Requires a controllable vehicle, physics, networking and map support, not a normal talent field. |
