# DIY 包规范与 Lua 接口

MortisBuffManager 4.4.0 和 HavocConditionManager 4.3.0 各自携带同一套包运行库，彼此独立，不要求互相安装。包格式是 `Darktide.DIY.Package` 版本 2，条目定义继续使用 `Darktide.DIY` 版本 1，Lua API 为主版本 1、次版本 0。

每个新包的 definitions.json 必须恰好包含一个词条。入门内容分别为死灵 12 个文件夹、HCM 34 个文件夹，各有自己的 lua/main.lua 和 resources 目录。声明式词条执行 JSON 规则，Lua 文件是可编辑的扩展入口。粘贴多词条 JSON 会逐词条拆成文件夹。原来的合并入门包在启动时迁移：子包保留原词条命名空间、原 Lua／资源及停用状态，完整旧文件夹移入 diy/package-backups/。迁移中断后可以继续，不会重复条目。旧版格式 1 仍可读取以兼容作者文件；可选 entry_namespace 用于拆包时保持稳定标识，新建独立包通常无需填写。

## 放入目录，启动即载入

每个包一个文件夹，分别放入：

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

启动游戏时自动发现、校验并合并有效包。首次使用会创建入门包，已有同名包则保留。死灵的「包管理」及 HCM 的「DIY 词条」页面显示包数量、条目数量和具体错误。**刷新用于游戏运行时新增或修改包**；原本就在目录里的包不需要先点刷新或逐个载入。

包载入后可以浏览、预选或进入奖励池；放入文件夹本身不会自动获得效果。任务开始时冻结本局 JSON、Lua 和资源内容。任务中刷新、粘贴 JSON 或启停包，只更新下一局的数据，不会在本局替换正在运行的代码。

旧 `diy` 目录中的松散 JSON 与已保存的旧配置库会一次性转换成规范目录，原文件保留；已保存的预选和死灵房主禁用记录会映射到新 ID。粘贴 JSON 会建立完整的数据包，不覆盖作者已有的 Lua 或资源；内容不同的同 ID 导入会生成带内容后缀的新包。点击「入门包」时已有模板会保留，不再把正常的“已存在”当作不明错误。「导出包」会把全部已载入包连同 Lua 和资源导出到新建的 `diy/exports/export-NNN/` 目录。

用「启用此包／停用此包」管理当前选中的包。依赖其他 DMF 模组的包，会在全部模组初始化后自动再检查一次，避免因为对方在加载顺序中较晚而必须手动刷新。

## 清单格式

`package.schema.json` 可供编辑器校验。运行库还会检查 Windows 路径、实际文件清单、原生字段以及依赖关系。

```json
{
  "format": "Darktide.DIY.Package",
  "version": 2,
  "id": "my-package",
  "package_version": "1.0.0",
  "name": {"en": "My package", "zh-cn": "我的包"},
  "description": "本地 Lua 天赋示例。",
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
  "extensions": {"my-author.notes": "作者扩展信息"}
}
```

文件夹名必须等于 `id`。包和条目 ID 以 ASCII 小写字母开头，只允许小写字母、数字、下划线、短横线，最长 64 字节，并排除 Windows 保留设备名。中文名称放在 `name` 中。`kind` 分别为死灵 `mortis`、词条 `conditions`，一个包只属于一个管理器。`package_version` 使用数字 `主.次.修订`，每段 0–9999；当前不接受预发布或构建后缀。可选 `author` 最长 256 字节，名称与说明沿用条目的三语言格式。

除 `package.json` 本身外，所有文件都必须列入 `files`，资源也不例外，路径拼写必须与实际文件一致。定义固定是 `definitions.json`；Lua 放在 `lua/` 下；附带资源放在 `resources/` 下。纯数据包可以没有 Lua、资源及 `entrypoint`。禁止绝对路径、反斜杠、`..`、隐藏路径段、Windows 备用数据流、重名路径和重解析点文件／目录。运行库不会去任意其他游戏目录寻找未声明的文件。

未知核心字段会报错，不会默默忽略。作者扩展信息放入 `extensions`，键名需要命名空间，例如 `my-author.notes`。能力名支持 `actions.v1`、`effects.v1`、`events.v1`、`resources.v1`、`modules.v1`、`cleanup.v1`、`native.v1`。这些是兼容性声明，不是安全权限开关。不支持的 API 主版本、所需次版本或能力会拒绝载入；未来兼容追加使用次版本，破坏性接口变化必须升级主版本。

## 依赖、命名空间与兼容

```json
{
  "dependencies": [{"id": "common-library", "min_version": "1.2.0", "before_version": "2.0.0"}],
  "conflicts": ["alternative-package"],
  "requires_mods": [{"id": "HavocEnemyDirector", "api_major": 1, "optional": false}]
}
```

`min_version` 包含边界，`before_version` 可省略且不包含边界。包依赖在同一管理器目录内解析。缺失、停用、循环、冲突或版本不符的包会显示原因，并连同依赖它的包一起排除；其他有效包继续使用。其他模组需求通过 `get_mod(id)`、启用状态及可选的 `mod.diy_api.version` 检查。标记 `optional` 的模组允许缺失，作者使用可选接口前仍需判断是否存在。

不同包允许使用相同的条目 ID、显示名称和互斥组名。内部 ID 由包 ID 与原条目 ID 稳定生成，内容更新不会改变该 ID；详情会显示作者使用的包／条目来源。不要写死内部散列值，使用 `ctx:qualify(条目ID, 可选包ID)`；外部模组可以调用 `get_mod("MortisBuffManager").diy_api.qualify(包ID, 条目ID)`，HCM 也提供同一方法。

JSON 的 `affix` 条件默认引用本包条目；`@common-library/entry-id` 引用已声明依赖的条目。JSON signal 动作、signal 条件、`event.signal_name` 比较及 `ctx:signal` 默认使用包内命名空间。需要跨包共享的名称写入 `shared_signals`，或在 Lua 中显式使用 `ctx:global_signal`。旧 JSON 转换时会保留原先共享的信号名。HCM 对外的 `diy_api.context().affix` 继续提供旧条目 ID 别名：任一同原 ID 的活动条目都算命中；新接口应使用完整限定 ID 避免歧义。

## Lua 真正参与运行

需要回调的条目必须写 `"script": true`，也允许只有脚本而没有 JSON 效果的条目。入口返回下列结构：

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
                    -- 清理本条目额外登记的原生监听器或资源。
                end)
            end,
            on_update = function(ctx, elapsed)
                ctx.state.restore()
            end,
            on_event = function(ctx, name, event)
                if event.attacker == ctx.owner then ctx.state.restore(event) end
            end,
            on_deactivate = function(ctx, reason)
                -- 随后还会执行 on_cleanup 登记的清理。
            end,
        },
    },
}
```

Lua 按可信本地模组代码运行，可以调用原生游戏接口，不是安全沙箱。启动校验只编译语法，不执行代码；只有相应条目被选中／获得，需要模块时才加载，且只在 SoloPlay 本地权威或 Realms 房主执行。每个包每局拥有独立环境与模块缓存；同包可共享辅助模块状态，不需要向游戏全局注册普通变量。每个条目／玩家绑定分别拥有 `ctx.state`。编译使用模组加载器保存的原始 Lua 编译器，即使游戏普通全局 `loadstring` 不可用也能加载；原生功能和加载器的 `Mods.lua` 备份仍可由作者使用。

`on_activate` 在绑定建立时执行一次，不受瞬时条件控制，用于初始化状态和效果。实际应用动态属性时仍检查目标、适配性与条件。`on_update`、`on_event` 和 context 排队动作会遵守条目条件。更新间隔必须为 0.1–600 秒，不会在卡顿后补发大量历史回调。HCM 全局更新的 `ctx.owner` 和 `ctx.unit` 为 nil，全队动作请明确填写 target；死灵更新属于获得该条目的玩家。

`on_event` 必须显式订阅事件，最多 64 个不重复名称；可用事件为 `event-contracts.json` 的原生事件，以及 `spawn`、`enemy_died`、`mission_start`、`signal`。回调参数是 `(ctx, 事件名, event)`，不同原生事件提供的字段不同。owner 绑定的 `enemy_died`／`signal` 会分发给活着的已选择玩家，其他事件跟随事件单位。HCM 全局回调会检查事件单位是否符合条目 targets，无单位事件可全局执行。当前适配层在回调或动作执行中抑制递归派发，避免连锁重入。

模块或回调错误会显示在包状态中。某回调出错后，清除该绑定的 Lua 属性、待执行动作和登记清理，本局停止该绑定的脚本；其独立 JSON 效果仍按定义处理。错误不会停止其他独立包。移除条目、玩家死亡和离局都会清理，已结束的引擎不能再次激活。下一局创建新运行环境，重新尝试该局快照中的脚本。

## Context 接口

| 接口／字段 | 含义 |
| --- | --- |
| `package_id`, `package_version`, `entry_id`, `qualified_id` | 来源信息，`entry_id` 是 JSON 中的原 ID。 |
| `owner`, `unit`, `time`, `state`, `role` | 拥有者、当前回调单位、引擎秒数、绑定状态和 `authority`。 |
| `resource(path)` | 返回已声明 `resources/` 文件的冻结原始字节，失败返回 nil／原因。 |
| `require(path)` | 加载并缓存本包中已声明的 `lua/` 模块。 |
| `dependency(id, path?)` | 加载已声明依赖的模块；省略 path 返回该包入口的 `exports`。 |
| `set_effects(table_or_nil)` | 替换本绑定的动态属性、关键词和修正；使用现有严格 effect 校验。 |
| `compile_action(action, slot?)` | 只验证并复制一次，返回接收可选 event 的动作函数。同 slot 的临时效果复用堆叠／寿命键。 |
| `action(action, event?, slot?)` | 直接验证并排队；高频回调优先使用编译后的动作。true 代表入队，不保证原生执行成功。 |
| `context(unit?, event?)` | 读取正常的原生／DIY 条件上下文，默认当前回调单位。 |
| `units(selector, radius?)` | 最多返回四名玩家或 64 个匹配单位；半径 1–50，中心为当前回调单位。 |
| `qualify(entry_id, package_id?)` | 生成稳定限定 ID，其他包必须已声明为依赖。 |
| `signal(name, duration)` | 本包信号，或清单指定的共享信号；持续 0.1–600 秒。 |
| `global_signal(name, duration)` | 显式共享信号。 |
| `random(key, chance)` | 按包／条目／key／玩家隔离的固定种子随机流，chance 为 0–1。 |
| `on_cleanup(function)` | 最多登记 64 项，按登记逆序执行并传入原因。 |
| `log(message)` | 配置日志适配器时，把信息交给管理器日志。 |

模块顶层可用 `package_require("lua/helpers.lua")`、`dependency_require("common-library", 可选路径)`。`require("./helpers.lua")` 是本包 `lua/helpers.lua` 的简写；其他 require 名称交给游戏原生解析器。模块循环会报错。不要在绑定结束后继续保存并使用其回调 context。

公共动作沿用现有原生适配器和所属效果清理。作者直接创建的原生 hook、监听器或资源需要对应的 `on_cleanup`。已经执行的治疗、伤害、生成等游戏事件无法撤销；信号和暂停持续时间按正常寿命到期，取消选择不会回滚这些事件。回调预算限制派发数量，但不能强行中断 Lua 函数内部的死循环。

## 资源与联机

资源接口返回冻结的原始字节，不会自动把 PNG、音频等文件导入 Stingray 资源数据库。作者可以读取并处理这些格式；显示／播放仍需要相应解码器或原生资源接入。已有的原生材质、音效动作仍需有效的目录标识符。原始资源不会自动传给其他玩家。

死灵入池使用 SHA-256，覆盖条目、清单、包内全部 Lua／资源以及完整依赖闭包。同一条目所属包和依赖的字节必须在全房间一致，各玩家额外安装的其他包可以不同。房间协议为 10，旧版玩家不能确认新指纹。网络只发送 ID／指纹及原有聚合效果，不发送或执行网络 Lua。HCM 脚本由房主执行，客机接收原版同步结果及现有玩家聚合属性。客户端预测、特殊引擎资源、完整四人战斗仍需实机验收。

## 限制与可复制示例

每个管理器最多 256 个包；每包最多 256 个声明文件加清单、32 MiB，总保留包数据最多 128 MiB。单个 Lua 最多 256 KiB，定义 JSON 最多 512 KiB，单个资源最多 8 MiB。路径最多八段、192 字节。合并后的规范化定义最多 128 条目、512 KiB、30,000 个 JSON 节点；超限时整包及其依赖者被排除，不导入半个包。

现有触发、动作、队列限制见 GUIDE.zh-CN.md；Lua 每次引擎更新间最多派发 128 个回调。未选择的条目没有事件或定时回调。目录扫描、读文件、语法编译和散列只发生于启动或明确刷新／导入，不进入逐帧、属性或击杀流程；启动阶段的其他模组依赖复查只执行一次。

把 `package-examples/lua-mortis-example` 或 `package-examples/lua-conditions-example` 整个文件夹复制到对应目录即可使用实际执行 Lua 的示例。附带的纯数据示例也已转换成完整包文件夹，可以直接编辑和分享。文档目录原有的单独 JSON 继续作为定义参考，也可通过粘贴转换为包。

包管理不包含奖励上限。Realms 准备界面的死灵天赋控件由房主设置独立 DIY 开关和点数上限，使用减号、数字直接编辑和加号（0–99）。每项 DIY 天赋消耗 1 点，与等级无关；SoloPlay 保留独立的「奖励设置」页面。等级仅作标签，旧的等级配额会被忽略。HCM 会应用所有已启用且勾选的词条。词条页不设随机抽取、种子或数量配额，旧权重与互斥组不再筛掉已勾选词条。悬停一行即可查看详情，不改变勾选；文件操作保留在独立的「包管理」页面。
