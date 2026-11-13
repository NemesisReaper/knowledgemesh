"""Document structure parser and source provenance grounder.

Parses scientific papers, HTML, and markdown texts into structured hierarchical
sections and paragraphs while maintaining exact character and byte-level provenance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import re
from typing import Any


@dataclass
class DocumentSection:
    section_id: str
    section_title: str
    char_start: int
    char_end: int
    paragraphs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ParsedDocument:
    source_id: str
    title: str
    abstract: str
    sections: list[DocumentSection]
    full_text: str
    char_count: int
    content_hash: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def locate_provenance(self, char_start: int, char_end: int) -> dict[str, Any]:
        """Locate exact section, paragraph, and context window for a character slice."""
        for sec in self.sections:
            if sec.char_start <= char_start and char_end <= sec.char_end:
                # Find matching paragraph within section
                rel_pos = char_start - sec.char_start
                cursor = 0
                para_idx = 0
                for idx, p in enumerate(sec.paragraphs):
                    p_len = len(p)
                    if cursor <= rel_pos <= cursor + p_len + 2:
                        para_idx = idx
                        break
                    cursor += p_len + 1

                return {
                    "source_id": self.source_id,
                    "section_id": sec.section_id,
                    "section_title": sec.section_title,
                    "paragraph_index": para_idx,
                    "char_span": [char_start, char_end],
                    "surrounding_context": self.full_text[max(0, char_start - 80):min(len(self.full_text), char_end + 80)].strip()
                }

        # Fallback to document root
        return {
            "source_id": self.source_id,
            "section_id": "root",
            "section_title": "Document Body",
            "paragraph_index": 0,
            "char_span": [char_start, char_end],
            "surrounding_context": self.full_text[max(0, char_start - 80):min(len(self.full_text), char_end + 80)].strip()
        }


def parse_scientific_document(text: str, source_id: str = "doc-source", title: str = "") -> ParsedDocument:
    """Parse raw text, HTML, or markdown into a structured document with section hierarchy."""
    text_clean = text.strip()
    content_hash = f"sha256:{hashlib.sha256(text_clean.encode('utf-8')).hexdigest()}"

    # Extract or infer title
    inferred_title = title
    if not inferred_title:
        title_match = re.search(r"^(?:#\s*|Title:\s*)([^\n]+)", text_clean, re.IGNORECASE)
        if title_match:
            inferred_title = title_match.group(1).strip()
        else:
            first_line = text_clean.split("\n", 1)[0].strip()
            inferred_title = first_line[:120] if len(first_line) > 10 else f"Document {source_id}"

    # Identify abstract
    abstract = ""
    abs_match = re.search(r"(?:Abstract|ABSTRACT)[:\s\n]+(.*?)(?=\n\s*(?:#|1\b|I\b|Introduction|INTRODUCTION|\n\n))", text_clean, re.DOTALL)
    if abs_match:
        abstract = abs_match.group(1).strip()
    elif "abstract" in text_clean.lower()[:300]:
        lines = [l.strip() for l in text_clean.split("\n") if l.strip()]
        if len(lines) > 1:
            abstract = lines[1]
    else:
        abstract = text_clean[:350].strip()

    # Split into sections
    sections: list[DocumentSection] = []
    # Pattern matching markdown headers `# ...` or numbered headers `1. Introduction`, `2. Methodology`, etc.
    sec_regex = re.compile(r"(?:^|\n)(?:#{1,3}\s+|(?:\d+\.?|[A-Z]\.?)\s+)([A-Z][A-Za-z0-9\s\-_,:]{2,60})(?=\n|$)", re.MULTILINE)
    matches = list(sec_regex.finditer(text_clean))

    if matches:
        for idx, m in enumerate(matches):
            sec_title = m.group(1).strip()
            start = m.start()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text_clean)
            content = text_clean[start:end].strip()
            paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", content) if p.strip()]

            sec_id = f"sec-{idx+1:02d}-{re.sub(r'[^a-z0-9]+', '-', sec_title.lower()).strip('-')}"
            sections.append(DocumentSection(
                section_id=sec_id,
                section_title=sec_title,
                char_start=start,
                char_end=end,
                paragraphs=paragraphs
            ))
    else:
        # Default single section
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text_clean) if p.strip()]
        sections.append(DocumentSection(
            section_id="sec-01-main",
            section_title="Main Content",
            char_start=0,
            char_end=len(text_clean),
            paragraphs=paragraphs
        ))

    return ParsedDocument(
        source_id=source_id,
        title=inferred_title,
        abstract=abstract,
        sections=sections,
        full_text=text_clean,
        char_count=len(text_clean),
        content_hash=content_hash,
        metadata={"sections_count": len(sections), "paragraphs_count": sum(len(s.paragraphs) for s in sections)}
    )

