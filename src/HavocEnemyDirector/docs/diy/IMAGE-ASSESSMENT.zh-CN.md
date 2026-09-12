# 三张图片逐行可行性评估

本表保留原图片第 3–122 行，覆盖 120 行，包括空白与待定。名称作阅读整理，判断以图片效果描述为依据；图片中文字没有被当作执行指令。

**S**：本版接口支持主要效果（模板或可直接配置）。**P**：可实现部分或提供近似，后半栏明确差异。**A**：需要新增原生适配，当前 JSON 尚不能完成。**R**：缺少明确规则、外部资源或属于独立玩法。**B**：空白/待定。S 也不等于所有原生伤害路径与四人实机均已验证。

提供的模板是可修改示例，并未把图片所有效果都实现。接口列中的代码名可以在手册及原生目录查找；泛称某适配器表示未来需要建设的接口，不是可在 JSON 中填写的新字段。

| 图片行 | 名称/含义 | 结论 | 已用或所需接口 | 实际支持与缺口 |
| --- | --- | --- | --- | --- |
| 3 | 至死不渝·精英 | A | fatal-hit interception; death scheduling | 需在致命伤提交前拦截并保留死亡归属，再延迟 4 秒处决；现有受击事件发生得太晚。 |
| 4 | 恐怖来袭 II | S | spawn.health_multiplier | 可按 breed/tag 乘算初始生命；monster_health_150 模板选择三种普通怪物。 |
| 5 | 恐怖来袭 III | S | spawn.health_multiplier | 同上；monster_health_200 提供 ×2，两个模板互斥。 |
| 6 | 弹药匮乏 I | S | modifiers.ammo_pickup_multiplier | ammo_scarcity 将原生拾弹结算结果乘 0.75，与浩劫修正叠乘。 |
| 7 | 弹尽粮绝 II | P | ammo_pickup_failure_chance; pickup/deployable adapter | 已支持 50% 空弹药；医疗包和部署箱失效仍需分别接入使用流程。 |
| 8 | 团结治疗 III | S | interval; coherency; heal; corruption | coherent_medic 每秒恢复生命和腐化各 0.3，遵守原生禁疗与连携计数。 |
| 9 | 团结防御 II | S | conditions; toughness_damage_taken_multiplier | coherent_defence 提供连携时 35% 韧性减伤。 |
| 10 | 混乱火炮 IV | A | projectile/explosion; telegraph; native placement | 可用 interval 调度，但 4–8 个预警圈、轨迹、阵营与护甲伤害需专门弹幕适配；尚未实现。 |
| 11 | 受伤加深 I | S | damage_taken_multiplier | deeper_wounds 提供玩家承伤 ×1.1。 |
| 12 | 堕落之人 I | S | corruption_taken_multiplier | corrupting_touch 对读取该原生属性的腐化来源乘 1.3。 |
| 13 | 永恒之火 III | P | native_buff; liquid lifetime adapter | 可施加和续期已支持的敌方燃烧状态；全部环境火焰永不熄灭及所有层数永久保留未实现。 |
| 14 | 空白／待定 | B | — | 未提供具体效果；不推测或生成隐藏规则。 |
| 15 | 帝皇赐福 IV | P | on_hit; kill; mission result adapter | 可对普通可生成敌人实施受限处决；不能据此保证全敌人秒杀或直接改任务胜负。 |
| 16 | 扭曲裂隙 | P | enemy_died; spawn_enemy; HED | 可死亡后请求不同敌人增援；原地缩小模型、继承骨骼/行为/血量的分裂需额外适配。 |
| 17 | 脚扭了 I | P | dodge_distance_modifier; dodge_speed_multiplier; dodge_cooldown_reset_modifier | slow_feet 已覆盖距离、速度；原图所有闪避恢复速度的统一 -10% 未完整覆盖。 |
| 18 | 坚不可摧 II·精英 | S | spawn.health_multiplier | elite_endurance 对原生标签 elite 的敌人增加 40% 初始生命。 |
| 19 | 掠夺一空 | A | pickup spawning; level props; medicae interactions | 现接口可生成拾取物，不能统一禁止地图预置物、掉落与医疗站；需分来源拦截。 |
| 20 | 韧性衰减 | A | melee health-bleedthrough calculation | 增加韧性承伤不等于改变满韧性近战生命泄漏比例；需适配原生伤害拆分。 |
| 21 | 战争狂热 | P | enemy_died; effect; max_stacks | battle_fervour 实现 0.1% 能量、500 层、30 秒共享续期；原图防御增益和独立层计时未实现。 |
| 22 | 绑架 | A | respawn/rescue manager | 禁止死亡后救援需接入重生与任务救援流程，不能用普通属性可靠替代。 |
| 23 | 双生奸奇 | P | enemy_died; spawn_enemy; HED | split_reinforcements 是精英死亡后有限次请求两个行尸；未实现每种敌人的原地分裂。 |
| 24 | 暗无天日 | A | flashlight; perception ranges; environment | 个人照明和敌人感知是不同系统；需限定范围并同步各端。 |
| 25 | 保底 | P | pickup; loot-container interaction adapter | 可以在玩家附近生成箱子；指定地图补给箱开启时必掉两箱尚未接入。 |
| 26 | 友谊诅咒 | A | coherency distance; pre-damage routing | 附近群体伤害动作不能精确代替受击前的伤害分摊、远距离判定与倒地规则。 |
| 27 | 未命名·随机死亡产物 | P | enemy_died; chance; spawn_enemy; pickup | 支持限定列表里的敌人与拾取物概率动作；爆桶和任意道具不在现接口内，随机互斥分支仍需扩展。 |
| 28 | 脚滑 | A | AI locomotion; animation; action state | 敌人攻击中移动需逐行为树/动画改造，单独移速属性不足以实现。 |
| 29 | 壁垒 | S | ranged_damage_taken_multiplier | ranged_monster_shield 对 monster 标签设远程承伤倍率为零；特殊绕行伤害路径除外。 |
| 30 | 奸奇闪电 | A | lightning FX; damage; despawn/replace | 闪电表现、命中选择、保留任务所有权的变形尚未实现；HED 新增怪物不等同原位变形。 |
| 31 | 友军之围 | A | native friendly-fire permission; attack profiles | 原生友伤许可与伤害配置需专门适配；对队友额外扣血不是等价实现。 |
| 32 | 破伤风 I | P | on_damage_taken; chance; damage-over-time | 可组合概率持续扣血，但原生玩家流血、狂战/Boss 加倍、绕韧概率需专门状态适配。 |
| 33 | 破伤风 II | P | on_damage_taken; chance; damage-over-time | 同 32 行；可以调整概率，未提供精确原图流血机制。 |
| 34 | 破伤风 III | P | on_damage_taken; chance; damage-over-time | 同 32 行；更高概率不改变所缺失的玩家流血适配。 |
| 35 | 慈父毒气 | A | minion FX; death callback; liquid/gas area | 生成时冒烟及死亡毒气区域需要可同步的特效与区域伤害生命周期。 |
| 36 | 混乱诅咒 | A | spawn replacement; loot replacement; seeded pool | 已有确定种子的配置抽取，但全局替换原生敌人与拾取结果需新增来源适配及兼容规则。 |
| 37 | 回归本源 | A | profile/talent/equipment adapters | 不会通过 DIY 改写玩家装备和正式天赋；临时隔离构筑也需独立、可恢复的适配。 |
| 38 | 荒诞惊喜 | P | ammo_pickup_multiplier; pickup; loot adapter | 弹药量翻倍和扣弹可做；同时影响手雷、取得结果转为扣当前一半需要拾取事件前适配。 |
| 39 | 俄祢连击 | A | weapon action state; charge timing; self damage | 伤害倍率可改，但蓄力不自动释放、充能曲线和自伤时点需武器动作适配。 |
| 40 | 写实模式 | A | HUD visibility; per-client UI | 需要本地 UI 开关及房间约定；服务端属性无法替所有客机隐藏所有界面。 |
| 41 | 纳垢花园显现 | P | health fraction conditions; native_buff; corrosion adapter | 可按低生命条件施加支持的增益；玩家长期 1 腐化和全套毒花增益需进一步适配。 |
| 42 | 蝇群感染 | A | minigame/interaction trigger; spawned area FX | 刷取任务交互和可近战击破的蝇群实体需要专门资产与交互适配。 |
| 43 | 战争首领 | P | interval; spawn_formation; HED | 可在 Boss 存活条件下请求增援；若要连长招手动作、专属呼叫节奏需接入 AI 行为。 |
| 44 | 血祭血神 | P | on_hit; kill; toughness; damage | 支持普通敌人受限处决及扣韧/生命；玩家首击清空韧性再按近战判死需原生伤害适配。 |
| 45 | 布娃娃模式 | P | impact/stat consumers; stagger adapter | 可调整读取属性的冲击；敌我通用“击飞强度翻倍”还涉及阈值、布娃娃和各攻击配置。 |
| 46 | 终极困难 | P | prevent_all_healing; HED composition; event adapters | no_healing 已实现禁疗；HCM/HED 可编辑编成和增援，但没有统一替换全部普通敌人与新增任务事件。 |
| 47 | 血手之怒 | S | on_sweep_start; toughness; stats | blood_price 提供消耗韧性与攻速、能量、恢复加成；以原生近战 sweep 事件计费。 |
| 48 | 圣梅基丽娜的赐福 | S | on_kill; heal; coherency; effect | martyr_blessing 近战击杀回血并在连携时提供短时能量加成。 |
| 49 | 聋的传人 | A | audio buses; per-client settings | 需受控的音频总线适配；现 sound 动作只播放原生 UI 音效。 |
| 50 | 你再看看你后面呢 | A | enemy audio event routing | 需筛选敌人警告与攻击音频事件，不能用全局静音代替。 |
| 51 | 吃吃爆 | P | HED specials; audio routing | 可增加自爆特感请求；仅消除自爆音效仍需音频适配。 |
| 52 | 混沌卵开智 | A | boss behavior tree; carried minion; animation | 抓取、持有并投掷另一敌人是新的复合 AI 动作，现通用接口不覆盖。 |
| 53 | 飞起来 | A | jump locomotion; prediction | 不是已验证的通用 Buff 属性；需人物运动与客户端预测适配。 |
| 54 | 灵魂链 | A | damage redistribution; proximity; incapacitation | 精确分摊需受击前拦截、保护递归和倒地状态处理；群体伤害动作只能近似。 |
| 55 | mine! | P | spawn_enemy; AI flee; pickup | 可有限生成敌人和死亡掉落物；宝藏哥原生逃跑行为与专属单位未开放为自由生成。 |
| 56 | 变幻无常 | A | interval; lightning; transformation | 周期调度可用；对玩家雷击并随机变形敌人的复合机制尚需独立适配。 |
| 57 | 破伤风 max | P | chance; damage; native_buff | 可配置部分概率与伤害；精确玩家流血、BOSS 秒杀和绕甲分支未实现。 |
| 58 | 失忆症 | A | perception/aggro/target state | 需要逐敌人清理目标并允许之后重新发现；不等同隐身关键词。 |
| 59 | 等等! | S | pause_spawns | wait_a_moment 暂停许可检查与 HED 30 秒；任务脚本绕行生成不保证停止。 |
| 60 | 手无寸铁 | P | spawn; ammo; health; rescue-specific event | 可以在生成时扣弹和生命；仅针对获救、不影响首次出生的判定尚需救援事件。 |
| 61 | 剑圣 | A | heavy-attack classification; critical roll | 全近战必暴可表达，但只让重击在原生判暴前必暴需要精确动作时序适配。 |
| 62 | 暴毙 | S | extra_max_amount_of_wounds | 可用现有原生数值减少生命格；最终最小格数及职业规则由游戏决定。 |
| 63 | 腐蚀环境 | P | interval; toughness; health condition; damage | corrosive_air 实现扣韧与空韧掉血；原图同时压制全部韧性恢复的程度需另配属性。 |
| 64 | 友军之围·敌方版 | A | AI attack profiles; friendly-fire damage | 需要审计敌方各攻击路径的友伤倍率，不是玩家承伤字段。 |
| 65 | 克扣物资 | S | ammo current_fraction; grenades | supply_tax 扣每把武器当前弹药的一半并清空手雷，整数向零取整。 |
| 66 | 大爆炸 | P | explosion stats; explosion template adapter | 能改变读取现有属性的玩家爆炸路径；所有敌我和地图爆炸范围/伤害并未统一覆盖。 |
| 67 | 空白／待定 | B | — | 未提供具体效果；不推测或生成隐藏规则。 |
| 68 | 帝皇庇佑 IV | P | on_kill; heal; interval damage | 可近似击杀回血后衰减，但缺少独立临时生命池与不会误扣真实生命的消耗规则。 |
| 69 | 敏感肌 | P | on_damage_taken; chance; effect | 受击概率增益可做；按命中次数计数后从互斥增益池抽一项需计数/分支扩展。 |
| 70 | 治疗伤势 II | S | corruption; heal | field_restoration 按原生限制清腐化再回血；默认在首次观察到单位时执行。 |
| 71 | 治疗伤势 I | P | heal; corruption; medicae adapter | 清腐化和回血可组合；要精确等于某次医疗站的生命格规则需专门医疗站适配。 |
| 72 | 圣亚瑞克的赐福 | S | sprinting condition; toughness/power stats | stillness_blessing 按非疾跑状态提供韧性减伤与能量。 |
| 73 | 圣凯恩的赐福 | S | movement/block/stamina/spread stats | agility_blessing 提供四项原生属性修正。 |
| 74 | 圣阿特的赐福 | P | on_kill; effect.invisible | melee_shelter 提供 3 秒隐身并加 5 秒冷却；原图无冷却，可自行调整，但仍受原生感知规则。 |
| 75 | 快马加鞭 | P | movement/attack stats; DOT cadence adapter | 能修改消费属性的移速和攻速；敌我全动作、换弹切枪及 DOT 结算统一翻倍未实现。 |
| 76 | 排山倒海 | S | HCM/HED compositions; spawn_formation | 可在编队与类别编成中提高罐头比例；原图未给确定比例，需作者选定分配。 |
| 77 | 空白／待定 | B | — | 未提供具体效果；不推测或生成隐藏规则。 |
| 78 | 瘟疫传染 | A | coherency comparisons; corruption damage | 需要比较邻近玩家腐化比例并施加限定腐化；现条件不支持跨玩家数值公式，也没有施加腐化动作。 |
| 79 | 寻找巴丁 | R | model scale; animation; collision; hit zones | 缩小玩家涉及外观、碰撞、镜头与命中区；笑话补充不能当作已定义规则。 |
| 80 | 找到巴丁 | A | hit-zone/weakspot classification | 需更改原生命中区判定；增加弱点伤害不会让下半身自动成为弱点。 |
| 81 | 快如闪电 | A | AI action timing; animation/network | 取消敌人前摇需逐动作审计，不能用攻速倍率保证所有攻击无前摇。 |
| 82 | 风暴兵 | P | spread_modifier; recoil/sway paths | 可增大散布模拟射击偏差；“任何敌人都打不中”不是可保证的数值效果。 |
| 83 | 超级地球的援助 | P | damage_vs_*; explosion consumers | 可按护甲/敌人类型减伤及部分爆炸路径调整；原图武器惩罚的全部路径需逐武器验证。 |
| 84 | 二次元 | R | external assets; client cosmetics | 不强制下载安装其他模组；人物替换资源与各端外观同步不属于此数据框架。 |
| 85 | 阿贝拉德! | R | companion assets/behavior; dialogue | 图片只有台词，没有确定战斗规则；需先定义随从、语音或效果。 |
| 86 | 我是奶龙 | R | external media; audio event mapping | 自定义音频资源、全部事件映射和每客户端播放适配尚未提供。 |
| 87 | 铁斩波 | S | on_damage_dealt; toughness event_damage | iron_river 按实际事件伤害恢复等量韧性，含 0.1 秒冷却和原生恢复修正。 |
| 88 | 我是答案但问题是什么 | A | checkpoint/mission flow; interaction UI | 需要新增任务交互、题库、暂停/通过规则及多人同步，当前接口不覆盖。 |
| 89 | 空白／待定 | B | — | 未提供具体效果；不推测或生成隐藏规则。 |
| 90 | 呼叫补给 | P | interval; pickup | call_supplies 示例给每人落两箱；随机单人、背包占用检测与直接入槽未实现。 |
| 91 | 空白／待定 | B | — | 未提供具体效果；不推测或生成隐藏规则。 |
| 92 | 救赎教的怒火 | P | fire damage consumers; self damage | 部分火焰属性可配；排除魂火且让所有火焰伤害灵能者，需区分火焰来源与友伤许可。 |
| 93 | 大聪明 | A | minigame result event; damage | 伤害动作已存在；任务小游戏失误的可靠事件与玩家归属需新增适配。 |
| 94 | 力量蜕变 | A | pre/post damage; despawn/replace; seeded pool | 现 HED 增援不替换受击单位；需保护任务实体、死亡归属和新旧单位交接。 |
| 95 | 无限火力 | S | no_ammo_consumption; overheat_amount; ability_cooldown_modifier | infinite_test 提供不耗弹、热量增量零和技能冷却 -80%；不等于无限手雷或危机值。 |
| 96 | 空白／待定 | B | — | 未提供具体效果；不推测或生成隐藏规则。 |
| 97 | 同归于尽 | P | enemy_died; delay; damage; projectile adapter | 可延迟造成邻近生命伤害；真实敌方核弹手雷、爆炸表现和物理抛掷尚未提供。 |
| 98 | 你走了那我们吃什么 | R | membership event; external audio | 成员变化可由未来适配捕捉；此音频素材和自定义播放接口未提供。 |
| 99 | 是啊吃什么 | R | behavior specification; media | 没有触发条件和明确效果，不能推断为可执行词条。 |
| 100 | 再三套 | R | defined detection source; per-client audio | “检测到新三相关内容”缺少可判定条件；静音也需本地音频适配。 |
| 101 | 哪里逃 | A | dodge hit rejection; movement damage reductions | 修改闪避距离/余效不能保证移除所有闪避无敌和动作减伤，需逐原生判定适配。 |
| 102 | 不堪重负 | A | inventory carry state; sprint/slide transitions | 需物品携带与职业判定，接入疾跑/滑铲状态转换；通用移速降低不是等价行为。 |
| 103 | animals | R | enemy_died; external audio | 死亡触发已有；指定音乐素材、授权来源与各端播放属于外部资源适配。 |
| 104 | 释然了 | R | downed event; external audio | 可利用原生倒地事件，但指定歌曲播放未提供。 |
| 105 | 烫手山芋 | A | custom pocketable; inventory transfer; explosion | 需要新可携带物、计时爆炸、掉落/转移与多人所有权，超出现有 pickup 动作。 |
| 106 | 混合物 | P | on_syringe_used; native_buff | mixed_stimms 附加能量、速度、技能药剂；未把所有治疗药剂的即时治疗行为一并复刻。 |
| 107 | 经典 DOOM 模式 | P | no_ammo_consumption; ammo/clip adapter | 不耗弹关键词可近似；“仍耗备用弹但免换弹”的严格版本需自动弹匣供弹适配。 |
| 108 | 战败 CG | R | mission-end UI; external video | 需要视频资源、播放 UI 和各端退出清理，当前框架不加载外部视频。 |
| 109 | RON | P | damage/power/stamina stats | 可组合数值惩罚，但“肌无力”没有给出具体属性与幅度。 |
| 110 | COD | S | recoil_modifier | deadeye_recoil 将原生后坐倍率降为零；其他瞄准晃动仍按原生处理。 |
| 111 | GFL | R | behavior specification; model/weapon system | 没有可实现的明确规则；若指人物变武器，需要独立玩法和资产。 |
| 112 | Batman | R | behavior specification | “能做任何事”没有可验收的范围，不能作为接口实现承诺。 |
| 113 | PVP 模式 | R | chat messaging policy; game rule specification | 没有实现自动辱骂或替玩家发言；可另行定义不发送聊天消息的对战规则。 |
| 114 | 空白／待定 | B | — | 未提供具体效果；不推测或生成隐藏规则。 |
| 115 | 空白／待定 | B | — | 未提供具体效果；不推测或生成隐藏规则。 |
| 116 | 空白／待定 | B | — | 未提供具体效果；不推测或生成隐藏规则。 |
| 117 | 空白／待定 | B | — | 未提供具体效果；不推测或生成隐藏规则。 |
| 118 | 空白／待定 | B | — | 未提供具体效果；不推测或生成隐藏规则。 |
| 119 | 亡灵杀手 | S | damage_vs_chaos_poxwalker; damage_vs_chaos_newly_infected | undead_hunter 对这两类原生行尸增加 50% 伤害；特殊变异行尸可自行补目录 ID。 |
| 120 | 地狱已满 | P | selection; pause_spawns; stats; ammo; stamina | 可组合多数数值惩罚和暂停类别；仅随机可抽、排斥全部其他词条、移除闪避滑铲和全敌人行为缩放尚需扩展。 |
| 121 | 近战疲劳 | P | on_hit; stamina; interval; effect | labour_melee 按命中事件扣体力，空体力短时减攻速/伤害；有 0.05 秒节流，密集多目标命中不会逐个无限计费。 |
| 122 | PANZER | R | vehicle asset; input; physics; networking | 需要全新的可操作载具及地图适配，不是普通天赋或 Buff 字段。 |
