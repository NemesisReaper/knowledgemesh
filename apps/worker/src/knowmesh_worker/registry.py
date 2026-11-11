from .jobs.base import execute
from .jobs.impact_propagation import Job as Impact
from .jobs.decay_prediction import Job as Decay
from .jobs.reputation import Job as Reputation
from .jobs.discovery import Job as Discovery
from .jobs.adversarial_review import Job as Adversarial
from .jobs.knowledge_evolution import Job as Evolution
from .jobs.claim_extraction import Job as Claims
JOBS={j.name:j for j in (Impact(),Decay(),Reputation(),Discovery(),Adversarial(),Evolution(),Claims())}
def run_job(name,payload):
 if name not in JOBS: raise KeyError(f"unknown job: {name}")
 return execute(JOBS[name],payload)
