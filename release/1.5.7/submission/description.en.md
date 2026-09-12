# Havoc Enemy Director - Advanced Spawning

Havoc Enemy Director requires SoloPlay and Havoc Condition Manager, and also supports Realms sessions. It adds an Advanced page to the condition manager, groups the selected conditions' native spawn sources and builds an editable set of generators for the next mission. In Realms, spawning follows the host's configuration.

## Generators, pools and pacing

Edit timed and travel-based spawning, ambient enemies and supported event sources. Weak monsters retain separate handling. The director uses several groups where their behavior differs; it does not reduce every condition to one universal spawner.

- Adjust batch sizes, intervals, travel distances and generator limits.
- Change unit weights, ban units and edit enemy-category or total population caps.
- Add custom timed or travel generators; pause, delete or reset a generator.
- Restore the full default generator set from the selected conditions.

Changing conditions rebuilds the default generator configuration to match their combined effects. Set conditions and multipliers first, then make custom edits. In-mission changes are saved for the next mission snapshot.

## Editing unit pools

Use Add unit at the bottom of the pool to select an eligible unit; the menu opens upwards when needed. A new member starts at weight 1. The + beside a unit name adds it, and × removes it from this generator. The All tab also lists available units with zero weight; In pool shows the configured members. The separate Allow/Ban button controls all advanced generators and retains saved weights. Globally banned units must be unbanned before adding them through the menu.

Custom generator IDs use the lowest available number: deleting #2 from #1/#2/#3 lets the next new generator use #2. Remaining generators keep their IDs and settings.

## Multipliers and capacity

The highest selected enemy multiplier sets the default total capacity: 1× = 240, 2× = 330, 3× = 420, 4× = 510 and 5× = 600. Category defaults scale with their corresponding multipliers: at 1×, common enemies use 120, elites 45, specialists 16 and bosses 4. These are editable limits, not promised enemy counts.

Click a number to type or paste a value. Enter or clicking elsewhere confirms; Esc cancels. Hold + or − for about 400 ms to begin repeating, then repeat steps occur every 80 ms.

Batch count, interval and travel distance can be edited independently. Changing the batch count no longer recalculates the other two fields. Multiplier previews continue to follow the chosen multiplier and mode.

## Extra spawns switch

Extra spawns is on by default. Turning it off suppresses native anti-rush, split-team/loner penalties, heat-based specialist injections and ordinary elite patrols. This includes the extra native injection after a lone player is pounced.

Selected-condition generators and native patrols explicitly required by a condition remain subject to their own rules. Mission and event spawns retain their separate controls. The switch applies next mission, survives condition changes and restoring defaults, and does not add a scan of every enemy on the map.

Scripted events controls only map-event waves, continuous reinforcements and event specialists. Rotten Armour, rituals and other condition effects remain active under their own rules. Named mission actors and objective logic are retained. This switch applies next mission and survives condition edits and generator resets.

Twin ambush is a separate switch, on by default. It controls only the twin ambush supplied by Havoc difficulty conditions. Turning it on uses the native probability and trigger; turning it off suppresses that ambush. It does not affect the dedicated Twins mission or twins added to a custom pool. Settings apply next mission and survive condition edits and generator resets.

## Requirements and installation

Requires Darktide Mod Loader, Darktide Mod Framework, SoloPlay and Havoc Condition Manager. For Realms co-op, also install Realms; SoloPlay remains required. The companion versions for this release are Solo Play 2.6.2 and Havoc Condition Manager 2.4.8.

## Vortex installation

- Close the game. Set up Darktide as a managed game in Vortex and install the requirements listed above, including Havoc Condition Manager.
- Download this mod's installation ZIP from Files. In Vortex, use Install From File to import it, then enable the mod and select Deploy Mods.
- Open Load Order and enable the relevant entries in this order: SoloPlay → HavocConditionManager → HavocEnemyDirector. Preserve your other mods.
- Start the game, open Havoc Condition Manager from Mod Options and use the side arrows to reach Advanced.

## Manual installation

- Close the game and install the requirements listed above, following each dependency's instructions.
- Open the Darktide game folder. In Steam: Properties → Installed Files → Browse.
- Open the game's mods folder and extract this ZIP there. Its top-level folder is HavocEnemyDirector. The resulting path must be mods/HavocEnemyDirector.
- Open mods/mod_load_order.txt and add HavocEnemyDirector on its own line after HavocConditionManager. SoloPlay must precede both. Preserve all other entries.
- Save the file, start the game and open the Advanced page in Havoc Condition Manager.

Open Havoc Condition Manager from Mod Options, choose your conditions and multipliers, then use the side arrows to reach Advanced. English, Simplified Chinese and Traditional Chinese follow the game language; restart after changing it.

## Framework switch

Use the enable/disable switch in Darktide Mod Framework. In the hub, it applies immediately. During a local or Realms mission, the switch is saved for the next mission; the current mission keeps its initialized condition and spawning configuration. A notification confirms a deferred change. Saved settings are retained.

Havoc Condition Manager 2.4.7 or newer must be installed and enabled. When the director is disabled, its Advanced page is hidden; the manager can still run in basic mode.

## Known issues and scope

A deleted travel generator can return after a difficulty change because some generator identifiers depend on difficulty. This remains unresolved in 1.5.7. Recheck the compiled generator list after changing difficulty; the mod should not be relied upon to enforce a Boss-only run.

Stranded-enemy cleanup or redeployment is not included. Higher caps can increase CPU load and frame time, especially at 5×; reduce caps or spawn rates if needed. This release supports SoloPlay and player-hosted Realms missions, with spawning controlled by the host. It does not claim official matchmaking support.

Code, condition-rule and simulated UI checks passed. There has been no new live-game test for this release. Other spawn overhauls can replace the same systems.

## Version 1.5.7

- Deleted custom generator numbers are now reused, starting with the lowest free number. Surviving generators keep their IDs; old saved counters are recalculated automatically.
- Added an Add unit selection menu and per-row add/remove buttons. Added units start at weight 1. Removing a unit affects only the current pool; global bans remain separate.
- Unit selection respects category, forced faction and condition replacement rules. Removed units cannot return through a source unit that conditions replace with them.
- Reused IDs start without deleted overrides. Updated English, Simplified Chinese and Traditional Chinese controls and offline UI previews. Changes apply next mission.

## Version 1.5.6

- Fixed batch-count edits unintentionally changing the default interval and travel distance. Typed input, clicks and held buttons edit each parameter independently; scaled previews still update.
- Scripted events now controls map-event waves, continuous reinforcements and event specialists, while preserving Rotten Armour, rituals and other condition effects.
- Added an independent Twin ambush switch, on by default, for Havoc difficulty ambushes. Named mission twins and custom unit pools are unaffected.
- Preserved all three switches through condition edits and generator resets. Added per-mission logs of their effective states and configuration revision.
- Retained named mission actors and objective progression. Settings apply next mission.

## Credits

Built for Havoc Condition Manager and deluxghost's Solo Play. Native systems and referenced assets: Fatshark. Game-source reference: Aussiemon/Darktide-Source-Code. This is an independent community project.
