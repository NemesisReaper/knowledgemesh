from dataclasses import dataclass
from itertools import combinations
from collections.abc import Iterable
from .claims import Claim

@dataclass(frozen=True)
class Contradiction:
    left_claim_id: str
    right_claim_id: str
    reason: str
    subject: str = ""
    predicate: str = ""

def detect_contradictions(claims: Iterable[Claim]) -> list[Contradiction]:
    """Detect explicit object-value conflicts in normalized subject/predicate triples.

    This deliberately avoids broad natural-language contradiction guessing.
    """
    groups = {}
    for c in claims:
        if c.subject.strip() and c.predicate.strip() and c.object.strip():
            key = (c.subject.casefold().strip(), c.predicate.casefold().strip())
            groups.setdefault(key, []).append(c)
    found = []
    for (subject,predicate), items in groups.items():
        for a,b in combinations(items,2):
            if a.object.casefold().strip() != b.object.casefold().strip():
                found.append(Contradiction(a.claim_id,b.claim_id,
                    f"Conflicting object values: {a.object!r} vs {b.object!r}",subject,predicate))
    return found
