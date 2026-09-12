local mod=get_mod("HavocEnemyDirector")
local L={
    mod_name={en="Havoc Enemy Director",["zh-cn"]="浩劫敌人导演",["zh-tw"]="浩劫敵人導演"},
    mod_description={en="Configure formations, independent encounter rules, adaptive pressure and native enemy templates. Requires Havoc Condition Manager; changes apply next mission.",["zh-cn"]="配置独立编队、投放规则、自适应压力与原版敌人模板。需要浩劫词条管理器；修改在下一局生效。",["zh-tw"]="設定獨立編隊、投放規則、自適應壓力與原版敵人範本。需要浩劫詞條管理器；修改在下一局生效。"},
    director_open={en="Open enemy director",["zh-cn"]="打开敌人导演",["zh-tw"]="開啟敵人導演"},
    open={en="Open",["zh-cn"]="打开",["zh-tw"]="開啟"},
    toggle_next_mission={en="Switch saved. The current mission keeps its configuration; the new state applies next mission.",["zh-cn"]="开关已保存；当前任务保持原配置，下一局应用新的开关状态。",["zh-tw"]="開關已儲存；目前任務保持原設定，下一局套用新的開關狀態。"},
}
for key,value in pairs(mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/preset_localization")) do L[key]=value end
for key,value in pairs(mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_localization")) do L[key]=value end
L.template_scope=L.director_summary_help
L.template_load_hint={en="Loading replaces HCM values and all HED settings, including formations, deployment rules and both seeds. Changes apply next mission.",
    ["zh-cn"]="加载会替换 HCM 数值及全部 HED 设置，包括编队、投放规则和两类种子；下一局生效。",
    ["zh-tw"]="載入會取代 HCM 數值及全部 HED 設定，包括編隊、投放規則與兩類種子；下一局生效。"}
return L
