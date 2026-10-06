from datetime import datetime
from urllib.parse import urljoin
import httpx
from app.models import Tender,Item
BASE="https://public-api.prozorro.gov.ua/api/2.5/tenders"
def dt(v):
 try:return datetime.fromisoformat(str(v).replace("Z","+00:00")).replace(tzinfo=None)
 except:return None
async def fetch(limit=200):
 out=[]; seen=set(); url=BASE; params={"limit":100,"descending":1}
 async with httpx.AsyncClient(timeout=35,follow_redirects=True,headers={"User-Agent":"CEE-Tender-Intelligence/0.3"}) as c:
  while url and len(seen)<limit:
   feed=await c.get(url,params=params);feed.raise_for_status();body=feed.json();params=None
   rows=body.get("data",[])
   for row in rows:
    rid=row.get("id")
    if not rid or rid in seen:continue
    seen.add(rid)
    rr=await c.get(f"{BASE}/{rid}");rr.raise_for_status();x=rr.json().get("data",{});v=x.get("value") or {};per=x.get("tenderPeriod") or {};e=x.get("procuringEntity") or {};tid=x.get("tenderID",rid)
    items=[Item(i.get("description","") or "",i.get("quantity"),(i.get("unit") or {}).get("name"),(i.get("classification") or {}).get("id")) for i in x.get("items",[])]
    title=x.get("title") or x.get("title_en") or tid
    out.append(Tender("prozorro:"+tid,"prozorro","UKR",title,e.get("name","") or "",x.get("description","") or "",v.get("amount"),v.get("currency"),dt(per.get("endDate")),dt(x.get("dateModified") or x.get("dateCreated")),x.get("status","") or "",f"https://prozorro.gov.ua/tender/{tid}",items=items))
    if len(seen)>=limit:break
   nxt=(body.get("next_page") or {}).get("uri");url=urljoin(BASE,nxt) if nxt else None
 return out
