"""Versioned identity, mutation, lineage, split and merge primitives for KnowMesh."""
from .identity import KnowledgeIdentity, identity_fingerprint
from .mutations import Mutation, MutationKind, MutationResult, apply_mutation
from .splits import SplitResult, split_knowledge
from .merges import MergeResult, MergeConflict, merge_knowledge
from .lineage import LineageGraph, LineageEvent, LineageRelation
from .history import KnowledgeHistory, HistoryEntry
__all__ = [
    "KnowledgeIdentity", "identity_fingerprint", "Mutation", "MutationKind",
    "MutationResult", "apply_mutation", "SplitResult", "split_knowledge",
    "MergeResult", "MergeConflict", "merge_knowledge", "LineageGraph",
    "LineageEvent", "LineageRelation", "KnowledgeHistory", "HistoryEntry",
]
