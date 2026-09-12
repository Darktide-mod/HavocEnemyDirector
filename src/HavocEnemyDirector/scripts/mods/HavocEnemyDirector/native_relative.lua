-- Relative values enter the native compiler after HCM's broad values and
-- before its rule binding/cache. Native fractional timing and slot capacity
-- must not be coerced through the fixed-value editor's validation bounds.
local mod=get_mod("HavocEnemyDirector")
local base=get_mod("HavocConditionManager")
local S,A,E,C=base.template_schema,base.template_registry,base.template_runtime,mod.director_config
local depth,in_config,snapshot=0,false,nil
mod:hook(E,"config",function(fn,...)
    local previous=in_config;in_config=true
    local ok,cfg=pcall(fn,...);in_config=previous
    if not ok then error(cfg,0) end
    if cfg._hed_relative==nil then
        cfg._hed_relative={}
        if base.has_local_gameplay_authority() and mod.is_gameplay_enabled() then
            cfg._hed_relative=S.copy(mod.peek_config().relative)
        end
    end
    if next(cfg._hed_relative) then cfg.changed=true end
    snapshot=cfg
    return cfg
end)
mod:hook(E,"prepare",function(fn,...)
    depth=depth+1
    local ok,result=pcall(fn,...);depth=depth-1
    if not ok then error(result,0) end
    return result
end)
mod:hook(S,"apply",function(fn,root,family,coarse,...)
    local result,changed,invalid=fn(root,family,coarse,...)
    if depth>0 and not in_config and snapshot then
        local entry=A.by_table[root]
        local relative=entry and snapshot._hed_relative[entry.id]
        if relative then
            local applied
            result,applied=C.apply_relative(result,entry,relative,coarse)
            changed=changed+applied
        end
    end
    return result,changed,invalid
end)
return true
