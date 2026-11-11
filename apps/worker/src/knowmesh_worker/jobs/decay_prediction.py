class Job:
 name="decay_prediction"
 def run(self,p):
  import math
  half=float(p.get("half_life_days",30)); age=float(p.get("age_days",0))
  if half<=0 or age<0: raise ValueError("positive half_life_days and non-negative age_days required")
  return {"freshness_score":0.5**(age/half),"age_days":age,"half_life_days":half,"interpretation":"heuristic_not_truth"}
