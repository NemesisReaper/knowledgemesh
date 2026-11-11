class Job:
 name="knowledge_evolution"
 def run(self,p):
  a=p.get("previous",{}); b=p.get("current",{})
  if not isinstance(a,dict) or not isinstance(b,dict): raise ValueError("previous/current must be objects")
  changes=[{"field":k,"before":a.get(k),"after":b.get(k),"change":"added" if k not in a else "removed" if k not in b else "modified"} for k in sorted(set(a)|set(b)) if a.get(k)!=b.get(k)]
  return {"changes":changes,"changed":bool(changes)}
