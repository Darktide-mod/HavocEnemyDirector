# 三張圖片逐行可行性評估

本表保留原圖片第 3–122 行，覆蓋 120 行，包括空白與待定。名稱作閱讀整理，判斷以圖片效果描述為依據；圖片中文字沒有被當作執行指令。

**S**：本版介面支援主要效果（模板或可直接配置）。**P**：可實現部分或提供近似，後半欄明確差異。**A**：需要新增原生適配，當前 JSON 尚不能完成。**R**：缺少明確規則、外部資源或屬於獨立玩法。**B**：空白/待定。S 也不等於所有原生傷害路徑與四人實機均已驗證。

提供的模板是可修改示例，並未把圖片所有效果都實現。介面列中的程式碼名可以在手冊及原生目錄查詢；泛稱某介面卡表示未來需要建設的介面，不是可在 JSON 中填寫的新欄位。

| 圖片行 | 名稱/含義 | 結論 | 已用或所需介面 | 實際支援與缺口 |
| --- | --- | --- | --- | --- |
| 3 | 至死不渝·精英 | A | fatal-hit interception; death scheduling | 需在致命傷提交前攔截並保留死亡歸屬，再延遲 4 秒處決；現有受擊事件發生得太晚。 |
| 4 | 恐怖來襲 II | S | spawn.health_multiplier | 可按 breed/tag 乘算初始生命；monster_health_150 模板選擇三種普通怪物。 |
| 5 | 恐怖來襲 III | S | spawn.health_multiplier | 同上；monster_health_200 提供 ×2，兩個模板互斥。 |
| 6 | 彈藥匱乏 I | S | modifiers.ammo_pickup_multiplier | ammo_scarcity 將原生拾彈結算結果乘 0.75，與浩劫修正疊乘。 |
| 7 | 彈盡糧絕 II | P | ammo_pickup_failure_chance; pickup/deployable adapter | 已支援 50% 空彈藥；醫療包和部署箱失效仍需分別接入使用流程。 |
| 8 | 團結治療 III | S | interval; coherency; heal; corruption | coherent_medic 每秒恢復生命和腐化各 0.3，遵守原生禁療與連攜計數。 |
| 9 | 團結防禦 II | S | conditions; toughness_damage_taken_multiplier | coherent_defence 提供連攜時 35% 韌性減傷。 |
| 10 | 混亂火炮 IV | A | projectile/explosion; telegraph; native placement | 可用 interval 排程，但 4–8 個預警圈、軌跡、陣營與護甲傷害需專門彈幕適配；尚未實現。 |
| 11 | 受傷加深 I | S | damage_taken_multiplier | deeper_wounds 提供玩家承傷 ×1.1。 |
| 12 | 墮落之人 I | S | corruption_taken_multiplier | corrupting_touch 對讀取該原生屬性的腐化來源乘 1.3。 |
| 13 | 永恆之火 III | P | native_buff; liquid lifetime adapter | 可施加和續期已支援的敵方燃燒狀態；全部環境火焰永不熄滅及所有層數永久保留未實現。 |
| 14 | 空白／待定 | B | — | 未提供具體效果；不推測或生成隱藏規則。 |
| 15 | 帝皇賜福 IV | P | on_hit; kill; mission result adapter | 可對普通可生成敵人實施受限處決；不能據此保證全敵人秒殺或直接改任務勝負。 |
| 16 | 扭曲裂隙 | P | enemy_died; spawn_enemy; HED | 可死亡後請求不同敵人增援；原地縮小模型、繼承骨骼/行為/血量的分裂需額外適配。 |
| 17 | 腳扭了 I | P | dodge_distance_modifier; dodge_speed_multiplier; dodge_cooldown_reset_modifier | slow_feet 已覆蓋距離、速度；原圖所有閃避恢復速度的統一 -10% 未完整覆蓋。 |
| 18 | 堅不可摧 II·精英 | S | spawn.health_multiplier | elite_endurance 對原生標籤 elite 的敵人增加 40% 初始生命。 |
| 19 | 掠奪一空 | A | pickup spawning; level props; medicae interactions | 現介面可生成拾取物，不能統一禁止地圖預置物、掉落與醫療站；需分來源攔截。 |
| 20 | 韌性衰減 | A | melee health-bleedthrough calculation | 增加韌性承傷不等於改變滿韌性近戰生命洩漏比例；需適配原生傷害拆分。 |
| 21 | 戰爭狂熱 | P | enemy_died; effect; max_stacks | battle_fervour 實現 0.1% 能量、500 層、30 秒共享續期；原圖防禦增益和獨立層計時未實現。 |
| 22 | 綁架 | A | respawn/rescue manager | 禁止死亡後救援需接入重生與任務救援流程，不能用普通屬性可靠替代。 |
| 23 | 雙生奸奇 | P | enemy_died; spawn_enemy; HED | split_reinforcements 是精英死亡後有限次請求兩個行屍；未實現每種敵人的原地分裂。 |
| 24 | 暗無天日 | A | flashlight; perception ranges; environment | 個人照明和敵人感知是不同系統；需限定範圍並同步各端。 |
| 25 | 保底 | P | pickup; loot-container interaction adapter | 可以在玩家附近生成箱子；指定地圖補給箱開啟時必掉兩箱尚未接入。 |
| 26 | 友誼詛咒 | A | coherency distance; pre-damage routing | 附近群體傷害動作不能精確代替受擊前的傷害分攤、遠距離判定與倒地規則。 |
| 27 | 未命名·隨機死亡產物 | P | enemy_died; chance; spawn_enemy; pickup | 支援限定列表裡的敵人與拾取物機率動作；爆桶和任意道具不在現介面內，隨機互斥分支仍需擴充套件。 |
| 28 | 腳滑 | A | AI locomotion; animation; action state | 敵人攻擊中移動需逐行為樹/動畫改造，單獨移速屬性不足以實現。 |
| 29 | 壁壘 | S | ranged_damage_taken_multiplier | ranged_monster_shield 對 monster 標籤設遠端承傷倍率為零；特殊繞行傷害路徑除外。 |
| 30 | 奸奇閃電 | A | lightning FX; damage; despawn/replace | 閃電錶現、命中選擇、保留任務所有權的變形尚未實現；HED 新增怪物不等同原位變形。 |
| 31 | 友軍之圍 | A | native friendly-fire permission; attack profiles | 原生友傷許可與傷害配置需專門適配；對隊友額外扣血不是等價實現。 |
| 32 | 破傷風 I | P | on_damage_taken; chance; damage-over-time | 可組合機率持續扣血，但原生玩家流血、狂戰/Boss 加倍、繞韌機率需專門狀態適配。 |
| 33 | 破傷風 II | P | on_damage_taken; chance; damage-over-time | 同 32 行；可以調整機率，未提供精確原圖流血機制。 |
| 34 | 破傷風 III | P | on_damage_taken; chance; damage-over-time | 同 32 行；更高機率不改變所缺失的玩家流血適配。 |
| 35 | 慈父毒氣 | A | minion FX; death callback; liquid/gas area | 生成時冒煙及死亡毒氣區域需要可同步的特效與區域傷害生命週期。 |
| 36 | 混亂詛咒 | A | spawn replacement; loot replacement; seeded pool | 已有確定種子的配置抽取，但全域性替換原生敵人與拾取結果需新增來源適配及相容規則。 |
| 37 | 迴歸本源 | A | profile/talent/equipment adapters | 不會透過 DIY 改寫玩家裝備和正式天賦；臨時隔離構築也需獨立、可恢復的適配。 |
| 38 | 荒誕驚喜 | P | ammo_pickup_multiplier; pickup; loot adapter | 彈藥量翻倍和扣彈可做；同時影響手雷、取得結果轉為扣當前一半需要拾取事件前適配。 |
| 39 | 俄禰連擊 | A | weapon action state; charge timing; self damage | 傷害倍率可改，但蓄力不自動釋放、充能曲線和自傷時點需武器動作適配。 |
| 40 | 寫真實模式 | A | HUD visibility; per-client UI | 需要本地 UI 開關及房間約定；服務端屬性無法替所有客機隱藏所有介面。 |
| 41 | 納垢花園顯現 | P | health fraction conditions; native_buff; corrosion adapter | 可按低生命條件施加支援的增益；玩家長期 1 腐化和全套毒花增益需進一步適配。 |
| 42 | 蠅群感染 | A | minigame/interaction trigger; spawned area FX | 刷取任務互動和可近戰擊破的蠅群實體需要專門資產與互動適配。 |
| 43 | 戰爭首領 | P | interval; spawn_formation; HED | 可在 Boss 存活條件下請求增援；若要連長招手動作、專屬呼叫節奏需接入 AI 行為。 |
| 44 | 血祭血神 | P | on_hit; kill; toughness; damage | 支援普通敵人受限處決及扣韌/生命；玩家首擊清空韌性再按近戰判死需原生傷害適配。 |
| 45 | 布娃娃模式 | P | impact/stat consumers; stagger adapter | 可調整讀取屬性的衝擊；敵我通用“擊飛強度翻倍”還涉及閾值、布娃娃和各攻擊配置。 |
| 46 | 終極困難 | P | prevent_all_healing; HED composition; event adapters | no_healing 已實現禁療；HCM/HED 可編輯編成和增援，但沒有統一替換全部普通敵人與新增任務事件。 |
| 47 | 血手之怒 | S | on_sweep_start; toughness; stats | blood_price 提供消耗韌性與攻速、能量、恢復加成；以原生近戰 sweep 事件計費。 |
| 48 | 聖梅基麗娜的賜福 | S | on_kill; heal; coherency; effect | martyr_blessing 近戰擊殺回血並在連攜時提供短時能量加成。 |
| 49 | 聾的傳人 | A | audio buses; per-client settings | 需受控的音訊匯流排適配；現 sound 動作只播放原生 UI 音效。 |
| 50 | 你再看看你後面呢 | A | enemy audio event routing | 需篩選敵人警告與攻擊音訊事件，不能用全域性靜音代替。 |
| 51 | 吃吃爆 | P | HED specials; audio routing | 可增加自爆特感請求；僅消除自爆音效仍需音訊適配。 |
| 52 | 混沌卵開智 | A | boss behavior tree; carried minion; animation | 抓取、持有並投擲另一敵人是新的複合 AI 動作，現通用介面不覆蓋。 |
| 53 | 飛起來 | A | jump locomotion; prediction | 不是已驗證的通用 Buff 屬性；需人物運動與客戶端預測適配。 |
| 54 | 靈魂鏈 | A | damage redistribution; proximity; incapacitation | 精確分攤需受擊前攔截、保護遞迴和倒地狀態處理；群體傷害動作只能近似。 |
| 55 | mine! | P | spawn_enemy; AI flee; pickup | 可有限生成敵人和死亡掉落物；寶藏哥原生逃跑行為與專屬單位未開放為自由生成。 |
| 56 | 變幻無常 | A | interval; lightning; transformation | 週期排程可用；對玩家雷擊並隨機變形敵人的複合機制尚需獨立適配。 |
| 57 | 破傷風 max | P | chance; damage; native_buff | 可配置部分機率與傷害；精確玩家流血、BOSS 秒殺和繞甲分支未實現。 |
| 58 | 失憶症 | A | perception/aggro/target state | 需要逐敵人清理目標並允許之後重新發現；不等同隱身關鍵詞。 |
| 59 | 等等! | S | pause_spawns | wait_a_moment 暫停許可檢查與 HED 30 秒；任務指令碼繞行生成不保證停止。 |
| 60 | 手無寸鐵 | P | spawn; ammo; health; rescue-specific event | 可以在生成時扣彈和生命；僅針對獲救、不影響首次出生的判定尚需救援事件。 |
| 61 | 劍聖 | A | heavy-attack classification; critical roll | 全近戰必暴可表達，但只讓重擊在原生判暴前必暴需要精確動作時序適配。 |
| 62 | 暴斃 | S | extra_max_amount_of_wounds | 可用現有原生數值減少生命格；最終最小格數及職業規則由遊戲決定。 |
| 63 | 腐蝕環境 | P | interval; toughness; health condition; damage | corrosive_air 實現扣韌與空韌掉血；原圖同時壓制全部韌性恢復的程度需另配屬性。 |
| 64 | 友軍之圍·敵方版 | A | AI attack profiles; friendly-fire damage | 需要審計敵方各攻擊路徑的友傷倍率，不是玩家承傷欄位。 |
| 65 | 剋扣物資 | S | ammo current_fraction; grenades | supply_tax 扣每把武器當前彈藥的一半並清空手雷，整數向零取整。 |
| 66 | 大爆炸 | P | explosion stats; explosion template adapter | 能改變讀取現有屬性的玩家爆炸路徑；所有敵我和地圖爆炸範圍/傷害並未統一覆蓋。 |
| 67 | 空白／待定 | B | — | 未提供具體效果；不推測或生成隱藏規則。 |
| 68 | 帝皇庇佑 IV | P | on_kill; heal; interval damage | 可近似擊殺回血後衰減，但缺少獨立臨時生命池與不會誤扣真實生命的消耗規則。 |
| 69 | 敏感肌 | P | on_damage_taken; chance; effect | 受擊機率增益可做；按命中次數計數後從互斥增益池抽一項需計數/分支擴充套件。 |
| 70 | 治療傷勢 II | S | corruption; heal | field_restoration 按原生限制清腐化再回血；預設在首次觀察到單位時執行。 |
| 71 | 治療傷勢 I | P | heal; corruption; medicae adapter | 清腐化和回血可組合；要精確等於某次醫療站的生命格規則需專門醫療站適配。 |
| 72 | 聖亞瑞克的賜福 | S | sprinting condition; toughness/power stats | stillness_blessing 按非疾跑狀態提供韌性減傷與能量。 |
| 73 | 聖凱恩的賜福 | S | movement/block/stamina/spread stats | agility_blessing 提供四項原生屬性修正。 |
| 74 | 聖阿特的賜福 | P | on_kill; effect.invisible | melee_shelter 提供 3 秒隱身並加 5 秒冷卻；原圖無冷卻，可自行調整，但仍受原生感知規則。 |
| 75 | 快馬加鞭 | P | movement/attack stats; DOT cadence adapter | 能修改消費屬性的移速和攻速；敵我全動作、換彈切槍及 DOT 結算統一翻倍未實現。 |
| 76 | 排山倒海 | S | HCM/HED compositions; spawn_formation | 可在編隊與類別編成中提高罐頭比例；原圖未給確定比例，需作者選定分配。 |
| 77 | 空白／待定 | B | — | 未提供具體效果；不推測或生成隱藏規則。 |
| 78 | 瘟疫傳染 | A | coherency comparisons; corruption damage | 需要比較鄰近玩家腐化比例並施加限定腐化；現條件不支援跨玩家數值公式，也沒有施加腐化動作。 |
| 79 | 尋找巴丁 | R | model scale; animation; collision; hit zones | 縮小玩家涉及外觀、碰撞、鏡頭與命中區；笑話補充不能當作已定義規則。 |
| 80 | 找到巴丁 | A | hit-zone/weakspot classification | 需更改原生命中區判定；增加弱點傷害不會讓下半身自動成為弱點。 |
| 81 | 快如閃電 | A | AI action timing; animation/network | 取消敵人前搖需逐動作審計，不能用攻速倍率保證所有攻擊無前搖。 |
| 82 | 風暴兵 | P | spread_modifier; recoil/sway paths | 可增大散佈模擬射擊偏差；“任何敵人都打不中”不是可保證的數值效果。 |
| 83 | 超級地球的援助 | P | damage_vs_*; explosion consumers | 可按護甲/敵人型別減傷及部分爆炸路徑調整；原圖武器懲罰的全部路徑需逐武器驗證。 |
| 84 | 二次元 | R | external assets; client cosmetics | 不強制下載安裝其他模組；人物替換資源與各端外觀同步不屬於此資料框架。 |
| 85 | 阿貝拉德! | R | companion assets/behavior; dialogue | 圖片只有臺詞，沒有確定戰鬥規則；需先定義隨從、語音或效果。 |
| 86 | 我是奶龍 | R | external media; audio event mapping | 自定義音訊資源、全部事件對映和每客戶端播放適配尚未提供。 |
| 87 | 鐵斬波 | S | on_damage_dealt; toughness event_damage | iron_river 按實際事件傷害恢復等量韌性，含 0.1 秒冷卻和原生恢復修正。 |
| 88 | 我是答案但問題是什麼 | A | checkpoint/mission flow; interaction UI | 需要新增任務互動、題庫、暫停/透過規則及多人同步，當前介面不覆蓋。 |
| 89 | 空白／待定 | B | — | 未提供具體效果；不推測或生成隱藏規則。 |
| 90 | 呼叫補給 | P | interval; pickup | call_supplies 示例給每人落兩箱；隨機單人、揹包佔用檢測與直接入槽未實現。 |
| 91 | 空白／待定 | B | — | 未提供具體效果；不推測或生成隱藏規則。 |
| 92 | 救贖教的怒火 | P | fire damage consumers; self damage | 部分火焰屬性可配；排除魂火且讓所有火焰傷害靈能者，需區分火焰來源與友傷許可。 |
| 93 | 大聰明 | A | minigame result event; damage | 傷害動作已存在；任務小遊戲失誤的可靠事件與玩家歸屬需新增適配。 |
| 94 | 力量蛻變 | A | pre/post damage; despawn/replace; seeded pool | 現 HED 增援不替換受擊單位；需保護任務實體、死亡歸屬和新舊單位交接。 |
| 95 | 無限火力 | S | no_ammo_consumption; overheat_amount; ability_cooldown_modifier | infinite_test 提供不耗彈、熱量增量零和技能冷卻 -80%；不等於無限手雷或危機值。 |
| 96 | 空白／待定 | B | — | 未提供具體效果；不推測或生成隱藏規則。 |
| 97 | 同歸於盡 | P | enemy_died; delay; damage; projectile adapter | 可延遲造成鄰近生命傷害；真實敵方核彈手雷、爆炸表現和物理拋擲尚未提供。 |
| 98 | 你走了那我們吃什麼 | R | membership event; external audio | 成員變化可由未來適配捕捉；此音訊素材和自定義播放介面未提供。 |
| 99 | 是啊吃什麼 | R | behavior specification; media | 沒有觸發條件和明確效果，不能推斷為可執行詞條。 |
| 100 | 再三套 | R | defined detection source; per-client audio | “檢測到新三相關內容”缺少可判定條件；靜音也需本地音訊適配。 |
| 101 | 哪裡逃 | A | dodge hit rejection; movement damage reductions | 修改閃避距離/餘效不能保證移除所有閃避無敵和動作減傷，需逐原生判定適配。 |
| 102 | 不堪重負 | A | inventory carry state; sprint/slide transitions | 需物品攜帶與職業判定，接入疾跑/滑鏟狀態轉換；通用移速降低不是等價行為。 |
| 103 | animals | R | enemy_died; external audio | 死亡觸發已有；指定音樂素材、授權來源與各端播放屬於外部資源適配。 |
| 104 | 釋然了 | R | downed event; external audio | 可利用原生倒地事件，但指定歌曲播放未提供。 |
| 105 | 燙手山芋 | A | custom pocketable; inventory transfer; explosion | 需要新可攜帶物、計時爆炸、掉落/轉移與多人所有權，超出現有 pickup 動作。 |
| 106 | 混合物 | P | on_syringe_used; native_buff | mixed_stimms 附加能量、速度、技能藥劑；未把所有治療藥劑的即時治療行為一併復刻。 |
| 107 | 經典 DOOM 模式 | P | no_ammo_consumption; ammo/clip adapter | 不耗彈關鍵詞可近似；“仍耗備用彈但免換彈”的嚴格版本需自動彈匣供彈適配。 |
| 108 | 戰敗 CG | R | mission-end UI; external video | 需要影片資源、播放 UI 和各端退出清理，當前框架不載入外部影片。 |
| 109 | RON | P | damage/power/stamina stats | 可組合數值懲罰，但“肌無力”沒有給出具體屬性與幅度。 |
| 110 | COD | S | recoil_modifier | deadeye_recoil 將原生後坐倍率降為零；其他瞄準晃動仍按原生處理。 |
| 111 | GFL | R | behavior specification; model/weapon system | 沒有可實現的明確規則；若指人物變武器，需要獨立玩法和資產。 |
| 112 | Batman | R | behavior specification | “能做任何事”沒有可驗收的範圍，不能作為介面實現承諾。 |
| 113 | PVP 模式 | R | chat messaging policy; game rule specification | 沒有實現自動辱罵或替玩家發言；可另行定義不傳送聊天訊息的對戰規則。 |
| 114 | 空白／待定 | B | — | 未提供具體效果；不推測或生成隱藏規則。 |
| 115 | 空白／待定 | B | — | 未提供具體效果；不推測或生成隱藏規則。 |
| 116 | 空白／待定 | B | — | 未提供具體效果；不推測或生成隱藏規則。 |
| 117 | 空白／待定 | B | — | 未提供具體效果；不推測或生成隱藏規則。 |
| 118 | 空白／待定 | B | — | 未提供具體效果；不推測或生成隱藏規則。 |
| 119 | 亡靈殺手 | S | damage_vs_chaos_poxwalker; damage_vs_chaos_newly_infected | undead_hunter 對這兩類原生行屍增加 50% 傷害；特殊變異行屍可自行補目錄 ID。 |
| 120 | 地獄已滿 | P | selection; pause_spawns; stats; ammo; stamina | 可組合多數數值懲罰和暫停類別；僅隨機可抽、排斥全部其他詞條、移除閃避滑鏟和全敵人行為縮放尚需擴充套件。 |
| 121 | 近戰疲勞 | P | on_hit; stamina; interval; effect | labour_melee 按命中事件扣體力，空體力短時減攻速/傷害；有 0.05 秒節流，密集多目標命中不會逐個無限計費。 |
| 122 | PANZER | R | vehicle asset; input; physics; networking | 需要全新的可操作載具及地圖適配，不是普通天賦或 Buff 欄位。 |
