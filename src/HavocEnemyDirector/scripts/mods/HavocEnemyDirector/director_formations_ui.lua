local mod=get_mod("HavocEnemyDirector")
local S=get_mod("HavocConditionManager").template_schema
return function(view,ui,U)
    local cfg=mod.peek_config();local C=mod.director_config
    local selected=U.find(cfg.formations,view._hed_formation_id) or cfg.formations[1]
    if selected then view._hed_formation_id=selected.id end
    ui:panel("hed_form_list_panel",105,282,475,680)
    ui:panel("hed_form_detail_panel",595,282,1220,680)
    ui:text("hed_form_new_label",125,299,435,34,U.loc("new_family"),21,"muted")
    local family=view._hed_new_family or "hordes"
    local families={};for _,id in ipairs(C.families) do families[#families+1]={id,U.loc("family_"..id)} end
    ui:choice("hed_form_new_family",125,340,435,48,family,families,function(id) view._hed_new_family=id end)
    ui:button("hed_form_add",125,402,435,48,U.loc("add_formation"),#cfg.formations<32 and function()
        U.save(view,function(next_cfg)
            local options=U.breeds(family);local name
            if family=="hordes" or family=="trickle" then name="chaos_poxwalker" else name=options[1] and options[1][1] end
            local f=C.new_formation(next_cfg,U.loc("new_formation",next_cfg.next_id),family,name)
            view._hed_formation_id=f.id;view._hed_variant=1
        end)
    end)
    U.list(view,ui,"hed_form_list",cfg.formations,selected and selected.id,function(id) view._hed_formation_id=id;view._hed_variant=1;view._hed_delete_formation=nil end,474,7)
    if not selected then ui:text("hed_form_empty",625,369,1160,160,U.loc("no_formations"),27,"muted");return end
    local f=selected
    local function change(fn) return U.record(view,"formations",f.id,fn) end
    ui:button("hed_form_name",615,302,874,52,f.name,function() U.rename(view,"formations",f) end)
    ui:button("hed_form_copy",1505,302,290,52,U.loc("copy"),#cfg.formations<32 and function()
        U.save(view,function(next_cfg)
            local copy=S.copy(f);copy.id=C.allocate(next_cfg,"f");copy.name=U.copy_name(f.name)
            next_cfg.formations[#next_cfg.formations+1]=copy;view._hed_formation_id=copy.id;view._hed_variant=1
        end)
    end)
    ui:text("hed_form_category",615,367,1180,44,U.loc("formation_immutable",U.loc("family_"..f.family)),20,"muted")
    local index=math.min(view._hed_variant or 1,#f.variants);view._hed_variant=index
    local variant=f.variants[index];local options={}
    for i,v in ipairs(f.variants) do options[#options+1]={i,U.loc("variant",i,v.weight)} end
    ui:choice("hed_form_variant",615,428,560,48,index,options,function(i) view._hed_variant=i end)
    ui:button("hed_form_variant_add",1191,428,290,48,U.loc("add_variant"),#f.variants<8 and function()
        change(function(v) v.variants[#v.variants+1]=S.copy(variant);view._hed_variant=#v.variants end)
    end)
    ui:button("hed_form_variant_delete",1497,428,298,48,U.loc("delete_variant"),#f.variants>1 and function()
        change(function(v) table.remove(v.variants,index);view._hed_variant=math.min(index,#v.variants) end)
    end,false,nil,true)
    local offset=ui:window("hed_form_members_"..f.id.."_"..index,#variant.members,4,1,1230,749,565)
    for row=1,math.min(4,#variant.members-offset) do
        local i=offset+row;local m=variant.members[i];local y=498+(row-1)*60
        ui:choice("hed_member_"..i,615,y,550,52,m.name,U.breeds(f.family),function(name)
            change(function(v) v.variants[index].members[i].name=name end)
        end)
        for bound=1,2 do
            local x=1180+(bound-1)*248
            ui:text("hed_member_amount_"..i.."_"..bound.."_label",x,y,105,52,U.loc(bound==1 and "min_count" or "max_count"),17,"muted")
            ui:number("hed_member_amount_"..i.."_"..bound,x+105,y,120,52,tostring(m.amount[bound]),{
                label=U.loc(bound==1 and "min_count" or "max_count"),value=m.amount[bound],min=0,max=300,integer=true,
                set=function(n)
                    change(function(v)
                        local amount=v.variants[index].members[i].amount;amount[bound]=n
                        if bound==1 then amount[2]=math.max(n,amount[2]) else amount[1]=math.min(n,amount[1]) end
                    end)
                end})
        end
        ui:button("hed_member_delete_"..i,1685,y,110,52,"−",#variant.members>1 and function()
            change(function(v) table.remove(v.variants[index].members,i) end)
        end)
    end
    ui:button("hed_member_add",615,749,595,42,U.loc("add_member"),#variant.members<16 and function()
        change(function(v) v.variants[index].members[#v.variants[index].members+1]={name=variant.members[#variant.members].name,amount={0,1}} end)
    end)
    U.number(ui,"hed_form_weight",615,811,1180,U.loc("variant_weight"),variant.weight,0.01,100,1,false,function(n)
        change(function(v) v.variants[index].weight=n end)
    end)
    local references=0;for _,rule in ipairs(cfg.deployments) do if rule.formation_id==f.id then references=references+1 end end
    ui:text("hed_form_help",615,869,1180,44,U.loc("formation_help"),17,"muted")
    if references>0 then ui:text("hed_form_references",615,915,880,36,U.loc("referenced",references),16,"muted") end
    ui:button("hed_form_delete",1515,914,280,36,U.loc(view._hed_delete_formation==f.id and "confirm_delete" or "delete"),references==0 and function()
        if view._hed_delete_formation==f.id then
            U.save(view,function(next_cfg)
                for i,v in ipairs(next_cfg.formations) do if v.id==f.id then table.remove(next_cfg.formations,i);break end end
            end);view._hed_formation_id=nil;view._hed_delete_formation=nil
        else view._hed_delete_formation=f.id end
    end,false,nil,true)
end
