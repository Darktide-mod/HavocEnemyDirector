import re
from PIL import ImageFont

total=0
for name in ('HavocConditionManager','HavocEnemyDirector'):
    for key,value in L.globals().mods[name].localization.items():
        assert all(isinstance(value[lang],str) and value[lang] for lang in ('en','zh-cn','zh-tw')),(name,key)
        formats=[[spec for spec in re.findall(r'%(?:[-+ #0]*\d*(?:\.\d+)?[cdfgiousxXq]|%)',value[lang]) if spec!='%%'] for lang in ('en','zh-cn','zh-tw')]
        assert formats[0]==formats[1]==formats[2],(name,key,formats)
        assert not re.search('[\u3400-\u9fff]',value['en']),(name,key,'Chinese in English')
        total+=1
for key,value in L.globals().mods.HavocConditionManager.auric_conditions.localizations.items():
    assert all(value[lang] for lang in ('en','zh-cn','zh-tw'))
    total+=1

locale_layouts={}
fontpath=r'C:\Windows\Fonts\msyh.ttc'
fonts={}
issues=[]
for language in ('en','zh-cn','zh-tw'):
    L.globals().test_language=language
    L.globals().test_view._current.havoc_theme_circumstance='default'
    L.globals().test_view._options.havoc_theme_circumstance=tbl([{'id':'default','display_name':{'en':'No special environment','zh-cn':'无特殊环境','zh-tw':'無特殊環境'}[language]}])
    catalog=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_catalog')
    L.globals().mods.HavocConditionManager.condition_catalog=catalog
    catalog.extend(settings)
    load_mod('HavocEnemyDirector/scripts/mods/HavocEnemyDirector/editor')
    locale_paging=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging')
    for page in range(1,5):
        view=L.globals().test_view
        view._hcm_page=page; view._hcm_choice=None; view._hcm_number=None
        locale_paging.refresh(view,settings)
        items=plain_items(view._hcm_ui)
        locale_layouts[f'{language}_{page}']=items
        for item in items:
            text=item['text']; key=item['key']
            assert not re.search(r'\bui_\d+\b',text),(language,key,text)
            # These names are provided by the engine and have placeholder text in this harness.
            if key.startswith(('condition_','unit_')) or item.get('panel'): continue
            if language=='en': assert not re.search('[\u3400-\u9fff]',text),(language,key,text)
            size=item.get('font',22); f=fonts.setdefault(size,ImageFont.truetype(fontpath,size))
            pad=42 if item.get('checkbox') else 2 if item.get('center') else 12
            right=item.get('text_right_padding') or (40 if item.get('choice') else 2 if item.get('center') else 12)
            width=item['w']-pad-right
            lines=[]
            for paragraph in text.split('\n'):
                line=''
                for ch in paragraph:
                    if line and f.getlength(line+ch)>width: lines.append(line); line=ch
                    else: line+=ch
                lines.append(line)
            height=round(size*1.28)*len(lines)
            if height>item['h']+3: issues.append((language,key,height,item['h'],text))
    # Exercise translated native numeric popup labels and validation feedback.
    L.execute('''
test_view._hcm_page=4
Paging.refresh(test_view,test_settings)
local item=find_control("total_cap_value")
Paging.numeric.open(test_view,item)
test_view._widgets_by_name.hcm_number_input.content.input_text="bad"
assert(not Paging.numeric.commit(test_view))
Paging.refresh(test_view,test_settings)
assert(test_view._hcm_number.error and not test_view._hcm_number.error:find("ui_",1,true))
Paging.numeric.cancel(test_view)
''')
L.globals().test_language=None
L.globals().mods.HavocConditionManager.condition_catalog=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_catalog')
L.globals().mods.HavocConditionManager.condition_catalog.extend(settings)
load_mod('HavocEnemyDirector/scripts/mods/HavocEnemyDirector/editor')
(CHECKS/'three-language-layouts.json').write_text(json.dumps(locale_layouts,ensure_ascii=False,indent=2),encoding='utf-8')
for issue in issues: print(issue)
assert not issues, f'{len(issues)} translated controls overflow'
print(f'Three languages: {total} entries, format placeholders, actual page builds, input messages and translated text bounds: PASS')
