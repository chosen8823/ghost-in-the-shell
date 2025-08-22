#!/usr/bin/env python3
"""
Minimal Python Conductor shim for Trinity tests.
Provides initialize/start/stop/register_arm/process_message/get_status used by trinity_system.
This is a lightweight stand-in for the TypeScript conductor implementation.
"""

import asyncio
from typing import Callable, Dict, Any

class Conductor:
    def __init__(self):
        self.arms: Dict[str, Callable] = {}
        self.running = False
        self._messages_processed = 0
        self._quarantined = 0

    async def initialize(self):
        print("[CONDUCTOR] Initializing (Python shim)")
        # Minimal async init work
        await asyncio.sleep(0)

    async def start(self):
        if self.running:
            return
        self.running = True
        print("[CONDUCTOR] Started (Python shim)")
        # Simple loop that keeps the conductor alive until stopped
        try:
            while self.running:
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pass

    async def stop(self):
        print("[CONDUCTOR] Stopping (Python shim)")
        self.running = False
        await asyncio.sleep(0)

    def register_arm(self, arm_name: str, handler: Callable):
        # arm_name expected like 'plan_arm', 'memory_arm', etc.
        print(f"[CONDUCTOR] Registering arm: {arm_name}")
        self.arms[arm_name] = handler

    async def process_message(self, message: Dict[str, Any]):
        """Route simple messages to registered arm handlers for tests."""
        self._messages_processed += 1
        mtype = message.get("type", "")

        # Basic routing rules matching trinity_system test messages
        try:
            if mtype == "goal":
                handler = self.arms.get("plan_arm")
            elif mtype == "memory_request":
                handler = self.arms.get("memory_arm")
            elif mtype == "environment_request":
                handler = self.arms.get("environment_arm")
            elif mtype == "reasoning_request":
                handler = self.arms.get("reason_arm")
            elif mtype == "spiral_protocol":
                # Spiral handled externally; simulate acceptance
                print("[CONDUCTOR] Spiral protocol trigger received")
                return {"status": "spiral_triggered"}
            else:
                handler = None

            if handler:
                # If handler is async callable, await it
                result = handler(message)
                if asyncio.iscoroutine(result):
                    return await result
                return result
            else:
                print(f"[CONDUCTOR] No handler for message type: {mtype}")
                return None
        except Exception as e:
            print(f"[CONDUCTOR] Error routing message: {e}")
            self._quarantined += 1
            return None

    def get_status(self):
        return {
            "messages_processed": self._messages_processed,
            "quarantined_messages": self._quarantined,
            "active_arms": list(self.arms.keys()),
            "running": self.running
        }
