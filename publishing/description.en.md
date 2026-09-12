# Havoc Enemy Director

Build named enemy formations, give each deployment its own schedule, and let an optional adaptive director vary the pressure in SoloPlay and Realms. HED also provides detailed editing of the game's native enemy templates and follows HCM's overall multipliers where you choose.

## DIY condition and talent integration

Havoc Condition Manager DIY conditions and Mortis DIY talents can request an existing named formation or an allowed enemy breed. Requests enter the director's normal admission and spawning flow, following live capacity, placement, phase and pacing requirements. A successful request means it was queued; it does not guarantee every requested enemy will appear.

The deployment editor and native-template rules support active condition IDs and named signals. Copy an ID, click the condition value and paste it. DIY pause actions can stop HED admission and pending creation; completion, expiration and mission cleanup release queued state. Requests have per-request, concurrent-state and mission limits to bound reinforcement chains.

The installation includes a documented API, editable JSON examples and three-language guides in docs/diy. Install the current HCM and Mortis DIY releases for their respective integrations; HCM remains required for HED. Ordinary DIY units retain a distinct source label through the shared spawn path; specialist and monster paths keep their native registration.

## Getting started

[color=#ff6666]Open Havoc Enemy Director from Mod Options, or open Detailed tuning in the local-game settings. The five sections are Director, Formation library, Deployment rules, Native templates, and Presets & changes.[/color]

- Create a formation and choose its enemy category, member types and count ranges.
- Create a deployment rule that references it. Choose elapsed time, forward progress, or a condition becoming true as the trigger.
- Set the earliest arrival, conditions and mission quota. Enable the extra director when the setup is ready.

The extra director starts disabled. Native template editing remains available independently. Settings save automatically and apply next mission; the running mission retains its starting configuration.

Click a number to type or paste, then press Enter or click outside to confirm. Esc cancels. Hold + or - for repeated adjustments. Click a formation or rule name to rename it; names support up to 48 characters. Lists and menus scroll when needed, and only the selected dropdown option is marked.

## Formation library

Keep up to 32 independent formations, with up to 64 deployment rules. Categories include: horde groups, trickle groups, specialists, monsters or patrols. A formation has up to eight weighted variants, with up to sixteen member types per variant. One encounter draws one variant; a member's minimum and maximum are counts, while the variant weight controls selection.

A formation can be called by several deployment rules. Duplicating a formation or rule creates a separate object. Each new deployment identity has its own random streams. A referenced formation must be unlinked by removing its deployment rules before it can be deleted.

Each variant supports up to 300 ordinary troops, 16 specialists or 3 monsters before runtime scaling. Monster formations support Plague Ogryns, Beasts of Nurgle and Chaos Spawn; mission actors and scripted bosses remain outside this library.

## Deployment rules

Each rule owns its first-arrival delay, later interval, cooldown, mission quota and active-encounter limit. Several rules can use the same formation without sharing these counters.

- Time: choose a minimum and maximum interval. The next interval starts with the first accepted member.
- Progress: choose the initial main-path distance and the additional travel for another encounter. Crossing several thresholds at once does not create a backlog.
- Condition edge: fire when the condition set becomes true. It must become false before it can trigger again.
- A time window, wave count and wave gap can further shape the encounter.

Combine up to eight conditions with All or Any. Conditions cover capable players, combat load, native pacing stage, monsters, mission events, native horde generation, coherency and route progress. By default they gate the start; continuing to check them after the first member arrives is optional. An encounter should not invalidate itself merely because its first monster has appeared.

The mission quota counts encounters with at least one accepted member. Zero means unlimited encounters for that rule. Pending and living encounters both occupy active limits. These limits are separate from member count and wave count.

When several rules qualify, choose priority followed by weight, or weight alone. Higher priority can keep lower-priority rules waiting. A phase requirement applies to the adaptive director.

## Adaptive pressure and arrival limits

Rule-driven mode follows the configured rules. Adaptive mode cycles through Build, Pressure and Recovery, with independent duration ranges, member multipliers and frequency multipliers. High combat load or too few capable players can start recovery early. Recovery ends only after its duration and low-load requirement are satisfied. A phase frequency of zero pauses additional HED submissions.

The director controls its extra formations. Native pacing and mission scripts continue to run. Global HED limits set admission spacing, active encounters, minimum capable players, combat load and whether extra arrivals may begin during mission events.

Ordinary members arrive through paced native spawning and groups. Patrols use native patrol behavior; specialists occupy available native slots; monsters use native monster registration. Ordinary and monster placement uses HCM's distance, visibility and navigation checks. Native specialist placement and protection rules can delay or change specialist arrivals.

One HED encounter is bounded to 256 ordinary troops, 16 specialists or 3 monsters across its waves. If the scaled force is too large, member counts are reduced proportionally; the number of waves is also bounded by this encounter budget. Waiting groups take turns. Unfulfilled requests expire instead of accumulating missed attacks. Already accepted native specialist slots keep their native lifecycle. HED-owned ordinary encounters stay outside HCM's automatic retirement/redeployment pool, preserving their independent active limits; native encounters retain HCM recovery.

## HCM linkage and native templates

A deployment can follow HCM member and frequency multipliers, then apply its own multipliers. Ordinary horde and trickle members follow their respective size controls; elites follow Elite members per group. Specialists follow slot capacity and monsters follow encounter count. Ordinary patrol members start at one. Horde, trickle and specialist intervals follow their matching frequency controls; other categories start at one. First-arrival delays, cooldowns and explicit wave settings retain their own values.

Native templates cover pacing and heat, roamers, hordes, specialists, monsters, automatic events, condition mechanics and supported mission combat nodes. Choose the family, mode and branch, then use Common, All or Edited fields. Resistance and challenge branches are labeled separately; they are not Havoc ranks.

For a native numeric field, choose Follow HCM, Use a fixed value, or Multiply the HCM value. Separate readouts show the original value, the HCM result and the HED template result. Percentages are displayed as percentages. Native identifiers can be shown in details.

Native encounter rules append to existing checks. Only supported coordinated-horde condition lists allow replacement. Selecting a template does not activate its source. Task objectives and unsupported function-driven fields remain under native control. The legacy concurrent-horde field is excluded from common controls because an active consumer was not confirmed in the audited source.

Difficulty, active conditions and runtime modifiers may still change a template's effect. Mission-event point budgets are not enemy counts: HCM's event multiplier also applies to the final native budget and cap.

## Seeds

The director seed and roamer-layout seed have separate fixed-seed switches. Off follows the mission seed; on enables integer input from 1 to 2147483646. Turning either switch off preserves its saved number. The director uses independent timer, variant and member-count streams for each stable deployment identity, without reseeding the game's global random generator.

Matching seeds and matching inputs reproduce HED choices. Player movement, native random decisions, rule competition and available locations can still change the final battle. The layout seed controls roamer placement; it does not select the mission map or seed every native system.

## Presets

Presets include HCM values, native fixed and relative overrides, native rules, formations, deployment rules, director settings, both HED seed switches and values, and the HCM condition-event seed setting. Older presets without the HCM seed keep its current setting. Mission, condition, faction and environment selections remain in SoloPlay.

Folder: %APPDATA%/Fatshark/Darktide/HavocEnemyDirector/templates

- Save under a name of up to 64 characters; overwriting requires confirmation.
- Select a file, review its summary and load it for the next mission.
- Share a JSON file or copy its share data. Import from the clipboard, or place a file in the folder and refresh. Importing does not load it automatically.
- Deleting a file requires confirmation and does not reset the currently loaded configuration.

Files are limited to 256 KiB. Native-editor presets from the previous format are migrated; unsupported old generator presets remain on disk. Invalid fields and incompatible members are rejected. Presets contain data and never execute Lua.

The library's full reset clears all HED settings, formations, rules and seeds, retaining HCM values and preset files. The director summary also has a separate reset for native overrides alone. Both resets require a second click.

## Requirements and compatibility

Requires Darktide Mod Loader, Darktide Mod Framework, SoloPlay and the current Havoc Condition Manager with shared navigation support. Realms is optional for player-hosted sessions. The local host owns gameplay changes; English, Simplified Chinese and Traditional Chinese follow the game language.

Use compatible companion versions and restart the game after installation. Other mods replacing the same native templates or scheduling methods may conflict. HCM can run alone when HED is disabled.

## Vortex installation

- Close the game and install the requirements. Import this ZIP with Install From File, enable it and select Deploy Mods.
- Use Load Order: SoloPlay → HavocConditionManager → HavocEnemyDirector.
- Restart the game and open Havoc Enemy Director from Mod Options.

## Manual installation

- Close the game. For an upgrade, remove the old HavocEnemyDirector installation folder before extracting the new ZIP. Saved settings and presets are stored separately.
- Extract into Darktide/mods, producing mods/HavocEnemyDirector.
- Add HavocEnemyDirector after HavocConditionManager in mods/mod_load_order.txt, with SoloPlay before both.
- Restart the game and open Havoc Enemy Director from Mod Options.

## Credits

SoloPlay: deluxghost. Native game systems and assets: Fatshark. Game-source reference: Aussiemon/Darktide-Source-Code.

