"""KnowMesh search package: indexing, lexical/semantic/hybrid search and retrieval."""

from .indexing import (
    DocumentRecord, SearchIndex, IndexingError, normalize_document,
    tokenize, build_index,
)
from .ranking import BM25Ranker, SearchHit, rank_bm25
from .semantic import SemanticEncoder, SemanticIndex, cosine_similarity
from .hybrid import HybridSearcher, HybridSearchConfig, reciprocal_rank_fusion
from .retrieval import RetrievalService, RetrievalResult, RetrievalError

__all__ = [
    "DocumentRecord", "SearchIndex", "IndexingError", "normalize_document",
    "tokenize", "build_index", "BM25Ranker", "SearchHit", "rank_bm25",
    "SemanticEncoder", "SemanticIndex", "cosine_similarity",
    "HybridSearcher", "HybridSearchConfig", "reciprocal_rank_fusion",
    "RetrievalService", "RetrievalResult", "RetrievalError",
]
