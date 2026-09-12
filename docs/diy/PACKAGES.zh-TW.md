# DIY 包規範與 Lua 介面

MortisBuffManager 4.4.0 和 HavocConditionManager 4.3.0 各自攜帶同一套包執行庫，彼此獨立，不要求互相安裝。包格式是 `Darktide.DIY.Package` 版本 2，條目定義繼續使用 `Darktide.DIY` 版本 1，Lua API 為主版本 1、次版本 0。

每個新包的 definitions.json 必須恰好包含一個詞條。入門內容分別為死靈 12 個資料夾、HCM 34 個資料夾，各有自己的 lua/main.lua 和 resources 目錄。宣告式詞條執行 JSON 規則，Lua 檔案是可編輯的擴充套件入口。貼上多詞條 JSON 會逐詞條拆成資料夾。原來的合併入門包在啟動時遷移：子包保留原詞條名稱空間、原 Lua／資源及停用狀態，完整舊資料夾移入 diy/package-backups/。遷移中斷後可以繼續，不會重複條目。舊版格式 1 仍可讀取以相容作者檔案；可選 entry_namespace 用於拆包時保持穩定標識，新建獨立包通常無需填寫。

## 放入目錄，啟動即載入

每個包一個資料夾，分別放入：

```text
%APPDATA%/Fatshark/Darktide/MortisBuffManager/diy/packages/
%APPDATA%/Fatshark/Darktide/HavocConditionManager/diy/packages/

packages/
  my-package/
    package.json
    definitions.json
    lua/
      main.lua
      helpers.lua
    resources/
      amount.txt
```

啟動遊戲時自動發現、校驗並合併有效包。首次使用會建立入門包，已有同名包則保留。死靈的「包管理」及 HCM 的「DIY 詞條」頁面顯示包數量、條目數量和具體錯誤。**重新整理用於遊戲執行時新增或修改包**；原本就在目錄裡的包不需要先點重新整理或逐個載入。

包載入後可以瀏覽、預選或進入獎勵池；放入資料夾本身不會自動獲得效果。任務開始時凍結本局 JSON、Lua 和資源內容。任務中重新整理、貼上 JSON 或啟停包，只更新下一局的資料，不會在本局替換正在執行的程式碼。

舊 `diy` 目錄中的鬆散 JSON 與已儲存的舊配置庫會一次性轉換成規範目錄，原檔案保留；已儲存的預選和死靈房主禁用記錄會對映到新 ID。貼上 JSON 會建立完整的資料包，不覆蓋作者已有的 Lua 或資源；內容不同的同 ID 匯入會生成帶內容字尾的新包。點選「入門包」時已有模板會保留，不再把正常的“已存在”當作不明錯誤。「匯出包」會把全部已載入包連同 Lua 和資源匯出到新建的 `diy/exports/export-NNN/` 目錄。

用「啟用此包／停用此包」管理當前選中的包。依賴其他 DMF 模組的包，會在全部模組初始化後自動再檢查一次，避免因為對方在載入順序中較晚而必須手動重新整理。

## 清單格式

`package.schema.json` 可供編輯器校驗。執行庫還會檢查 Windows 路徑、實際檔案清單、原生欄位以及依賴關係。

```json
{
  "format": "Darktide.DIY.Package",
  "version": 2,
  "id": "my-package",
  "package_version": "1.0.0",
  "name": {"en": "My package", "zh-cn": "我的包"},
  "description": "本地 Lua 天賦示例。",
  "kind": "mortis",
  "api": {"major": 1, "min_minor": 0},
  "definitions": "definitions.json",
  "entrypoint": "lua/main.lua",
  "files": ["definitions.json", "lua/main.lua", "lua/helpers.lua", "resources/amount.txt"],
  "dependencies": [],
  "conflicts": [],
  "requires_mods": [],
  "capabilities": ["effects.v1", "actions.v1", "resources.v1", "modules.v1", "cleanup.v1"],
  "shared_signals": [],
  "extensions": {"my-author.notes": "作者擴充套件資訊"}
}
```

資料夾名必須等於 `id`。包和條目 ID 以 ASCII 小寫字母開頭，只允許小寫字母、數字、下劃線、短橫線，最長 64 位元組，並排除 Windows 保留裝置名。中文名稱放在 `name` 中。`kind` 分別為死靈 `mortis`、詞條 `conditions`，一個包只屬於一個管理器。`package_version` 使用數字 `主.次.修訂`，每段 0–9999；當前不接受預釋出或構建字尾。可選 `author` 最長 256 位元組，名稱與說明沿用條目的三語言格式。

除 `package.json` 本身外，所有檔案都必須列入 `files`，資源也不例外，路徑拼寫必須與實際檔案一致。定義固定是 `definitions.json`；Lua 放在 `lua/` 下；附帶資源放在 `resources/` 下。純資料包可以沒有 Lua、資源及 `entrypoint`。禁止絕對路徑、反斜槓、`..`、隱藏路徑段、Windows 備用資料流、重名路徑和重解析點檔案／目錄。執行庫不會去任意其他遊戲目錄尋找未宣告的檔案。

未知核心欄位會報錯，不會默默忽略。作者擴充套件資訊放入 `extensions`，鍵名需要名稱空間，例如 `my-author.notes`。能力名支援 `actions.v1`、`effects.v1`、`events.v1`、`resources.v1`、`modules.v1`、`cleanup.v1`、`native.v1`。這些是相容性宣告，不是安全許可權開關。不支援的 API 主版本、所需次版本或能力會拒絕載入；未來相容追加使用次版本，破壞性介面變化必須升級主版本。

## 依賴、名稱空間與相容

```json
{
  "dependencies": [{"id": "common-library", "min_version": "1.2.0", "before_version": "2.0.0"}],
  "conflicts": ["alternative-package"],
  "requires_mods": [{"id": "HavocEnemyDirector", "api_major": 1, "optional": false}]
}
```

`min_version` 包含邊界，`before_version` 可省略且不包含邊界。包依賴在同一管理器目錄內解析。缺失、停用、迴圈、衝突或版本不符的包會顯示原因，並連同依賴它的包一起排除；其他有效包繼續使用。其他模組需求透過 `get_mod(id)`、啟用狀態及可選的 `mod.diy_api.version` 檢查。標記 `optional` 的模組允許缺失，作者使用可選介面前仍需判斷是否存在。

不同包允許使用相同的條目 ID、顯示名稱和互斥組名。內部 ID 由包 ID 與原條目 ID 穩定生成，內容更新不會改變該 ID；詳情會顯示作者使用的包／條目來源。不要寫死內部雜湊值，使用 `ctx:qualify(條目ID, 可選包ID)`；外部模組可以呼叫 `get_mod("MortisBuffManager").diy_api.qualify(包ID, 條目ID)`，HCM 也提供同一方法。

JSON 的 `affix` 條件預設引用本包條目；`@common-library/entry-id` 引用已宣告依賴的條目。JSON signal 動作、signal 條件、`event.signal_name` 比較及 `ctx:signal` 預設使用包內名稱空間。需要跨包共享的名稱寫入 `shared_signals`，或在 Lua 中顯式使用 `ctx:global_signal`。舊 JSON 轉換時會保留原先共享的訊號名。HCM 對外的 `diy_api.context().affix` 繼續提供舊條目 ID 別名：任一同原 ID 的活動條目都算命中；新介面應使用完整限定 ID 避免歧義。

## Lua 真正參與執行

需要回撥的條目必須寫 `"script": true`，也允許只有指令碼而沒有 JSON 效果的條目。入口返回下列結構：

```lua
local helpers = package_require("lua/helpers.lua")

return {
    api_version = { major = 1, minor = 0 },
    exports = {},
    entries = {
        my_talent = {
            interval = 5,
            events = { "enemy_died" },
            on_activate = function(ctx)
                local bonus = tonumber(assert(ctx:resource("resources/amount.txt")))
                ctx:set_effects({ stats = { damage = helpers.clamp(bonus, 0, 1) } })
                ctx.state.restore = ctx:compile_action({ type = "toughness", amount = 2 })
                ctx:on_cleanup(function(reason)
                    -- 清理本條目額外登記的原生監聽器或資源。
                end)
            end,
            on_update = function(ctx, elapsed)
                ctx.state.restore()
            end,
            on_event = function(ctx, name, event)
                if event.attacker == ctx.owner then ctx.state.restore(event) end
            end,
            on_deactivate = function(ctx, reason)
                -- 隨後還會執行 on_cleanup 登記的清理。
            end,
        },
    },
}
```

Lua 按可信本地模組程式碼執行，可以呼叫原生遊戲介面，不是安全沙箱。啟動校驗只編譯語法，不執行程式碼；只有相應條目被選中／獲得，需要模組時才載入，且只在 SoloPlay 本地權威或 Realms 房主執行。每個包每局擁有獨立環境與模組快取；同包可共享輔助模組狀態，不需要向遊戲全域性註冊普通變數。每個條目／玩家繫結分別擁有 `ctx.state`。編譯使用模組載入器儲存的原始 Lua 編譯器，即使遊戲普通全域性 `loadstring` 不可用也能載入；原生功能和載入器的 `Mods.lua` 備份仍可由作者使用。

`on_activate` 在繫結建立時執行一次，不受瞬時條件控制，用於初始化狀態和效果。實際應用動態屬性時仍檢查目標、適配性與條件。`on_update`、`on_event` 和 context 排隊動作會遵守條目條件。更新間隔必須為 0.1–600 秒，不會在卡頓後補發大量歷史回撥。HCM 全域性更新的 `ctx.owner` 和 `ctx.unit` 為 nil，全隊動作請明確填寫 target；死靈更新屬於獲得該條目的玩家。

`on_event` 必須顯式訂閱事件，最多 64 個不重複名稱；可用事件為 `event-contracts.json` 的原生事件，以及 `spawn`、`enemy_died`、`mission_start`、`signal`。回撥引數是 `(ctx, 事件名, event)`，不同原生事件提供的欄位不同。owner 繫結的 `enemy_died`／`signal` 會分發給活著的已選擇玩家，其他事件跟隨事件單位。HCM 全域性回撥會檢查事件單位是否符合條目 targets，無單位事件可全域性執行。當前適配層在回撥或動作執行中抑制遞迴派發，避免連鎖重入。

模組或回撥錯誤會顯示在包狀態中。某回撥出錯後，清除該繫結的 Lua 屬性、待執行動作和登記清理，本局停止該繫結的指令碼；其獨立 JSON 效果仍按定義處理。錯誤不會停止其他獨立包。移除條目、玩家死亡和離局都會清理，已結束的引擎不能再次啟用。下一局建立新執行環境，重新嘗試該局快照中的指令碼。

## Context 介面

| 介面／欄位 | 含義 |
| --- | --- |
| `package_id`, `package_version`, `entry_id`, `qualified_id` | 來源資訊，`entry_id` 是 JSON 中的原 ID。 |
| `owner`, `unit`, `time`, `state`, `role` | 擁有者、當前回撥單位、引擎秒數、繫結狀態和 `authority`。 |
| `resource(path)` | 返回已宣告 `resources/` 檔案的凍結原始位元組，失敗返回 nil／原因。 |
| `require(path)` | 載入並快取本包中已宣告的 `lua/` 模組。 |
| `dependency(id, path?)` | 載入已宣告依賴的模組；省略 path 返回該包入口的 `exports`。 |
| `set_effects(table_or_nil)` | 替換本繫結的動態屬性、關鍵詞和修正；使用現有嚴格 effect 校驗。 |
| `compile_action(action, slot?)` | 只驗證並複製一次，返回接收可選 event 的動作函式。同 slot 的臨時效果複用堆疊／壽命鍵。 |
| `action(action, event?, slot?)` | 直接驗證並排隊；高頻回撥優先使用編譯後的動作。true 代表入隊，不保證原生執行成功。 |
| `context(unit?, event?)` | 讀取正常的原生／DIY 條件上下文，預設當前回撥單位。 |
| `units(selector, radius?)` | 最多返回四名玩家或 64 個匹配單位；半徑 1–50，中心為當前回撥單位。 |
| `qualify(entry_id, package_id?)` | 生成穩定限定 ID，其他包必須已宣告為依賴。 |
| `signal(name, duration)` | 本包訊號，或清單指定的共享訊號；持續 0.1–600 秒。 |
| `global_signal(name, duration)` | 顯式共享訊號。 |
| `random(key, chance)` | 按包／條目／key／玩家隔離的固定種子隨機流，chance 為 0–1。 |
| `on_cleanup(function)` | 最多登記 64 項，按登記逆序執行並傳入原因。 |
| `log(message)` | 配置日誌介面卡時，把資訊交給管理器日誌。 |

模組頂層可用 `package_require("lua/helpers.lua")`、`dependency_require("common-library", 可選路徑)`。`require("./helpers.lua")` 是本包 `lua/helpers.lua` 的簡寫；其他 require 名稱交給遊戲原生解析器。模組迴圈會報錯。不要在繫結結束後繼續儲存並使用其回撥 context。

公共動作沿用現有原生介面卡和所屬效果清理。作者直接建立的原生 hook、監聽器或資源需要對應的 `on_cleanup`。已經執行的治療、傷害、生成等遊戲事件無法撤銷；訊號和暫停持續時間按正常壽命到期，取消選擇不會回滾這些事件。回撥預算限制派發數量，但不能強行中斷 Lua 函式內部的死迴圈。

## 資源與聯機

資源介面返回凍結的原始位元組，不會自動把 PNG、音訊等檔案匯入 Stingray 資源資料庫。作者可以讀取並處理這些格式；顯示／播放仍需要相應解碼器或原生資源接入。已有的原生材質、音效動作仍需有效的目錄識別符號。原始資源不會自動傳給其他玩家。

死靈入池使用 SHA-256，覆蓋條目、清單、包內全部 Lua／資源以及完整依賴閉包。同一條目所屬包和依賴的位元組必須在全房間一致，各玩家額外安裝的其他包可以不同。房間協議為 10，舊版玩家不能確認新指紋。網路只傳送 ID／指紋及原有聚合效果，不傳送或執行網路 Lua。HCM 指令碼由房主執行，客機接收原版同步結果及現有玩家聚合屬性。客戶端預測、特殊引擎資源、完整四人戰鬥仍需實機驗收。

## 限制與可複製示例

每個管理器最多 256 個包；每包最多 256 個宣告檔案加清單、32 MiB，總保留包資料最多 128 MiB。單個 Lua 最多 256 KiB，定義 JSON 最多 512 KiB，單個資源最多 8 MiB。路徑最多八段、192 位元組。合併後的規範化定義最多 128 條目、512 KiB、30,000 個 JSON 節點；超限時整包及其依賴者被排除，不匯入半個包。

現有觸發、動作、佇列限制見 GUIDE.zh-TW.md；Lua 每次引擎更新間最多派發 128 個回撥。未選擇的條目沒有事件或定時回撥。目錄掃描、讀檔案、語法編譯和雜湊只發生於啟動或明確重新整理／匯入，不進入逐幀、屬性或擊殺流程；啟動階段的其他模組依賴複查只執行一次。

把 `package-examples/lua-mortis-example` 或 `package-examples/lua-conditions-example` 整個資料夾複製到對應目錄即可使用實際執行 Lua 的示例。附帶的純資料示例也已轉換成完整包資料夾，可以直接編輯和分享。文件目錄原有的單獨 JSON 繼續作為定義參考，也可透過貼上轉換為包。

包管理不包含獎勵上限。Realms 準備介面的死靈天賦控制元件由房主設定獨立 DIY 開關和點數上限，使用減號、數字直接編輯和加號（0–99）。每項 DIY 天賦消耗 1 點，與等級無關；SoloPlay 保留獨立的「獎勵設定」頁面。等級僅作標籤，舊的等級配額會被忽略。HCM 會應用所有已啟用且勾選的詞條。詞條頁不設隨機抽取、種子或數量配額，舊權重與互斥組不再篩掉已勾選詞條。懸停一行即可檢視詳情，不改變勾選；檔案操作保留在獨立的「包管理」頁面。
