# DIY 天赋与词条使用手册

设计与验证：另见 ARCHITECTURE.zh-CN.md 与 VERIFICATION.zh-CN.md。

适用：MortisBuffManager 4.4.0、HavocConditionManager 4.3.0、HavocEnemyDirector 3.2.0。数据格式为 `Darktide.DIY` 版本 `1`。原生接口审计基于游戏 Lua 1.12.5，提交 `0f0cb45991e9305ef4a7b925370792d7d6035f95`。已完成源代码及离线原生方法检查；尚未完成游戏中的多人实机验收。

## 先开始使用

1. 在大厅输入 `/mortisbuffs`，三种奖励模式均可进入统一的「死灵天赋池」。在「包管理」中检查自动载入的包、导出入门包或把粘贴 JSON 转换为包。HCM 保留自己的「DIY 词条」页面。
2. 死灵入门模板共十二项，含 `fivefold_salvo`；HCM 共 34 项。完整的数据包及可执行 Lua 示例位于 `package-examples/`，每个词条一个文件夹，独立保存本词条的 JSON、Lua 和资源，复制到对应目录后可单独管理。
3. 原生与 DIY 开关彼此独立。房主设置房间规则和 DIY 单项权限；原生只有整池开关。列表支持直接搜索、来源／可入池筛选、详情，以及覆盖全部筛选页的批量操作。
4. 预选模式在开局前选择，原生与 DIY 名额分开计算。进度／竞争模式将适配的原生与 DIY 放入同一套奖励卡；只要原生池开启，开局仍先选原生流派。只有 DIY 开启时，开局直接抽选 DIY。所有模式均可查看列表。
5. Realms 每位真人都须确认对应 DIY 定义一致，该项才可入池。缺少或定义不同会对全房间置灰，详情列出玩家姓名；其他已安装包可以不同，对应条目的包 ID、内容与依赖须一致。所有玩家须使用当前死灵版本，修改权重也属于定义变化。
6. 配置后进入新任务，任务中锁定本局选择与房间控件；刷新和导入可以准备下一局的包。HCM 应用所有已启用且勾选的词条；死灵由当前奖励模式决定获得方式。每项 DIY 天赋消耗 1 点，总点数默认六点。等级仅为展示标签，不限制抽选数量；适配与互斥规则继续决定可入池资格。

用户文件目录分别为：

```text
%APPDATA%/Fatshark/Darktide/MortisBuffManager/diy/packages/
%APPDATA%/Fatshark/Darktide/HavocConditionManager/diy/packages/
```

启动自动发现并合并有效包，刷新用于游戏中新增或修改文件。无效包显示原因，其他独立有效包继续载入。未选择的条目不生效，导出保留完整包且不覆盖作者文件。JSON 仍是严格数据结构；可选的本地 Lua 通过版本化包接口实际执行。目录、依赖、资源及脚本示例见 [PACKAGES.zh-CN.md](PACKAGES.zh-CN.md)。

死灵按当前奖励模式统一使用原生与 DIY 天赋，不改写官方天赋树、物品栏或服务器结算奖励。HCM DIY 仍独立于官方词条。

## 敌人更新与清理

玩家和敌人的原生类会复制继承方法，运行时分别接入实际类。已选的敌人效果或事件规则会启用原本空闲的敌人 buff 更新，覆盖运行时启动前已生成的敌人。两个 DIY 模组共用更新所有权；最后一个使用者停止后，无原生 buff 的敌人恢复原生属性和空闲状态，有原生 buff 的敌人继续原生更新。仅作用于玩家的被动配置不启用空闲敌人更新。大量敌人的条件效果仍有逐敌人计算开销，密集场景性能需实机测量。

## 配置结构

最小示例：

```json
{
  "format": "Darktide.DIY",
  "version": 1,
  "kind": "mortis",
  "id": "my_talents",
  "name": {"en": "My talents", "zh-cn": "我的天赋"},
  "entries": [{
    "id": "steady",
    "name": "稳健射手",
    "description": "换弹速度提高 10%。",
    "tier": 1,
    "passive": {"stats": {"reload_speed": 0.1}}
  }]
}
```

HCM 使用 `"kind":"conditions"`。两个文件类型不可混用。

| 层级 | 字段与含义 |
| --- | --- |
| 配置库 | `format`、`version`、`kind`、`id`、`name`、可选 `description`、`entries` |
| 条目 | 必填 `id`、`name`、`description`；可选 `enabled`（默认 true）、`tier`（展示标签 1–4，默认 1）、`weight`（0–1000，默认 1）、`exclusive_group`、`source_row` |
| 作用范围 | `targets`、`availability`、`conditions`、`match`；至少提供 `passive`、`spawn` 或非空 `rules` 中的一项 |
| 常驻效果 | `passive` 包含 `stats`、`keywords`、`modifiers` 中的一项或多项 |
| 生成时效果 | HCM 专用 `spawn: {"health_multiplier": 1.4}`；静态筛选，不支持与条目级动态 `conditions` 同时使用 |
| 事件规则 | `rules` 数组；每条有独立 ID、事件、条件、概率、冷却、次数、延迟和动作 |

ID 以小写字母开头，后续只能是小写字母、数字、下划线和短横线，最长 64 字节；同一配置库条目 ID 唯一，同一条目的规则 ID 唯一。名称和说明可用一个字符串，也可用 `en`、`zh-cn`、`zh-tw` 的对象；至少提供英语或简体中文。字符串中的换行写作 `\n`。百分号直接写 `%`。界面仅展示有限长度的详情，完整说明保留在 JSON 中。

死灵的 `exclusive_group` 表示同组最多选择一个，手动选择与加权抽取都受总数、互斥组及条目 `enabled` 限制；HCM 只按启用状态与勾选列表应用词条。加权抽取只从适配且在池内的候选按正权重抽取；等级不改变抽选或点数消耗。死灵的职业可用性在人物生效时检查，初选不会自动替换当前职业不可用的条目。

### 目标与条件

`targets` 默认 `{"kind":"players"}`。`kind` 可选 `players`、`minions`、`all`；死灵条目只允许 `players`。`breeds` 和 `archetypes` 数组内部是任选其一；`tags` 要全部满足，`exclude_tags` 任意命中即排除；不同筛选字段之间是“并且”。标识符必须来自 `native-catalog.json`。例如所有精英为 `{"kind":"minions","tags":["elite"]}`。

死灵还可设置 `availability: {"archetypes":["veteran"],"families":["fire"],"talents":["实际天赋ID"]}`。三个维度同时满足才生效。原生流派 ID 和职业列在目录中；`talents` 检查角色 profile 中为 true 或大于零的天赋。自定义天赋不负责分配这些原生天赋。

条件示例：`{"subject":"self","field":"health","op":"lt","value":0.5}`。`subject` 默认 self，也可选 target 或 attacker。`match` 默认 all，可设 any。不存在的数据不会满足任何比较，包括 `ne` 和 `not_contains`。

| 条件字段 | 数值、单位或语义 |
| --- | --- |
| `health`, `toughness`, `corruption`, `ammo`, `stamina`, `warp_charge`, `overheat` | 0–1 比例；弹药为副武器当前弹匣加备用量占总容量的比例 |
| `coherency` | 原生连携计数；模板用至少 2，实际包含关系遵守游戏原生实现 |
| `progress` | 主路径推进米数，不是 0–100 百分比 |
| `load`, `players`, `monsters` | 原生战斗负担、可行动玩家数、已仇恨怪物数 |
| `elapsed` | 当前 DIY 运行实例经过的秒数 |
| `stage`, `phase` | 原生 Pacing 状态字符串；HED 阶段为 build/pressure/recovery |
| `breed`, `archetype`, `attack_type` | 原生标识符；攻击类型取当前事件，未提供时条件不满足 |
| `critical`, `weakspot` | 当前事件提供的暴击/弱点布尔值 |
| `sprinting`, `dodging`, `sliding`, `knocked_down` | 当前人物状态 |
| `in_combat` | 本框架近 8 秒收到受伤、造成伤害或命中事件；不是一个新增原生战斗判定 |
| `native_condition`, `affix`, `signal`, `tag` | 集合：官方词条 ID、当前 HCM DIY 条目 ID、有效信号 ID、单位标签 |
| `event.FIELD` | 原生事件里的白名单标量字段；95 个字段及类型见目录。并非每个事件都包含所有字段 |

数值比较：`eq/ne/gt/ge/lt/le`。字符串、布尔：`eq/ne`。集合：`contains/not_contains`。条件不支持任意表达式、跨单位数值公式或执行代码。

### 属性与关键词

完整目录提供 **411 个原生属性、181 个关键词、105 个原生事件、95 个事件标量字段**。这是可表达接口范围，不代表每个字段对所有职业、武器、敌人和伤害路径都有作用；游戏必须实际读取该属性。内部特殊关键词尤其需要结合原生实现使用。

| 原生属性类型 | JSON 值的意义 | 例子 |
| --- | --- | --- |
| `additive_multiplier` | 在原生倍率上增加差值；各层差值相加 | `reload_speed: 0.1` 为 +10%；`recoil_modifier: -0.5` 为 -50% 倍率差值 |
| `multiplicative_multiplier` | 与原生值及各 DIY 层相乘 | `damage_taken_multiplier: 0.8` 为承伤 ×0.8 |
| `value` | 原生数值上加值；单位依消费者决定 | 暴击几率通常 0.1 表示 10 个百分点；查目录类型及对应原生消费者 |
| `max_value` | 与原生值及其他效果取最大值 | 不按叠层次数重复累加 |

每个 effect 最多 64 个 stats、32 个 keywords。单项数值 -1000–1000；乘法倍率与最大值不得为负，加法倍率差值不得小于 -1。汇总也有边界：乘法最大 1000，加法倍率差值最低 -1。极端值可能越过原生预期，不等于所有组合都有合理玩法效果。

`keywords` 是启用关键词的字符串数组，不支持关闭其他模组或原生已拥有的关键词。DIY 撤销只移除自身贡献。`modifiers` 支持 `ammo_pickup_multiplier`（0–10，多个效果相乘）和 `ammo_pickup_failure_chance`（0–1，多个独立失败率合成为 1−各成功率之积）。拾弹倍率作用于原版拾取函数算出的结果，不覆盖医疗箱或部署型箱子的使用逻辑。

### 事件规则

```json
{
  "id": "counter",
  "event": "on_damage_taken",
  "cooldown": 0.5,
  "chance": 1,
  "max_triggers": 20,
  "delay": 0,
  "actions": [{
    "type": "effect",
    "duration": 4,
    "max_stacks": 3,
    "effects": {"stats": {"melee_power_level_modifier": 0.15}}
  }]
}
```

规则默认概率 1、冷却 0、次数 0（不限次数）、延迟 0。即使写冷却 0，同一规则状态仍有 0.05 秒最小间隔。`scope` 默认 unit，为每个事件所属单位分别计数与冷却；HCM 可选 global，整个规则共享状态。global 不取消条目的目标筛选。死灵规则始终属于选择它的玩家。

除原生事件目录外，支持 `interval`、`spawn`、`enemy_died`、`mission_start`、`signal`：

- `interval` 必填 `interval`，0.1–600 秒；掉帧后仅触发一轮，不追补错过的所有轮次。
- `spawn` 是框架观察到的单位生成；HCM 包含敌人，死灵观察玩家。
- `mission_start` 在玩家单位首次被当前运行实例观察到时发出；重生为新单位时可再次出现。每个角色整局只一次的效果需要额外设计，不能仅依靠 unit scope 的 `max_triggers:1`。
- `enemy_died` 为死亡广播。HCM 以死者为 self，死灵广播给每个存活的天赋持有者并以持有者为 self。只奖励自己的击杀应使用原生 `on_kill`；target 为死者，attacker 为击杀来源（若有）。
- `signal` 在下一次更新派发，使用 `event.signal_name` 筛选。HCM 的 global signal 规则可无单位执行；要作用全队，应显式写动作 target=players。跨模组共享的是信号状态，不会替另一个模组直接派发一次 signal 事件。

原生 proc 由对应 Buff 扩展提供；事件缺少参数时相关条件不会通过。字段表中提供的是全部支持字段的并集。`source_row` 仅是对照图片用的说明，不影响执行。

### 动作完整表

所有动作均可写 `target`：self（默认）、target、attacker、players、nearby_players、minions、nearby_minions、matching。nearby 以 self 为中心，`radius` 默认 8 米、允许 1–50 米；matching 使用条目的 targets。非效果动作每次最多匹配 4 名玩家或 64 名敌人。死亡单位不能接受资源、伤害或原生状态动作。

| type | 字段与行为 |
| --- | --- |
| `effect` | 必填 `effects`、`duration`（0.1–600 秒）；`max_stacks` 1–500，默认 1；`refresh` 默认 true。叠层共用一个到期时间，false 不续期，不是每层独立倒计时 |
| `heal` | `amount` 非负；调用原生 buff 治疗，遵守腐化上限、治疗倍率与禁疗关键词 |
| `corruption` | `amount` 非负；移除腐化，使用原生 buff_corruption_healing，可跨生命格；不直接补普通生命，不用于施加腐化 |
| `toughness` | 正数恢复，遵守原生恢复倍率；负数调用原生韧性扣除并启动恢复延迟 |
| `ammo` | 正数补备用弹，负数先扣备用弹再扣弹匣，遍历装备中的武器槽；按整数向零取整 |
| `grenades` | 调整原生投掷技能充能，限制在 0 到该能力最大值；无此能力则无效果 |
| `ability_cooldown` | 非负秒数减少战斗技能冷却；fraction 按最大冷却算，不增加充能上限 |
| `stamina` | 正数增加，负数调用原生体力消耗，保留原生消耗修正及耗尽事件 |
| `warp_charge` | 平值按百分点、fraction 按 0–1；正数加危机值但不直接引爆，负数消退；限有原生危机值模板的职业 |
| `overheat` | 平值按百分点、fraction 按 0–1；负数原生散热，正数遵守原生热量倍率与锁定/爆炸状态；限有过热配置的副武器 |
| `damage` | 非负直接生命伤害；使用私有原生伤害配置并继续原生攻击流程。绕过韧性，不保证绕过所有原生减伤、无敌和伤害规则 |
| `kill` | 无 amount；必须显式 target/匹配敌人类范围，只允许目录中的普通可生成敌人，不允许处决玩家或特殊任务实体 |
| `native_buff` | `name` 必须在 15 个已审计原生状态中；`duration` 默认 10、最大 120 秒；`count` 1–10。期限是本框架移除上限，原生状态可能提前结束 |
| `signal` | `name` 为 ID，`duration` 0.1–600；发布有期限的状态信号 |
| `pause_spawns` | `name` 为 all/hordes/trickle_hordes/roamers/specials/monsters/hed，`duration` 0.1–600；暂停许可检查及 HED 调度，不移除已生成单位，不保证暂停绕过 Pacing 的任务脚本 |
| `spawn_formation` | `name` 为当前任务 HED 配置中已有编队 ID。提出一次调度请求，不是立即在身边生成 |
| `spawn_enemy` | `breed` 从 40 个可生成敌人中选择；普通/特感 `count` 1–16，怪物模板动作每次 1；经 HED 的位置、数量、原生槽位检查 |
| `pickup` | `name` 为目录中的拾取物；`count` 1–4，生成在目标单位身旁，不直接强塞进物品槽 |
| `sound` | `name` 为 456 个已知原生 UI 音效之一；房主本地播放，不是自定义音乐播放器 |
| `notification` | `text` 字符串或三语言对象，最长 512 字节；房主本地通知 |

资源动作的 `amount_kind` 默认 flat；fraction 是目标最大资源量的比例，不是当前持有量。只有 ammo 额外支持 current_fraction，用于扣除当前剩余弹药的比例。heal/toughness/damage 可用 event_damage，将事件的 damage/damage_amount/damage_dealt 乘以 amount（0–5）；事件无伤害数值时为零。

signal、pause_spawns、生成请求不使用动作 target/radius；sound 和 notification 只执行一次。effect 的 players/minions/matching 是动态范围层：持续期间符合条件的新单位也会取得效果；nearby 是触发时选中的有限单位集。已获得的单单位临时层不会因为之后离开原条目条件而自动提前消失。

## HED 与其他模组接口

生成动作需要 HED 并启用其导演调度。HED 缺失或未就绪时请求失败，不退回无约束生成。原生刷新暂停需要启用 HCM；单独死灵仍可发布自身信号和暂停标志，HED 读取 hed/all 暂停。HCM 汇总死灵与自身的信号及暂停，因此死灵天赋也可以驱动 HED 条件。

HCM 导出 `mod.diy_api.version == 1`，提供 `active()`、`paused(family)`、`context(table)`、`emit_signal(name,duration)`、`status()`。active 返回 HCM 选中条目 ID；context 写入 affix 和有效 signal 集合。死灵的同名接口提供 `paused`、`context`、`status`，共享信号但不把私人天赋伪装成全局词条。

HED 导出 `diy_api.status()` 与 `diy_api.request(request)`。外部 Lua 模组可调用：

```lua
local hed = get_mod("HavocEnemyDirector")
local ok, request_id_or_reason = hed.diy_api.request({
    breed = "chaos_poxwalker", count = 2,
    source = "my_mod/my_entry/my_rule", seed = 12345,
})
```

request 只能包含 formation 或 breed（二选一）、count、source、seed。formation 模式 count 只能省略或为 1。breed 模式外部 API 每次最多 16，怪物最多 3；DIY JSON 怪物动作更保守，每次 1。source 为至多 192 字节的字母数字及 `_:/-`；seed 为 1–2147483646 整数，可省略以采用导演种子。返回 true 仅代表排队成功，后续可因位置、容量、暂停或超时而取消。主要失败原因：director_not_ready、request_target、request_breed、formation_missing、request_capacity、mission_request_budget。

HED 条件编辑器新增 `affix_active` 和 `signal_active`，点击值粘贴 ID。例如 `signal_active=diy_pressure` 对应模板中的导演信号。生成来源条件 `event.spawn_source` 在 HCM 敌人 spawn 事件可用；普通 HED 生成标记 hed_director，DIY 普通单位标记 hed_diy，其他原生来源保留其批次来源或 native。怪物和特感走各自原生注册/槽位路径，不能依赖它们也拥有这两个来源标签。

每个 HED 任务最多接纳 128 次外部请求，同时最多保留 32 个外部状态；每个请求最多等候 120 秒。任务脚本、地图位置和原生实体上限仍有最终决定权。不是尸体原地克隆，也没有承诺严格 FIFO 或每请求必定成功。HED 原有全局分帧提交速度、存活组数、路线与容量限制继续有效。

## 联机、清理与性能边界

SoloPlay 或 Realms 本地房主执行动作，普通远程服务器和客机不执行任意 DIY 动作。Realms 每个参与者需要对应新版模组；死灵还要求房内玩家对应条目的包、Lua、资源及依赖的 SHA-256 指纹一致。房主批准私人选择后，该角色同局不能通过重复握手切换。HCM 由房主统一选择词条，客机接收聚合属性效果，无须配置相同词条文件。

客机仅接收自己角色的属性、关键词和少量修正；不接收可执行 JSON 程序。网络包检查房主身份、玩家成员、角色、会话 nonce 和递增序号；效果超过 3 秒未续期即撤销。房主约每 0.5 秒同步一次，运行层约每 0.1 秒更新；客机属性可能存在这一量级的延迟。客户端预测、特殊关键词资源及完整四人战斗仍须实机检查，不能从离线测试推导“联机完全无差异”。

合并后的规范化定义最大 512 KiB、30,000 个 JSON 节点、深度 20、128 条目；每条目最多 16 规则，每规则最多 8 动作、12 条件。每 tick 最多 128 次触发评估、64 个动作，延迟队列最多 512；每单位和动态全局层最多 128 项；原生受控状态记录最多 256，拾取物每库每局最多 32。达到预算时部分工作被拒绝或延期，不保证高负载逐事件无损。不要用大批量 interval+全体目标替代游戏自身的持续效果系统。

配置撤销、退出任务、权限丢失和禁用清理本框架持有的临时状态、队列及资源记录。已产生的实际伤害、治疗、弹药变化、拾取物和敌人属于已完成动作，不会倒放撤销。原生状态移除只删除本框架申请的索引，不扫除其他模组的同名状态。

## 图片评估与扩展方向

完整逐行结果见 `IMAGE-ASSESSMENT.zh-CN.md`；空白行和只写玩笑名称的行也已单独列出。已提供数值、条件、状态、资源、信号及合规增援的通用接口；致命伤延迟、玩家流血、仇恨重置、敌人变形、弹幕/爆炸物、地图拾取池、UI 隐藏、音视频资源、装备重置、任务交互与载具仍需各自专门适配，不是加一个不存在的字段就能实现。

扩展时先确认原生方法与网络所有者，再在 schema 中增加严格数据字段、给原生适配器增加一个明确动作、补充真实原生方法边界测试和模板；更改语义应升级 schema，不能让同一版本文件在房主与客机解释不同。`native-catalog.json` 是版本固定的目录，不接受从 JSON 动态加入原生属性或网络 Buff 编号。


### 抽选前的配装适配

`availability` 在手选、随机预览、开局抽选、房主接纳和实际生效时检查。全部字段必须满足；不适配项先移出候选池，不占总数或互斥组。配装未完整同步时暂缓选择；同局已经确定的 DIY 选择不会因配置变化重新随机。

| 字段 | 含义 |
| --- | --- |
| `archetypes` / `families` | 职业／死灵流派列表，列表内任一匹配。未确定流派不能满足流派要求。 |
| `talents` | 全部原生天赋节点必须已选中（true 或正数）。 |
| `weapons` / `weapon_keywords` | 两个装备槽的原生模板名／武器关键词，列表内任一匹配。 |
| `grenade_abilities` | 当前闪击的准确原生能力名。 |
| `combat_abilities` | 当前战斗技能的 `ability_group`。 |
| `resources` / `any_resources` | 全部／至少一种资源机制存在。 |

资源可选 `ammo`、`reload`、`overheat`、`warp_charge`、`grenade_charges`、`combat_ability`、`melee`、`ranged`。例如 `"availability":{"archetypes":["psyker"],"grenade_abilities":["psyker_throwing_knives"],"resources":["ammo","grenade_charges"]}` 要求灵能者当前带飞刀且装备有弹药机制。资源是否存在与当前弹药、生命或过热数值分开；低血量等仍写在 `conditions`，不会因开局满血被排除。

已审计的弹药／换弹等属性与自身资源动作会自动增加硬性要求；复杂事件、特殊关键词和专属武器机制仍须作者声明准确的武器、技能、天赋条件。`any_resources` 可声明灵能／过热替代动作，但不能绕过被动效果的硬性要求。完整对照见 [适配规则核对](ELIGIBILITY-AUDIT.zh-CN.md)。

## 死灵权重、权限与五重齐射

`weight` 范围为 0–1000，默认 1，允许正小数。0 表示只可手选。混合的非流派奖励中，每个原生候选权重为 1，每个卡位从剩余适配候选中按权重抽取，且不重复。只有权重 1、2、7 三项时，第一个卡位概率为 10%、20%、70%；整组三张卡的出现概率不同。仅原生模式保留原版分类权重，开局流派仍按原生流派规则。房主禁用、缺少玩家定义和配装不符均在抽取前过滤；每次发放后再次检查总数和互斥组。

批量操作覆盖全部筛选结果，包括其他页；明确选择「我的预选」或房主的「房间 DIY 池」作为操作对象。房主不能逐项禁用原生天赋。灰色技能仍可查看详情；只对已预选／已获得受影响技能的玩家提醒。房间权限不会改写玩家保存的选择。

`passive.modifiers.ranged_salvo_count` 仅限死灵天赋，接受 1–5 的整数。五重齐射示例使用 5，要求远程武器。每次生成五份攻击，但只支付一次原本消耗；原生额外弹体参与乘算，激涌暴击共十发。延迟法杖弹体保留原充能。霰弹复制共用原散布；火焰与闪电重复原生脉冲，并遵守原版叠层上限。该修饰器多个来源取最大值，不复制近战、闪击或战斗技能攻击。

只有 DIY 时，进度模式最多十项奖励，没有原生路线自动奖励。混合模式使用统一奖励轮次，并遵守独立的 DIY 点数上限。原生与 DIY 支持四种开关组合；两者都关会在本 mod 支持并接管的死灵流程中停用两类奖励。

包大小、文件限制和 Lua 语义见 PACKAGES.zh-CN.md。脚本专用条目需要职业、武器或资源机制时，作者应显式填写 availability。

包管理不包含奖励上限。Realms 准备界面的死灵天赋控件由房主设置独立 DIY 开关和点数上限，使用减号、数字直接编辑和加号（0–99）。每项 DIY 天赋消耗 1 点，与等级无关；SoloPlay 保留独立的「奖励设置」页面。等级仅作标签，旧的等级配额会被忽略。HCM 会应用所有已启用且勾选的词条。词条页不设随机抽取、种子或数量配额，旧权重与互斥组不再筛掉已勾选词条。悬停一行即可查看详情，不改变勾选；文件操作保留在独立的「包管理」页面。

## 按管理器设置随机种子

词条事件的概率随机流在 HCM「整体调节 → 随机种子」设置；HED「导演 → 随机种子」分别设置自身编队调度与原生驻军布局。关闭固定种子时沿用任务种子；HCM 无法取得任务种子时，每局只随机生成一次后备用值。开启后可输入 1–2147483646 的整数，关闭会保留输入值，修改用于下一局。这些种子不选择任务地图，也不统一原生尸潮、特感、怪物和脚本事件的全部随机性；Lua 作者直接使用 math.random 时仍属于独立的原生随机来源。
