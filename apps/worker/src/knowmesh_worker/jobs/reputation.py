class Job:
 name="reputation"
 def run(self,p):
  a=int(p.get("accepted",0)); r=int(p.get("rejected",0))
  if min(a,r)<0: raise ValueError("counts must be non-negative")
  n=a+r
  return {"accepted":a,"rejected":r,"observations":n,"score":a/n if n else None,"sample_size_warning":n<10}
