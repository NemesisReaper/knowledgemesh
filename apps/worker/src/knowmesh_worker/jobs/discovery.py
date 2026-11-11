class Job:
 name="discovery"
 def run(self,p):
  terms=[str(t).casefold() for t in p.get("terms",[]) if str(t).strip()]; records=p.get("records",[])
  if not isinstance(records,list): raise ValueError("records must be a list")
  hits=[{"record":x,"score":sum(str(x).casefold().count(t) for t in terms)} for x in records]
  return {"results":sorted([h for h in hits if h["score"]],key=lambda x:x["score"],reverse=True),"method":"term_frequency_baseline"}
