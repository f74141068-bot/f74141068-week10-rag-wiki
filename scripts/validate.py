#!/usr/bin/env python3
"""Offline structural verifier for the Week 10 deliverable. Python 3 stdlib only."""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]

class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=set(); self.links=[]; self.slides=[]; self.scripts=[]; self.lang=None
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.add(d['id'])
        if tag=='html':self.lang=d.get('lang')
        if tag in ('a','link') and 'href' in d:self.links.append((tag,d['href']))
        if tag=='script' and 'src' in d:self.scripts.append(d['src'])
        if tag=='section' and 'slide' in d.get('class','').split():self.slides.append(d)

def load_html(path):
    p=Collector();p.feed(path.read_text(encoding='utf-8'));return p

def check_all(deck):
    failures=[];out=[]
    def ck(c,msg):
        (out if c else failures).append(('PASS' if c else 'FAIL')+' | '+msg)
    manifest=json.loads((ROOT/'raw/sources.json').read_text(encoding='utf-8'))
    ids=[x['id'] for x in manifest['items']];valid=set(ids)
    ck(len(ids)>=5 and len(set(ids))==len(ids),f'至少 5 篇唯一來源：{len(ids)}')
    ck(all(x['url'].startswith('https://') and x['title'] and x['facts'] for x in manifest['items']),'每筆來源有 HTTPS URL、標題及摘記')
    ck(all((ROOT/'raw'/f'{i}.md').is_file() for i in ids),f'來源原始摘記完整：{len(ids)} / {len(ids)}')
    ck(all((ROOT/'cards'/f'{i}.md').is_file() for i in ids),f'來源證據卡完整：{len(ids)} / {len(ids)}')
    wiki_files=list((ROOT/'wiki').glob('[0-9][0-9]_*.md'))
    ck(len(wiki_files)>=5,f'Wiki 主題條目數：{len(wiki_files)}')
    written='\n'.join(x.read_text(encoding='utf-8') for x in wiki_files)
    wiki_cites=set(re.findall(r'\[(S\d{2})\]',written))
    ck(wiki_cites==valid,f'Wiki 使用六篇來源：{sorted(wiki_cites)}')
    ck(not(set(re.findall(r'\[(S\d{2})\]',written))-valid),'Wiki 未使用未知來源 ID')
    ck(deck.is_file(),'HTML 簡報檔案存在')
    if not deck.is_file():return out+failures,failures
    parsed=load_html(deck);slides=parsed.slides
    ck(8<=len(slides)<=15,f'簡報頁數符合 8–15：{len(slides)}')
    ck(len(slides)==len(set(x.get('id') for x in slides)),'所有頁面有不重複的 ID')
    invalid=[];uncited=[];all_cited=set()
    for num,attrs in enumerate(slides,1):
        sid=[s.strip() for s in attrs.get('data-sources','').split(',') if s.strip()]
        if not sid:uncited.append(num)
        for k in sid:
            all_cited.add(k)
            if k not in valid:invalid.append((num,k))
    ck(not uncited, f'每張簡報有來源：{len(slides)-len(uncited)} / {len(slides)}'+(f'；缺 {uncited}' if uncited else ''))
    ck(not invalid,'來源 ID 均存在'+(f'；錯誤 {invalid}' if invalid else ''))
    ck(all_cited==valid,f'六篇資料皆出現在簡報來源列：{sorted(all_cited)}')
    ck(parsed.lang=='zh-Hant','簡報語言標記為繁體中文')
    ck(any('assets/deck.js' in x for x in parsed.scripts),'簡報包含本地互動 JS')
    HTMLS=['index.html','wiki.html','workflow.html','slides.html']
    pages={filename:load_html(ROOT/filename) for filename in HTMLS if (ROOT/filename).exists()}
    broken=[];total=0
    for filename,parsedPage in pages.items():
        for typ,link in parsedPage.links+[("script",x) for x in parsedPage.scripts]:
            if not link or link.startswith(('mailto:','tel:','data:','javascript:')):continue
            parts=urlsplit(link)
            if parts.scheme or parts.netloc:continue
            total+=1
            if parts.path:
                target=ROOT/unquote(parts.path).lstrip('/')
            else:
                target=ROOT/filename
            if not target.is_file():broken.append(f'{filename}: {link} [檔案不存在]')
            elif parts.fragment:
                q=load_html(target)
                if parts.fragment not in q.ids:broken.append(f'{filename}: {link} [錨點不存在]')
    ck(not broken,f'本地連結及錨點：{total} 條、錯誤 {len(broken)}'+('；'+str(broken[:5]) if broken else ''))
    for name in ['AGENTS.md','REQUIREMENTS.md','SOURCE_MAPPING.md','workflow/GRAPH.md','outline.md','drafts/slide_script.md','REPORT.md','SUBMISSION.txt']:
        ck((ROOT/name).is_file(),f'應交檔案存在：{name}')
    return out+failures,failures

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--deck',default='slides.html',help='deck path, relative to project root')
    args=ap.parse_args()
    target=ROOT/args.deck
    lines,failures=check_all(target)
    print('\n'.join(lines));print(f'\nRESULT: {len(lines)-len(failures)}/{len(lines)} PASS; {len(failures)} FAIL')
    return 0 if not failures else 1
if __name__=='__main__':sys.exit(main())
