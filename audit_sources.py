from pathlib import Path
import json,urllib.request,hashlib,re,html
from concurrent.futures import ThreadPoolExecutor
P=Path(__file__).parent;S=json.loads((P/'study.json').read_text(encoding='utf-8'))
urls=list(dict.fromkeys([x['url']for x in S['quotes']+S['confessions']]))
def check(url):
 for attempt in range(2):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=15)as r:raw=r.read();status=r.status
   text=html.unescape(re.sub('<[^>]*>','',raw.decode('utf-8')))
   quotes=[{'quote':x['text'],'exact':x['text']in text}for x in S['quotes']if x['url']==url]
   return {'url':url,'status':status,'sha256':hashlib.sha256(raw).hexdigest(),'quotes':quotes}
  except Exception as e:error=str(e)
 return {'url':url,'error':error}
with ThreadPoolExecutor(max_workers=4)as pool:result=list(pool.map(check,urls))
(P/'qa').mkdir(exist_ok=True)
(P/'qa/source-audit.json').write_text(json.dumps({'date':'2026-11-07','sources':result},ensure_ascii=False,indent=2),encoding='utf-8')
assert all(x.get('status')==200 and all(q['exact']for q in x['quotes'])for x in result),result
print('PASS: CCI links live; all six short quotations match their designated source text.')

