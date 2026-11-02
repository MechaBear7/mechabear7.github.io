#!/usr/bin/env python3
"""Build both languages from shared Chinese templates and an explicit English catalog.

Run before previewing or publishing. Any new untranslated Chinese string blocks the
build, so content and layout maintenance must cover both language versions.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit
import json,re

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
CATALOG=json.loads((ROOT/'content/en.json').read_text())
HAN=re.compile(r'[\u4e00-\u9fff]')
MISSING=set()
class Page(HTMLParser):
    def __init__(self,lang,filename):
        super().__init__(convert_charrefs=True)
        self.lang,self.filename,self.out=lang,filename,[]
    def translate(self,value):
        key=value.strip()
        if self.lang=='zh' or not key:return value
        if key in CATALOG:
            return value[:len(value)-len(value.lstrip())]+CATALOG[key]+value[len(value.rstrip()):]
        if HAN.search(key):MISSING.add(key)
        return value
    def handle_decl(self,value):self.out.append('<!'+value+'>')
    def handle_comment(self,value):self.out.append('<!--'+value+'-->')
    def handle_starttag(self,tag,attrs):
        out=[]
        for key,value in attrs:
            if tag=='html' and key=='lang':value='en' if self.lang=='en' else 'zh-CN'
            if value and key in ('alt','title','aria-label','content'):value=self.translate(value)
            if value and key in ('src','href','poster'):
                u=urlsplit(value)
                if not u.scheme and not u.netloc:
                    if value.startswith(('styles.css','app.js')):value=u.path+'?v=bilingual-20261102'
                    if self.lang=='zh' and (value.startswith('assets/') or value.startswith(('styles.css','app.js'))):value='../'+value
            out.append(key if value is None else f'{key}="{escape(value,quote=True)}"')
        self.out.append('<'+tag+(' '+' '.join(out) if out else '')+'>')
    def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
    def handle_data(self,value):self.out.append(escape(self.translate(value),quote=False))
    def handle_endtag(self,tag):
        if tag=='head':
            name=self.filename
            self.out.append(f'<link rel="alternate" hreflang="en" href="https://mechabear7.github.io/{name}"><link rel="alternate" hreflang="zh-CN" href="https://mechabear7.github.io/zh/{name}"><link rel="alternate" hreflang="x-default" href="https://mechabear7.github.io/{name}">')
        self.out.append('</'+tag+'>')
    def result(self):
        out=''.join(self.out)
        target=('zh/' if self.lang=='en' else '../')+self.filename
        label='中文' if self.lang=='en' else 'EN'
        switch=f'<a class="language-switch" href="{target}" lang="'+('zh-CN' if self.lang=='en' else 'en')+'" hreflang="'+('zh-CN' if self.lang=='en' else 'en')+'" aria-label="'+('切换到中文' if self.lang=='en' else 'Switch to English')+'">'+label+'</a>'
        # The first nav is the main navigation; project outlines are unchanged.
        out=out.replace('</nav></header>','<span class="language-divider" aria-hidden="true"></span>'+switch+'</nav></header>',1)
        if self.lang=='en' and self.filename=='index.html':
            out=out.replace('<h1>杨贺磊 <span>Helei Yang</span></h1>','<h1>Helei Yang <span lang="zh-CN">杨贺磊</span></h1>')
        return out

def build():
    pages=sorted((ROOT/'content/zh').glob('*.html'))
    outputs={}
    for p in pages:
        for lang in ('en','zh'):
            parser=Page(lang,p.name);parser.feed(p.read_text())
            out=DIST/p.name if lang=='en' else DIST/'zh'/p.name
            outputs[out]=parser.result()
    media_zh=json.loads((ROOT/'content/media.zh.json').read_text())
    media_en=json.loads(json.dumps(media_zh))
    for spec in media_en.values():
        for key in ('alt','previewAlt','caption'):
            if spec.get(key):
                value=spec[key]
                if value in CATALOG:spec[key]=CATALOG[value]
                elif HAN.search(value):MISSING.add(value)
    outputs[DIST/'assets/media.zh.json']=json.dumps(media_zh,ensure_ascii=False,indent=2)+'\n'
    outputs[DIST/'assets/media.json']=json.dumps(media_en,ensure_ascii=False,indent=2)+'\n'
    if MISSING:raise SystemExit('Missing English translations:\n'+'\n'.join(sorted(MISSING)))
    for p,text in outputs.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
    print(f'Built {len(pages)} pages in each language ({len(pages)*2} HTML pages total); all translations present.')

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=DIST,help='Generated site directory (default: dist)')
    DIST=parser.parse_args().output.resolve()
    build()
