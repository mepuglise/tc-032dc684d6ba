#!/usr/bin/env python3
"""Usage: python3 add_card.py [/path/Card.html ...]  -> copies cards (byte-identical), rebuilds thumbs + index.html.
Then: git add -A && git commit -m 'add card' && git push"""
import sys,os,re,base64,shutil,io,html
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
for p in sys.argv[1:]:
    shutil.copyfile(p,os.path.join(D,'cards',os.path.basename(p)))
    src=os.path.dirname(os.path.dirname(os.path.abspath(p)))  # new-style card: also copy its portrait + shared back + thumb
    for rel in re.findall(r'src="\.\./((?:portraits|assets)/[^"]+)"',open(p).read())+['thumbs/'+os.path.basename(p)[:-5]+'.jpg']:
        if os.path.exists(os.path.join(src,rel)) and not os.path.exists(os.path.join(D,rel)):
            os.makedirs(os.path.dirname(os.path.join(D,rel)),exist_ok=True);shutil.copyfile(os.path.join(src,rel),os.path.join(D,rel))
items=[]
for f in sorted(os.listdir(os.path.join(D,'cards'))):
    if not f.endswith('.html'): continue
    n=f[:-5]; s=open(os.path.join(D,'cards',f),encoding='utf-8',errors='ignore').read()
    m=re.search(r'class="art">\s*<img src="data:image/\w+;base64,([^"]+)"',s) or re.search(r'data:image/\w+;base64,([^"\')]+)',s)
    t=os.path.join(D,'thumbs',n+'.jpg')
    if m and not os.path.exists(t):
        im=Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB'); im.thumbnail((480,480)); im.save(t,quality=82)
    items.append(n)
cards=''.join(f'<a class="c" href="cards/{html.escape(n)}.html"><img src="thumbs/{html.escape(n)}.jpg" alt="{html.escape(n)}" loading="lazy"><span>{html.escape(n)}</span></a>' for n in items)
open(os.path.join(D,'index.html'),'w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>The Company Pokédex — Caught 2026</title>
<style>body{{margin:0;font-family:system-ui,sans-serif;background:#12101c;color:#f3eefc}}header{{padding:20px 16px 8px;text-align:center}}h1{{font-size:1.4rem;margin:0 0 6px}}p{{margin:0;opacity:.7;font-size:.85rem}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:14px;padding:16px;max-width:1000px;margin:auto}}
.c{{display:block;background:linear-gradient(160deg,#2b2347,#1a1530);border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;box-shadow:0 4px 14px #0008}}.c img{{width:100%;aspect-ratio:1;object-fit:cover;display:block}}.c span{{display:block;padding:8px;text-align:center;font-weight:700}}</style></head>
<body><header><h1>The Company Pokédex — Caught 2026</h1><p>A private trainer gift. Not official Pokémon. Tap a card to open it.</p></header><main class="g">{cards}</main></body></html>''')
print('cards:',items)
