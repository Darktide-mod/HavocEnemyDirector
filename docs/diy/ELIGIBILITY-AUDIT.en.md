# Mortis eligibility audit

Compared MortisBuffManager 4.0.0 with local game Lua 1.12.5, commit `0f0cb45991e9305ef4a7b925370792d7d6035f95`. Fix: MortisBuffManager 4.0.1. This is a source audit with offline execution, not live gameplay acceptance.

Current behavior: eligibility precedes weights, total limits and exclusive groups. Mortis DIY now participates in the unified reward pool; tier is only a label. The following native eligibility audit remains applicable.

| Rule | Native behavior | Mod result |
| --- | --- | --- |
| Class | Generic plus current archetype legendary pools. | Already enforced for native rewards; now checked for DIY before manual/random selection, preview, host acceptance and application. |
| Blitz | Pool keyed by equipped ability `name`. | Native filtering retained; DIY adds `grenade_abilities`. |
| Combat ability | Pool keyed by equipped `ability_group`. | Native filtering retained; DIY adds `combat_abilities`. |
| Talents | Selected talent-specific rewards enter the pool. | Retained; false and zero do not count as selected. |
| Family | Selected-family rewards and independent legendary rewards. | Isolation retained. DIY family restrictions also apply before selection; an undetermined family cannot satisfy them. |
| Weapons | No universal equipment-compatibility filter in the native selector. | Eight audited secondary-slot dependencies are filtered; DIY gains explicit weapon, keyword and resource requirements. |
| Stale or duplicate rewards | Previously granted and backend-excluded entries are removed. | Retained; equipment changes invalidate shown cards before spending a round. Ineligible DIY entries consume no selection slots or exclusive groups. |
| Basic Ogryn box | Native selector grants a hidden cluster adapter. | Added to the custom award flow without using a reward slot; native-owned instances are preserved. |
| Combat conditions | Effects check conditions during combat. | Low health and similar transient conditions do not become opening eligibility requirements. An empty gun still has an ammunition mechanism. |

## Audited native weapon requirements

Secondary ammunition is required by `hordes_buff_auto_clip_fill_while_melee`, `hordes_buff_no_ammo_consumption_on_crits`, `hordes_buff_bonus_crit_chance_on_ammo`, `hordes_buff_melee_damage_missing_ammo_in_clip`, `hordes_buff_weakspot_ranged_hit_gives_infinite_ammo` and `hordes_buff_veteran_infinite_ammo_during_stance`. Existing class/ability restrictions remain in force.

A secondary reload action is required by `hordes_buff_increased_damage_after_reload` and `hordes_buff_improved_weapon_reload_on_melee_kill`. Staff builds cannot choose the cowboy family whose foundation requires ammunition; other families lose only incompatible entries. Plasma weapons have both ammunition and overheat mechanisms. This table records individually audited dependencies, not a claim of universal native compatibility detection.

## DIY declarations

All `availability` fields must pass. Lists for `archetypes`, `families`, `weapons`, `weapon_keywords`, `grenade_abilities` and `combat_abilities` each allow any listed match. Every `talents` and `resources` entry is required; `any_resources` needs at least one match.

Resources are `ammo`, `reload`, `overheat`, `warp_charge`, `grenade_charges`, `combat_ability`, `melee` and `ranged`. Warp charge belongs to the archetype, overheat to weapons, and grenade charges require a positive maximum charge count on the equipped Blitz. Exact weapon templates/keywords inspect both equipped slots and follow native progression-template priority.

Incomplete build data postpones selection. Hub checks use saved equipment; mission checks prefer live equipment. Mission choices remain fixed rather than rerolling when the build changes; incompatible effects are withdrawn, and the next mission checks the build again.

Known resource-dependent stats, keywords and self-resource actions infer hard requirements. Complex events, special keywords and weapon-specific mechanics still need explicit declarations by the author; registry membership does not guarantee arbitrary combinations work. `any_resources` supports explicitly authored alternative resource actions without bypassing passive requirements.

The 11 Mortis starter entries have updated declarations. Saved user libraries are preserved; inferred checks still apply, and exporting a new starter provides the new declarations. HCM global conditions do not use one player's Mortis eligibility. HCM 4.0.1 carries compatible shared modules and documentation; HED stays at 3.1.0.

## Evidence and limits

Offline checks cover 128 combinations against the actual native selector, all seven archetypes and 132 combinations from actual ability definitions, the native weapon resolver with source-extracted weapon metadata, and 1000 seeded DIY draws. Additional tests cover false/zero talents, pending equipment, stale cards, resource alternatives, host rejection of incompatible class/weapon requests, next-mission changes and basic-box adapter ownership. All three project regressions and six DIY suites are included.

Ability capture uses real ability definitions; rendering, attack actions and world services are outside that test boundary. Lifecycle services and network transport are simulated. SoloPlay and four-player Realms gameplay acceptance remain outstanding.

Native sources: `scripts/managers/mission_buffs/{mission_buffs_selector,mission_buffs_allowed_buffs,mission_buffs_settings}.lua`; actual effect implementations under `scripts/settings/buff/hordes_buffs/`; ability definitions under `scripts/settings/ability/player_abilities/abilities/`; and `scripts/utilities/weapon/weapon_template.lua`.

Mod sources: `modules/mortis_catalog.lua`, `mortis_draft.lua`, `mortis_buffs.lua`, `diy_mortis.lua`, and `modules/diy/diy_eligibility.lua`.
