local mod=get_mod("HavocEnemyDirector")
return {
    name=mod:localize("mod_name"),description=mod:localize("mod_description"),is_togglable=true,
    options={widgets={
        {setting_id="director_open",type="button",button_text="open",function_name="open_settings"},
    }},
}
