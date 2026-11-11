from dataclasses import dataclass,field
from datetime import datetime,timezone
from uuid import uuid4
@dataclass
class JobResult:
    job_id:str
    job_type:str
    status:str
    output:dict=field(default_factory=dict)
    errors:list=field(default_factory=list)
    started_at:str=""
    finished_at:str=""
def execute(job,payload):
    start=datetime.now(timezone.utc).isoformat()
    try: return JobResult(str(uuid4()),job.name,"succeeded",job.run(payload),[],start,datetime.now(timezone.utc).isoformat())
    except Exception as e: return JobResult(str(uuid4()),job.name,"failed",{},[f"{type(e).__name__}: {e}"],start,datetime.now(timezone.utc).isoformat())
