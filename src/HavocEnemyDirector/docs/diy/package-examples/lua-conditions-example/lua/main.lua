-- Trusted local mod code; activated only for the selected entry on the authority.
local helpers = package_require("lua/helpers.lua")
return {
    api_version = { major = 1, minor = 0 },
    exports = { description = "Executable package example" },
    entries = {
        team_training = {
            interval = 5,
            on_activate = function(ctx)
                local bytes = assert(ctx:resource("resources/amount.txt"))
                ctx:set_effects({ stats = { damage = helpers.clamp(tonumber(bytes), 0, 1) } })
                ctx.state.restore = ctx:compile_action({ type = "toughness", amount = 2, target = "players" })
                ctx:on_cleanup(function(reason)
                    -- Release extra native resources/listeners here if you add any.
                    ctx.state.restore = nil
                end)
            end,
            on_update = function(ctx, elapsed)
                ctx.state.restore()
            end,
        },
    },
}
