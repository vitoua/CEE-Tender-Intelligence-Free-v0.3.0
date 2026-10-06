from datetime import datetime
import httpx
from app.models import Tender,Item
URL="https://api.ted.europa.eu/v3/notices/search"
FIELDS=["publication-number","notice-title","buyer-name","buyer-country","total-value","total-value-cur","publication-date","deadline","classification-cpv","description-proc","description-lot"]
def first(v):
 if isinstance(v,dict):
  for k in ("eng","pol","ukr","deu","fra"):
   if k in v:return first(v[k])
  return first(next(iter(v.values()),""))
 if isinstance(v,list):return first(v[0]) if v else ""
 return str(v or "")
def dt(v):
 try:return datetime.fromisoformat(first(v)[:10])
 except:return None
def error_text(r):
 try:return str(r.json())[:700]
 except:return r.text[:700]
async def fetch(limit=200):
 queries=[
  'FT~"SSD" OR FT~"NVMe" OR FT~"DDR4" OR FT~"DDR5" OR FT~"memory card" OR FT~"flash drive"',
  'classification-cpv IN (30233100 30233130 30234100 30236100 30237200)'
 ]
 notices=[];last_error=""
 async with httpx.AsyncClient(timeout=45,follow_redirects=True,headers={"User-Agent":"CEE-Tender-Intelligence/0.3","Accept":"application/json"}) as c:
  for query in queries:
   payload={"query":query,"fields":FIELDS,"page":1,"limit":min(limit,200),"scope":"ACTIVE","checkQuerySyntax":False,"paginationMode":"PAGE_NUMBER","onlyLatestVersions":True}
   r=await c.post(URL,json=payload)
   if r.status_code==200:
    notices=(r.json().get("notices") or []);break
   last_error=f"HTTP {r.status_code}: {error_text(r)}"
  else:raise RuntimeError("TED API: "+last_error)
 out=[]
 for x in notices:
  n=first(x.get("publication-number")) or first(x.get("notice-identifier"));cpvs=x.get("classification-cpv") or [];des=first(x.get("description-proc")) or first(x.get("description-lot"))
  val=x.get("total-value")
  if isinstance(val,list):val=val[0] if val else None
  try:value=float(val)
  except:value=None
  items=[Item(des or first(x.get("notice-title")),cpv=first(cpv)) for cpv in (cpvs if isinstance(cpvs,list) else [cpvs])] or [Item(des or first(x.get("notice-title")))]
  out.append(Tender("ted:"+n,"ted",first(x.get("buyer-country"))[:3] or "EU",first(x.get("notice-title")) or n,first(x.get("buyer-name")),des,value,first(x.get("total-value-cur")),dt(x.get("deadline")),dt(x.get("publication-date")),"active",f"https://ted.europa.eu/en/notice/-/detail/{n}",items=items))
 return out
