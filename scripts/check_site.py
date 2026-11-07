"""Check local routes, assets, fragments, metadata, and structured data."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
import json
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent
BASE='https://afafloudini.com'
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.links=[]; self.ids=[]; self.h1=0; self.canonical=[]; self.og={}; self.json_blocks=[]; self.in_json=False; self.buffer=''; self.noindex=False
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='h1': self.h1+=1
        for key in ('href','src'):
            if key in a: self.links.append(a[key])
        if tag=='img': assert 'alt' in a and a.get('width') and a.get('height'),a
        if tag=='iframe': assert a.get('title'),a
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a['href'])
        if tag=='meta' and a.get('property','').startswith('og:'): self.og[a['property']]=a['content']
        if tag=='meta' and a.get('name')=='robots': self.noindex='noindex' in a.get('content','')
        if tag=='script' and a.get('type')=='application/ld+json': self.in_json=True; self.buffer=''
    def handle_data(self,data):
        if self.in_json: self.buffer+=data
    def handle_endtag(self,tag):
        if tag=='script' and self.in_json: self.json_blocks.append(json.loads(self.buffer)); self.in_json=False
pages={p.name:Document(p.read_text()) for p in ROOT.glob('*.html')}
for name,page in pages.items():
    assert page.h1==1,(name,'one h1 required')
    assert len(page.ids)==len(set(page.ids)),(name,'duplicate ids')
    assert page.json_blocks,(name,'missing structured data')
    expected=BASE+('/' if name=='index.html' else '/'+name)
    assert page.og['og:url']==expected,name
    assert page.noindex if name=='404.html' else page.canonical==[expected],name
    for link in page.links:
        url=urlsplit(link)
        if url.scheme and url.scheme not in ('http','https'): continue
        if url.netloc and url.netloc!='afafloudini.com': continue
        target=unquote(url.path).lstrip('/') or (name if not url.path else 'index.html')
        if target=='/': target='index.html'
        assert (ROOT/target).is_file(),(name,link,'missing file')
        if url.fragment and target in pages: assert url.fragment in pages[target].ids,(name,link,'missing anchor')
sitemap=[x.text for x in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url/{*}loc')]
assert set(sitemap)=={BASE+('/' if n=='index.html' else '/'+n) for n in pages if n!='404.html'}
assert (ROOT/'CNAME').read_text().strip()=='afafloudini.com'
assert 'Sitemap: '+BASE+'/sitemap.xml' in (ROOT/'robots.txt').read_text()
print(f'PASS: {len(pages)} pages; local links, assets, anchors, h1s, image accessibility, JSON-LD, canonical/social URLs, sitemap and domain configuration.')
