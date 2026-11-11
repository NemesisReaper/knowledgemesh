import re


class Job:
    name = "claim_extraction"

    def run(self, p):
        ss = [
            s.strip()
            for s in re.split(r"(?<=[.!?])\s+", str(p.get("text", "")))
            if s.strip()
        ]
        return {
            "candidate_claims": [
                {"text": s, "status": "proposed", "requires_evidence": True}
                for s in ss
            ],
            "count": len(ss),
            "note": "sentence segmentation only; no semantic verification",
        }
