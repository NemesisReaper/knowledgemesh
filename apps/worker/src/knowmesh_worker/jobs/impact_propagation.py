class Job:
 name="impact_propagation"
 def run(self,p):
  edges=p.get("edges",[]); source=p.get("source_id")
  if not isinstance(edges,list) or not source: raise ValueError("edges and source_id required")
  adj={}
  for e in edges: adj.setdefault(str(e["source"]),set()).add(str(e["target"]))
  seen={str(source)}; frontier=[str(source)]; levels=[]
  while frontier:
   levels.append(frontier); nxt=sorted({v for u in frontier for v in adj.get(u,set()) if v not in seen}); seen.update(nxt); frontier=nxt
  return {"source_id":str(source),"affected":sorted(seen-{str(source)}),"levels":levels,"max_depth":len(levels)-1}
