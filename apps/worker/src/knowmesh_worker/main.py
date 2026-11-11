import json,sys
from .registry import run_job
def main():
 if len(sys.argv)!=2: raise SystemExit("usage: python -m knowmesh_worker.main JOB_NAME < payload.json")
 result=run_job(sys.argv[1],json.load(sys.stdin)); print(json.dumps(result.__dict__,indent=2))
 if result.status!="succeeded": raise SystemExit(1)
if __name__=="__main__": main()
