# DIY packages and Lua API

MortisBuffManager 4.4.0 and HavocConditionManager 4.3.0 use the same package contract independently. Each manager includes its own loader; installing one does not require the other. The package format is `Darktide.DIY.Package` version 2. Definitions remain `Darktide.DIY` version 1. The Lua API is major 1, minor 0.

Every new package contains exactly one entry in definitions.json. The starter sets contain 12 Mortis folders and 34 HCM folders, each with its own lua/main.lua and resources directory. Declarative entries use their JSON rules; their Lua file is an editable optional extension. Clipboard imports split multi-entry documents into individual folders. Existing aggregate starter folders migrate on startup: each child preserves the original entry namespace, copied Lua/resources and disabled state, and the complete original folder moves to diy/package-backups/. An interrupted migration can resume without duplicate entries. Version-one packages remain readable for compatibility. Optional entry_namespace preserves stable identities during a split; new independent authors should normally omit it.

## Install and refresh

Put a complete package folder in the relevant directory:

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

Start the game: valid packages are discovered and merged automatically. The first startup creates a starter package when none with that ID exists. Open Mortis **Package manager**, or HCM **DIY conditions**, to see loaded packages, entry counts and errors. Refresh after adding or editing files while the game is running. Package changes, including enable/disable, are staged for the next mission. Current mission definitions, Lua and resources keep their frozen bytes. Selecting or receiving an entry controls whether its effects run; merely installing a package does not grant its talents or conditions.

Legacy loose JSON in the old `diy` directory and a previously saved library are converted once into package folders. Original files remain. Saved selections and Mortis host exclusions are mapped to qualified IDs. Clipboard JSON creates a complete data package; it never overwrites another package's Lua or resources. A changed duplicate clipboard import gets a content suffix. The existing starter is preserved when **Starter package** is pressed. **Export packages** writes all loaded packages, including their Lua and resources, to a new `diy/exports/export-NNN/` directory.

Use **Enable package / Disable package** to change the selected package's state. Refresh is discovery and validation; it is not a prerequisite for packages already present at startup. Dependencies on other DMF mods are checked again once all mods have loaded, so a later mod load position does not require a manual refresh.

## Manifest

`package.schema.json` supplies an editor-facing JSON Schema. Runtime validation additionally enforces safe Windows paths, complete file inventory, native definition identifiers and dependency resolution.

```json
{
  "format": "Darktide.DIY.Package",
  "version": 2,
  "id": "my-package",
  "package_version": "1.0.0",
  "name": {"en": "My package", "zh-cn": "我的包"},
  "description": "A local Lua talent example.",
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
  "extensions": {"my-author.notes": "Optional author metadata"}
}
```

The folder name must equal `id`. IDs begin with a lowercase ASCII letter and contain only lowercase letters, digits, `_` and `-`, at most 64 bytes; reserved Windows device names are rejected. `kind` is `mortis` or `conditions`. A package belongs to one manager. `package_version` is a numeric `MAJOR.MINOR.PATCH` core, with each component from 0 to 9999; prerelease/build suffixes are not supported by this API. `author` is optional text up to 256 bytes. Name/description use the same localization contract as definitions.

Every file except `package.json` must be listed, including resources. All declared files must exist with the exact spelling. Definitions always use `definitions.json`; Lua files belong below `lua/`, resources below `resources/`. Lua and resources are optional. A data-only package omits `entrypoint`. Dot segments, absolute paths, backslashes, hidden path components, alternate streams, duplicate paths and reparse-point files/directories are rejected. The loader does not search arbitrary game directories for undeclared files.

Unknown core fields fail validation. Put additive author metadata in `extensions` under a namespaced key such as `my-author.notes`. Supported capability names are `actions.v1`, `effects.v1`, `events.v1`, `resources.v1`, `modules.v1`, `cleanup.v1` and `native.v1`. They declare compatibility requirements, not a security permission system. An unsupported required API/capability rejects the package. Future API minor additions must preserve existing behavior; a breaking contract requires a new major.

## Dependencies and identities

```json
{
  "dependencies": [{"id": "common-library", "min_version": "1.2.0", "before_version": "2.0.0"}],
  "conflicts": ["alternative-package"],
  "requires_mods": [{"id": "HavocEnemyDirector", "api_major": 1, "optional": false}]
}
```

`min_version` is inclusive; `before_version` is optional and exclusive. Dependencies resolve inside the same manager's package directory. Missing, disabled, cyclic, conflicting or incompatible packages are excluded with their reason. Dependent packages are excluded too; independent valid packages remain available. Other mod requirements use `get_mod(id)`, the mod's enabled state and, when specified, `mod.diy_api.version`. Optional mod requirements may be absent. Package APIs should check optional integrations before using them.

Different packages may reuse an entry ID, display name or exclusive-group name. The runtime qualifies IDs from the package ID and original entry ID; these IDs remain stable when the package contents change. UI details show the author-facing source IDs. Never hard-code an internal hash: use `ctx:qualify(entry_id, optional_package_id)` or `get_mod("MortisBuffManager").diy_api.qualify(package_id, entry_id)` (also available on HCM).

JSON `affix` conditions refer to entries in their own package. `@common-library/entry-id` addresses a declared dependency. Signals are private to their package by default, including JSON signal actions, `signal` conditions, `event.signal_name` comparisons and `ctx:signal`. List intentionally shared names in `shared_signals`, or use `ctx:global_signal` for explicit interoperability. Legacy JSON migration retains its existing shared signal names. HCM's external `diy_api.context().affix` also retains original-ID aliases for old integrations; an alias means any active entry with that original ID. New integrations should use qualified IDs to avoid ambiguity.

## Executable Lua

Set `"script": true` on every definition that has callbacks. Script-only entries are allowed. The entrypoint returns a table:

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
                    -- Release any additional native listener/resource owned here.
                end)
            end,
            on_update = function(ctx, elapsed)
                ctx.state.restore()
            end,
            on_event = function(ctx, name, event)
                if event.attacker == ctx.owner then ctx.state.restore(event) end
            end,
            on_deactivate = function(ctx, reason)
                -- Optional final callback; registered cleanup runs afterward.
            end,
        },
    },
}
```

Lua is trusted local mod code and can call native game APIs. It is not sandboxed. JSON validation and startup syntax compilation do not execute it. Modules are evaluated lazily when a selected/awarded script entry needs them, only under local SoloPlay or Realms host authority. Each package has one private environment and module cache per mission; each entry/owner binding has its own `ctx.state`. This permits shared helper state within a package without creating ordinary game globals. Native libraries/functions are available through the game environment and the loader's `Mods.lua` backups. Package modules compile with that same loader compiler, including when the ordinary global `loadstring` is unavailable.

`on_activate` runs once when a binding is created, regardless of transient entry conditions. Use it to register state and effects. Dynamic effects are filtered by the entry's target, availability and conditions when applied. `on_update`, `on_event` and queued context actions respect entry conditions. `on_update` requires an interval from 0.1 to 600 seconds and does not run catch-up bursts. HCM global updates receive `ctx.owner == nil` and `ctx.unit == nil`; select explicit targets for team actions. Mortis updates belong to the selected owner.

`on_event` requires explicit event subscriptions, up to 64 unique names: audited native events from `event-contracts.json`, plus `spawn`, `enemy_died`, `mission_start` and `signal`. It receives `(ctx, event_name, event)`. Native payload availability varies by event. Owner `enemy_died`/`signal` subscriptions are broadcast to living selected owners; other owner events follow their event unit. HCM global subscriptions match the definition's targets against the event unit, or run for unitless events. Lua callbacks cannot recursively dispatch another native event through this adapter while a callback/action is running.

Callback/module errors are shown for the package. A failed callback clears its Lua effects, pending context actions and registered cleanup, then stops that binding for this mission. Its separate JSON effects remain governed by the definition. A bad module does not stop independent packages. Removing an entry, owner death and mission exit run cleanup; reusing an engine after finish cannot reactivate it. Script modules retry in a new mission, using that mission's package snapshot.

## Context API

| Member | Contract |
| --- | --- |
| `package_id`, `package_version`, `entry_id`, `qualified_id` | Source identity; `entry_id` is the original JSON ID. |
| `owner`, `unit`, `time`, `state`, `role` | Owner, current callback unit, engine seconds, per-binding state and `authority`. |
| `resource(path)` | Returns frozen raw bytes or nil/reason; only declared `resources/` files. |
| `require(path)` | Loads/caches a declared `lua/` module in this package. |
| `dependency(id, path?)` | Loads a declared dependency module; without path, returns its entrypoint's `exports`. |
| `set_effects(table_or_nil)` | Replaces this binding's dynamic stats/keywords/modifiers; validates the regular effect schema. |
| `compile_action(action, slot?)` | Validates and copies an action once; returns a function accepting optional event data. Repeated temporary effects with the same slot reuse their stack/lifetime key. |
| `action(action, event?, slot?)` | Convenience validation/queue call; use compiled actions in frequent callbacks. True means queued, not guaranteed native execution. |
| `context(unit?, event?)` | Reads the normal native/DIY condition context; defaults to the current callback unit. |
| `units(selector, radius?)` | Returns up to four players or 64 matching units. Radius 1–50 is centered on the callback unit. |
| `qualify(entry_id, package_id?)` | Stable qualified ID; a different package must be a declared dependency. |
| `signal(name, duration)` | Emits a package-scoped signal, or a declared shared signal. Duration 0.1–600 seconds. |
| `global_signal(name, duration)` | Emits an explicitly shared signal. |
| `random(key, chance)` | Deterministic stream per package/entry/key/owner; chance 0–1. |
| `on_cleanup(function)` | Registers up to 64 callbacks, run in reverse registration order with a reason. |
| `log(message)` | Sends text to the manager's package log adapter when one is configured. |

At module scope, `package_require("lua/helpers.lua")` and `dependency_require("common-library", optional_path)` provide the same module access. `require("./helpers.lua")` is an alias for a local `lua/helpers.lua` module. Other `require` names use the native game resolver. Module cycles raise a package error. Do not retain callback context beyond its active binding.

Common context actions reuse the existing validated native adapter and its ownership cleanup. Direct native hooks/listeners/resources created by an author require matching `on_cleanup` work. Already executed healing, damage, spawns or other irreversible gameplay events cannot be undone. Signals and pause durations expire normally; they are not rewound on deselection. Callback budgets bound dispatch count, but cannot preempt a Lua function that loops indefinitely.

## Resources and multiplayer

Resources are frozen byte strings, not an automatic import into Stingray's resource database. Reading a PNG, sound file or another format is supported as bytes; rendering/playing it needs a suitable decoder or native engine resource integration supplied by the author. Existing action identifiers for native materials/sounds stay subject to the audited catalog. Raw files are not uploaded to another player.

Mortis availability compares a SHA-256 entry fingerprint covering definitions, manifest, all declared Lua/resources and the complete declared dependency closure. All participating room members must have matching bytes for an entry's package and dependencies; their other packages may differ. The room protocol is ten, so earlier peers cannot confirm these fingerprints. IDs/fingerprints and existing aggregate effects cross the network; Lua and resource bytes do not. HCM Lua executes on the host; clients continue to receive normal synchronized results and existing aggregate player effects. Client prediction, unusual engine resources and four-player combat still require live-game acceptance testing.

## Limits and examples

Each manager allows 256 package folders, 256 declared files plus the manifest per package, 32 MiB per package and 128 MiB of retained package data. Lua files are at most 256 KiB, definition JSON at most 512 KiB, and each raw resource at most 8 MiB. Paths have at most eight components and 192 bytes. Combined normalized definitions must fit 128 entries, 512 KiB and 30,000 JSON nodes; a package that would exceed the aggregate limit is excluded as a whole, along with dependents.

The existing runtime retains its trigger/action/queue limits in GUIDE.en.md. Lua adds at most 128 callback invocations between updates. Unsubscribed/unselected entries have no event or timer callback. Directory discovery, file reads, syntax compilation and hashing occur at startup or explicit refresh/import, never in the frame/effect/kill path. Startup's optional mod-dependency pass is one-shot.

Copy `package-examples/lua-mortis-example` or `package-examples/lua-conditions-example` into its matching directory to try executable examples. The provided data-only examples are also complete package folders. Their source can be edited and distributed as a folder without losing dependencies or resources. The older individual JSON files in docs remain reference definitions and may be converted through clipboard import.

Package management does not contain reward limits. In the Realms Mortis preparation controls, the host edits the independent DIY switch and point limit using minus/plus or direct numeric entry (0–99). Each DIY talent costs one point regardless of tier. SoloPlay has a separate Reward settings page. Tier is only a label; old saved tier quotas are ignored. HCM applies every enabled checked condition. Its list has no random-selection mode, seed or quantity quota; legacy weights and exclusion groups do not remove checked entries. Hover a row to inspect its details without changing selection. Files stay on the separate Package manager page.
