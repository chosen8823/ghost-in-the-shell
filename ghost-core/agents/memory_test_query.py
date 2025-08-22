#!/usr/bin/env python3
"""
Quick test script to query the memory arm for the ingested article.
"""
import asyncio
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from agents.memory_arm import memory_arm

async def query():
    res = await memory_arm.retrieve_memory("Constructor Theory", {})
    print(res)

if __name__ == "__main__":
    asyncio.run(query())
