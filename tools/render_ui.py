from pathlib import Path

import json,re,sys,argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from project_env import CHECKS
from PIL import Image,ImageDraw,ImageFont
parser=argparse.ArgumentParser(description='Render offline UI assets to an explicit release location.')
parser.add_argument('--layouts',type=Path,default=CHECKS/'ui-layouts.json')
parser.add_argument('--output',type=Path,default=ROOT/'publishing')
parser.add_argument('--report',type=Path,default=CHECKS/'ui-images.json')
args=parser.parse_args()
OUT=args.output

layouts=json.loads(args.layouts.read_text(encoding='utf-8'))
fonts={}
def font(n):
    if n not in fonts:fonts[n]=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',n)
    return fonts[n]
names_en={'chaos_armored_infected':'Armoured Groaner','chaos_lesser_mutated_poxwalker':'Mutated Poxwalker','chaos_mutated_poxwalker':'Mutated Poxwalker','chaos_newly_infected':'Groaner','chaos_poxwalker':'Poxwalker','cultist_assault':'Dreg Stalker','cultist_melee':'Dreg Bruiser','cultist_vanguard':'Dreg Vanguard','renegade_assault':'Scab Stalker','renegade_melee':'Scab Bruiser','renegade_rifleman':'Scab Shooter','renegade_vanguard':'Scab Vanguard'}
names_cn={'chaos_armored_infected':'披甲呻吟者','chaos_lesser_mutated_poxwalker':'变异瘟疫行者','chaos_mutated_poxwalker':'触手瘟疫行者','chaos_newly_infected':'呻吟者','chaos_poxwalker':'瘟疫行者','cultist_assault':'渣滓潜行者','cultist_melee':'渣滓格斗兵','cultist_vanguard':'渣滓先锋','renegade_assault':'血痂潜行者','renegade_melee':'血痂格斗兵','renegade_rifleman':'血痂射手','renegade_vanguard':'血痂先锋'}
from opencc import OpenCC
_converter=OpenCC('s2twp')
def tw(text): return _converter.convert(text)
palette={'gold':(221,194,122),'muted':(151,167,152)}
issues=[];records=[]
for key,specs in layouts.items():
    lang,kind=key.split('_',1)
    name=ROOT.name
    filename={'director': '01-director', 'numeric': '02-number-input', 'add_unit': '03-add-unit', 'native': '04-native-mode', 'templates':'05-templates', 'delete_template':'06-delete-template'}.get(kind,kind)+'.'+lang+'.png'
    path=OUT/'images'/filename;path.parent.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGB',(1920,1080),(9,16,13));draw=ImageDraw.Draw(im)
    dmf=kind.endswith('Manager')
    title=({'en':'Mod options','zh-cn':'模组选项','zh-tw':'模組選項'} if dmf else {'en':'Local game','zh-cn':'本地游戏','zh-tw':'本地遊戲'})[lang]
    draw.text((180,65) if dmf else (92,38),title,font=font(38 if dmf else 46),fill=palette['gold'])
    note={'en':'UI layout preview · Sample configuration · Not a gameplay capture','zh-cn':'界面布局预览 · 示例配置 · 非游戏实拍','zh-tw':'介面佈局預覽 · 範例配置 · 非遊戲實拍'}[lang]
    draw.text((120,1032) if dmf else (1130,55),note,font=font(18 if lang=='en' else 20),fill=(126,145,132))
    if not dmf:draw.line((100,119,1820,119),fill=(52,65,49),width=1)
    for item in sorted(specs,key=lambda x:(x.get('z',45 if x.get('overlay') else 0),not bool(x.get('panel')))):
        x,y,w,h=(item[k] for k in ('x','y','w','h'))
        if item.get('rgba'):
            ImageDraw.Draw(im,'RGBA').rectangle((x,y,x+w-1,y+h-1),fill=tuple(item['rgba']))
            continue
        if item.get('fill'):
            bg=(15,23,19) if item.get('panel') else (51,70,44) if item.get('selected') else (25,35,27)
            draw.rectangle((x,y,x+w-1,y+h-1),fill=bg)
            if not item.get('panel'):draw.line((x,y+h-1,x+w-1,y+h-1),fill=(57,69,50))
        if item.get('selected'):draw.rectangle((x,y,x+2,y+h),fill=palette['gold'])
        if item.get('input'):draw.rectangle((x,y,x+w-1,y+h-1),outline=palette['gold'],width=1)
        text=item['text']
        if item['key'].startswith(('unit_','choice_add_pool_unit_')):
            unit=item['key'].removeprefix('unit_') if item['key'].startswith('unit_') else item['key'].removeprefix('choice_add_pool_unit_')
            text=(names_en if lang=='en' else names_cn).get(unit,text)
            if lang=='zh-tw':text=tw(text)
        if item.get('panel') or not text:continue
        fs=item.get('font',22);f=font(fs)
        color=(220,133,117) if item.get('danger') else palette.get(item.get('color'),palette['gold'] if item.get('selected') else (222,229,214))
        pad=42 if item.get('checkbox') else 2 if item.get('center') else 12
        right=item.get('text_right_padding') or (40 if item.get('choice') else 2 if item.get('center') else 12)
        if item.get('checkbox'):
            cx,cy=x+24,y+h/2;draw.rectangle((cx-10,cy-10,cx+10,cy+10),outline=(120,143,119),width=1)
            if item.get('selected'):draw.line((cx-6,cy,cx-1,cy+5,cx+7,cy-6),fill=palette['gold'],width=2)
        if item.get('choice'):
            cx,cy=x+w-21,y+h/2;direction=-1 if item.get('expanded') and not item.get('upwards') else 1
            draw.line((cx-6,cy-direction*3,cx,cy+direction*3,cx+6,cy-direction*3),fill=palette['gold'],width=2)
        lines=[]
        for para in text.split('\n'):
            line=''
            tokens=para.split(' ') if lang=='en' else list(para)
            for token in tokens:
                candidate=line+(' ' if lang=='en' and line else '')+token
                if line and draw.textlength(candidate,font=f)>w-pad-right:lines.append(line);line=token
                else:line=candidate
            lines.append(line)
        lh=round(fs*1.28);bh=lh*len(lines)
        if bh>h+3:issues.append((key,item['key'],text,bh,h))
        ty=y+(h-bh)/2-1
        for line in lines:
            tx=x+(w-draw.textlength(line,font=f))/2 if item.get('center') else x+pad
            draw.text((tx,ty),line,font=f,fill=color);ty+=lh
    if not dmf:
        for x,direction in ((28,-1),(1844,1)):
            cx=x+24;pts=[(cx-direction*14,514),(cx+direction*14,538),(cx-direction*14,562)]
            draw.line(pts,fill=palette['gold'] if direction<0 else (56,69,54),width=8)
        draw.text((120,1031),{'en':'[ESC] Back','zh-cn':'[ESC] 返回','zh-tw':'[ESC] 返回'}[lang],font=font(21),fill=palette['gold'])
    if lang=='en':assert not any(re.search('[\u3400-\u9fff]',i['text']) for i in specs),key
    im.save(path,optimize=True)
    records.append({'mod':name,'language':lang,'file':str(path.relative_to(OUT)).replace('\\','/'),'kind':kind})
assert not issues,issues
if args.report:
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('Rendered',len(records),'UI images; English text and all text bounds checked.')
