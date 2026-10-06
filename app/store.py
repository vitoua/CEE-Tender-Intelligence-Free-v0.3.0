from datetime import datetime
from app.matching import match
class Store:
 def __init__(self):self.tenders={};self.runs=[]
 def ingest(self,source,rows):
  relevant=0
  for t in rows:
   t.category,t.score,hits=match(" ".join([t.title,t.description]+[i.description for i in t.items]))
   for i in t.items:i.matched_terms=hits
   self.tenders[t.id]=t
   if t.score>=25:relevant+=1
  self.runs.insert(0,{"source":source,"status":"ok","fetched":len(rows),"relevant":relevant,"at":datetime.utcnow(),"error":""});self.runs=self.runs[:8];return len(rows),relevant
 def error(self,source,e):self.runs.insert(0,{"source":source,"status":"error","fetched":0,"relevant":0,"at":datetime.utcnow(),"error":f"{type(e).__name__}: {e}"})
store=Store()
