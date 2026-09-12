# 死灵试炼适配规则核对

核对对象：MortisBuffManager 4.0.0 与本地游戏 Lua 1.12.5（提交 `0f0cb45991e9305ef4a7b925370792d7d6035f95`）。修复版本：MortisBuffManager 4.0.1。结论来自源码和离线执行，不是游戏实机验收。

当前行为：职业、当前闪击、战斗技能、天赋和资源条件先决定候选资格，再按权重抽取。DIY 已加入统一奖励池；等级仅为标签。以下原生适配审计仍然适用。

| 维度 | 原版 | Mod 核对与修复 |
| --- | --- | --- |
| 职业 | 通用传奇池加当前职业池。 | 原生愁绪已遵循；DIY 现在在手选、随机预览、开局选择、房主接纳和持续应用时检查。 |
| 闪击 | 使用已装备闪击的准确 `name` 取池。 | 原生愁绪已有；DIY 新增 `grenade_abilities`，按当前闪击名检查。 |
| 战斗技能 | 使用已装备战斗技能的 `ability_group` 取池。 | 原生愁绪已有；DIY 新增 `combat_abilities`，填写技能组，不是天赋节点名。 |
| 特定天赋 | 仅将选中天赋对应的传奇加入候选。 | 已有；Mod 将 true 或正数视为选中，false／0 不满足要求。 |
| 流派 | 先选流派，后续流派奖励只从该流派取；传奇奖励独立。 | 原有隔离保留。DIY 的 `families` 在抽选时也检查；未确定流派时，限定流派的 DIY 不具备资格。 |
| 武器与资源 | 原版选择器没有通用的装备适配过滤，部分效果在运行时访问远程槽弹药或换弹。 | 补充下列 8 个已审计原生愁绪的资源限制。DIY 可声明准确武器、武器关键词、全部／任一资源要求，并自动推断已审计的硬性资源依赖。 |
| 重复与失效候选 | 排除已获得奖励及后台排除项。 | 原有规则保留；换装使已显示卡片失效时重新生成候选，旧卡片回复不能消耗次数。DIY 不适配项先剔除，不占数量或互斥组名额。 |
| 欧格林基础手雷箱 | 选择器自动添加隐藏的集束适配效果。 | 为 Mod 自定义发奖流程补齐；不占奖励名额。仅清理由 Mod 添加的实例，保留原版已有实例。 |
| 低血量等战斗条件 | 由效果本身在战斗中判断。 | 不用开局满血、满弹等状态否定抽选资格；装备拥有资源机制与当前资源数值分开判断。 |

## 原生武器依赖清单

以下条目检查 `slot_secondary`。这是一份逐项核对的依赖表，不宣称原版存在覆盖全部效果的自动武器兼容规则。

| 原生 ID | 必须具备 |
| --- | --- |
| `hordes_buff_auto_clip_fill_while_melee` | 弹药机制 |
| `hordes_buff_no_ammo_consumption_on_crits` | 弹药机制 |
| `hordes_buff_bonus_crit_chance_on_ammo` | 弹药机制 |
| `hordes_buff_melee_damage_missing_ammo_in_clip` | 弹药机制 |
| `hordes_buff_weakspot_ranged_hit_gives_infinite_ammo` | 弹药机制 |
| `hordes_buff_veteran_infinite_ammo_during_stance` | 弹药机制，同时保留原有职业／技能限制 |
| `hordes_buff_increased_damage_after_reload` | 换弹动作 |
| `hordes_buff_improved_weapon_reload_on_melee_kill` | 换弹动作 |

法杖不再进入依赖弹药基础奖励的牛仔流派；其他流派只移除不兼容项目。弹药为零的枪仍拥有弹药机制，不会因缺弹被排除。等离子枪同时具有弹药和过热机制。

## DIY 编写规则

`availability` 各字段之间取“同时满足”。`archetypes`、`families`、`weapons`、`weapon_keywords`、`grenade_abilities`、`combat_abilities` 各列表内部取“任一匹配”；`talents` 和 `resources` 则要求全部满足；`any_resources` 要求其中至少一种存在。

资源名：`ammo`、`reload`、`overheat`、`warp_charge`、`grenade_charges`、`combat_ability`、`melee`、`ranged`。灵能是职业机制；过热是武器机制；手雷次数根据当前闪击是否具有正数最大次数判断，不能把所有闪击都视为可补手雷。

武器名与关键词来自原生武器模板，按两个装备槽检查。物品有 `weapon_progression_template` 时遵循原版解析优先级。配置未完整同步时暂缓选择，不能用未知配置放行。大厅以已保存配装为准，任务中优先读取实际装备。任务内已确定的 DIY 选择不重新随机；条件失配时移除其效果，下次任务重新检查。

自动推断覆盖已审计的弹药／换弹／过热／灵能／技能冷却等属性与自身资源动作。复杂事件、特殊关键词、专属武器机制不能仅凭任意 JSON 的文字自动推断；作者必须明确填写对应武器、技能或天赋要求。目录收录原生字段不等于任意组合都有效。`any_resources` 允许模板明确声明“灵能或过热”的替代动作；它不能绕过被动效果自身的硬性要求。

11 个死灵入门模板已补充相应要求。已保存的旧库不会被覆盖；自动资源检查仍生效，新增模板声明可通过重新导出入门库取得。HCM 的 34 个全局词条不套用某一玩家的 Mortis 选择资格；共享库随兼容更新发布为 4.0.1。HED 保持 3.1.0。

## 验证与源码依据

- 原版实际选择器与数据：128 组职业／闪击／技能池组合；逐流派优先奖励、传奇分类、后台排除和奖励顺序。
- 原生能力定义及原版武器解析器：7 职业、132 组技能组合；武器相关元数据来自实际枪械、法杖、等离子枪与近战模板，未执行渲染和攻击动作。
- DIY：1000 个种子的抽选，检查不适配高权重项不能占配额；手选互斥组、缺失配装、0／false 天赋、资源组合和下局换装。
- 实际 Mod 生命周期与协议：房主拒绝不符职业／武器的请求，缺失配装时等待，同局锁定、重生、断线和清理；场景服务及网络传输采用测试替身。
- 原生卡片失效及基础手雷箱辅助效果的名额、归属、换闪击和清理检查。
- 三个工程回归及六个 DIY 套件。尚需游戏内 SoloPlay／四人 Realms 配装与网络验收。

源码定位（均相对原生源码或 Mod 的脚本目录）：

- 原生 `scripts/managers/mission_buffs/mission_buffs_selector.lua`、`mission_buffs_allowed_buffs.lua`、`mission_buffs_settings.lua`。
- 原生 `scripts/settings/buff/hordes_buffs/hordes_family_buff_templates/`、`hordes_legendary_buff_templates/` 中的实际效果实现。
- 原生 `scripts/settings/ability/player_abilities/abilities/` 与 `scripts/utilities/weapon/weapon_template.lua`。
- Mod `modules/mortis_catalog.lua`、`modules/mortis_draft.lua`、`modules/mortis_buffs.lua`、`modules/diy_mortis.lua`、`modules/diy/diy_eligibility.lua`。
