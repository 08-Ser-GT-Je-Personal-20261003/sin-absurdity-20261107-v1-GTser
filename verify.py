from pathlib import Path
from html.parser import HTMLParser
import json,re
P=Path(__file__).parent
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.append(a['id'])
  if 'href'in a:self.links.append(a['href'])
checks=[]
for file in (P/'dist').glob('*.html'):
 raw=file.read_text(encoding='utf-8');h=Page();h.feed(raw)
 assert len(set(h.ids))==len(h.ids),file
 assert 'name="viewport"'in raw
 for link in h.links:
  if link.startswith('#'):assert link[1:]in h.ids,(file,link)
  elif not re.match('https?://',link):assert (file.parent/link.split('#')[0]).exists(),(file,link)
 checks.append({'page':file.name,'anchors':len(h.ids),'links':len(h.links)})
C=json.loads((P/'content.json').read_text(encoding='utf-8'));S=json.loads((P/'study.json').read_text(encoding='utf-8'))
assert [x['id']for x in C['sermon']]==['officers','nicodemus']
assert len(S['discussions'])==18 and len(S['quotes'])==6 and len(S['comparisons'])==3
assert all(x['url'].startswith('https://ccifellowship.org/')for x in S['quotes'])
assert not (P/'dist/CNAME').exists(),'Surge CNAME must not enter Pages artifact'
print(json.dumps({'static':'PASS','pages':checks,'sermon_points':2,'discussions':18,'source_quotes':6}))
