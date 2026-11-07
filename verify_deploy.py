from pathlib import Path
import urllib.request,json,concurrent.futures
P=Path(__file__).parent
bases=['https://08-ser-gt-je-personal-20261003.github.io/sin-absurdity-20261107-v1-GTser/','https://sin-absurdity-20261107-v1-gtser.surge.sh/']
jobs=[(b,f)for b in bases for f in ['index.html','sermon.html','style.css','app.js']]
def check(job):
 b,f=job
 for attempt in range(3):
  try:
   req=urllib.request.Request(b+f,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=12)as r:raw=r.read();status=r.status
   return {'url':b+f,'status':status,'matches_local':raw.decode('utf-8').replace('\r\n','\n')==(P/'dist'/f).read_text(encoding='utf-8')}
  except Exception as e:error=str(e)
 return {'url':b+f,'status':None,'matches_local':False,'error':error}
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:result=list(pool.map(check,jobs))
(P/'qa/deployment.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
assert all(x['status']==200 and x['matches_local']for x in result),result
print('PASS: both public sites, two HTML pages and both resource files match local outputs.')

