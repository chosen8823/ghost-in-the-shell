#!/usr/bin/env python3
"""
Simple ingestion helper to store large text/article content into Sophia's memory as a semantic memory.
"""
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Ensure repository root is on sys.path so `from agents.memory_arm import memory_arm` works
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from agents.memory_arm import memory_arm

ARTICLE = {
    "title": "Constructor Theory Application to Social Physics",
    "author": "Jakub Bareš",
    "source": "Intelligence Strategy Research Institute",
    "date": "2024-05-22",
    "type": "semantic",
    "tags": ["constructor theory", "social physics", "belief systems", "economics"],
    "content": (
        "Chapter 1: The Foundations of Constructor Theory\n"
        "Introduction to Traditional Physical Theories\n"
        "For centuries, the pursuit of understanding the universe has driven the development of various physical theories. "
        "Classical mechanics, formulated by Isaac Newton in the 17th century, laid the foundation by describing the motion of macroscopic objects. "
        "This theory provided precise predictions about the behavior of objects under the influence of forces, revolutionizing science and engineering. "
        "However, as scientists probed deeper into the fabric of reality, they encountered phenomena that classical mechanics couldn't explain.\n\n"
        "At the dawn of the 20th century, quantum mechanics emerged to address the behavior of particles at the atomic and subatomic levels. "
        "This theory introduced the concept of wave-particle duality and the probabilistic nature of particle properties. Simultaneously, Albert Einstein's theory of relativity redefined our understanding of space, time, and gravity, explaining phenomena such as the bending of light around massive objects and the expansion of the universe.\n\n"
        "Despite their successes, these traditional physical theories have limitations. They describe the universe in terms of what happens rather than what is possible or impossible. "
        "They struggle to unify under a single framework, leading to the search for a more fundamental theory that can encompass all physical phenomena.\n\n"
        "Genesis of Constructor Theory\n"
        "In this quest for unification, David Deutsch, a pioneer in the field of quantum computation, and Chiara Marletto, a theoretical physicist, proposed Constructor Theory. "
        "This revolutionary approach shifts the focus from descriptions of actual events to the principles governing what transformations are possible.\n\n"
        "(content truncated)"
    ),
}


async def ingest_article(article: dict):
    payload = {
        "id": f"ingest_{datetime.now().isoformat()}",
        "role": "ingest",
        "type": "memory_request",
        "payload": {
            "type": "store",
            "data": {
                "title": article.get("title"),
                "author": article.get("author"),
                "source": article.get("source"),
                "date": article.get("date"),
                "type": article.get("type", "semantic"),
                "tags": article.get("tags", []),
                "content": article.get("content")[:10000],  # truncate to 10k chars
                "importance": 0.8,
                "topic": article.get("title")
            },
            "context": {"source": "memory_ingest.py"}
        },
        "ts": datetime.now().isoformat()
    }

    res = await memory_arm.handle_memory_message(payload)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    asyncio.run(ingest_article(ARTICLE))
