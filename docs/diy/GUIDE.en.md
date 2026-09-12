# DIY talents and conditions

For MortisBuffManager 4.4.0, HavocConditionManager 4.3.0 and HavocEnemyDirector 3.2.0. The data contract is `Darktide.DIY` version `1`. Native API review uses game Lua 1.12.5, commit `0f0cb45991e9305ef4a7b925370792d7d6035f95`. Source, offline lifecycle and original native-method checks have passed. In-game multiplayer acceptance testing remains outstanding.

## Getting started

1. In the hub enter `/mortisbuffs`. The unified **Mortis talent pool** is available in preselection, progress and competition modes. Use **Package manager** to inspect automatically loaded packages, export a starter or convert clipboard JSON. HCM keeps its **DIY conditions** page.
2. The Mortis starter contains twelve examples, including `fivefold_salvo`; HCM contains 34. Complete data and executable Lua examples are in `package-examples/`. Each entry has its own folder with JSON, Lua and resources and can be installed or disabled independently.
3. Use the native and DIY source switches independently. The host alone edits room settings and per-entry DIY permissions; native talents have only a whole-pool switch. The list supports typed search, availability/source filters, details and batch operations across all filtered pages.
4. In preselection mode choose your talents before the mission. Native and DIY totals are separate. In progress/competition mode the reward cards combine eligible native and DIY entries; whenever native is enabled, the opening still selects a native family. Only-DIY play begins with a DIY choice. The list remains readable in all modes.
5. A DIY entry is available only when every human in the Realms room confirms the same entry package and dependency contents. Missing/different definitions are grey for everyone, with player names in the details. Other installed packages may differ; the entry package ID and contents must match. Every participant needs the current Mortis release; changing weight also changes the definition.
6. Start a new mission after configuration. Room controls and current selections lock during missions; refresh/import can stage packages for the next mission. HCM applies every enabled checked condition; Mortis uses the chosen reward mode. Each DIY talent costs one point, with a separate total default of six. Tier is a display label only; weighted draws have no tier quota. Exclusive groups and equipment eligibility still define which entries can enter the pool.

Folders:

```text
%APPDATA%/Fatshark/Darktide/MortisBuffManager/diy/packages/
%APPDATA%/Fatshark/Darktide/HavocConditionManager/diy/packages/
```

Packages load and merge automatically at startup. Refresh is for files added or changed in game. Invalid packages display their error and do not prevent independent valid packages from loading. Unselected entries remain inactive. JSON retains its strict data-only schema; optional local Lua executes through the versioned package API. See [PACKAGES.en.md](PACKAGES.en.md) for folder structure, dependencies, resources and executable examples.

Mortis combines native and DIY talents in its selected reward mode. It does not rewrite official talent trees, inventory or backend rewards. HCM DIY remains separate from official circumstances.

## Document contract

```json
{
  "format": "Darktide.DIY", "version": 1, "kind": "mortis",
  "id": "my_talents", "name": "My talents",
  "entries": [{
    "id": "steady", "name": "Steady aim",
    "description": "Reload speed increases by 10%.",
    "tier": 1, "passive": {"stats": {"reload_speed": 0.1}}
  }]
}
```

Use `kind: "conditions"` for HCM. The two kinds cannot be imported into one another.

| Scope | Fields |
| --- | --- |
| Document | Required format, version, kind, id, name, entries; optional description |
| Entry | Required id, name, description; optional enabled (true), tier (display label 1–4; default 1), weight (0–1000; default 1), exclusive_group, source_row |
| Applicability | targets, availability, conditions, match |
| Effects | passive, spawn, rules; at least one effective section is required |
| Passive | stats, keywords and/or modifiers |
| Spawn | HCM-only `health_multiplier` from 0.05 to 100; static targets only, incompatible with entry-level dynamic conditions |
| Rule | id, event, scope, interval, chance, cooldown, max_triggers, delay, conditions, match, actions |

IDs contain 1–64 bytes, start with a lowercase letter, and continue with lowercase letters, digits, `_` or `-`. Entry IDs must be unique within a library, and rule IDs within an entry. Name/description can be a string or a localization object with en, zh-cn and zh-tw keys; provide at least English or Simplified Chinese. Use `\n` for line breaks and ordinary `%` characters. Names are limited to 256 bytes, descriptions to 4096 bytes; the page displays a shorter details area while the file retains the full text.

For Mortis, the total limit, enabled flags and exclusive groups apply to both selection modes. HCM uses enabled flags and the checked list only. Weighted selection uses eligible pool entries and their positive weights; tier has no effect on selection or point cost. Identical canonical content, options and seed produce identical initial choices. Mortis availability is evaluated on the actual owner, so a randomly selected talent unavailable to that class is not automatically replaced.

### Selectors and conditions

`targets` defaults to `{"kind":"players"}`. Kinds are players/minions/all; Mortis entries must target players. Breeds and archetypes are lists of alternatives, tags must all match, exclude_tags reject any match, and different selector fields combine with AND. Identifiers must exist in `native-catalog.json`. Elites use `{"kind":"minions","tags":["elite"]}`.

Mortis-only `availability` can contain archetypes, families and talents arrays. All dimensions must match. Talents check the owner's profile values for true or a positive number; this does not grant those native talents. The native class and Mortis family IDs are included in the catalog.

A condition is `{"subject":"self","field":"health","op":"lt","value":0.5}`. Subject defaults to self, or may be target/attacker. Match defaults to all, or may be any. Missing data fails every comparison, including ne and not_contains.

| Fields | Meaning |
| --- | --- |
| health, toughness, corruption, ammo, stamina, warp_charge, overheat | Fractions from 0 to 1. Ammo reads the secondary weapon's clips plus reserve over total capacity |
| coherency | Native coherency count; examples require at least two, following the game's own count semantics |
| progress | Main-path progress in metres, not percent |
| load, players, monsters | Native challenge load, capable player count, aggroed monsters |
| elapsed | Seconds elapsed in the current DIY runtime instance |
| stage, phase | Native pacing state string; HED phase is build/pressure/recovery |
| breed, archetype, attack_type | Native identifiers; attack type must be supplied by the event |
| critical, weakspot | Boolean values supplied by the current event |
| sprinting, dodging, sliding, knocked_down | Current character state |
| in_combat | This runtime observed damage dealt/taken or a hit within eight seconds; not a new authoritative native combat state |
| native_condition, affix, signal, tag | Sets of official circumstance IDs, active HCM DIY entry IDs, unexpired signals and unit tags |
| event.FIELD | Whitelisted scalar event payload; 95 names/types are listed in the catalog. No individual event necessarily supplies all fields |

Numbers support eq/ne/gt/ge/lt/le; strings and booleans eq/ne; sets contains/not_contains. There are no arbitrary formulas, cross-unit numeric expressions or script execution.

### Native attributes and keywords

The catalog exposes 411 stat identifiers, 181 keywords and 105 native events. This is an expression surface, not a claim that every identifier affects every weapon, class, enemy or damage path. The relevant native consumer must read it. Specialized keywords may require additional native state or resources.

| Native type | Interpretation |
| --- | --- |
| additive_multiplier | Add a delta to the native multiplier. Example: reload_speed 0.1 adds 10%; recoil_modifier -0.5 subtracts 50 percentage points from that multiplier |
| multiplicative_multiplier | Multiply the native value and other layers. damage_taken_multiplier 0.8 multiplies incoming damage by 0.8 |
| value | Add a native numerical value. Its unit depends on the consumer; probability values commonly use 0.1 for ten percentage points |
| max_value | Take the maximum of native and DIY contributions; stack count does not repeatedly add it |

Each effect accepts at most 64 stats and 32 keywords. Individual values are bounded by -1000 and 1000; multiplicative/max values cannot be negative, and additive multiplier deltas cannot be below -1. Aggregate values are also bounded. Extreme values can exceed a native subsystem's practical assumptions.

Keywords are enabled by an array of identifiers. DIY cannot turn off a keyword owned by another native buff/mod. Removal withdraws only DIY's contribution. Modifiers include ammo_pickup_multiplier (0–10, multiplied across layers) and ammo_pickup_failure_chance (0–1, combined as one minus the product of success probabilities). Pickup scaling modifies the result of the native ammo pickup calculation; it does not disable medical or deployed crates.

### Rules and events

Rules default to chance 1, cooldown 0, max_triggers 0 (unlimited) and delay 0. The runtime still enforces a minimum 0.05-second interval per rule state. Cooldown allows 0–600 seconds, delay 0–120 seconds and max_triggers 0–10000. Conditions have independent all/any matching at entry and rule level. Scope defaults to unit; HCM can use global to share cooldown/count across event sources. Global scope still respects the entry selector. Mortis rules always belong to the selecting owner.

Five additional events supplement the native list:

- interval requires an interval of 0.1–600 seconds. A delayed update does not replay all missed periods.
- spawn observes player creation, and enemy creation in HCM.
- mission_start fires when the runtime first observes a player unit. A newly created respawn unit can produce it again; unit-scope max_triggers=1 is not a character-wide once-per-mission guarantee.
- enemy_died broadcasts a death. HCM self is the victim; Mortis self is each living talent owner. Use native on_kill for rewards belonging only to the killer. Target is the victim, and attacker is the source when available.
- signal is dispatched on the next update; filter event.signal_name. HCM global signal rules can run without a unit, so use target=players for team actions. Cross-mod integration shares signal state; it does not dispatch another mod's signal event.

Native proc parameters depend on the original event. Source_row is documentation metadata only.

### Complete action surface

Common target values are self (default), target, attacker, players, nearby_players, minions, nearby_minions and matching. Nearby targets are centred on self; radius defaults to eight metres and accepts 1–50. Matching uses the entry selector. Non-effect fanout is bounded to four players or 64 minions. Dead units do not receive resource, damage or native-status actions.

| Type | Fields and behavior |
| --- | --- |
| effect | Required effects and duration (0.1–600s), optional max_stacks (1–500; default 1) and refresh (true). Stacks share one expiry; false prevents refresh |
| heal | Nonnegative amount; native buff healing, respecting corruption, healing multipliers and prevention keywords |
| corruption | Nonnegative amount removes corruption through buff_corruption_healing across wound boundaries; does not separately restore ordinary health or inflict corruption |
| toughness | Positive recovery respects native modifiers; negative values apply native toughness damage and regeneration delay |
| ammo | Positive reserve addition; negative reserve-first, then clip removal across equipped weapon slots; rounded toward zero |
| grenades | Adjust native grenade ability charges within its actual capacity |
| ability_cooldown | Nonnegative seconds reduce combat ability cooldown; fraction uses its maximum cooldown |
| stamina | Add or consume native stamina, preserving cost modifiers and depletion events |
| warp_charge | Flat values are percentage points, fraction is 0–1. Positive values add peril without directly triggering explosion; negative values quell. Requires a native peril archetype |
| overheat | Flat values are percentage points, fraction is 0–1. Positive values follow native heat modifiers/lockout/explosion; negative values vent. Requires a secondary weapon with heat configuration |
| damage | Nonnegative direct health damage through a private native profile and the original attack path. Bypasses toughness, not necessarily every native reduction or immunity |
| kill | Explicit target or minion selector required, no amount. Restricted to ordinary freely spawnable catalog minions; cannot execute players or protected mission entities |
| native_buff | Name from 15 audited statuses; duration defaults to 10s, maximum 120s; count 1–10. Native expiry can occur earlier than DIY's removal deadline |
| signal | ID name and duration 0.1–600s publish a temporary state flag |
| pause_spawns | Name all/hordes/trickle_hordes/roamers/specials/monsters/hed and duration 0.1–600s. Holds permission checks and HED scheduling; does not remove existing enemies or promise to pause scripts bypassing Pacing |
| spawn_formation | Name is an existing HED formation ID in the frozen mission configuration; one scheduled request |
| spawn_enemy | Breed from 40 supported minions; count 1–16 for ordinary/special enemies, one monster per JSON action; uses HED placement/capacity/native slots |
| pickup | Native pickup name; count 1–4; drops beside the target rather than forcing it into inventory |
| sound | One of 456 native UI sound identifiers, played locally on the host; no external music loading |
| notification | Text string or localization object, maximum 512 bytes; local host notification |

Resource amount_kind defaults to flat. Fraction uses maximum capacity, not current holdings. Ammo alone supports current_fraction, for removing a fraction of remaining ammunition. Heal/toughness/damage support event_damage, multiplying event damage/damage_amount/damage_dealt by amount (0–5); missing damage means zero.

Signal, pause and spawn requests ignore target/radius; sound and notification execute once. Effect actions targeting players/minions/matching create a dynamic selector layer, so newly matching units can receive it during its lifetime. Nearby effects bind a finite set at activation. A temporary unit layer does not end early merely because the original trigger condition becomes false.

## HED integration

Spawn actions require HED with its director enabled. An unavailable director rejects requests instead of bypassing native placement. Native spawn pauses require enabled HCM. Mortis publishes its own signals and pause flags; HED reads its hed/all flags, and HCM merges Mortis signals/pauses with its own. Cross-mod flags are shared state, not executable requests from clients.

HCM exposes diy_api.version=1, active(), paused(family), context(table), emit_signal(name,duration) and status(). Active returns selected HCM IDs; context writes affix and signal sets. Mortis exposes paused(), context() and status(), sharing signals without presenting private talents as global affixes.

HED exposes status() and request(request):

```lua
local hed = get_mod("HavocEnemyDirector")
local ok, id_or_reason = hed.diy_api.request({
    breed = "chaos_poxwalker", count = 2,
    source = "my_mod/my_entry/my_rule", seed = 12345,
})
```

Only formation or breed (exclusive), count, source and seed are accepted. Formation count must be omitted or one. External breed requests allow at most 16 units or three monsters; JSON monster actions use one. Source permits letters, digits and `_:/-`, up to 192 bytes. Seed is an optional integer 1–2147483646; omission uses the director seed. True means admitted to the queue, not guaranteed creation. Failures include director_not_ready, request_target, request_breed, formation_missing, request_capacity and mission_request_budget.

HED rule editors support affix_active and signal_active; click the value to paste an ID. The starter signal uses diy_pressure. HCM enemy spawn events expose event.spawn_source: ordinary HED units use hed_director and ordinary DIY reinforcements hed_diy; other native sources retain their batch label or native. Monsters/specialists use separate native registration and slot paths, so those two labels are not guaranteed for them.

There are at most 128 accepted external requests per mission and 32 retained external states. A request can wait at most 120 seconds. Existing placement, visibility, route, per-breed capacity, live-group and paced submission limits still apply. Requests are not corpse-location cloning, strict FIFO, or guaranteed delivery.

## Multiplayer and lifecycle

Actions execute only with local SoloPlay/Realms host authority. Participating Realms clients need the corresponding current mod. Mortis also requires matching SHA-256 package and dependency fingerprints for an entry; the host approves IDs and freezes each character's choice for the mission. HCM is selected by the host, so clients need not load an identical conditions file.

Clients receive aggregate effects only for their own player, not executable programs. Packets validate host identity, membership, character, session nonce and increasing sequence. Effects expire after three seconds without a fresh state. Host snapshots run roughly every 0.5 seconds and the effect runtime roughly every 0.1 seconds; clients can observe that scale of delay. Prediction behavior, specialized keyword resources and complete four-player combat still require live testing.

Definitions limits: 512 KiB of combined normalized JSON, 30000 JSON nodes, depth 20, 128 entries, 16 rules/entry, eight actions/rule and 12 conditions/list. Each tick evaluates at most 128 triggers and executes 64 actions, with 512 queued actions, 128 layers per unit/global selector store, 256 tracked native statuses and 32 pickups per library/mission. Saturation can reject or defer work; this is not lossless capture of unlimited event traffic.

Exit, authority loss, disable and ownership withdrawal clean up owned temporary states and queues. Completed damage, healing, ammunition changes, pickups and spawned enemies are not rolled back. Native buff removal targets only indices allocated by this runtime.

Native player and minion classes are hooked separately because the game's class utility copies inherited methods. Selected enemy effects and rules keep otherwise-idle minion buff updates active, including enemies already present when the runtime starts. Both DIY mods share this update ownership. When the final owner stops, empty-buff enemies have their native stats reset and return to native idle behavior; enemies with native buffs retain native updates. Player-only passive libraries do not activate idle enemy updates. Broad enemy effects still add per-enemy work and should be profiled in a live dense encounter.

See IMAGE-ASSESSMENT.en.md for every supplied image row, including blank and underspecified entries, and NATIVE-CATALOG.en.md/native-catalog.json for identifiers. Fatal-hit interception, player bleeding, aggro resets, enemy transformation, projectiles/explosions, loot pools, HUD hiding, external media, inventory changes, mission interactions and vehicles require dedicated adapters. Extend the validated schema and native boundary together, with original-method tests and examples; change the schema version when changing semantics.


### Equipment eligibility before selection

`availability` is checked during manual selection, random preview, opening selection, host acceptance and application. All fields must pass. Ineligible entries leave the pool before totals or exclusive groups are consumed. Incomplete equipment postpones selection; accepted mission choices do not reroll when equipment changes.

| Field | Meaning |
| --- | --- |
| `archetypes` / `families` | Any listed class/family. An undetermined family cannot satisfy a family restriction. |
| `talents` | All listed native talents must be selected (true or a positive number). |
| `weapons` / `weapon_keywords` | Any listed native template/keyword across both equipped slots. |
| `grenade_abilities` | Exact equipped Blitz ability name. |
| `combat_abilities` | Equipped combat ability `ability_group`. |
| `resources` / `any_resources` | All / at least one listed resource mechanism must exist. |

Resources: `ammo`, `reload`, `overheat`, `warp_charge`, `grenade_charges`, `combat_ability`, `melee`, `ranged`. For example, `"availability":{"archetypes":["psyker"],"grenade_abilities":["psyker_throwing_knives"],"resources":["ammo","grenade_charges"]}` requires a Psyker with throwing knives and an ammunition weapon. Resource mechanisms are separate from current amounts; keep low-health and similar transient conditions in `conditions`.

Audited resource stats and self-resource actions infer hard requirements. Complex events, special keywords and weapon-specific mechanics still require explicit weapon/ability/talent declarations. `any_resources` supports alternative warp/overheat actions without bypassing passive requirements. See the [eligibility audit](ELIGIBILITY-AUDIT.en.md).

## Mortis weights, permissions and fivefold salvo

Set `weight` from 0 through 1000; the default is 1 and positive fractions are valid. Zero means manual selection only. In mixed non-route rewards, native candidates each weigh 1. Every card slot samples the remaining eligible candidates without replacement. With only weights 1, 2 and 7, first-slot probabilities are 10%, 20% and 70%; full three-card appearance probabilities differ. Native-only mode retains native category weighting. Family openings retain native family rules. Host exclusions, missing peer definitions and equipment eligibility are applied before drawing, with total/exclusive limits rechecked after every award.

Batch selection applies to every filtered result, across pages. Choose the personal preselection or the host's room DIY pool as the target. Native talents cannot be individually disabled by the host. Grey talents remain inspectable; notices are limited to players whose own saved/acquired choice becomes unavailable. Room policy changes do not rewrite saved personal selections.

`passive.modifiers.ranged_salvo_count` is a Mortis-only integer from 1 through 5. The fivefold example uses 5 and requires a ranged weapon. It produces five copies while paying the original shot cost once. Native additional projectiles multiply, giving ten projectiles for a Surge critical shot. Delayed staff projectiles retain their original charge. Shotgun copies share the original pellet pattern; fire and lightning repeat native pulses with native stack ceilings. Multiple copies of the modifier combine by maximum. This does not multiply melee, Blitz or combat ability attacks.

Only-DIY progress mode has at most ten awards and no native route grants. Mixed rewards use the shared round budget and the separate DIY point limit. Native and DIY switches cover all four on/off combinations. Both off suppresses both sources in this mod's supported managed Mortis flow.

Package limits and Lua API semantics are specified in PACKAGES.en.md. Script-only entries must declare their own class/weapon/resource availability when required.

Package management does not contain reward limits. In the Realms Mortis preparation controls, the host edits the independent DIY switch and point limit using minus/plus or direct numeric entry (0–99). Each DIY talent costs one point regardless of tier. SoloPlay has a separate Reward settings page. Tier is only a label; old saved tier quotas are ignored. HCM applies every enabled checked condition. Its list has no random-selection mode, seed or quantity quota; legacy weights and exclusion groups do not remove checked entries. Hover a row to inspect its details without changing selection. Files stay on the separate Package manager page.

## Seeds by manager

Use HCM Overall tuning → Random seeds for condition-event probability streams. Use HED Director → Seeds for its scheduling streams and native roamer layout, with separate switches. Off follows the mission seed; HCM draws a fallback once per mission if that seed is unavailable. On enables integer input from 1 to 2147483646. Turning off retains the saved number. Changes apply next mission. These seeds do not choose the mission map or control all native horde, specialist, monster and scripted-event randomness. Lua authors using native math.random directly keep that separate random source.
