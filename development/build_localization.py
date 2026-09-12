from pathlib import Path
import sys, json
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root.parent.parent/'dev-support/test-runtime'))
from opencc import OpenCC
convert=OpenCC('s2twp')
data=json.loads((root/'development/director-strings.json').read_text(encoding='utf-8-sig'))
quote=lambda s:json.dumps(s,ensure_ascii=False)
lines=['-- Player-facing director controls.','return {']
for key,(en,cn) in data.items():
    lines.append('    director_'+key+'={en='+quote(en)+',["zh-cn"]='+quote(cn)+',["zh-tw"]='+quote(convert.convert(cn))+'},')
lines.append('}')
(root/'src/HavocEnemyDirector/scripts/mods/HavocEnemyDirector/director_localization.lua').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(len(data),'localized director labels and help entries')
