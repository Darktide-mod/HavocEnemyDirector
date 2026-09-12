# Native text editing logic, with only engine text metrics and ASCII keyboard input stubbed.
L.execute('''
function table.append(a,b) for _,v in ipairs(b) do a[#a+1]=v end end
Utf8={string_length=function(s) return #s end,sub_string=function(s,a,b) return s:sub(a,b) end,
    find=string.find,string_insert=function(s,p,v) return s:sub(1,p-1)..v..s:sub(p) end,
    string_remove=function(s,p,n) return s:sub(1,p-1)..s:sub(p+(n or 1)) end}
Keyboard={BACKSPACE=8,DELETE=127,keystrokes=function() return test_keystrokes or {} end}
Clipboard={get=function() return test_clipboard end,put=function(t) test_clipboard=t; return true end}
Log={info=function() end}
''')
for name in ('body','body_medium','chat_input'):
    cache['scripts/managers/ui/ui_font_settings'][name]=tbl({'font_size':24,'font_type':'proxima_nova_bold'})
cache['scripts/managers/ui/ui_renderer']=L.eval('{text_size=function(_,s) return #s*12,24,nil,{#s*12,0} end}')
cache['scripts/ui/constant_elements/elements/chat/constant_element_chat_settings']=tbl({
    'window_margins':[0,0,0,0],'input_field_margins':[0,0,0,0],
    'insertion_caret_color':[255,255,255,255],'insertion_caret_size':[2,30],
    'input_text_idle_color':[255,255,255,255],'input_field_active_color':[255,20,20,20],
    'selected_text_color':[64,64,64,255],'placeholder_fade_time':1})
cache['scripts/ui/pass_templates/text_input_pass_templates']=lua_file(game/'scripts/ui/pass_templates/text_input_pass_templates.lua')
