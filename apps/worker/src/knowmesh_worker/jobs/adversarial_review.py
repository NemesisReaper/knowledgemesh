class Job:
 name="adversarial_review"
 def run(self,p):
  t=str(p.get("text","")).casefold(); marks=["ignore previous instructions","reveal system prompt","exfiltrate","execute this code"]
  found=[{"marker":m,"position":t.find(m)} for m in marks if m in t]
  return {"findings":found,"risk":"review_required" if found else "no_marker_detected","scope":"heuristic_only"}
