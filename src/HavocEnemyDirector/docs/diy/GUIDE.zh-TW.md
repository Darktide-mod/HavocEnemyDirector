# DIY 天賦與詞條使用手冊

設計與驗證：另見 ARCHITECTURE.zh-CN.md 與 VERIFICATION.zh-CN.md。

適用：MortisBuffManager 4.4.0、HavocConditionManager 4.3.0、HavocEnemyDirector 3.2.0。資料格式為 `Darktide.DIY` 版本 `1`。原生介面審計基於遊戲 Lua 1.12.5，提交 `0f0cb45991e9305ef4a7b925370792d7d6035f95`。已完成原始碼及離線原生方法檢查；尚未完成遊戲中的多人實機驗收。

## 先開始使用

1. 在大廳輸入 `/mortisbuffs`，三種獎勵模式均可進入統一的「死靈天賦池」。在「包管理」中檢查自動載入的包、匯出入門包或把貼上 JSON 轉換為包。HCM 保留自己的「DIY 詞條」頁面。
2. 死靈入門模板共十二項，含 `fivefold_salvo`；HCM 共 34 項。完整的資料包及可執行 Lua 示例位於 `package-examples/`，每個詞條一個資料夾，獨立儲存本詞條的 JSON、Lua 和資源，複製到對應目錄後可單獨管理。
3. 原生與 DIY 開關彼此獨立。房主設定房間規則和 DIY 單項許可權；原生只有整池開關。列表支援直接搜尋、來源／可入池篩選、詳情，以及覆蓋全部篩選頁的批次操作。
4. 預選模式在開局前選擇，原生與 DIY 名額分開計算。進度／競爭模式將適配的原生與 DIY 放入同一套獎勵卡；只要原生池開啟，開局仍先選原生流派。只有 DIY 開啟時，開局直接抽選 DIY。所有模式均可檢視列表。
5. Realms 每位真人都須確認對應 DIY 定義一致，該項才可入池。缺少或定義不同會對全房間置灰，詳情列出玩家姓名；其他已安裝包可以不同，對應條目的包 ID、內容與依賴須一致。所有玩家須使用當前死靈版本，修改權重也屬於定義變化。
6. 配置後進入新任務，任務中鎖定本局選擇與房間控制元件；重新整理和匯入可以準備下一局的包。HCM 應用所有已啟用且勾選的詞條；死靈由當前獎勵模式決定獲得方式。每項 DIY 天賦消耗 1 點，總點數預設六點。等級僅為展示標籤，不限制抽選數量；適配與互斥規則繼續決定可入池資格。

使用者檔案目錄分別為：

```text
%APPDATA%/Fatshark/Darktide/MortisBuffManager/diy/packages/
%APPDATA%/Fatshark/Darktide/HavocConditionManager/diy/packages/
```

啟動自動發現並合併有效包，重新整理用於遊戲中新增或修改檔案。無效包顯示原因，其他獨立有效包繼續載入。未選擇的條目不生效，匯出保留完整包且不覆蓋作者檔案。JSON 仍是嚴格資料結構；可選的本地 Lua 透過版本化包介面實際執行。目錄、依賴、資源及指令碼示例見 [PACKAGES.zh-CN.md](PACKAGES.zh-CN.md)。

死靈按當前獎勵模式統一使用原生與 DIY 天賦，不改寫官方天賦樹、物品欄或伺服器結算獎勵。HCM DIY 仍獨立於官方詞條。

## 敵人更新與清理

玩家和敵人的原生類會複製繼承方法，執行時分別接入實際類。已選的敵人效果或事件規則會啟用原本空閒的敵人 buff 更新，覆蓋執行時啟動前已生成的敵人。兩個 DIY 模組共用更新所有權；最後一個使用者停止後，無原生 buff 的敵人恢復原生屬性和空閒狀態，有原生 buff 的敵人繼續原生更新。僅作用於玩家的被動配置不啟用空閒敵人更新。大量敵人的條件效果仍有逐敵人計算開銷，密集場景效能需實機測量。

## 配置結構

最小示例：

```json
{
  "format": "Darktide.DIY",
  "version": 1,
  "kind": "mortis",
  "id": "my_talents",
  "name": {"en": "My talents", "zh-cn": "我的天賦"},
  "entries": [{
    "id": "steady",
    "name": "穩健射手",
    "description": "換彈速度提高 10%。",
    "tier": 1,
    "passive": {"stats": {"reload_speed": 0.1}}
  }]
}
```

HCM 使用 `"kind":"conditions"`。兩個檔案型別不可混用。

| 層級 | 欄位與含義 |
| --- | --- |
| 配置庫 | `format`、`version`、`kind`、`id`、`name`、可選 `description`、`entries` |
| 條目 | 必填 `id`、`name`、`description`；可選 `enabled`（預設 true）、`tier`（展示標籤 1–4，預設 1）、`weight`（0–1000，預設 1）、`exclusive_group`、`source_row` |
| 作用範圍 | `targets`、`availability`、`conditions`、`match`；至少提供 `passive`、`spawn` 或非空 `rules` 中的一項 |
| 常駐效果 | `passive` 包含 `stats`、`keywords`、`modifiers` 中的一項或多項 |
| 生成時效果 | HCM 專用 `spawn: {"health_multiplier": 1.4}`；靜態篩選，不支援與條目級動態 `conditions` 同時使用 |
| 事件規則 | `rules` 陣列；每條有獨立 ID、事件、條件、機率、冷卻、次數、延遲和動作 |

ID 以小寫字母開頭，後續只能是小寫字母、數字、下劃線和短橫線，最長 64 位元組；同一配置庫條目 ID 唯一，同一條目的規則 ID 唯一。名稱和說明可用一個字串，也可用 `en`、`zh-cn`、`zh-tw` 的物件；至少提供英語或簡體中文。字串中的換行寫作 `\n`。百分號直接寫 `%`。介面僅展示有限長度的詳情，完整說明保留在 JSON 中。

死靈的 `exclusive_group` 表示同組最多選擇一個，手動選擇與加權抽取都受總數、互斥組及條目 `enabled` 限制；HCM 只按啟用狀態與勾選列表應用詞條。加權抽取只從適配且在池內的候選按正權重抽取；等級不改變抽選或點數消耗。死靈的職業可用性在人物生效時檢查，初選不會自動替換當前職業不可用的條目。

### 目標與條件

`targets` 預設 `{"kind":"players"}`。`kind` 可選 `players`、`minions`、`all`；死靈條目只允許 `players`。`breeds` 和 `archetypes` 陣列內部是任選其一；`tags` 要全部滿足，`exclude_tags` 任意命中即排除；不同篩選欄位之間是“並且”。識別符號必須來自 `native-catalog.json`。例如所有精英為 `{"kind":"minions","tags":["elite"]}`。

死靈還可設定 `availability: {"archetypes":["veteran"],"families":["fire"],"talents":["實際天賦ID"]}`。三個維度同時滿足才生效。原生流派 ID 和職業列在目錄中；`talents` 檢查角色 profile 中為 true 或大於零的天賦。自定義天賦不負責分配這些原生天賦。

條件示例：`{"subject":"self","field":"health","op":"lt","value":0.5}`。`subject` 預設 self，也可選 target 或 attacker。`match` 預設 all，可設 any。不存在的資料不會滿足任何比較，包括 `ne` 和 `not_contains`。

| 條件欄位 | 數值、單位或語義 |
| --- | --- |
| `health`, `toughness`, `corruption`, `ammo`, `stamina`, `warp_charge`, `overheat` | 0–1 比例；彈藥為副武器當前彈匣加備用量佔總容量的比例 |
| `coherency` | 原生連攜計數；模板用至少 2，實際包含關係遵守遊戲原生實現 |
| `progress` | 主路徑推進米數，不是 0–100 百分比 |
| `load`, `players`, `monsters` | 原生戰鬥負擔、可行動玩家數、已仇恨怪物數 |
| `elapsed` | 當前 DIY 執行例項經過的秒數 |
| `stage`, `phase` | 原生 Pacing 狀態字串；HED 階段為 build/pressure/recovery |
| `breed`, `archetype`, `attack_type` | 原生識別符號；攻擊型別取當前事件，未提供時條件不滿足 |
| `critical`, `weakspot` | 當前事件提供的暴擊/弱點布林值 |
| `sprinting`, `dodging`, `sliding`, `knocked_down` | 當前人物狀態 |
| `in_combat` | 本框架近 8 秒收到受傷、造成傷害或命中事件；不是一個新增原生戰鬥判定 |
| `native_condition`, `affix`, `signal`, `tag` | 集合：官方詞條 ID、當前 HCM DIY 條目 ID、有效訊號 ID、單位標籤 |
| `event.FIELD` | 原生事件裡的白名單標量欄位；95 個欄位及型別見目錄。並非每個事件都包含所有欄位 |

數值比較：`eq/ne/gt/ge/lt/le`。字串、布林：`eq/ne`。集合：`contains/not_contains`。條件不支援任意表示式、跨單位數值公式或執行程式碼。

### 屬性與關鍵詞

完整目錄提供 **411 個原生屬性、181 個關鍵詞、105 個原生事件、95 個事件標量欄位**。這是可表達介面範圍，不代表每個欄位對所有職業、武器、敵人和傷害路徑都有作用；遊戲必須實際讀取該屬性。內部特殊關鍵詞尤其需要結合原生實現使用。

| 原生屬性型別 | JSON 值的意義 | 例子 |
| --- | --- | --- |
| `additive_multiplier` | 在原生倍率上增加差值；各層差值相加 | `reload_speed: 0.1` 為 +10%；`recoil_modifier: -0.5` 為 -50% 倍率差值 |
| `multiplicative_multiplier` | 與原生值及各 DIY 層相乘 | `damage_taken_multiplier: 0.8` 為承傷 ×0.8 |
| `value` | 原生數值上加值；單位依消費者決定 | 暴擊機率通常 0.1 表示 10 個百分點；查目錄型別及對應原生消費者 |
| `max_value` | 與原生值及其他效果取最大值 | 不按疊層次數重複累加 |

每個 effect 最多 64 個 stats、32 個 keywords。單項數值 -1000–1000；乘法倍率與最大值不得為負，加法倍率差值不得小於 -1。彙總也有邊界：乘法最大 1000，加法倍率差值最低 -1。極端值可能越過原生預期，不等於所有組合都有合理玩法效果。

`keywords` 是啟用關鍵詞的字串陣列，不支援關閉其他模組或原生已擁有的關鍵詞。DIY 撤銷只移除自身貢獻。`modifiers` 支援 `ammo_pickup_multiplier`（0–10，多個效果相乘）和 `ammo_pickup_failure_chance`（0–1，多個獨立失敗率合成為 1−各成功率之積）。拾彈倍率作用於原版拾取函式算出的結果，不覆蓋醫療箱或部署型箱子的使用邏輯。

### 事件規則

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

規則預設機率 1、冷卻 0、次數 0（不限次數）、延遲 0。即使寫冷卻 0，同一規則狀態仍有 0.05 秒最小間隔。`scope` 預設 unit，為每個事件所屬單位分別計數與冷卻；HCM 可選 global，整個規則共享狀態。global 不取消條目的目標篩選。死靈規則始終屬於選擇它的玩家。

除原生事件目錄外，支援 `interval`、`spawn`、`enemy_died`、`mission_start`、`signal`：

- `interval` 必填 `interval`，0.1–600 秒；掉幀後僅觸發一輪，不追補錯過的所有輪次。
- `spawn` 是框架觀察到的單位生成；HCM 包含敵人，死靈觀察玩家。
- `mission_start` 在玩家單位首次被當前執行例項觀察到時發出；重生為新單位時可再次出現。每個角色整局只一次的效果需要額外設計，不能僅依靠 unit scope 的 `max_triggers:1`。
- `enemy_died` 為死亡廣播。HCM 以死者為 self，死靈廣播給每個存活的天賦持有者並以持有者為 self。只獎勵自己的擊殺應使用原生 `on_kill`；target 為死者，attacker 為擊殺來源（若有）。
- `signal` 在下一次更新派發，使用 `event.signal_name` 篩選。HCM 的 global signal 規則可無單位執行；要作用全隊，應顯式寫動作 target=players。跨模組共享的是訊號狀態，不會替另一個模組直接派發一次 signal 事件。

原生 proc 由對應 Buff 擴充套件提供；事件缺少引數時相關條件不會透過。欄位表中提供的是全部支援欄位的並集。`source_row` 僅是對照圖片用的說明，不影響執行。

### 動作完整表

所有動作均可寫 `target`：self（預設）、target、attacker、players、nearby_players、minions、nearby_minions、matching。nearby 以 self 為中心，`radius` 預設 8 米、允許 1–50 米；matching 使用條目的 targets。非效果動作每次最多匹配 4 名玩家或 64 名敵人。死亡單位不能接受資源、傷害或原生狀態動作。

| type | 欄位與行為 |
| --- | --- |
| `effect` | 必填 `effects`、`duration`（0.1–600 秒）；`max_stacks` 1–500，預設 1；`refresh` 預設 true。疊層共用一個到期時間，false 不續期，不是每層獨立倒計時 |
| `heal` | `amount` 非負；呼叫原生 buff 治療，遵守腐化上限、治療倍率與禁療關鍵詞 |
| `corruption` | `amount` 非負；移除腐化，使用原生 buff_corruption_healing，可跨生命格；不直接補普通生命，不用於施加腐化 |
| `toughness` | 正數恢復，遵守原生恢復倍率；負數呼叫原生韌性扣除並啟動恢復延遲 |
| `ammo` | 正數補備用彈，負數先扣備用彈再扣彈匣，遍歷裝備中的武器槽；按整數向零取整 |
| `grenades` | 調整原生投擲技能充能，限制在 0 到該能力最大值；無此能力則無效果 |
| `ability_cooldown` | 非負秒數減少戰鬥技能冷卻；fraction 按最大冷卻算，不增加充能上限 |
| `stamina` | 正數增加，負數呼叫原生體力消耗，保留原生消耗修正及耗盡事件 |
| `warp_charge` | 平值按百分點、fraction 按 0–1；正數加危機值但不直接引爆，負數消退；限有原生危機值模板的職業 |
| `overheat` | 平值按百分點、fraction 按 0–1；負數原生散熱，正數遵守原生熱量倍率與鎖定/爆炸狀態；限有過熱配置的副武器 |
| `damage` | 非負直接生命傷害；使用私有原生傷害配置並繼續原生攻擊流程。繞過韌性，不保證繞過所有原生減傷、無敵和傷害規則 |
| `kill` | 無 amount；必須顯式 target/匹配敵人類範圍，只允許目錄中的普通可生成敵人，不允許處決玩家或特殊任務實體 |
| `native_buff` | `name` 必須在 15 個已審計原生狀態中；`duration` 預設 10、最大 120 秒；`count` 1–10。期限是本框架移除上限，原生狀態可能提前結束 |
| `signal` | `name` 為 ID，`duration` 0.1–600；釋出有期限的狀態訊號 |
| `pause_spawns` | `name` 為 all/hordes/trickle_hordes/roamers/specials/monsters/hed，`duration` 0.1–600；暫停許可檢查及 HED 排程，不移除已生成單位，不保證暫停繞過 Pacing 的任務指令碼 |
| `spawn_formation` | `name` 為當前任務 HED 配置中已有編隊 ID。提出一次排程請求，不是立即在身邊生成 |
| `spawn_enemy` | `breed` 從 40 個可生成敵人中選擇；普通/特感 `count` 1–16，怪物模板動作每次 1；經 HED 的位置、數量、原生槽位檢查 |
| `pickup` | `name` 為目錄中的拾取物；`count` 1–4，生成在目標單位身旁，不直接強塞進物品槽 |
| `sound` | `name` 為 456 個已知原生 UI 音效之一；房主本地播放，不是自定義音樂播放器 |
| `notification` | `text` 字串或三語言物件，最長 512 位元組；房主本地通知 |

資源動作的 `amount_kind` 預設 flat；fraction 是目標最大資源量的比例，不是當前持有量。只有 ammo 額外支援 current_fraction，用於扣除當前剩餘彈藥的比例。heal/toughness/damage 可用 event_damage，將事件的 damage/damage_amount/damage_dealt 乘以 amount（0–5）；事件無傷害數值時為零。

signal、pause_spawns、生成請求不使用動作 target/radius；sound 和 notification 只執行一次。effect 的 players/minions/matching 是動態範圍層：持續期間符合條件的新單位也會取得效果；nearby 是觸發時選中的有限單位集。已獲得的單單位臨時層不會因為之後離開原條目條件而自動提前消失。

## HED 與其他模組介面

生成動作需要 HED 並啟用其導演排程。HED 缺失或未就緒時請求失敗，不退回無約束生成。原生重新整理暫停需要啟用 HCM；單獨死靈仍可釋出自身訊號和暫停標誌，HED 讀取 hed/all 暫停。HCM 彙總死靈與自身的訊號及暫停，因此死靈天賦也可以驅動 HED 條件。

HCM 匯出 `mod.diy_api.version == 1`，提供 `active()`、`paused(family)`、`context(table)`、`emit_signal(name,duration)`、`status()`。active 返回 HCM 選中條目 ID；context 寫入 affix 和有效 signal 集合。死靈的同名介面提供 `paused`、`context`、`status`，共享訊號但不把私人天賦偽裝成全域性詞條。

HED 匯出 `diy_api.status()` 與 `diy_api.request(request)`。外部 Lua 模組可呼叫：

```lua
local hed = get_mod("HavocEnemyDirector")
local ok, request_id_or_reason = hed.diy_api.request({
    breed = "chaos_poxwalker", count = 2,
    source = "my_mod/my_entry/my_rule", seed = 12345,
})
```

request 只能包含 formation 或 breed（二選一）、count、source、seed。formation 模式 count 只能省略或為 1。breed 模式外部 API 每次最多 16，怪物最多 3；DIY JSON 怪物動作更保守，每次 1。source 為至多 192 位元組的字母數字及 `_:/-`；seed 為 1–2147483646 整數，可省略以採用導演種子。返回 true 僅代表排隊成功，後續可因位置、容量、暫停或超時而取消。主要失敗原因：director_not_ready、request_target、request_breed、formation_missing、request_capacity、mission_request_budget。

HED 條件編輯器新增 `affix_active` 和 `signal_active`，點選值貼上 ID。例如 `signal_active=diy_pressure` 對應模板中的導演訊號。生成來源條件 `event.spawn_source` 在 HCM 敵人 spawn 事件可用；普通 HED 生成標記 hed_director，DIY 普通單位標記 hed_diy，其他原生來源保留其批次來源或 native。怪物和特感走各自原生註冊/槽位路徑，不能依賴它們也擁有這兩個來源標籤。

每個 HED 任務最多接納 128 次外部請求，同時最多保留 32 個外部狀態；每個請求最多等候 120 秒。任務指令碼、地圖位置和原生實體上限仍有最終決定權。不是屍體原地克隆，也沒有承諾嚴格 FIFO 或每請求必定成功。HED 原有全域性分幀提交速度、存活組數、路線與容量限制繼續有效。

## 聯機、清理與效能邊界

SoloPlay 或 Realms 本地房主執行動作，普通遠端伺服器和客機不執行任意 DIY 動作。Realms 每個參與者需要對應新版模組；死靈還要求房內玩家對應條目的包、Lua、資源及依賴的 SHA-256 指紋一致。房主批准私人選擇後，該角色同局不能透過重複握手切換。HCM 由房主統一選擇詞條，客機接收聚合屬性效果，無須配置相同詞條檔案。

客機僅接收自己角色的屬性、關鍵詞和少量修正；不接收可執行 JSON 程式。網路包檢查房主身份、玩家成員、角色、會話 nonce 和遞增序號；效果超過 3 秒未續期即撤銷。房主約每 0.5 秒同步一次，執行層約每 0.1 秒更新；客機屬性可能存在這一量級的延遲。客戶端預測、特殊關鍵詞資源及完整四人戰鬥仍須實機檢查，不能從離線測試推導“聯機完全無差異”。

合併後的規範化定義最大 512 KiB、30,000 個 JSON 節點、深度 20、128 條目；每條目最多 16 規則，每規則最多 8 動作、12 條件。每 tick 最多 128 次觸發評估、64 個動作，延遲佇列最多 512；每單位和動態全域性層最多 128 項；原生受控狀態記錄最多 256，拾取物每庫每局最多 32。達到預算時部分工作被拒絕或延期，不保證高負載逐事件無損。不要用大批次 interval+全體目標替代遊戲自身的持續效果系統。

配置撤銷、退出任務、許可權丟失和禁用清理本框架持有的臨時狀態、佇列及資源記錄。已產生的實際傷害、治療、彈藥變化、拾取物和敵人屬於已完成動作，不會倒放撤銷。原生狀態移除只刪除本框架申請的索引，不掃除其他模組的同名狀態。

## 圖片評估與擴充套件方向

完整逐行結果見 `IMAGE-ASSESSMENT.zh-TW.md`；空白行和只寫玩笑名稱的行也已單獨列出。已提供數值、條件、狀態、資源、訊號及合規增援的通用介面；致命傷延遲、玩家流血、仇恨重置、敵人變形、彈幕/爆炸物、地圖拾取池、UI 隱藏、音影片資源、裝備重置、任務互動與載具仍需各自專門適配，不是加一個不存在的欄位就能實現。

擴充套件時先確認原生方法與網路所有者，再在 schema 中增加嚴格資料欄位、給原生介面卡增加一個明確動作、補充真實原生方法邊界測試和模板；更改語義應升級 schema，不能讓同一版本檔案在房主與客機解釋不同。`native-catalog.json` 是版本固定的目錄，不接受從 JSON 動態加入原生屬性或網路 Buff 編號。


### 抽選前的配裝適配

`availability` 在手選、隨機預覽、開局抽選、房主接納和實際生效時檢查。全部欄位必須滿足；不適配項先移出候選池，不佔總數或互斥組。配裝未完整同步時暫緩選擇；同局已經確定的 DIY 選擇不會因配置變化重新隨機。

| 欄位 | 含義 |
| --- | --- |
| `archetypes` / `families` | 職業／死靈流派列表，列表內任一匹配。未確定流派不能滿足流派要求。 |
| `talents` | 全部原生天賦節點必須已選中（true 或正數）。 |
| `weapons` / `weapon_keywords` | 兩個裝備槽的原生模板名／武器關鍵詞，列表內任一匹配。 |
| `grenade_abilities` | 當前閃擊的準確原生能力名。 |
| `combat_abilities` | 當前戰鬥技能的 `ability_group`。 |
| `resources` / `any_resources` | 全部／至少一種資源機制存在。 |

資源可選 `ammo`、`reload`、`overheat`、`warp_charge`、`grenade_charges`、`combat_ability`、`melee`、`ranged`。例如 `"availability":{"archetypes":["psyker"],"grenade_abilities":["psyker_throwing_knives"],"resources":["ammo","grenade_charges"]}` 要求靈能者當前帶飛刀且裝備有彈藥機制。資源是否存在與當前彈藥、生命或過熱數值分開；低血量等仍寫在 `conditions`，不會因開局滿血被排除。

已審計的彈藥／換彈等屬性與自身資源動作會自動增加硬性要求；複雜事件、特殊關鍵詞和專屬武器機制仍須作者宣告準確的武器、技能、天賦條件。`any_resources` 可宣告靈能／過熱替代動作，但不能繞過被動效果的硬性要求。完整對照見 [適配規則核對](ELIGIBILITY-AUDIT.zh-CN.md)。

## 死靈權重、許可權與五重齊射

`weight` 範圍為 0–1000，預設 1，允許正小數。0 表示只可手選。混合的非流派獎勵中，每個原生候選權重為 1，每個卡位從剩餘適配候選中按權重抽取，且不重複。只有權重 1、2、7 三項時，第一個卡位機率為 10%、20%、70%；整組三張卡的出現機率不同。僅原生模式保留原版分類權重，開局流派仍按原生流派規則。房主禁用、缺少玩家定義和配裝不符均在抽取前過濾；每次發放後再次檢查總數和互斥組。

批次操作覆蓋全部篩選結果，包括其他頁；明確選擇「我的預選」或房主的「房間 DIY 池」作為操作物件。房主不能逐項禁用原生天賦。灰色技能仍可檢視詳情；只對已預選／已獲得受影響技能的玩家提醒。房間許可權不會改寫玩家儲存的選擇。

`passive.modifiers.ranged_salvo_count` 僅限死靈天賦，接受 1–5 的整數。五重齊射示例使用 5，要求遠端武器。每次生成五份攻擊，但只支付一次原本消耗；原生額外彈體參與乘算，激湧暴擊共十發。延遲法杖彈體保留原充能。霰彈複製共用原散佈；火焰與閃電重複原生脈衝，並遵守原版疊層上限。該修飾器多個來源取最大值，不復制近戰、閃擊或戰鬥技能攻擊。

只有 DIY 時，進度模式最多十項獎勵，沒有原生路線自動獎勵。混合模式使用統一獎勵輪次，並遵守獨立的 DIY 點數上限。原生與 DIY 支援四種開關組合；兩者都關會在本 mod 支援並接管的死靈流程中停用兩類獎勵。

包大小、檔案限制和 Lua 語義見 PACKAGES.zh-CN.md。指令碼專用條目需要職業、武器或資源機制時，作者應顯式填寫 availability。

包管理不包含獎勵上限。Realms 準備介面的死靈天賦控制元件由房主設定獨立 DIY 開關和點數上限，使用減號、數字直接編輯和加號（0–99）。每項 DIY 天賦消耗 1 點，與等級無關；SoloPlay 保留獨立的「獎勵設定」頁面。等級僅作標籤，舊的等級配額會被忽略。HCM 會應用所有已啟用且勾選的詞條。詞條頁不設隨機抽取、種子或數量配額，舊權重與互斥組不再篩掉已勾選詞條。懸停一行即可檢視詳情，不改變勾選；檔案操作保留在獨立的「包管理」頁面。

## 按管理器設定隨機種子

詞條事件的機率隨機流在 HCM「整體調節 → 隨機種子」設定；HED「導演 → 隨機種子」分別設定自身編隊排程與原生駐軍佈局。關閉固定種子時沿用任務種子；HCM 無法取得任務種子時，每局只隨機生成一次後備用值。開啟後可輸入 1–2147483646 的整數，關閉會保留輸入值，修改用於下一局。這些種子不選擇任務地圖，也不統一原生屍潮、特感、怪物和指令碼事件的全部隨機性；Lua 作者直接使用 math.random 時仍屬於獨立的原生隨機來源。
