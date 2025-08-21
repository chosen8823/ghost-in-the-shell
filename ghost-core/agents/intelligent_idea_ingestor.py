#!/usr/bin/env python3
"""Minimal, clean Intelligent Idea Ingestor for the repo.

This module provides a small, self-contained ingestor suitable for CI and
headless environments. It uses a lightweight in-memory memory-arm fallback
when a project-provided memory implementation is not available.
"""
from __future__ import annotations

import asyncio
import json
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import sys


# ensure repo root on sys.path for local imports
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


class IdeaAnalysis:
    def __init__(
        self,
        key_concepts: List[str],
        novelty_score: float,
        confidence_score: float,
        genuineness_score: float,
        complexity_level: int,
        related_concepts: List[str],
        source_credibility: float,
        extraction_method: str,
    ) -> None:
        self.key_concepts = key_concepts
        self.novelty_score = novelty_score
        self.confidence_score = confidence_score
        self.genuineness_score = genuineness_score
        self.complexity_level = complexity_level
        self.related_concepts = related_concepts
        self.source_credibility = source_credibility
        self.extraction_method = extraction_method


class CrossReference:
    def __init__(
        self,
        memory_id: str,
        similarity_score: float,
        matching_concepts: List[str],
        contradiction_flag: bool,
        supporting_evidence: bool,
    ) -> None:
        self.memory_id = memory_id
        self.similarity_score = similarity_score
        self.matching_concepts = matching_concepts
        self.contradiction_flag = contradiction_flag
        self.supporting_evidence = supporting_evidence


class _InMemoryMemoryArm:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    async def search_memory(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        q = (query or '').lower()
        results = []
        for mid, item in self._store.items():
            text = json.dumps(item.get('content', '')) if isinstance(item.get('content', ''), (dict, list)) else str(item.get('content', ''))
            if q and q in text.lower():
                results.append({'id': mid, 'content': item, 'score': 1.0})
        return {'success': True, 'results': results}

    async def store_memory(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        raw = json.dumps(data, sort_keys=True, default=str).encode('utf-8')
        mid = hashlib.sha1(raw).hexdigest()[:12]
        self._store[mid] = data
        return {'success': True, 'memory_id': mid}


try:
    from agents.memory_arm import memory_arm  # type: ignore
except Exception:
    try:
        from agents.memory_arm_simple import memory_arm as memory_arm_simple  # type: ignore
        memory_arm = memory_arm_simple
    except Exception:
        memory_arm = _InMemoryMemoryArm()


class IntelligentIdeaIngestor:
    def __init__(self) -> None:
        self.memory_arm = memory_arm
        self.known_concepts_cache: set[str] = {'physics', 'chemistry', 'biology', 'mathematics', 'psychology', 'philosophy'}

    def _extract_ideas(self, content: str) -> List[str]:
        sentences = re.split(r'[\n\.]', content or '')
        candidates = [s.strip() for s in sentences if 40 < len(s.strip()) < 400]
        out: List[str] = []
        seen = set()
        for s in candidates:
            if s and s not in seen:
                seen.add(s)
                out.append(s)
            if len(out) >= 20:
                break
        return out

    async def _analyze_idea(self, idea: str, source: str) -> IdeaAnalysis:
        words = re.findall(r"\b[a-zA-Z]{3,}\b", (idea or '').lower())
        key_concepts = list(dict.fromkeys(words))[:10]
        novelty = sum(1 for k in key_concepts if k not in self.known_concepts_cache) / max(1, len(key_concepts))
        credibility = 0.5
        if source and any(d in source for d in ['.edu', '.gov', '.org']):
            credibility = min(1.0, credibility + 0.2)
        return IdeaAnalysis(
            key_concepts=key_concepts,
            novelty_score=float(novelty),
            confidence_score=0.5,
            genuineness_score=float(credibility),
            complexity_level=max(1, len(idea.split()) // 8),
            related_concepts=[],
            source_credibility=float(credibility),
            extraction_method='simple'
        )

    def _jaccard_similarity(self, a: str, b: str) -> float:
        sa = set(re.findall(r"\w+", (a or '').lower()))
        sb = set(re.findall(r"\w+", (b or '').lower()))
        if not sa or not sb:
            return 0.0
        return len(sa & sb) / len(sa | sb)

    async def _cross_reference_idea(self, idea: str, analysis: IdeaAnalysis) -> List[CrossReference]:
        refs: List[CrossReference] = []
        for concept in (analysis.key_concepts or [])[:5]:
            res = await self.memory_arm.search_memory(concept, {})
            if res.get('success'):
                for r in res.get('results', []):
                    text = str(r.get('content', ''))
                    sim = self._jaccard_similarity(idea, text)
                    refs.append(CrossReference(memory_id=r.get('id', ''), similarity_score=sim, matching_concepts=[concept], contradiction_flag=False, supporting_evidence=sim > 0.5))
        return refs

    def _should_store_idea(self, analysis: IdeaAnalysis, refs: List[CrossReference]) -> bool:
        if analysis.genuineness_score < 0.2:
            return False
        if analysis.novelty_score <= 0 and analysis.confidence_score < 0.6:
            return False
        return True

    async def _store_idea(self, idea: str, analysis: IdeaAnalysis, source: str, context: Dict[str, Any], refs: List[CrossReference]) -> Optional[str]:
        data = {
            'type': 'semantic',
            'content': idea,
            'key_concepts': analysis.key_concepts,
            'source': source,
            'analysis': analysis.__dict__,
            'cross_references': [r.__dict__ for r in refs],
            'ingestion_timestamp': datetime.now().isoformat(),
            'context': context,
        }
        res = await self.memory_arm.store_memory(data, context or {})
        if res.get('success'):
            return res.get('memory_id')
        return None

    async def ingest_content(self, content: str, source: str = 'unknown', context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if context is None:
            context = {}
        extracted = self._extract_ideas(content)
        stored: List[Dict[str, Any]] = []
        analyzed_count = 0
        for idea in extracted:
            analyzed_count += 1
            analysis = await self._analyze_idea(idea, source)
            refs = await self._cross_reference_idea(idea, analysis)
            if self._should_store_idea(analysis, refs):
                mid = await self._store_idea(idea, analysis, source, context, refs)
                if mid:
                    stored.append({'idea': idea, 'memory_id': mid, 'analysis': analysis.__dict__})

        return {
            'success': True,
            'source': source,
            'total_extracted': len(extracted),
            'analyzed': analyzed_count,
            'stored': len(stored),
            'stored_ideas': stored,
            'timestamp': datetime.now().isoformat(),
        }


idea_ingestor = IntelligentIdeaIngestor()


async def ingest_text_file(file_path: str, source_override: Optional[str] = None) -> Dict[str, Any]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        source = source_override or file_path
        return await idea_ingestor.ingest_content(content, source, {'file_path': file_path})
    except Exception as e:
        return {'success': False, 'error': str(e)}


async def ingest_url_content(url: str, content: str) -> Dict[str, Any]:
    return await idea_ingestor.ingest_content(content, url, {'url': url})


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Idea Ingestor CLI')
    parser.add_argument('--file', '-f')
    parser.add_argument('--content', '-c')
    parser.add_argument('--source', '-s')
    args = parser.parse_args()
    if args.content:
        asyncio.run(idea_ingestor.ingest_content(args.content, args.source or 'cli', {'test_mode': True}))
    elif args.file:
        asyncio.run(ingest_text_file(args.file, args.source))
