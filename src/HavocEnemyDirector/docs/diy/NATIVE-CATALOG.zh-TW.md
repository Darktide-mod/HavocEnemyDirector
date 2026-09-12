# DIY 原生介面完整目錄

固定於遊戲 Lua 1.12.5，提交 `0f0cb45991e9305ef4a7b925370792d7d6035f95`。識別符號與型別來自原生原始碼；存在於目錄不保證所有消費者、武器、職業或特殊狀態都支援任意組合。

修改前請閱讀 GUIDE.zh-CN.md，準確複製識別符號；載入器會拒絕未知名稱。機器可讀檔案為 native-catalog.json 和 event-contracts.json；後者逐個列出原生事件欄位，只有標量白名單允許作為 event.FIELD 條件。

## 屬性 (411)

| ID | 型別／後設資料 |
| --- | --- |
| `ability_cooldown_flat_reduction` | value |
| `ability_cooldown_modifier` | additive_multiplier |
| `ability_extra_charges` | value |
| `alternate_fire_movement_speed_reduction_modifier` | multiplicative_multiplier |
| `ammo_reserve_capacity` | additive_multiplier |
| `ammo_usage` | multiplicative_multiplier |
| `arc_chain_damage` | additive_multiplier |
| `arc_grenade_extra_arcs` | value |
| `armored_damage` | additive_multiplier |
| `assist_speed_modifier` | additive_multiplier |
| `attack_speed` | additive_multiplier |
| `backstab_damage` | additive_multiplier |
| `backstab_rending_multiplier` | additive_multiplier |
| `berserker_damage` | additive_multiplier |
| `block_angle_modifier` | additive_multiplier |
| `block_cost_modifier` | additive_multiplier |
| `block_cost_multiplier` | multiplicative_multiplier |
| `block_cost_ranged_modifier` | additive_multiplier |
| `block_cost_ranged_multiplier` | multiplicative_multiplier |
| `burning_damage` | additive_multiplier |
| `burning_duration` | additive_multiplier |
| `chain_lightning_arc_rifle_max_angle` | value |
| `chain_lightning_arc_rifle_max_jumps` | value |
| `chain_lightning_arc_rifle_max_radius` | value |
| `chain_lightning_damage` | additive_multiplier |
| `chain_lightning_jump_time_multiplier` | multiplicative_multiplier |
| `chain_lightning_max_angle` | value |
| `chain_lightning_max_jumps` | value |
| `chain_lightning_max_radius` | value |
| `chain_lightning_powermaul_max_angle` | value |
| `chain_lightning_powermaul_max_jumps` | value |
| `chain_lightning_powermaul_max_radius` | value |
| `chain_lightning_staff_max_jumps` | value |
| `charge_level_modifier` | additive_multiplier |
| `charge_movement_reduction_multiplier` | multiplicative_multiplier |
| `charge_up_time` | additive_multiplier |
| `clip_size_modifier` | additive_multiplier |
| `close_range_rending_multiplier` | additive_multiplier |
| `coherency_radius_modifier` | additive_multiplier |
| `coherency_radius_multiplier` | multiplicative_multiplier |
| `coherency_stickiness_time_value` | value |
| `combat_ability_cooldown_modifier` | additive_multiplier |
| `combat_ability_cooldown_regen_modifier` | additive_multiplier |
| `combat_ability_cooldown_replenish_modifier` | additive_multiplier |
| `companion_damage_modifier` | additive_multiplier |
| `companion_damage_multiplier` | multiplicative_multiplier |
| `companion_damage_vs_elites` | additive_multiplier |
| `companion_damage_vs_melee` | additive_multiplier |
| `companion_damage_vs_ranged` | additive_multiplier |
| `companion_damage_vs_special` | additive_multiplier |
| `consumed_hit_mass_modifier` | multiplicative_multiplier |
| `consumed_hit_mass_modifier_on_kill` | multiplicative_multiplier |
| `consumed_hit_mass_modifier_on_ranged_critical_hit` | multiplicative_multiplier |
| `consumed_hit_mass_modifier_on_ranged_hit` | multiplicative_multiplier |
| `consumed_hit_mass_modifier_on_weakspot_hit` | multiplicative_multiplier |
| `corruption_taken_grimoire_multiplier` | multiplicative_multiplier |
| `corruption_taken_multiplier` | multiplicative_multiplier |
| `critical_strike_chance` | value |
| `critical_strike_chance_to_damage_convert` | value |
| `critical_strike_damage` | additive_multiplier |
| `critical_strike_rending_multiplier` | additive_multiplier |
| `critical_strike_weakspot_damage` | additive_multiplier |
| `cryptic_chordclaw_damage` | additive_multiplier |
| `damage` | additive_multiplier |
| `damage_far` | additive_multiplier |
| `damage_near` | additive_multiplier |
| `damage_taken_by_attack_valkyrie_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_armored_hound_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_armored_infected_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_beast_of_nurgle_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_daemonhost_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_hound_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_hound_mutator_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_lesser_mutated_poxwalker_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_mutated_poxwalker_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_mutator_daemonhost_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_mutator_ritualist_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_newly_infected_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_ogryn_bulwark_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_ogryn_executor_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_ogryn_gunner_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_ogryn_houndmaster_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_plague_ogryn_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_poxwalker_bomber_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_poxwalker_multiplier` | multiplicative_multiplier |
| `damage_taken_by_chaos_spawn_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_assault_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_berzerker_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_captain_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_flamer_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_grenadier_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_gunner_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_melee_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_mutant_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_mutant_mutator_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_ritualist_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_shocktrooper_multiplier` | multiplicative_multiplier |
| `damage_taken_by_cultist_vanguard_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_assault_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_berzerker_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_captain_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_executor_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_flamer_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_flamer_mutator_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_grenadier_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_gunner_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_melee_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_netgunner_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_plasma_gunner_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_radio_operator_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_rifleman_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_shocktrooper_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_sniper_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_twin_captain_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_twin_captain_two_multiplier` | multiplicative_multiplier |
| `damage_taken_by_renegade_vanguard_multiplier` | multiplicative_multiplier |
| `damage_taken_from_bleeding` | additive_multiplier |
| `damage_taken_from_burning` | additive_multiplier |
| `damage_taken_from_electrocution` | additive_multiplier |
| `damage_taken_from_explosions` | additive_multiplier |
| `damage_taken_from_kinetic` | additive_multiplier |
| `damage_taken_from_prop_explosions` | additive_multiplier |
| `damage_taken_from_toxic_gas_multiplier` | multiplicative_multiplier |
| `damage_taken_from_toxin` | additive_multiplier |
| `damage_taken_modifier` | additive_multiplier |
| `damage_taken_multiplier` | multiplicative_multiplier |
| `damage_taken_vs_taunted` | additive_multiplier |
| `damage_vs_attack_valkyrie` | additive_multiplier |
| `damage_vs_bleeding` | additive_multiplier |
| `damage_vs_burning` | additive_multiplier |
| `damage_vs_captains` | additive_multiplier |
| `damage_vs_chaos_armored_hound` | additive_multiplier |
| `damage_vs_chaos_armored_infected` | additive_multiplier |
| `damage_vs_chaos_beast_of_nurgle` | additive_multiplier |
| `damage_vs_chaos_daemonhost` | additive_multiplier |
| `damage_vs_chaos_hound` | additive_multiplier |
| `damage_vs_chaos_hound_mutator` | additive_multiplier |
| `damage_vs_chaos_lesser_mutated_poxwalker` | additive_multiplier |
| `damage_vs_chaos_mutated_poxwalker` | additive_multiplier |
| `damage_vs_chaos_mutator_daemonhost` | additive_multiplier |
| `damage_vs_chaos_mutator_ritualist` | additive_multiplier |
| `damage_vs_chaos_newly_infected` | additive_multiplier |
| `damage_vs_chaos_ogryn_bulwark` | additive_multiplier |
| `damage_vs_chaos_ogryn_executor` | additive_multiplier |
| `damage_vs_chaos_ogryn_gunner` | additive_multiplier |
| `damage_vs_chaos_ogryn_houndmaster` | additive_multiplier |
| `damage_vs_chaos_plague_ogryn` | additive_multiplier |
| `damage_vs_chaos_poxwalker` | additive_multiplier |
| `damage_vs_chaos_poxwalker_bomber` | additive_multiplier |
| `damage_vs_chaos_spawn` | additive_multiplier |
| `damage_vs_cultist_assault` | additive_multiplier |
| `damage_vs_cultist_berzerker` | additive_multiplier |
| `damage_vs_cultist_captain` | additive_multiplier |
| `damage_vs_cultist_flamer` | additive_multiplier |
| `damage_vs_cultist_grenadier` | additive_multiplier |
| `damage_vs_cultist_gunner` | additive_multiplier |
| `damage_vs_cultist_melee` | additive_multiplier |
| `damage_vs_cultist_mutant` | additive_multiplier |
| `damage_vs_cultist_mutant_mutator` | additive_multiplier |
| `damage_vs_cultist_ritualist` | additive_multiplier |
| `damage_vs_cultist_shocktrooper` | additive_multiplier |
| `damage_vs_cultist_vanguard` | additive_multiplier |
| `damage_vs_electrocuted` | additive_multiplier |
| `damage_vs_elites` | additive_multiplier |
| `damage_vs_healthy` | additive_multiplier |
| `damage_vs_heavy_staggered` | additive_multiplier |
| `damage_vs_horde` | additive_multiplier |
| `damage_vs_medium_staggered` | additive_multiplier |
| `damage_vs_monsters` | additive_multiplier |
| `damage_vs_nonthreat` | additive_multiplier |
| `damage_vs_ogryn` | additive_multiplier |
| `damage_vs_ogryn_and_monsters` | additive_multiplier |
| `damage_vs_renegade_assault` | additive_multiplier |
| `damage_vs_renegade_berzerker` | additive_multiplier |
| `damage_vs_renegade_captain` | additive_multiplier |
| `damage_vs_renegade_executor` | additive_multiplier |
| `damage_vs_renegade_flamer` | additive_multiplier |
| `damage_vs_renegade_flamer_mutator` | additive_multiplier |
| `damage_vs_renegade_grenadier` | additive_multiplier |
| `damage_vs_renegade_gunner` | additive_multiplier |
| `damage_vs_renegade_melee` | additive_multiplier |
| `damage_vs_renegade_netgunner` | additive_multiplier |
| `damage_vs_renegade_plasma_gunner` | additive_multiplier |
| `damage_vs_renegade_radio_operator` | additive_multiplier |
| `damage_vs_renegade_rifleman` | additive_multiplier |
| `damage_vs_renegade_shocktrooper` | additive_multiplier |
| `damage_vs_renegade_sniper` | additive_multiplier |
| `damage_vs_renegade_twin_captain` | additive_multiplier |
| `damage_vs_renegade_twin_captain_two` | additive_multiplier |
| `damage_vs_renegade_vanguard` | additive_multiplier |
| `damage_vs_specials` | additive_multiplier |
| `damage_vs_staggered` | additive_multiplier |
| `damage_vs_suppressed` | additive_multiplier |
| `damage_vs_unaggroed` | additive_multiplier |
| `disgustingly_resilient_damage` | additive_multiplier |
| `dodge_cooldown_reset_modifier` | additive_multiplier |
| `dodge_distance_modifier` | additive_multiplier |
| `dodge_linger_time` | value |
| `dodge_linger_time_modifier` | additive_multiplier |
| `dodge_linger_time_vs_melee` | value |
| `dodge_linger_time_vs_ranged` | value |
| `dodge_speed_multiplier` | multiplicative_multiplier |
| `elusiveness_modifier` | multiplicative_multiplier |
| `explosion_arming_distance_multiplier` | multiplicative_multiplier |
| `explosion_impact_modifier` | additive_multiplier |
| `explosion_radius_modifier` | additive_multiplier |
| `explosion_radius_modifier_frag` | additive_multiplier |
| `explosion_radius_modifier_shock` | additive_multiplier |
| `extra_consecutive_dodges` | value |
| `extra_grenade_throw_chance` | value |
| `extra_max_amount_of_grenades` | value |
| `extra_max_amount_of_wounds` | value |
| `finesse_ability_multiplier` | multiplicative_multiplier |
| `finesse_close_range_modifier` | additive_multiplier |
| `finesse_modifier_bonus` | additive_multiplier |
| `first_target_melee_damage_modifier` | additive_multiplier |
| `flanking_damage` | additive_multiplier |
| `flanking_rending_multiplier` | additive_multiplier |
| `force_staff_melee_damage` | additive_multiplier |
| `force_staff_secondary_damage` | additive_multiplier |
| `force_staff_single_target_damage` | additive_multiplier |
| `force_weapon_damage` | additive_multiplier |
| `fov_multiplier` | multiplicative_multiplier |
| `frag_damage` | additive_multiplier |
| `fully_charged_damage` | additive_multiplier |
| `grenade_ability_cooldown_modifier` | additive_multiplier |
| `healing_recieved_modifier` | additive_multiplier |
| `health_segment_damage_taken_multiplier` | multiplicative_multiplier |
| `hit_mass_multiplier` | multiplicative_multiplier |
| `hit_mass_multiplier_vs_melee` | multiplicative_multiplier |
| `hit_mass_multiplier_vs_ranged` | multiplicative_multiplier |
| `impact_modifier` | additive_multiplier |
| `increased_suppression` | additive_multiplier |
| `inner_push_angle_modifier` | additive_multiplier |
| `knocked_down_health_modifier` | additive_multiplier |
| `krak_damage` | additive_multiplier |
| `leadbelcher_chance_bonus` | value |
| `leech` | value |
| `lunge_distance` | value |
| `max_health_damage_taken_per_hit` | value |
| `max_health_damage_taken_per_hit_from_captains` | value |
| `max_health_damage_taken_per_hit_from_monsters` | value |
| `max_health_damage_taken_per_hit_from_ogryns` | value |
| `max_health_modifier` | additive_multiplier |
| `max_health_multiplier` | multiplicative_multiplier |
| `max_hit_mass_attack_modifier` | additive_multiplier |
| `max_hit_mass_impact_modifier` | additive_multiplier |
| `max_melee_hit_mass_attack_modifier` | additive_multiplier |
| `medical_crate_healing_modifier` | additive_multiplier |
| `melee_attack_speed` | additive_multiplier |
| `melee_critical_strike_chance` | value |
| `melee_critical_strike_damage` | additive_multiplier |
| `melee_damage` | additive_multiplier |
| `melee_damage_bonus` | value |
| `melee_damage_taken_modifier` | additive_multiplier |
| `melee_damage_taken_multiplier` | multiplicative_multiplier |
| `melee_finesse_modifier_bonus` | additive_multiplier |
| `melee_fully_charged_damage` | additive_multiplier |
| `melee_heavy_damage` | additive_multiplier |
| `melee_heavy_damage_vs_elites` | additive_multiplier |
| `melee_heavy_power_level_modifier` | additive_multiplier |
| `melee_heavy_rending_multiplier` | additive_multiplier |
| `melee_impact_modifier` | additive_multiplier |
| `melee_power_level_modifier` | additive_multiplier |
| `melee_rending_multiplier` | additive_multiplier |
| `melee_rending_vs_staggered_multiplier` | additive_multiplier |
| `melee_toughness_damage_taken_modifier` | additive_multiplier |
| `melee_toughness_damage_taken_multiplier` | multiplicative_multiplier |
| `melee_weakspot_damage` | additive_multiplier |
| `melee_weakspot_damage_vs_bleeding` | additive_multiplier |
| `melee_weakspot_damage_vs_staggered` | additive_multiplier |
| `melee_weakspot_damage_vs_toxin_status` | additive_multiplier |
| `melee_weakspot_impact_modifier` | additive_multiplier |
| `melee_weakspot_power_modifier` | additive_multiplier |
| `min_toughness_coherency_regen_rate_modifier` | additive_multiplier |
| `minion_accuracy_modifier` | multiplicative_multiplier |
| `minion_num_shots_modifier` | multiplicative_multiplier |
| `minion_shoot_cooldown_modifier` | multiplicative_multiplier |
| `monster_damage_taken_multiplier` | multiplicative_multiplier |
| `movement_speed` | additive_multiplier |
| `non_warp_damage_taken_multiplier` | multiplicative_multiplier |
| `ogryn_damage_taken_multiplier` | multiplicative_multiplier |
| `ogryn_friendly_rock_damage_modifier` | additive_multiplier |
| `ogryn_grenade_box_cluster_amount` | value |
| `opt_in_stagger_duration_multiplier` | multiplicative_multiplier |
| `outer_push_angle_modifier` | additive_multiplier |
| `overheat_amount` | multiplicative_multiplier |
| `overheat_dissipation_multiplier` | multiplicative_multiplier |
| `overheat_explosion_damage_modifier` | additive_multiplier |
| `overheat_explosion_radius_modifier` | additive_multiplier |
| `overheat_explosion_speed_modifier` | additive_multiplier |
| `overheat_immediate_amount` | multiplicative_multiplier |
| `overheat_immediate_amount_critical_strike` | multiplicative_multiplier |
| `overheat_over_time_amount` | multiplicative_multiplier |
| `perfect_block_timing` | value |
| `permanent_damage_converter` | value |
| `permanent_damage_converter_resistance` | value |
| `permanent_damage_ratio` | value |
| `pocketable_ability_cooldown_modifier` | additive_multiplier |
| `power_level` | value |
| `power_level_modifier` | additive_multiplier |
| `power_level_modifier_vs_aggroed_elites` | additive_multiplier |
| `power_level_modifier_vs_aggroed_monsters` | additive_multiplier |
| `psyker_force_field_movespeed_reduction_multiplier` | multiplicative_multiplier |
| `psyker_smite_cost_multiplier` | multiplicative_multiplier |
| `psyker_smite_max_hit_mass_attack_modifier` | additive_multiplier |
| `psyker_smite_max_hit_mass_impact_modifier` | additive_multiplier |
| `psyker_throwing_knife_speed_modifier` | additive_multiplier |
| `psyker_throwing_knives_damage_multiplier` | additive_multiplier |
| `push_cost_multiplier` | multiplicative_multiplier |
| `push_impact_modifier` | additive_multiplier |
| `push_speed_modifier` | additive_multiplier |
| `random_damage_immunity_chance` | value |
| `ranged_attack_speed` | additive_multiplier |
| `ranged_critical_strike_chance` | value |
| `ranged_critical_strike_damage` | additive_multiplier |
| `ranged_critical_strike_rending_multiplier` | additive_multiplier |
| `ranged_damage` | additive_multiplier |
| `ranged_damage_far` | additive_multiplier |
| `ranged_damage_taken_multiplier` | multiplicative_multiplier |
| `ranged_damage_vs_captains` | additive_multiplier |
| `ranged_damage_vs_monsters` | additive_multiplier |
| `ranged_damage_vs_ogryn` | additive_multiplier |
| `ranged_finesse_modifier_bonus` | additive_multiplier |
| `ranged_impact_modifier` | additive_multiplier |
| `ranged_max_hit_mass_attack_modifier` | additive_multiplier |
| `ranged_power_level_modifier` | additive_multiplier |
| `ranged_rending_multiplier` | additive_multiplier |
| `ranged_toughness_damage_taken_modifier` | additive_multiplier |
| `ranged_toughness_damage_taken_multiplier` | multiplicative_multiplier |
| `ranged_weakspot_damage` | additive_multiplier |
| `ranged_weakspot_damage_vs_staggered` | additive_multiplier |
| `recoil_modifier` | additive_multiplier |
| `reload_decrease_movement_reduction` | multiplicative_multiplier |
| `reload_speed` | additive_multiplier |
| `rending_multiplier` | additive_multiplier |
| `rending_vs_electrocuted_multiplier` | additive_multiplier |
| `rending_vs_staggered_multiplier` | additive_multiplier |
| `resistant_damage` | additive_multiplier |
| `revive_duration_multiplier` | multiplicative_multiplier |
| `revive_speed_modifier` | additive_multiplier |
| `shout_damage` | additive_multiplier |
| `shout_impact_modifier` | additive_multiplier |
| `shout_radius_modifier` | additive_multiplier |
| `smite_attack_speed` | additive_multiplier |
| `smite_damage` | additive_multiplier |
| `smite_damage_multiplier` | multiplicative_multiplier |
| `smite_same_target_discount` | multiplicative_multiplier |
| `smoke_fog_duration_modifier` | additive_multiplier |
| `spread_modifier` | additive_multiplier |
| `sprint_dodge_reduce_angle_threshold_rad` | max_value |
| `sprint_movement_speed` | additive_multiplier |
| `sprinting_cost_multiplier` | multiplicative_multiplier |
| `stagger_burning_reduction_modifier` | multiplicative_multiplier |
| `stagger_count_damage` | additive_multiplier |
| `stagger_duration_multiplier` | multiplicative_multiplier |
| `stagger_weakspot_reduction_modifier` | multiplicative_multiplier |
| `stamina_cost_multiplier` | multiplicative_multiplier |
| `stamina_modifier` | value |
| `stamina_regeneration_delay` | value |
| `stamina_regeneration_modifier` | additive_multiplier |
| `stamina_regeneration_multiplier` | multiplicative_multiplier |
| `static_movement_reduction_multiplier` | multiplicative_multiplier |
| `super_armor_crit_impact_modifier` | additive_multiplier |
| `super_armor_damage` | additive_multiplier |
| `suppression_dealt` | additive_multiplier |
| `suppressor_decay_multiplier` | multiplicative_multiplier |
| `sway_modifier` | multiplicative_multiplier |
| `syringe_duration` | value |
| `threat_weight_multiplier` | multiplicative_multiplier |
| `toughness` | value |
| `toughness_bonus` | additive_multiplier |
| `toughness_bonus_flat` | value |
| `toughness_coherency_regen_rate_modifier` | value |
| `toughness_coherency_regen_rate_multiplier` | additive_multiplier |
| `toughness_damage` | additive_multiplier |
| `toughness_damage_taken_modifier` | additive_multiplier |
| `toughness_damage_taken_multiplier` | multiplicative_multiplier |
| `toughness_extra_regen_rate` | value |
| `toughness_melee_replenish` | additive_multiplier |
| `toughness_regen_delay_modifier` | additive_multiplier |
| `toughness_regen_delay_multiplier` | multiplicative_multiplier |
| `toughness_regen_percent` | value |
| `toughness_regen_rate_modifier` | additive_multiplier |
| `toughness_regen_rate_multiplier` | multiplicative_multiplier |
| `toughness_replenish_modifier` | additive_multiplier |
| `toughness_replenish_multiplier` | multiplicative_multiplier |
| `toxin_power` | additive_multiplier |
| `unarmored_damage` | additive_multiplier |
| `vent_overheat_damage_multiplier` | multiplicative_multiplier |
| `vent_overheat_speed` | multiplicative_multiplier |
| `vent_warp_charge_damage_multiplier` | multiplicative_multiplier |
| `vent_warp_charge_decrease_movement_reduction` | multiplicative_multiplier |
| `vent_warp_charge_multiplier` | multiplicative_multiplier |
| `vent_warp_charge_speed` | multiplicative_multiplier |
| `warp_attacks_rending_multiplier` | additive_multiplier |
| `warp_charge_amount` | multiplicative_multiplier |
| `warp_charge_amount_smite` | multiplicative_multiplier |
| `warp_charge_block_cost` | multiplicative_multiplier |
| `warp_charge_dissipation_multiplier` | multiplicative_multiplier |
| `warp_charge_immediate_amount` | multiplicative_multiplier |
| `warp_charge_over_time_amount` | multiplicative_multiplier |
| `warp_damage` | additive_multiplier |
| `warp_damage_taken_multiplier` | multiplicative_multiplier |
| `weakspot_damage` | additive_multiplier |
| `weakspot_damage_taken` | additive_multiplier |
| `weakspot_power_level_modifier` | additive_multiplier |
| `weapon_action_movespeed_reduction_multiplier` | multiplicative_multiplier |
| `weapon_special_max_activations` | value |
| `wield_speed` | additive_multiplier |
| `windup_action_movespeed_reduction_multiplier` | multiplicative_multiplier |

## 關鍵詞 (181)

| ID | 型別／後設資料 |
| --- | --- |
| `adamant_dog_bloodlust` | — |
| `adamant_drone_shocks_enemies_in_range` | — |
| `adamant_hunt_stance` | — |
| `adamant_mine_explode_on_finish` | — |
| `adamant_terminus_warrant` | — |
| `allow_backstabbing` | — |
| `allow_extra_ability_charges` | — |
| `allow_flanking` | — |
| `allow_hipfire_during_sprint` | — |
| `armor_penetrating` | — |
| `beast_of_nurgle_liquid_immunity` | — |
| `beast_of_nurgle_vomit` | — |
| `bleeding` | — |
| `blessed_by_nurgle_parasite` | — |
| `block_gives_warp_charge` | — |
| `block_unblockable` | — |
| `bolstered` | — |
| `bolter_proficiency` | — |
| `broker_combat_ability_focus` | — |
| `broker_combat_ability_punk_rage` | — |
| `broker_punk_rage_exhaustion` | — |
| `broker_stimm_field_shocks_enemies_in_range` | — |
| `burning` | — |
| `can_attack_during_invisibility` | — |
| `can_block_ranged` | — |
| `cluster_explode_on_super_armored` | — |
| `coherency_with_all_no_chain` | — |
| `concealed` | — |
| `corrupted` | — |
| `count_as_blocking` | — |
| `count_as_blocking_vs_ranged` | — |
| `count_as_dodge_vs_all` | — |
| `count_as_dodge_vs_chaos_hound_pounce` | — |
| `count_as_dodge_vs_melee` | — |
| `count_as_dodge_vs_netgunner` | — |
| `count_as_dodge_vs_ranged` | — |
| `count_as_staggered` | — |
| `critical_hit_infinite_cleave` | — |
| `critical_melee_hit_infinite_cleave` | — |
| `critical_strike_second_projectile` | — |
| `cryptic_bionic_senses` | — |
| `cryptic_chordclaw` | — |
| `cryptic_chordclaw_kill_restores_charge` | — |
| `cryptic_discharge_ability_always_full_charges_bonus` | — |
| `cryptic_force_field_liquid_area_when_expired` | — |
| `cryptic_grenade_ability_force_field` | — |
| `cryptic_power_generation` | — |
| `cryptic_precision_stance` | — |
| `cryptic_precision_stance_duration_extension_on_elite_hit` | — |
| `cryptic_servo_skull_flamethrower_uses_no_charge` | — |
| `cultist_flamer_liquid_immunity` | — |
| `damage_immune` | — |
| `damage_volume_burning` | — |
| `damage_volume_electrical` | — |
| `damage_volume_instakill` | — |
| `damage_volume_radioactive` | — |
| `despawn_on_death` | — |
| `deterministic_recoil` | — |
| `disable_elite_minions_collision_during_dodge` | — |
| `disable_elite_minions_collision_during_sprint` | — |
| `disable_horde_minions_collision_during_dodge` | — |
| `disable_horde_minions_collision_during_sprint` | — |
| `disable_minions_collision_during_dodge` | — |
| `disable_minions_collision_during_sprint` | — |
| `double_ammo_consumption` | — |
| `electrocuted` | — |
| `electrocuted_arc` | — |
| `electrocuted_arc_ability` | — |
| `electrocuted_arc_grenade` | — |
| `electrocuted_chain_lightning` | — |
| `electrocuted_shock_mine` | — |
| `empowered` | — |
| `enable_auto_aim` | — |
| `expeditions_death_imminent` | — |
| `fire_trail_on_lunge` | — |
| `free_dodges` | — |
| `fully_charged_attacks_infinite_cleave` | — |
| `guaranteed_critical_strike` | — |
| `guaranteed_leadbelcher` | — |
| `guaranteed_melee_critical_strike` | — |
| `guaranteed_ranged_critical_strike` | — |
| `guaranteed_smite_critical_strike` | — |
| `guaranteed_weakspot_on_hit` | — |
| `guaranteed_wind_slash_critical_strike` | — |
| `has_nurgle_parasite` | — |
| `havoc_gardens_embrace` | — |
| `health_segment_breaking_reduce_damage_taken` | — |
| `hit_mass_reduction_on_weakspot_hit` | — |
| `hud_nameplates_disabled` | — |
| `ignore_armor_aborts_attack` | — |
| `ignore_armor_aborts_attack_critical_strike` | — |
| `improved_ammo_pickups` | — |
| `improved_medical_crate` | — |
| `in_toxic_gas` | — |
| `infested_head_armor_override` | — |
| `invisible` | — |
| `invulnerable` | — |
| `knock_down_on_slide` | — |
| `limit_health_damage_taken` | — |
| `limit_health_damage_taken_from_captains` | — |
| `limit_health_damage_taken_from_monsters` | — |
| `limit_health_damage_taken_from_ogryns` | — |
| `melee_alternate_fire_interrupt_immune` | — |
| `melee_infinite_cleave` | — |
| `melee_infinite_cleave_critical_strike` | — |
| `melee_infinite_cleave_on_headshot` | — |
| `melee_push_immune` | — |
| `no_ammo_consumption` | — |
| `no_ammo_consumption_on_crits` | — |
| `no_coherency_stickiness_limit` | — |
| `no_parry_block_cost` | — |
| `no_sprint` | — |
| `no_stagger` | — |
| `nurgle_flies` | — |
| `ogryn_basic_box_spawns_cluster` | — |
| `ogryn_box_of_surprise` | — |
| `ogryn_combat_ability_stance` | — |
| `ogryn_improved_lunge` | — |
| `plasma_proficiency` | — |
| `pocketable_broker_syringe` | — |
| `power_weapon_proficiency` | — |
| `prevent_all_healing` | — |
| `prevent_coherency_buffs_from_other_players` | — |
| `prevent_coherency_toughness_buff` | — |
| `prevent_critical_strike` | — |
| `prevent_healing_corruption` | — |
| `prevent_healing_health` | — |
| `prevent_toughness_regen_when_depleted` | — |
| `prevent_toughness_replenish` | — |
| `prevent_toughness_replenish_except_abilities` | — |
| `prevent_toughness_replenish_except_all_combat_abilities` | — |
| `psychic_fortress` | — |
| `psyker_chain_lightning_full_charge` | — |
| `psyker_empowered_grenade` | — |
| `psyker_overcharge` | — |
| `puked_on` | — |
| `random_damage_immune` | — |
| `ranged_alternate_fire_interrupt_immune` | — |
| `ranged_attack_infinite_cleave` | — |
| `ranged_push_immune` | — |
| `reduced_ammo_consumption` | — |
| `reduced_toughness_generation` | — |
| `renegade_flamer_liquid_immunity` | — |
| `renegade_grenadier_liquid_immunity` | — |
| `resist_death` | — |
| `rotten_armor` | — |
| `shock_grenade_shock` | — |
| `shout_forces_strong_stagger` | — |
| `slowdown_immune` | — |
| `special_ammo` | — |
| `sprint_dodge_in_overtime` | — |
| `sticky_projectiles` | — |
| `stimmed` | — |
| `stun_immune` | — |
| `stun_immune_block_broken` | — |
| `stun_immune_toughness_broken` | — |
| `super_armor_override` | — |
| `suppression_immune` | — |
| `syringe` | — |
| `syringe_ability` | — |
| `syringe_broker` | — |
| `syringe_power` | — |
| `syringe_speed` | — |
| `taunted` | — |
| `toxin` | — |
| `training_ground_force_companion_in_combat_state` | — |
| `uninterruptible` | — |
| `unperceivable` | — |
| `use_overheat_soft_lockout` | — |
| `use_reduced_hit_mass` | — |
| `uses_nearby_broadphase` | — |
| `veteran_combat_ability_stance` | — |
| `veteran_tag` | — |
| `warpfire_burning` | — |
| `weakspot_hit_gains_armor_penetration` | — |
| `weapon_malfunction` | — |
| `weapon_special_extra_explosion_on_hit_armor` | — |
| `zealot_channel_heals_corruption` | — |
| `zealot_maniac_empowered_martyrdom` | — |
| `zealot_toughness` | — |
| `zero_slide_friction` | — |

## 原生事件 (105)

| ID | 型別／後設資料 |
| --- | --- |
| `on_action_damage_target` | attacked_unit: unit; attacking_unit: unit; damage_type: string |
| `on_action_finish` | action_name: string; action_settings: table; charge_level: number |
| `on_action_start` | action_name: string; action_settings: table |
| `on_all_grimoires_picked_up` | unit: unit |
| `on_ally_knocked_down` | downed_unit: unit |
| `on_alternative_fire_start` | unit: unit |
| `on_ammo_consumed` | ammo_usage: number; charged_ammo: bool; is_critical_strike: bool; is_leadbelcher_shot: bool; num_shots_fired: number; saved_ammo: number; t: number |
| `on_ammo_pickup` | new_ammo_amount: number; pickup_amount: number; pickup_name: string |
| `on_bleed_on_activated_hit_trait_hit` | actual_damage_dealt: number; alternative_fire: bool; attack_direction: Vector3; attack_instigator_unit: unit; attack_instigator_unit_breed_name: string; attack_result: string; attack_type: string; attacked_unit: unit; attacking_unit: unit; attacking_unit_breed_name: string; breed_name: string; charge_level: number; close_explosion_hit: bool; damage: number; damage_efficiency: string; damage_profile: table; damage_type: string; hit_weakspot: bool; hit_world_position: Vector3; hit_zone_name: string; is_backstab: bool; is_critical_strike: bool; is_instakill: bool; melee_attack_strength: string; one_hit_kill: bool; overkill_damage: number; stagger_result: string; sticky_attack: bool; tags: table; target_index: number; weapon_special: bool |
| `on_bleeding_minion_death` | attack_type: string; attacking_unit: unit; bleed_stacks: number; breed_name: string; damage_profile_name: string; damage_type: string; dying_unit: unit; position: Vector3; side_name: string; tags: table |
| `on_block` | attack_type: string; attacking_unit: unit; block_broken: bool; block_cost: number |
| `on_buff_added` | template_name: string; unit: unit |
| `on_buff_stack_added` | template_name: string; unit: unit |
| `on_chain_lightning_finish` | unit: unit |
| `on_chain_lightning_jump` | unit: unit |
| `on_chain_lightning_start` | unit: unit |
| `on_coherency_enter` | enter_unit: unit; number_of_unit_in_coherency: unit |
| `on_coherency_exit` | exit_unit: unit; number_of_unit_in_coherency: unit |
| `on_coherency_player_block_broken_server` | attack_type: string; attacking_unit: unit; player_unit: unit |
| `on_combat_ability` | unit: unit; warp_charge_percent: number |
| `on_combat_ability_charge_consumed` | num_charges_consumed: number; unit: unit |
| `on_combat_ability_charge_replenished` | num_charges_gained: number; unit: unit |
| `on_critical_strike` | attack_type: string; attacking_unit: unit |
| `on_damage_dealt` | actual_damage_dealt: number; alternative_fire: bool; attack_direction: Vector3; attack_instigator_unit: unit; attack_result: string; attack_type: string; attacked_unit: unit; attacking_unit: unit; breed_name: string; charge_level: number; close_explosion_hit: bool; damage: number; damage_efficiency: string; damage_profile_name: string; damage_type: string; hit_weakspot: bool; hit_world_position: Vector3; is_backstab: bool; is_critical_strike: bool; melee_attack_strength: string; one_hit_kill: bool; stagger_result: string; sticky_attack: bool; tags: table; target_index: number; weapon_special: bool |
| `on_damage_taken` | attack_type: string; attacked_unit: unit; attacking_unit: unit; attacking_unit_owner_unit: unit; damage_amount: number; damage_profile_name: string; permanent_damage: number; toughness_damage_amount: number; will_die: bool |
| `on_death` | attack_type: string; attacking_unit: unit; breed_name: string; damage_profile_name: string; damage_type: string; dying_unit: unit; position: Vector3; side_name: string; tags: table |
| `on_deployable_placed` | deployable_name: string; life_time: number; position: Vector3 |
| `on_direct_flamer_hit` | — |
| `on_dodge_end` | — |
| `on_dodge_start` | — |
| `on_explosion_hit` | attack_instigator_unit: unit; attacking_unit: unit; charge_level: number; explosion_template_name: string; item_slot_origin: string; number_of_hit_units: number; weapon_special: bool |
| `on_grenade_ability_charge_consumed` | num_charges_consumed: number; unit: unit |
| `on_grenade_ability_charge_replenished` | num_charges_gained: number; unit: unit |
| `on_grenade_thrown` | unit: unit |
| `on_healing_taken` | heal_amount: number; heal_type: string |
| `on_hit` | actual_damage_dealt: number; alternative_fire: bool; attack_direction: Vector3; attack_instigator_unit: unit; attack_instigator_unit_breed_name: string; attack_result: string; attack_type: string; attacked_unit: unit; attacking_unit: unit; attacking_unit_breed_name: string; breed_name: string; charge_level: number; close_explosion_hit: bool; damage: number; damage_efficiency: string; damage_profile: table; damage_type: string; hit_weakspot: bool; hit_world_position: Vector3; hit_zone_name: string; is_backstab: bool; is_critical_strike: bool; is_instakill: bool; melee_attack_strength: string; one_hit_kill: bool; overkill_damage: number; stagger_result: string; sticky_attack: bool; tags: table; target_index: number; weapon_special: bool |
| `on_kill` | alternative_fire: bool; attack_direction: Vector3; attack_instigator_unit: unit; attack_instigator_unit_breed_name: string; attack_result: string; attack_type: string; attacked_unit: unit; attacked_unit_position: Vector3; attacking_unit: unit; attacking_unit_breed_name: string; breed_name: string; charge_level: number; close_explosion_hit: bool; damage: number; damage_efficiency: string; damage_type: string; hit_weakspot: bool; hit_world_position: Vector3; is_backstab: bool; is_critical_strike: bool; is_instakill: bool; melee_attack_strength: string; one_hit_kill: bool; overkill_damage: number; stagger_result: string; sticky_attack: bool; tags: table; target_index: number; weapon_special: bool |
| `on_lunge_aim_end` | — |
| `on_lunge_aim_start` | — |
| `on_lunge_end` | last_hit_unit: unit; lunge_direction: Vector3; lunge_template_name: string; lunging_unit: unit |
| `on_lunge_start` | lunge_direction: Vector3; lunge_template_name: string; lunging_unit: unit |
| `on_max_stack_refresh_buff` | template_name: string; unit: unit |
| `on_minion_damage_taken` | attack_type: string; attacked_unit: unit; attacking_unit: unit; attacking_unit_owner_unit: unit; damage_amount: number; damage_profile_name: string; keywords_on_death_or_nil: table; permanent_damage: number |
| `on_minion_death` | attack_type: string; attacking_unit: unit; breed_name: string; damage_profile_name: string; damage_type: string; dying_unit: unit; position: Vector3; side_name: string; tags: table |
| `on_ogryn_shout` | num_hits: number |
| `on_overheat_lockout` | — |
| `on_overheat_soft_lockout` | — |
| `on_pellet_hits` | attacked_unit: unit; damage: number; is_critical_strike: bool; max_number_of_pellets: number; number_of_pellets_hit: number |
| `on_perfect_block` | action_name: string; attacking_unit: unit; block_broken: bool; block_cost: number |
| `on_player_assist_done` | assist_type: string; assisted_unit: unit; interactor_unit: unit |
| `on_player_companion_knock_away` | companion_breed: string; companion_unit: unit; owner_unit: unit; target_unit_breed_name: string |
| `on_player_companion_pounce` | companion_breed: string; companion_unit: unit; owner_unit: unit; pounced_unit: unit; target_unit_breed_name: string |
| `on_player_companion_pounce_finish` | companion_breed: string; companion_unit: unit; owner_unit: unit; pounced_unit: unit; reason: string; target_unit_breed_name: string |
| `on_player_companion_spawn` | companion_breed_name: string; companion_unit: unit; owner_unit: unit |
| `on_player_grenade_exploded` | item_name: string; owner_unit: unit; position: Vector3; projectile_template: table; triggered_on_impact: bool |
| `on_player_hit_received` | alternative_fire: bool; attack_direction: Vector3; attack_instigator_unit: unit; attack_type: string; attacked_unit: unit; attacking_unit: unit; close_explosion_hit: bool; damage: number; damage_absorbed: number; damage_efficiency: string; damage_type: string; hit_weakspot: bool; is_backstab: bool; is_critical_strike: bool; melee_attack_strength: string; permanent_damage: number; result: string; sticky_attack: bool |
| `on_player_projectile_finished` | impact_hit: bool; num_impact_hit_elite: number; num_impact_hit_kill: number; num_impact_hit_minion: number; num_impact_hit_special: number; num_impact_hit_weakspot: number; projectile_name: string |
| `on_player_toughness_broken` | unit: unit |
| `on_projectile_stick` | owner_unit: unit; projectile_template_name: string; projectile_unit: unit; target_unit: unit |
| `on_psyker_force_field_equip` | — |
| `on_psyker_force_field_unequip` | — |
| `on_psyker_shout_finish` | num_hits: number |
| `on_psyker_shout_hit_ally` | ally_unit: unit |
| `on_pull_up` | target_unit: unit; unit: unit |
| `on_push_finish` | num_hit_units: number |
| `on_push_hit` | pushed_unit: unit; pushing_unit: unit; stagger_result: string |
| `on_ranged_dodge` | — |
| `on_reload` | shotgun: bool; weapon_template: table |
| `on_reload_finished` | shotgun: bool; weapon_template: table |
| `on_reload_start` | shotgun: bool; weapon_template: table |
| `on_remove_net` | target_unit: unit; unit: unit |
| `on_rescue` | target_unit: unit; unit: unit |
| `on_revive` | target_unit: unit; unit: unit |
| `on_shoot` | attacked_unit: unit; attacking_unit: unit; combo_count: number; hit_all_pellets: bool; hit_all_pellets_on_same: bool; hit_weakspot: bool; is_critical_strike: bool; num_hit_units: number; num_shots_fired: number |
| `on_shoot_finish` | — |
| `on_shoot_projectile` | attacking_unit: unit; combo_count: number; num_shots_fired: number; projectile_template_name: string |
| `on_shoot_start` | — |
| `on_side_mission_objective_complete` | unit: unit |
| `on_slide_end` | — |
| `on_slide_start` | — |
| `on_sprint_dodge` | — |
| `on_sprint_ended` | — |
| `on_sprint_started` | — |
| `on_stamina_depleted` | unit: unit |
| `on_successful_dodge` | attack_type: string; attacking_unit: unit; dodge_type: string; dodging_unit: unit |
| `on_sweep_finish` | combo_count: number; hit_weakspot: bool; is_heavy: bool; num_hit_units: number |
| `on_sweep_start` | combo_count: number; is_auto_completed: bool; is_chain_action: bool; is_heavy: bool; is_weapon_special_active: bool |
| `on_syringe_used` | — |
| `on_tag_unit` | tag_name: string; tagger_unit: unit; unit: unit |
| `on_toughness_replenished` | amount: number; reason: string; recovered_amount: number |
| `on_unit_enter_fog` | fog_owner_unit: unit; target_unit: unit |
| `on_unit_exit_fog` | fog_owner_unit: unit; target_unit: unit |
| `on_unit_leave_force_field` | force_field_owner_unit: unit; force_field_unit: unit; is_player_unit: bool; passing_unit: unit |
| `on_unit_touch_force_field` | force_field_owner_unit: unit; force_field_unit: unit; is_player_unit: bool; passing_unit: unit |
| `on_untag_unit` | tagger_unit: unit; unit: unit |
| `on_warp_charge_changed` | percentage_change: number |
| `on_warp_fire_applied` | buff_name: string; buffed_unit: unit; buffer_unit: unit |
| `on_weapon_chain_lightning_triggered` | — |
| `on_weapon_special_activate` | num_special_charges: number; t: number |
| `on_weapon_special_deactivate` | t: number |
| `on_wield` | weapon_template: table |
| `on_wield_melee` | previously_wielded_slot: string; weapon_template: table |
| `on_wield_ranged` | previously_wielded_slot: string; weapon_template: table |
| `on_windup_start` | combo_count: number |
| `on_windup_trigger` | — |

## 可用於條件的事件標量 (95)

| ID | 型別／後設資料 |
| --- | --- |
| `action_name` | string |
| `actual_damage_dealt` | number |
| `alternative_fire` | boolean |
| `ammo_usage` | number |
| `amount` | number |
| `assist_type` | string |
| `attack_instigator_unit_breed_name` | string |
| `attack_result` | string |
| `attack_type` | string |
| `attacking_unit_breed_name` | string |
| `bleed_stacks` | number |
| `block_broken` | boolean |
| `block_cost` | number |
| `breed_name` | string |
| `buff_name` | string |
| `charge_level` | number |
| `charged_ammo` | boolean |
| `close_explosion_hit` | boolean |
| `combo_count` | number |
| `companion_breed` | string |
| `companion_breed_name` | string |
| `damage` | number |
| `damage_absorbed` | number |
| `damage_amount` | number |
| `damage_efficiency` | string |
| `damage_profile_name` | string |
| `damage_type` | string |
| `deployable_name` | string |
| `dodge_type` | string |
| `explosion_template_name` | string |
| `heal_amount` | number |
| `heal_type` | string |
| `hit_all_pellets` | boolean |
| `hit_all_pellets_on_same` | boolean |
| `hit_weakspot` | boolean |
| `hit_zone_name` | string |
| `impact_hit` | boolean |
| `is_auto_completed` | boolean |
| `is_backstab` | boolean |
| `is_chain_action` | boolean |
| `is_critical_strike` | boolean |
| `is_heavy` | boolean |
| `is_instakill` | boolean |
| `is_leadbelcher_shot` | boolean |
| `is_player_unit` | boolean |
| `is_weapon_special_active` | boolean |
| `item_name` | string |
| `item_slot_origin` | string |
| `life_time` | number |
| `lunge_template_name` | string |
| `max_number_of_pellets` | number |
| `melee_attack_strength` | string |
| `new_ammo_amount` | number |
| `num_charges_consumed` | number |
| `num_charges_gained` | number |
| `num_hit_units` | number |
| `num_hits` | number |
| `num_impact_hit_elite` | number |
| `num_impact_hit_kill` | number |
| `num_impact_hit_minion` | number |
| `num_impact_hit_special` | number |
| `num_impact_hit_weakspot` | number |
| `num_shots_fired` | number |
| `num_special_charges` | number |
| `number_of_hit_units` | number |
| `number_of_pellets_hit` | number |
| `one_hit_kill` | boolean |
| `overkill_damage` | number |
| `percentage_change` | number |
| `permanent_damage` | number |
| `pickup_amount` | number |
| `pickup_name` | string |
| `previously_wielded_slot` | string |
| `projectile_name` | string |
| `projectile_template_name` | string |
| `reason` | string |
| `recovered_amount` | number |
| `result` | string |
| `saved_ammo` | number |
| `shotgun` | boolean |
| `side_name` | string |
| `signal_name` | string |
| `spawn_source` | string |
| `stagger_result` | string |
| `sticky_attack` | boolean |
| `t` | number |
| `tag_name` | string |
| `target_index` | number |
| `target_unit_breed_name` | string |
| `template_name` | string |
| `toughness_damage_amount` | number |
| `triggered_on_impact` | boolean |
| `warp_charge_percent` | number |
| `weapon_special` | boolean |
| `will_die` | boolean |

## 已知敵人篩選 (50)

| ID | 型別／後設資料 |
| --- | --- |
| `attack_valkyrie` | minion |
| `chaos_armored_hound` | disabler, minion, special |
| `chaos_armored_infected` | horde, melee, minion |
| `chaos_beast_of_nurgle` | minion, monster |
| `chaos_daemonhost` | minion, monster, witch |
| `chaos_hound` | disabler, minion, special |
| `chaos_hound_mutator` | disabler, minion, mutator, special |
| `chaos_lesser_mutated_poxwalker` | horde, melee, minion, poxwalker |
| `chaos_mutated_poxwalker` | horde, melee, minion, poxwalker |
| `chaos_mutator_daemonhost` | minion, monster, witch |
| `chaos_mutator_ritualist` | minion, ritualist |
| `chaos_newly_infected` | horde, melee, minion |
| `chaos_ogryn_bulwark` | bulwark, elite, melee, minion, ogryn |
| `chaos_ogryn_executor` | elite, melee, minion, ogryn |
| `chaos_ogryn_gunner` | elite, far, minion, ogryn |
| `chaos_ogryn_houndmaster` | melee, minion, monster, ogryn |
| `chaos_plague_ogryn` | minion, monster |
| `chaos_poxwalker` | horde, melee, minion, poxwalker |
| `chaos_poxwalker_bomber` | bomber, minion, scrambler, special |
| `chaos_spawn` | minion, monster |
| `cultist_assault` | close, far, minion, roamer |
| `cultist_berzerker` | elite, melee, minion |
| `cultist_captain` | cultist_captain, minion |
| `cultist_flamer` | minion, scrambler, special |
| `cultist_grenadier` | minion, special |
| `cultist_gunner` | elite, far, minion |
| `cultist_melee` | melee, minion, roamer |
| `cultist_mutant` | disabler, minion, special |
| `cultist_mutant_mutator` | disabler, minion, special |
| `cultist_ritualist` | minion, ritualist |
| `cultist_shocktrooper` | close, elite, minion |
| `cultist_vanguard` | melee, minion, roamer |
| `renegade_assault` | close, minion, roamer |
| `renegade_berzerker` | elite, melee, minion |
| `renegade_captain` | captain, minion |
| `renegade_executor` | elite, melee, minion |
| `renegade_flamer` | minion, scrambler, special |
| `renegade_flamer_mutator` | minion, mutator, scrambler, special |
| `renegade_grenadier` | minion, scrambler, special |
| `renegade_gunner` | elite, far, minion |
| `renegade_melee` | melee, minion, roamer |
| `renegade_netgunner` | disabler, minion, special |
| `renegade_plasma_gunner` | elite, exclude_for_havoc_speed_buff, far, minion |
| `renegade_radio_operator` | elite, far, minion |
| `renegade_rifleman` | far, minion, roamer |
| `renegade_shocktrooper` | close, elite, minion |
| `renegade_sniper` | minion, sniper, special |
| `renegade_twin_captain` | captain, minion |
| `renegade_twin_captain_two` | captain, minion |
| `renegade_vanguard` | melee, minion, roamer |

## 可自由生成的候選敵人 (40)

| ID | 型別／後設資料 |
| --- | --- |
| `chaos_armored_hound` | specials |
| `chaos_armored_infected` | hordes |
| `chaos_beast_of_nurgle` | monsters |
| `chaos_hound` | specials |
| `chaos_hound_mutator` | specials |
| `chaos_lesser_mutated_poxwalker` | hordes |
| `chaos_mutated_poxwalker` | hordes |
| `chaos_newly_infected` | hordes |
| `chaos_ogryn_bulwark` | hordes |
| `chaos_ogryn_executor` | hordes |
| `chaos_ogryn_gunner` | hordes |
| `chaos_plague_ogryn` | monsters |
| `chaos_poxwalker` | hordes |
| `chaos_poxwalker_bomber` | specials |
| `chaos_spawn` | monsters |
| `cultist_assault` | hordes |
| `cultist_berzerker` | hordes |
| `cultist_flamer` | specials |
| `cultist_grenadier` | specials |
| `cultist_gunner` | hordes |
| `cultist_melee` | hordes |
| `cultist_mutant` | specials |
| `cultist_mutant_mutator` | specials |
| `cultist_shocktrooper` | hordes |
| `cultist_vanguard` | hordes |
| `renegade_assault` | hordes |
| `renegade_berzerker` | hordes |
| `renegade_executor` | hordes |
| `renegade_flamer` | specials |
| `renegade_flamer_mutator` | specials |
| `renegade_grenadier` | specials |
| `renegade_gunner` | hordes |
| `renegade_melee` | hordes |
| `renegade_netgunner` | specials |
| `renegade_plasma_gunner` | hordes |
| `renegade_radio_operator` | hordes |
| `renegade_rifleman` | hordes |
| `renegade_shocktrooper` | hordes |
| `renegade_sniper` | specials |
| `renegade_vanguard` | hordes |

## 已審計原生狀態名稱 (15)

| ID | 型別／後設資料 |
| --- | --- |
| `bleed` | minions; scripts/settings/buff/weapon_buff_templates.lua |
| `bleed_long` | minions; scripts/settings/buff/weapon_buff_templates.lua |
| `flamer_assault` | minions; scripts/settings/buff/weapon_buff_templates.lua |
| `hordes_ailment_infinite_minion_bleed` | minions; scripts/settings/buff/hordes_buff_templates.lua |
| `hordes_ailment_minion_bleed` | minions; scripts/settings/buff/hordes_buff_templates.lua |
| `hordes_ailment_minion_burning` | minions; scripts/settings/buff/hordes_buff_templates.lua |
| `hordes_ailment_shock` | minions; scripts/settings/buff/hordes_buff_templates.lua |
| `mutator_stimmed_minion_blue` | minions; scripts/settings/buff/havoc_buff_templates.lua |
| `mutator_stimmed_minion_green` | minions; scripts/settings/buff/havoc_buff_templates.lua |
| `mutator_stimmed_minion_red` | minions; scripts/settings/buff/havoc_buff_templates.lua |
| `mutator_stimmed_minion_yellow` | minions; scripts/settings/buff/havoc_buff_templates.lua |
| `syringe_ability_boost_buff` | players; scripts/settings/buff/syringe_buff_templates.lua |
| `syringe_power_boost_buff` | players; scripts/settings/buff/syringe_buff_templates.lua |
| `syringe_speed_boost_buff` | players; scripts/settings/buff/syringe_buff_templates.lua |
| `warp_fire` | minions; scripts/settings/buff/weapon_buff_templates.lua |

## 拾取物 (9)

| ID | 型別／後設資料 |
| --- | --- |
| `ammo_cache_pocketable` | — |
| `large_clip` | — |
| `medical_crate_pocketable` | — |
| `small_clip` | — |
| `small_grenade` | — |
| `syringe_ability_boost_pocketable` | — |
| `syringe_corruption_pocketable` | — |
| `syringe_power_boost_pocketable` | — |
| `syringe_speed_boost_pocketable` | — |

## 本地介面音效 (456)

| ID | 型別／後設資料 |
| --- | --- |
| `ability_off_cooldown` | — |
| `add_profile_preset` | — |
| `apparel_enter` | — |
| `apparel_equip` | — |
| `apparel_equip_frame` | — |
| `apparel_equip_small` | — |
| `apparel_exit` | — |
| `apparel_select` | — |
| `apparel_zoom_in` | — |
| `apparel_zoom_out` | — |
| `aquilas_vendor_on_enter` | — |
| `aquilas_vendor_on_exit` | — |
| `aquilas_vendor_on_purchase` | — |
| `aquilas_vendor_purchase_aquilas` | — |
| `area_notification_popup_enter` | — |
| `barber_chirurgeon_on_enter` | — |
| `barber_chirurgeon_on_exit` | — |
| `character_appearance_change` | — |
| `character_appearence_confirm` | — |
| `character_appearence_enter` | — |
| `character_appearence_option_pressed` | — |
| `character_appearence_stop_voice_preview` | — |
| `character_create_abort` | — |
| `character_create_archetype_adamant` | — |
| `character_create_archetype_broker` | — |
| `character_create_archetype_confirm` | — |
| `character_create_archetype_cryptic` | — |
| `character_create_archetype_ogryn` | — |
| `character_create_archetype_pressed` | — |
| `character_create_archetype_psyker` | — |
| `character_create_archetype_veteran` | — |
| `character_create_archetype_zealot` | — |
| `character_create_class_confirm` | — |
| `character_create_class_select` | — |
| `character_create_confirm` | — |
| `character_create_enter` | — |
| `character_create_exit` | — |
| `character_create_hide_details` | — |
| `character_create_planet_select` | — |
| `character_create_show_details` | — |
| `character_create_toggle_class_description` | — |
| `cosmetics_vendor_on_enter` | — |
| `cosmetics_vendor_on_exit` | — |
| `cosmetics_vendor_show_with_gear` | — |
| `crafting_craft_button_activation` | — |
| `crafting_craft_button_deactivation` | — |
| `crafting_view_enhance_weapon` | — |
| `crafting_view_enhance_weapon_max` | — |
| `crafting_view_on_enter` | — |
| `crafting_view_on_exit` | — |
| `crafting_view_on_extract_trait` | — |
| `crafting_view_on_fuse_traits` | — |
| `crafting_view_on_replace_trait` | — |
| `crafting_view_on_reroll_perk` | — |
| `crafting_view_on_upgrade_item` | — |
| `crafting_view_sacrifice_weapon` | — |
| `credits_vendor_on_enter` | — |
| `credits_vendor_on_exit` | — |
| `credits_vendor_on_purchase` | — |
| `default_button_hovered` | — |
| `default_button_pressed` | — |
| `default_click` | — |
| `default_dropdown_expand` | — |
| `default_dropdown_minimize` | — |
| `default_menu_enter` | — |
| `default_menu_exit` | — |
| `default_mouse_hover` | — |
| `default_select` | — |
| `default_slider_drag` | — |
| `delete_character_confirm` | — |
| `emote_wheel_close` | — |
| `emote_wheel_entry_hover` | — |
| `emote_wheel_entry_select` | — |
| `emote_wheel_open` | — |
| `end_screen_enter` | — |
| `end_screen_exit` | — |
| `end_screen_item_drop_card_expand` | — |
| `end_screen_level_up_card_expand` | — |
| `end_screen_summary_card_expand` | — |
| `end_screen_summary_card_retract` | — |
| `end_screen_summary_card_slide_left` | — |
| `end_screen_summary_credits_progress` | — |
| `end_screen_summary_credits_start` | — |
| `end_screen_summary_credits_stop` | — |
| `end_screen_summary_credits_zero` | — |
| `end_screen_summary_currency_icon_in` | — |
| `end_screen_summary_currency_icon_out` | — |
| `end_screen_summary_currency_summation` | — |
| `end_screen_summary_diamantine_progress` | — |
| `end_screen_summary_diamantine_start` | — |
| `end_screen_summary_diamantine_stop` | — |
| `end_screen_summary_diamantine_zero` | — |
| `end_screen_summary_expeditions_credits_progress` | — |
| `end_screen_summary_expeditions_credits_start` | — |
| `end_screen_summary_expeditions_credits_stop` | — |
| `end_screen_summary_expeditions_credits_zero` | — |
| `end_screen_summary_expeditions_node_complete` | — |
| `end_screen_summary_expeditions_progress_progress` | — |
| `end_screen_summary_expeditions_progress_start` | — |
| `end_screen_summary_expeditions_progress_stop` | — |
| `end_screen_summary_expeditions_progress_zero` | — |
| `end_screen_summary_experience_progress` | — |
| `end_screen_summary_experience_start` | — |
| `end_screen_summary_experience_stop` | — |
| `end_screen_summary_experience_zero` | — |
| `end_screen_summary_level_up` | — |
| `end_screen_summary_mastery_bar_start` | — |
| `end_screen_summary_mastery_bar_stop` | — |
| `end_screen_summary_mastery_level_up` | — |
| `end_screen_summary_plasteel_progress` | — |
| `end_screen_summary_plasteel_start` | — |
| `end_screen_summary_plasteel_stop` | — |
| `end_screen_summary_plasteel_zero` | — |
| `end_screen_summary_reward_in_rarity_1` | — |
| `end_screen_summary_reward_in_rarity_2` | — |
| `end_screen_summary_reward_in_rarity_3` | — |
| `end_screen_summary_reward_in_rarity_4` | — |
| `end_screen_summary_reward_in_rarity_5` | — |
| `end_screen_summary_reward_in_rarity_6` | — |
| `end_screen_summary_xp_bar_progress` | — |
| `end_screen_summary_xp_bar_start` | — |
| `end_screen_summary_xp_bar_stop` | — |
| `expedition_compass_marker` | — |
| `expedition_menu_enter` | — |
| `expedition_menu_exit` | — |
| `expedition_menu_extraction` | — |
| `expedition_menu_keep_exploring` | — |
| `expedition_menu_select` | — |
| `expedition_menu_start` | — |
| `expedition_menu_vote_confirmed` | — |
| `expedition_menu_vote_tick` | — |
| `expedition_timer_end` | — |
| `expedition_timer_half` | — |
| `expedition_timer_running_out` | — |
| `expedition_timer_start` | — |
| `expedition_view_hover` | — |
| `expedition_view_select_locked` | — |
| `expedition_view_select_unlockable` | — |
| `expedition_view_select_unlocked` | — |
| `expedition_view_select_unlocked_end` | — |
| `expedition_view_select_unlocked_loop` | — |
| `expedition_view_unlocking` | — |
| `finalize_creation_confirm` | — |
| `group_finder_enter` | — |
| `group_finder_exit` | — |
| `group_finder_filter_list_back` | — |
| `group_finder_filter_list_category_pressed` | — |
| `group_finder_filter_list_tag_deselected` | — |
| `group_finder_filter_list_tag_selected` | — |
| `group_finder_group_element_selected` | — |
| `group_finder_incoming_request` | — |
| `group_finder_own_group_advertisement_start` | — |
| `group_finder_own_group_advertisement_stop` | — |
| `group_finder_refresh_group_list` | — |
| `group_finder_request_button_accept` | — |
| `group_finder_request_button_decline` | — |
| `group_finder_request_to_join_group` | — |
| `havoc_charge_change` | — |
| `havoc_eor_card_full` | — |
| `havoc_eor_card_short` | — |
| `havoc_eor_rank_down` | — |
| `havoc_eor_rank_up` | — |
| `havoc_terminal_deny_mission` | — |
| `havoc_terminal_enter` | — |
| `havoc_terminal_exit` | — |
| `havoc_terminal_rank_down` | — |
| `havoc_terminal_rank_up` | — |
| `havoc_terminal_rank_up_final_tier` | — |
| `havoc_terminal_rank_up_next_tier` | — |
| `havoc_terminal_start_mission` | — |
| `havoc_weekly_reward` | — |
| `horde_new_objective` | — |
| `horde_wave_completed` | — |
| `interact_popup_enter` | — |
| `interact_popup_exit` | — |
| `interaction_view_internal_back` | — |
| `interaction_view_internal_enter` | — |
| `item_result_overlay_reward_in_rarity_1` | — |
| `item_result_overlay_reward_in_rarity_2` | — |
| `item_result_overlay_reward_in_rarity_3` | — |
| `item_result_overlay_reward_in_rarity_4` | — |
| `item_result_overlay_reward_in_rarity_5` | — |
| `item_result_overlay_reward_in_rarity_6` | — |
| `main_menu_enter` | — |
| `main_menu_exit` | — |
| `main_menu_select_character` | — |
| `main_menu_start_button_hover_enter` | — |
| `main_menu_start_button_hover_leave` | — |
| `main_menu_start_game` | — |
| `mark_vendor_on_enter` | — |
| `mark_vendor_on_exit` | — |
| `mark_vendor_on_purchase` | — |
| `mark_vendor_replace_contract` | — |
| `mastery_empower_weapon` | — |
| `mastery_empower_weapon_max` | — |
| `mastery_select_weapon` | — |
| `mastery_trait_unlock_blocked` | — |
| `mastery_trait_unlocked` | — |
| `mastery_trait_unlocked_rank_2` | — |
| `mastery_trait_unlocked_rank_3` | — |
| `mastery_trait_unlocked_rank_4` | — |
| `mastery_traits_rank_up` | — |
| `mastery_traits_rank_up_max` | — |
| `mission_board_enter` | — |
| `mission_board_exit` | — |
| `mission_board_hide_icon` | — |
| `mission_board_node_hover` | — |
| `mission_board_node_pressed` | — |
| `mission_board_receiving` | — |
| `mission_board_receiving_soon` | — |
| `mission_board_show_icon` | — |
| `mission_board_start_mission` | — |
| `mission_briefing_start` | — |
| `mission_briefing_stop` | — |
| `mission_buffs_buff_hold_start` | — |
| `mission_buffs_buff_hold_stop` | — |
| `mission_buffs_buff_hover_enter` | — |
| `mission_buffs_enter` | — |
| `mission_buffs_exit` | — |
| `mission_buffs_family_blessing_chosen` | — |
| `mission_buffs_generic_blessing_chosen` | — |
| `mission_buffs_timer_1_secs_left` | — |
| `mission_buffs_timer_2_secs_left` | — |
| `mission_buffs_timer_3_secs_left` | — |
| `mission_buffs_timer_4_secs_left` | — |
| `mission_buffs_timer_end` | — |
| `mission_lobby_abort` | — |
| `mission_lobby_all_players_ready` | — |
| `mission_lobby_matchmade_players_join` | — |
| `mission_lobby_player_ready` | — |
| `mission_lobby_player_unready` | — |
| `mission_lobby_ready_up` | — |
| `mission_lobby_unready` | — |
| `mission_objective_popup_complete` | — |
| `mission_objective_popup_new` | — |
| `mission_objective_popup_new_expeditions` | — |
| `mission_objective_popup_part_complete` | — |
| `mission_vote_player_declined` | — |
| `mission_vote_popup_accept` | — |
| `mission_vote_popup_decline` | — |
| `mission_vote_popup_enter` | — |
| `mission_vote_popup_hide_details` | — |
| `mission_vote_popup_show_details` | — |
| `news_feed_slide_enter` | — |
| `news_feed_slide_exit` | — |
| `news_popup_enter` | — |
| `news_popup_exit` | — |
| `news_popup_slide_next` | — |
| `news_popup_slide_previous` | — |
| `notification_achievement` | — |
| `notification_assist_assisted` | — |
| `notification_assist_cleansed` | — |
| `notification_assist_gifted` | — |
| `notification_assist_rescued` | — |
| `notification_assist_revived` | — |
| `notification_assist_saved` | — |
| `notification_collectible_pickup` | — |
| `notification_collectible_pickup_helped` | — |
| `notification_cosmetic_received` | — |
| `notification_crafting_material_recieved_diamantine` | — |
| `notification_crafting_material_recieved_pasteel` | — |
| `notification_currency_recieved` | — |
| `notification_default_enter` | — |
| `notification_default_exit` | — |
| `notification_destroyed_destructible` | — |
| `notification_expedition_currency_recieved_loot` | — |
| `notification_expedition_currency_recieved_salvage` | — |
| `notification_invite_canceled` | — |
| `notification_item_received_rarity_1` | — |
| `notification_item_received_rarity_2` | — |
| `notification_item_received_rarity_3` | — |
| `notification_item_received_rarity_4` | — |
| `notification_item_received_rarity_5` | — |
| `notification_item_received_rarity_6` | — |
| `notification_join_party_failed` | — |
| `notification_matchmaking_failed` | — |
| `notification_player_join_party` | — |
| `notification_player_leave_party` | — |
| `notification_trait_received_rarity_1` | — |
| `notification_trait_received_rarity_2` | — |
| `notification_trait_received_rarity_3` | — |
| `notification_trait_received_rarity_4` | — |
| `notification_warning` | — |
| `notification_weapon_skin_received` | — |
| `onboarding_popup_message_enter` | — |
| `onboarding_popup_message_exit` | — |
| `options_slider_master_click` | — |
| `options_slider_master_drag` | — |
| `options_slider_master_release` | — |
| `options_slider_music_click` | — |
| `options_slider_music_drag` | — |
| `options_slider_music_release` | — |
| `options_slider_sfx_click` | — |
| `options_slider_sfx_drag` | — |
| `options_slider_sfx_release` | — |
| `options_slider_vo_click` | — |
| `options_slider_vo_release` | — |
| `options_slider_voip_click` | — |
| `options_slider_voip_drag` | — |
| `options_slider_voip_release` | — |
| `penance_menu_carousel_hovered` | — |
| `penance_menu_carousel_move_pass` | — |
| `penance_menu_carousel_move_start` | — |
| `penance_menu_carousel_move_stop` | — |
| `penance_menu_enter` | — |
| `penance_menu_exit` | — |
| `penance_menu_penance_complete` | — |
| `penance_menu_penance_hover` | — |
| `penance_menu_penance_track` | — |
| `penance_menu_penance_untrack` | — |
| `penance_menu_reward_scroll` | — |
| `penance_menu_wintrack_bar_progress` | — |
| `penance_menu_wintrack_bar_start` | — |
| `penance_menu_wintrack_bar_stop` | — |
| `penance_menu_wintrack_level_up` | — |
| `penance_menu_wintrack_move_page` | — |
| `penance_menu_wintrack_page_button_hovered` | — |
| `penance_menu_wintrack_page_button_pressed` | — |
| `penance_menu_wintrack_reward_claim` | — |
| `penance_menu_wintrack_reward_claim_button_activate` | — |
| `penance_menu_wintrack_reward_claimed` | — |
| `penance_menu_wintrack_reward_reached` | — |
| `play_ui_character_create_select_cartel_iron` | — |
| `play_ui_character_create_select_cartel_show` | — |
| `play_ui_character_create_select_cartel_threadlighties` | — |
| `play_ui_character_create_select_cartel_water` | — |
| `play_ui_character_create_select_forge_world_01` | — |
| `play_ui_character_create_select_forge_world_02` | — |
| `play_ui_character_create_select_forge_world_03` | — |
| `play_ui_character_create_select_forge_world_04` | — |
| `play_ui_live_event_resource_pledged_01` | — |
| `play_ui_live_event_resource_pledged_02` | — |
| `profile_preset_clicked` | — |
| `prologue_tutorial_message_enter` | — |
| `prologue_tutorial_message_exit` | — |
| `remove_profile_preset` | — |
| `rumble_changed` | — |
| `rumble_enabled` | — |
| `rumble_enabled_ps5` | — |
| `smart_tag_hud_default` | — |
| `smart_tag_location_attention_enter` | — |
| `smart_tag_location_attention_enter_others` | — |
| `smart_tag_location_default_enter` | — |
| `smart_tag_location_default_enter_others` | — |
| `smart_tag_location_threat_enter` | — |
| `smart_tag_location_threat_enter_others` | — |
| `smart_tag_pickup_default_enter` | — |
| `smart_tag_pickup_default_enter_others` | — |
| `social_menu_block_player` | — |
| `social_menu_cancel_friend_request` | — |
| `social_menu_cancel_invite` | — |
| `social_menu_cycle_sort_method` | — |
| `social_menu_friend_request_accept` | — |
| `social_menu_friend_request_reject` | — |
| `social_menu_initiate_kick_vote` | — |
| `social_menu_leave_party` | — |
| `social_menu_mute_player_text` | — |
| `social_menu_mute_player_voice` | — |
| `social_menu_popup_button_hovered` | — |
| `social_menu_popup_button_pressed` | — |
| `social_menu_popup_enter` | — |
| `social_menu_popup_exit` | — |
| `social_menu_receive_invite` | — |
| `social_menu_see_player_profile` | — |
| `social_menu_send_friend_request` | — |
| `social_menu_send_invite` | — |
| `social_menu_unblock_player` | — |
| `social_menu_unfriend_player` | — |
| `social_menu_unmute_player_text` | — |
| `social_menu_unmute_player_voice` | — |
| `special_assignment_mission_board_enter` | — |
| `special_assignment_mission_board_exit` | — |
| `special_assignment_mission_board_vox_hover` | — |
| `stimm_talent_node_add_point` | — |
| `stimm_talent_node_base_unlock` | — |
| `stimm_talent_node_select_ability` | — |
| `stimm_talent_node_select_aura` | — |
| `stimm_talent_node_select_default` | — |
| `stimm_talent_node_select_keystone` | — |
| `stop_ui_character_create_select_cartel_loops` | — |
| `stop_ui_character_create_select_forge_world_loops` | — |
| `story_mission_enter` | — |
| `story_mission_exit` | — |
| `story_mission_lore_screen_enter` | — |
| `story_mission_lore_screen_exit` | — |
| `story_mission_lore_screen_play_video` | — |
| `story_mission_open_mission_board_button` | — |
| `story_mission_option_mouse_hover` | — |
| `story_mission_option_selected` | — |
| `story_mission_start_button_activation` | — |
| `story_mission_start_mission` | — |
| `summary_popup_enter` | — |
| `summary_popup_exit` | — |
| `switch_profile_preset` | — |
| `system_menu_enter` | — |
| `system_menu_exit` | — |
| `system_popup_enter` | — |
| `system_popup_exit` | — |
| `tab_button_hovered` | — |
| `tab_button_pressed` | — |
| `tab_secondary_button_hovered` | — |
| `tab_secondary_button_pressed` | — |
| `talent_last_point_spent` | — |
| `talent_menu_enter` | — |
| `talent_menu_exit` | — |
| `talent_node_add_point` | — |
| `talent_node_clear` | — |
| `talent_node_clear_all` | — |
| `talent_node_click` | — |
| `talent_node_hover_default` | — |
| `talent_node_line_connection_start` | — |
| `talent_node_line_connection_stop` | — |
| `talent_node_select_ability` | — |
| `talent_node_select_aura` | — |
| `talent_node_select_default` | — |
| `talent_node_select_keystone` | — |
| `talent_node_select_stat` | — |
| `talent_node_select_tactical` | — |
| `talents_equip_talent` | — |
| `talents_talent_hover` | — |
| `talents_unequip_talent` | — |
| `title_equip` | — |
| `title_screen_continue` | — |
| `title_screen_enter` | — |
| `title_screen_exit` | — |
| `tutorial_popup_enter` | — |
| `tutorial_popup_exit` | — |
| `tutorial_popup_slide_next` | — |
| `tutorial_popup_slide_previous` | — |
| `weapons_customize_enter` | — |
| `weapons_customize_exit` | — |
| `weapons_discard_back` | — |
| `weapons_discard_complete` | — |
| `weapons_discard_continue` | — |
| `weapons_discard_enter` | — |
| `weapons_discard_exit` | — |
| `weapons_discard_hold` | — |
| `weapons_discard_release` | — |
| `weapons_enter` | — |
| `weapons_equip_gadget` | — |
| `weapons_equip_mark` | — |
| `weapons_equip_weapon` | — |
| `weapons_exit` | — |
| `weapons_favorite` | — |
| `weapons_select_weapon` | — |
| `weapons_skin_confirm` | — |
| `weapons_skin_select` | — |
| `weapons_swap` | — |
| `weapons_switch_mark` | — |
| `weapons_trinket_select` | — |
| `wintrack_item_reward_overlay_in_rarity_1` | — |
| `wintrack_item_reward_overlay_in_rarity_2` | — |
| `wintrack_item_reward_overlay_in_rarity_3` | — |
| `wintrack_item_reward_overlay_in_rarity_4` | — |
| `wintrack_item_reward_overlay_in_rarity_5` | — |
| `wintrack_item_reward_overlay_in_rarity_6` | — |

## 職業 (7)

| ID | 型別／後設資料 |
| --- | --- |
| `adamant` | — |
| `broker` | — |
| `cryptic` | — |
| `ogryn` | — |
| `psyker` | — |
| `veteran` | — |
| `zealot` | — |

## 死靈流派 (7)

| ID | 型別／後設資料 |
| --- | --- |
| `cowboy` | — |
| `critical` | — |
| `electric` | — |
| `elementalist` | — |
| `fire` | — |
| `unkillable` | — |
| `unstoppable` | — |

## 原生標籤 (22)

| ID | 型別／後設資料 |
| --- | --- |
| `bomber` | — |
| `bulwark` | — |
| `captain` | — |
| `close` | — |
| `cultist_captain` | — |
| `disabler` | — |
| `elite` | — |
| `exclude_for_havoc_speed_buff` | — |
| `far` | — |
| `horde` | — |
| `melee` | — |
| `minion` | — |
| `monster` | — |
| `mutator` | — |
| `ogryn` | — |
| `poxwalker` | — |
| `ritualist` | — |
| `roamer` | — |
| `scrambler` | — |
| `sniper` | — |
| `special` | — |
| `witch` | — |

## 武器模板 (215)

| ID | 型別／後設資料 |
| --- | --- |
| `WeaponStats` | — |
| `adamant_grenade` | — |
| `ammo_cache_pocketable` | — |
| `arc_grenade` | — |
| `arc_rifle_p1_m1` | — |
| `area_buff_drone` | — |
| `auspex_map` | — |
| `auspex_scanner` | — |
| `autogun_p1_m1` | — |
| `autogun_p1_m2` | — |
| `autogun_p1_m3` | — |
| `autogun_p2_m1` | — |
| `autogun_p2_m2` | — |
| `autogun_p2_m3` | — |
| `autogun_p3_m1` | — |
| `autogun_p3_m2` | — |
| `autogun_p3_m3` | — |
| `autopistol_p1_m1` | — |
| `bolter_p1_m1` | — |
| `bolter_p1_m2` | — |
| `boltpistol_p1_m1` | — |
| `boltpistol_p1_m2` | — |
| `bot_autogun_killshot` | — |
| `bot_combataxe_linesman` | — |
| `bot_combatsword_linesman_p1` | — |
| `bot_combatsword_linesman_p2` | — |
| `bot_lasgun_killshot` | — |
| `bot_laspistol_killshot` | — |
| `bot_zola_laspistol` | — |
| `brace` | — |
| `breach_charge` | — |
| `breach_charge_pocketable` | — |
| `broker_stimm_field` | — |
| `chainaxe_p1_m1` | — |
| `chainaxe_p1_m2` | — |
| `chainsword_2h_p1_m1` | — |
| `chainsword_2h_p1_m2` | — |
| `chainsword_p1_m1` | — |
| `chainsword_p1_m2` | — |
| `charge` | — |
| `charge_explosion` | — |
| `charge_flame` | — |
| `charged_enough` | — |
| `combataxe_p1_m1` | — |
| `combataxe_p1_m2` | — |
| `combataxe_p1_m3` | — |
| `combataxe_p2_m1` | — |
| `combataxe_p2_m2` | — |
| `combataxe_p2_m3` | — |
| `combataxe_p3_m1` | — |
| `combataxe_p3_m2` | — |
| `combataxe_p3_m3` | — |
| `combatknife_p1_m1` | — |
| `combatknife_p1_m2` | — |
| `combatsword_p1_m1` | — |
| `combatsword_p1_m2` | — |
| `combatsword_p1_m3` | — |
| `combatsword_p2_m1` | — |
| `combatsword_p2_m2` | — |
| `combatsword_p2_m3` | — |
| `combatsword_p3_m1` | — |
| `combatsword_p3_m2` | — |
| `combatsword_p3_m3` | — |
| `communications_hack_device_pocketable` | — |
| `crowbar_p1_m1` | — |
| `cryptic_servo_skull_order_point` | — |
| `deployable_force_field_pocketable` | — |
| `dual_autopistols_p1_m1` | — |
| `dual_shivs_p1_m1` | — |
| `dual_shivs_p1_m2` | — |
| `dual_stubpistols_p1_m1` | — |
| `expedition_grenade_airstrike_pocketable` | — |
| `expedition_grenade_artillery_strike_pocketable` | — |
| `expedition_grenade_valkyrie_hover_pocketable` | — |
| `expedition_loot_crate_tier_1_pocketable` | — |
| `expedition_loot_crate_tier_2_pocketable` | — |
| `expedition_loot_crate_tier_3_pocketable` | — |
| `expeditions_big_grenade` | — |
| `fire_grenade` | — |
| `flamer_p1_m1` | — |
| `forcestaff_p1_m1` | — |
| `forcestaff_p2_m1` | — |
| `forcestaff_p3_m1` | — |
| `forcestaff_p4_m1` | — |
| `forcesword_2h_p1_m1` | — |
| `forcesword_2h_p1_m2` | — |
| `forcesword_p1_m1` | — |
| `forcesword_p1_m2` | — |
| `forcesword_p1_m3` | — |
| `frag_grenade` | — |
| `galvanic_rifle_p1_m1` | — |
| `grimoire_pocketable` | — |
| `heavy_attack` | — |
| `high_bot_autogun_killshot` | — |
| `high_bot_lasgun_killshot` | — |
| `krak_grenade` | — |
| `lasgun_p1_m1` | — |
| `lasgun_p1_m2` | — |
| `lasgun_p1_m3` | — |
| `lasgun_p2_m1` | — |
| `lasgun_p2_m2` | — |
| `lasgun_p2_m3` | — |
| `lasgun_p3_m1` | — |
| `lasgun_p3_m2` | — |
| `lasgun_p3_m3` | — |
| `laspistol_p1_m1` | — |
| `laspistol_p1_m3` | — |
| `light_attack` | — |
| `luggable` | — |
| `luggable_light` | — |
| `luggable_mission` | — |
| `medical_crate_pocketable` | — |
| `missile_launcher` | — |
| `motion_detection_mine_explosive_pocketable` | — |
| `motion_detection_mine_fire_pocketable` | — |
| `motion_detection_mine_shock_pocketable` | — |
| `needlepistol_p1_m1` | — |
| `needlepistol_p1_m2` | — |
| `needlepistol_p1_m3` | — |
| `ogryn_club_p1_m1` | — |
| `ogryn_club_p1_m2` | — |
| `ogryn_club_p1_m3` | — |
| `ogryn_club_p2_m1` | — |
| `ogryn_club_p2_m2` | — |
| `ogryn_club_p2_m3` | — |
| `ogryn_combatblade_p1_m1` | — |
| `ogryn_combatblade_p1_m2` | — |
| `ogryn_combatblade_p1_m3` | — |
| `ogryn_gauntlet_p1_m1` | — |
| `ogryn_grenade_box` | — |
| `ogryn_grenade_box_cluster` | — |
| `ogryn_grenade_frag` | — |
| `ogryn_grenade_friend_rock` | — |
| `ogryn_heavystubber_p1_m1` | — |
| `ogryn_heavystubber_p1_m2` | — |
| `ogryn_heavystubber_p1_m3` | — |
| `ogryn_heavystubber_p2_m1` | — |
| `ogryn_heavystubber_p2_m2` | — |
| `ogryn_heavystubber_p2_m3` | — |
| `ogryn_pickaxe_2h_p1_m1` | — |
| `ogryn_pickaxe_2h_p1_m2` | — |
| `ogryn_pickaxe_2h_p1_m3` | — |
| `ogryn_powermaul_p1_m1` | — |
| `ogryn_powermaul_slabshield_p1_m1` | — |
| `ogryn_rippergun_p1_m1` | — |
| `ogryn_rippergun_p1_m2` | — |
| `ogryn_rippergun_p1_m3` | — |
| `ogryn_thumper_p1_m1` | — |
| `ogryn_thumper_p1_m2` | — |
| `phosphor_pistol_p1_m1` | — |
| `plasmagun_p1_m1` | — |
| `plasmagun_p1_m2` | — |
| `powermaul_2h_p1_m1` | — |
| `powermaul_p1_m1` | — |
| `powermaul_p1_m2` | — |
| `powermaul_p2_m1` | — |
| `powermaul_p3_m1` | — |
| `powermaul_shield_p1_m1` | — |
| `powermaul_shield_p1_m2` | — |
| `powersword_2h_p1_m1` | — |
| `powersword_2h_p1_m2` | — |
| `powersword_p1_m1` | — |
| `powersword_p1_m2` | — |
| `powersword_p2_m1` | — |
| `powersword_p2_m2` | — |
| `powersword_p3_m1` | — |
| `psyker_chain_lightning` | — |
| `psyker_force_field` | — |
| `psyker_force_field_dome` | — |
| `psyker_smite` | — |
| `psyker_throwing_knives` | — |
| `quick_flash_grenade` | — |
| `saw_p1_m1` | — |
| `scanner_equip` | — |
| `scripts/settings/equipment/weapon_templates/%s` | — |
| `servo_skull` | — |
| `shock_grenade` | — |
| `shock_mine` | — |
| `shoot` | — |
| `shoot_charged` | — |
| `shoot_pressed` | — |
| `shoot_release` | — |
| `shoot_release_charged` | — |
| `shotgun_p1_m1` | — |
| `shotgun_p1_m2` | — |
| `shotgun_p1_m3` | — |
| `shotgun_p2_m1` | — |
| `shotgun_p4_m1` | — |
| `shotgun_p4_m2` | — |
| `shotpistol_shield_p1_m1` | — |
| `skull_decoder` | — |
| `skull_decoder_02` | — |
| `smoke_grenade` | — |
| `stubrevolver_p1_m1` | — |
| `stubrevolver_p1_m2` | — |
| `syringe_ability_boost_pocketable` | — |
| `syringe_broker_pocketable` | — |
| `syringe_corruption_pocketable` | — |
| `syringe_power_boost_pocketable` | — |
| `syringe_speed_boost_pocketable` | — |
| `thunderhammer_2h_p1_m1` | — |
| `thunderhammer_2h_p1_m2` | — |
| `tome_pocketable` | — |
| `tox_grenade` | — |
| `transonic_claw_p1_m1` | — |
| `transonic_knife_p1_m1` | — |
| `transonic_sword_p1_m1` | — |
| `transonic_sword_transonic_knife_p1_m1` | — |
| `unarmed` | — |
| `unarmed_hub_human` | — |
| `unarmed_hub_ogryn` | — |
| `unarmed_training_grounds` | — |
| `zealot_relic` | — |
| `zealot_throwing_knives` | — |
| `zoom` | — |

## 武器關鍵詞 (63)

| ID | 型別／後設資料 |
| --- | --- |
| `activated` | — |
| `adamant` | — |
| `arc_rifle` | — |
| `autogun` | — |
| `autopistol` | — |
| `bolter` | — |
| `boltpistol` | — |
| `chain_axe` | — |
| `chain_sword` | — |
| `chain_sword_2h` | — |
| `combat_axe` | — |
| `combat_blade` | — |
| `combat_knife` | — |
| `combat_sword` | — |
| `crowbar` | — |
| `cryptic` | — |
| `devices` | — |
| `dual_shivs` | — |
| `flamer` | — |
| `force_staff` | — |
| `force_sword` | — |
| `galvanic_rifle` | — |
| `grenade` | — |
| `grenadier_gauntlet` | — |
| `grimoire` | — |
| `heavystubber` | — |
| `lasgun` | — |
| `laspistol` | — |
| `lasweapon` | — |
| `luggable` | — |
| `melee` | — |
| `needlepistol` | — |
| `ogryn_club` | — |
| `ogryn_power_maul` | — |
| `ogryn_powermaul_slabshield` | — |
| `p1` | — |
| `p2` | — |
| `p3` | — |
| `p4` | — |
| `phosphor_pistol` | — |
| `plasma_rifle` | — |
| `pocketable` | — |
| `power_maul` | — |
| `power_maul_2h` | — |
| `power_sword` | — |
| `power_sword_2h` | — |
| `powermaul_shield` | — |
| `psyker` | — |
| `ranged` | — |
| `rippergun` | — |
| `saw` | — |
| `shotgun` | — |
| `shotgun_grenade` | — |
| `shotpistol_shield` | — |
| `stub_pistol` | — |
| `syringe` | — |
| `thunder_hammer` | — |
| `transonic_claw` | — |
| `transonic_knife` | — |
| `transonic_sword` | — |
| `transonic_sword_transonic_knife` | — |
| `unarmed` | — |
| `zealot` | — |

## 能力名稱目錄（閃擊篩選使用已裝備名稱） (61)

| ID | 型別／後設資料 |
| --- | --- |
| `ability_template_tweak_data` | — |
| `adamant_area_buff_drone` | — |
| `adamant_charge` | — |
| `adamant_grenade` | — |
| `adamant_grenade_improved` | — |
| `adamant_shock_mine` | — |
| `adamant_shout` | — |
| `adamant_shout_improved` | — |
| `adamant_stance` | — |
| `adamant_whistle` | — |
| `arc_grenade` | — |
| `archetypes` | — |
| `broker_ability_focus` | — |
| `broker_ability_focus_improved` | — |
| `broker_ability_punk_rage` | — |
| `broker_ability_stimm_field` | — |
| `broker_ability_syringe` | — |
| `broker_flash_grenade` | — |
| `broker_flash_grenade_improved` | — |
| `broker_missile_launcher` | — |
| `broker_tox_grenade` | — |
| `cryptic_chordclaw` | — |
| `cryptic_discharge` | — |
| `cryptic_discharge_base` | — |
| `cryptic_force_field` | — |
| `cryptic_precision_stance` | — |
| `cryptic_servo_skull_order` | — |
| `cryptic_servo_skull_order_base` | — |
| `cryptic_servo_skull_order_base_inactive` | — |
| `ogryn_charge` | — |
| `ogryn_charge_bleed` | — |
| `ogryn_charge_cooldown_reduction` | — |
| `ogryn_charge_damage` | — |
| `ogryn_charge_increased_distance` | — |
| `ogryn_grenade_box` | — |
| `ogryn_grenade_box_cluster` | — |
| `ogryn_grenade_frag` | — |
| `ogryn_grenade_friend_rock` | — |
| `ogryn_ranged_stance` | — |
| `ogryn_taunt_shout` | — |
| `pause_cooldown_settings` | — |
| `psyker_chain_lightning` | — |
| `psyker_force_field` | — |
| `psyker_force_field_dome` | — |
| `psyker_force_field_improved` | — |
| `psyker_overcharge_stance` | — |
| `psyker_smite` | — |
| `psyker_throwing_knives` | — |
| `veteran_combat_ability_shout` | — |
| `veteran_combat_ability_stance` | — |
| `veteran_combat_ability_stance_improved` | — |
| `veteran_combat_ability_stealth` | — |
| `veteran_frag_grenade` | — |
| `veteran_krak_grenade` | — |
| `veteran_smoke_grenade` | — |
| `zealot_fire_grenade` | — |
| `zealot_invisibility` | — |
| `zealot_invisibility_improved` | — |
| `zealot_relic` | — |
| `zealot_shock_grenade` | — |
| `zealot_throwing_knives` | — |

## 戰鬥技能組 (27)

| ID | 型別／後設資料 |
| --- | --- |
| `adamant_area_buff_drone` | — |
| `adamant_charge` | — |
| `adamant_shout` | — |
| `adamant_stance` | — |
| `adamant_whistle` | — |
| `bolstering_prayer` | — |
| `broker_focus_stance` | — |
| `broker_punk_rage_stance` | — |
| `broker_stimm_field` | — |
| `broker_syringe` | — |
| `cryptic_chordclaw` | — |
| `cryptic_discharge` | — |
| `cryptic_force_field` | — |
| `cryptic_precision_stance` | — |
| `cryptic_servo_skull_order` | — |
| `ogryn_charge` | — |
| `ogryn_gunlugger_stance` | — |
| `ogryn_taunt_shout` | — |
| `psyker_overcharge_stance` | — |
| `psyker_shield` | — |
| `psyker_shout` | — |
| `veteran_combat_ability` | — |
| `veteran_stealth` | — |
| `voice_of_command` | — |
| `volley_fire_stance` | — |
| `zealot_dash` | — |
| `zealot_invisibility` | — |

