# 死靈試煉適配規則核對

核對物件：MortisBuffManager 4.0.0 與本地遊戲 Lua 1.12.5（提交 `0f0cb45991e9305ef4a7b925370792d7d6035f95`）。修復版本：MortisBuffManager 4.0.1。結論來自原始碼和離線執行，不是遊戲實機驗收。

當前行為：職業、當前閃擊、戰鬥技能、天賦和資源條件先決定候選資格，再按權重抽取。DIY 已加入統一獎勵池；等級僅為標籤。以下原生適配審計仍然適用。

| 維度 | 原版 | Mod 核對與修復 |
| --- | --- | --- |
| 職業 | 通用傳奇池加當前職業池。 | 原生愁緒已遵循；DIY 現在在手選、隨機預覽、開局選擇、房主接納和持續應用時檢查。 |
| 閃擊 | 使用已裝備閃擊的準確 `name` 取池。 | 原生愁緒已有；DIY 新增 `grenade_abilities`，按當前閃擊名檢查。 |
| 戰鬥技能 | 使用已裝備戰鬥技能的 `ability_group` 取池。 | 原生愁緒已有；DIY 新增 `combat_abilities`，填寫技能組，不是天賦節點名。 |
| 特定天賦 | 僅將選中天賦對應的傳奇加入候選。 | 已有；Mod 將 true 或正數視為選中，false／0 不滿足要求。 |
| 流派 | 先選流派，後續流派獎勵只從該流派取；傳奇獎勵獨立。 | 原有隔離保留。DIY 的 `families` 在抽選時也檢查；未確定流派時，限定流派的 DIY 不具備資格。 |
| 武器與資源 | 原版選擇器沒有通用的裝備適配過濾，部分效果在執行時訪問遠端槽彈藥或換彈。 | 補充下列 8 個已審計原生愁緒的資源限制。DIY 可宣告準確武器、武器關鍵詞、全部／任一資源要求，並自動推斷已審計的硬性資源依賴。 |
| 重複與失效候選 | 排除已獲得獎勵及後臺排除項。 | 原有規則保留；換裝使已顯示卡片失效時重新生成候選，舊卡片回覆不能消耗次數。DIY 不適配項先剔除，不佔數量或互斥組名額。 |
| 歐格林基礎手雷箱 | 選擇器自動新增隱藏的集束適配效果。 | 為 Mod 自定義發獎流程補齊；不佔獎勵名額。僅清理由 Mod 新增的例項，保留原版已有例項。 |
| 低血量等戰鬥條件 | 由效果本身在戰鬥中判斷。 | 不用開局滿血、滿彈等狀態否定抽選資格；裝備擁有資源機制與當前資源數值分開判斷。 |

## 原生武器依賴清單

以下條目檢查 `slot_secondary`。這是一份逐項核對的依賴表，不宣稱原版存在覆蓋全部效果的自動武器相容規則。

| 原生 ID | 必須具備 |
| --- | --- |
| `hordes_buff_auto_clip_fill_while_melee` | 彈藥機制 |
| `hordes_buff_no_ammo_consumption_on_crits` | 彈藥機制 |
| `hordes_buff_bonus_crit_chance_on_ammo` | 彈藥機制 |
| `hordes_buff_melee_damage_missing_ammo_in_clip` | 彈藥機制 |
| `hordes_buff_weakspot_ranged_hit_gives_infinite_ammo` | 彈藥機制 |
| `hordes_buff_veteran_infinite_ammo_during_stance` | 彈藥機制，同時保留原有職業／技能限制 |
| `hordes_buff_increased_damage_after_reload` | 換彈動作 |
| `hordes_buff_improved_weapon_reload_on_melee_kill` | 換彈動作 |

法杖不再進入依賴彈藥基礎獎勵的牛仔流派；其他流派只移除不相容專案。彈藥為零的槍仍擁有彈藥機制，不會因缺彈被排除。等離子槍同時具有彈藥和過熱機制。

## DIY 編寫規則

`availability` 各欄位之間取“同時滿足”。`archetypes`、`families`、`weapons`、`weapon_keywords`、`grenade_abilities`、`combat_abilities` 各列表內部取“任一匹配”；`talents` 和 `resources` 則要求全部滿足；`any_resources` 要求其中至少一種存在。

資源名：`ammo`、`reload`、`overheat`、`warp_charge`、`grenade_charges`、`combat_ability`、`melee`、`ranged`。靈能是職業機制；過熱是武器機制；手雷次數根據當前閃擊是否具有正數最大次數判斷，不能把所有閃擊都視為可補手雷。

武器名與關鍵詞來自原生武器模板，按兩個裝備槽檢查。物品有 `weapon_progression_template` 時遵循原版解析優先順序。配置未完整同步時暫緩選擇，不能用未知配置放行。大廳以已儲存配裝為準，任務中優先讀取實際裝備。任務內已確定的 DIY 選擇不重新隨機；條件失配時移除其效果，下次任務重新檢查。

自動推斷覆蓋已審計的彈藥／換彈／過熱／靈能／技能冷卻等屬性與自身資源動作。複雜事件、特殊關鍵詞、專屬武器機制不能僅憑任意 JSON 的文字自動推斷；作者必須明確填寫對應武器、技能或天賦要求。目錄收錄原生欄位不等於任意組合都有效。`any_resources` 允許模板明確宣告“靈能或過熱”的替代動作；它不能繞過被動效果自身的硬性要求。

11 個死靈入門模板已補充相應要求。已儲存的舊庫不會被覆蓋；自動資源檢查仍生效，新增模板宣告可透過重新匯出入門庫取得。HCM 的 34 個全域性詞條不套用某一玩家的 Mortis 選擇資格；共享庫隨相容更新發布為 4.0.1。HED 保持 3.1.0。

## 驗證與原始碼依據

- 原版實際選擇器與資料：128 組職業／閃擊／技能池組合；逐流派優先獎勵、傳奇分類、後臺排除和獎勵順序。
- 原生能力定義及原版武器解析器：7 職業、132 組技能組合；武器相關後設資料來自實際槍械、法杖、等離子槍與近戰模板，未執行渲染和攻擊動作。
- DIY：1000 個種子的抽選，檢查不適配高權重項不能佔配額；手選互斥組、缺失配裝、0／false 天賦、資源組合和下局換裝。
- 實際 Mod 生命週期與協議：房主拒絕不符職業／武器的請求，缺失配裝時等待，同局鎖定、重生、斷線和清理；場景服務及網路傳輸採用測試替身。
- 原生卡片失效及基礎手雷箱輔助效果的名額、歸屬、換閃擊和清理檢查。
- 三個工程迴歸及六個 DIY 套件。尚需遊戲內 SoloPlay／四人 Realms 配裝與網路驗收。

原始碼定位（均相對原生原始碼或 Mod 的指令碼目錄）：

- 原生 `scripts/managers/mission_buffs/mission_buffs_selector.lua`、`mission_buffs_allowed_buffs.lua`、`mission_buffs_settings.lua`。
- 原生 `scripts/settings/buff/hordes_buffs/hordes_family_buff_templates/`、`hordes_legendary_buff_templates/` 中的實際效果實現。
- 原生 `scripts/settings/ability/player_abilities/abilities/` 與 `scripts/utilities/weapon/weapon_template.lua`。
- Mod `modules/mortis_catalog.lua`、`modules/mortis_draft.lua`、`modules/mortis_buffs.lua`、`modules/diy_mortis.lua`、`modules/diy/diy_eligibility.lua`。
