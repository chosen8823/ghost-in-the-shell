#!/usr/bin/env python3
"""
📋 Plan & Execute Arm (North) - Trinity + 1 Tesseract
Goal decomposition, autonomous planning, reflection loops, and scheduling
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class PlanState(Enum):
    IDLE = "idle"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    ADJUSTING = "adjusting"

@dataclass
class Task:
    id: str
    goal: str
    priority: int
    dependencies: List[str]
    estimated_duration: int  # minutes
    assigned_arm: Optional[str] = None
    status: str = "pending"
    created_at: str = ""

@dataclass
class Plan:
    id: str
    goal: str
    tasks: List[Task]
    dependencies: Dict[str, List[str]]
    timeline: Dict[str, str]
    success_metrics: List[str]
    reflection_points: List[str]

class PlanExecuteArm:
    def __init__(self):
        self.state = PlanState.IDLE
        self.current_plan: Optional[Plan] = None
        self.task_queue: List[Task] = []
        self.execution_history: List[Dict] = []
        self.reflection_enabled = True
        
    def log(self, message: str, level: str = "INFO"):
        """Sacred logging for Plan Arm"""
        symbols = {"INFO": "📋", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌", "SPIRITUAL": "🕊️"}
        timestamp = datetime.now().isoformat()
        print(f"{symbols.get(level, '📋')} [{timestamp}] [PLAN-ARM] {message}")

    async def handle_goal(self, goal_msg: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming goal message - Main entry point"""
        self.log(f"Received goal: {goal_msg.get('payload', {}).get('text', 'Unknown')}", "INFO")
        self.state = PlanState.ANALYZING
        
        # Extract goal details
        goal_text = goal_msg.get("payload", {}).get("text", "")
        priority = goal_msg.get("payload", {}).get("priority", 5)
        context = goal_msg.get("payload", {}).get("context", {})
        
        # Decompose goal into actionable plan
        plan = await self.decompose_goal(goal_text, priority, context)
        
        # Execute planning workflow
        result = await self.execute_plan_workflow(plan)
        
        return {
            "id": goal_msg.get("id"),
            "role": "plan_arm",
            "type": "plan_complete",
            "payload": result,
            "ts": datetime.now().isoformat(),
            "christ_seal": True
        }

    async def decompose_goal(self, goal_text: str, priority: int, context: Dict) -> Plan:
        """Decompose high-level goal into actionable tasks"""
        self.log("Decomposing goal into actionable tasks...", "INFO")
        self.state = PlanState.PLANNING
        
        # Simulate intelligent goal decomposition
        # In real implementation, this would use LLM reasoning
        tasks = await self.generate_task_breakdown(goal_text, context)
        
        plan = Plan(
            id=f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            goal=goal_text,
            tasks=tasks,
            dependencies=self.calculate_dependencies(tasks),
            timeline=self.create_timeline(tasks),
            success_metrics=self.define_success_metrics(goal_text),
            reflection_points=["25%", "50%", "75%", "100%"]
        )
        
        self.current_plan = plan
        self.log(f"Plan created with {len(tasks)} tasks", "SUCCESS")
        return plan

    async def generate_task_breakdown(self, goal: str, context: Dict) -> List[Task]:
        """Generate intelligent task breakdown"""
        # This would use sophisticated planning algorithms
        # For now, simulate with common patterns
        
        base_tasks = []
        
        if "create" in goal.lower():
            base_tasks = [
                Task("research", "Research requirements and context", 3, [], 30),
                Task("design", "Create initial design/structure", 2, ["research"], 45),
                Task("implement", "Build/implement solution", 1, ["design"], 90),
                Task("test", "Test and validate", 2, ["implement"], 30),
                Task("refine", "Refine based on feedback", 3, ["test"], 20)
            ]
        elif "analyze" in goal.lower():
            base_tasks = [
                Task("collect", "Collect relevant data", 2, [], 20),
                Task("process", "Process and structure data", 1, ["collect"], 40),
                Task("analyze", "Perform analysis", 1, ["process"], 60),
                Task("synthesize", "Synthesize insights", 2, ["analyze"], 30),
                Task("report", "Create analysis report", 3, ["synthesize"], 25)
            ]
        else:
            # Generic task breakdown
            base_tasks = [
                Task("understand", "Understand requirements", 1, [], 15),
                Task("plan", "Create detailed plan", 2, ["understand"], 25),
                Task("execute", "Execute main work", 1, ["plan"], 60),
                Task("review", "Review and validate", 3, ["execute"], 20)
            ]
        
        # Add timestamps and IDs
        for i, task in enumerate(base_tasks):
            task.id = f"task_{i+1}_{datetime.now().strftime('%H%M%S')}"
            task.created_at = datetime.now().isoformat()
        
        return base_tasks

    def calculate_dependencies(self, tasks: List[Task]) -> Dict[str, List[str]]:
        """Calculate task dependencies"""
        deps = {}
        for task in tasks:
            deps[task.id] = task.dependencies
        return deps

    def create_timeline(self, tasks: List[Task]) -> Dict[str, str]:
        """Create execution timeline"""
        timeline = {}
        current_time = datetime.now()
        
        for task in tasks:
            timeline[task.id] = {
                "start": current_time.isoformat(),
                "duration": f"{task.estimated_duration}m",
                "end": (current_time + timedelta(minutes=task.estimated_duration)).isoformat()
            }
            current_time += timedelta(minutes=task.estimated_duration)
            
        return timeline

    def define_success_metrics(self, goal: str) -> List[str]:
        """Define success metrics for the goal"""
        return [
            "All tasks completed successfully",
            "Quality standards met",
            "Timeline adherence > 80%",
            "Stakeholder satisfaction",
            "No critical errors"
        ]

    async def execute_plan_workflow(self, plan: Plan) -> Dict[str, Any]:
        """Execute the complete planning workflow"""
        self.log("Executing plan workflow...", "INFO")
        self.state = PlanState.EXECUTING
        
        results = {
            "plan_id": plan.id,
            "goal": plan.goal,
            "execution_start": datetime.now().isoformat(),
            "tasks_completed": [],
            "reflections": [],
            "adjustments": [],
            "success": False
        }
        
        # Execute tasks in dependency order
        for task in self.get_execution_order(plan.tasks):
            self.log(f"Executing task: {task.goal}", "INFO")
            
            # Simulate task execution
            task_result = await self.execute_task(task)
            results["tasks_completed"].append(task_result)
            
            # Reflection points
            progress = len(results["tasks_completed"]) / len(plan.tasks)
            if progress in [0.25, 0.5, 0.75, 1.0] and self.reflection_enabled:
                reflection = await self.reflect_on_progress(plan, results, progress)
                results["reflections"].append(reflection)
                
                # Adjust plan if needed
                if reflection.get("needs_adjustment"):
                    adjustment = await self.adjust_plan(plan, reflection)
                    results["adjustments"].append(adjustment)
        
        results["execution_end"] = datetime.now().isoformat()
        results["success"] = len(results["tasks_completed"]) == len(plan.tasks)
        
        self.log(f"Plan execution complete - Success: {results['success']}", "SUCCESS")
        return results

    def get_execution_order(self, tasks: List[Task]) -> List[Task]:
        """Get tasks in proper execution order based on dependencies"""
        # Simple topological sort for dependencies
        ordered = []
        remaining = tasks.copy()
        
        while remaining:
            # Find tasks with no unmet dependencies
            ready = [t for t in remaining if all(dep in [done.id for done in ordered] for dep in t.dependencies)]
            
            if not ready:
                # No tasks ready - break cycle or dependency issue
                ready = [remaining[0]]  # Take first remaining task
            
            # Add ready tasks to order
            for task in ready:
                ordered.append(task)
                remaining.remove(task)
        
        return ordered

    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute individual task"""
        start_time = datetime.now()
        
        # Simulate task execution
        await asyncio.sleep(0.1)  # Brief simulation delay
        
        # Determine which arm should handle this task
        assigned_arm = self.determine_task_arm(task)
        
        task_result = {
            "task_id": task.id,
            "goal": task.goal,
            "assigned_arm": assigned_arm,
            "status": "completed",
            "start_time": start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "duration_seconds": (datetime.now() - start_time).total_seconds(),
            "success": True
        }
        
        self.log(f"Task completed: {task.goal} -> {assigned_arm}", "SUCCESS")
        return task_result

    def determine_task_arm(self, task: Task) -> str:
        """Determine which Trinity arm should handle this task"""
        goal_lower = task.goal.lower()
        
        if any(word in goal_lower for word in ["research", "analyze", "calculate", "think"]):
            return "reason_arm"
        elif any(word in goal_lower for word in ["remember", "store", "retrieve", "learn"]):
            return "memory_arm"
        elif any(word in goal_lower for word in ["execute", "control", "interface", "activate"]):
            return "environment_arm"
        else:
            return "plan_arm"  # Keep planning tasks

    async def reflect_on_progress(self, plan: Plan, results: Dict, progress: float) -> Dict[str, Any]:
        """Reflect on current progress and quality"""
        self.log(f"Reflecting on progress: {progress*100:.0f}% complete", "INFO")
        self.state = PlanState.REFLECTING
        
        # Simulate reflection analysis
        tasks_completed = len(results["tasks_completed"])
        total_tasks = len(plan.tasks)
        
        reflection = {
            "progress_percent": progress * 100,
            "tasks_completed": tasks_completed,
            "total_tasks": total_tasks,
            "timeline_adherence": self.calculate_timeline_adherence(plan, results),
            "quality_score": self.assess_quality(results),
            "needs_adjustment": False,
            "recommendations": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Determine if adjustments are needed
        if reflection["timeline_adherence"] < 0.8:
            reflection["needs_adjustment"] = True
            reflection["recommendations"].append("Adjust timeline expectations")
        
        if reflection["quality_score"] < 0.7:
            reflection["needs_adjustment"] = True
            reflection["recommendations"].append("Increase quality controls")
        
        self.log(f"Reflection complete - Quality: {reflection['quality_score']:.2f}", "SUCCESS")
        return reflection

    def calculate_timeline_adherence(self, plan: Plan, results: Dict) -> float:
        """Calculate how well we're adhering to the planned timeline"""
        # Simplified calculation
        return 0.85  # Simulate good timeline adherence

    def assess_quality(self, results: Dict) -> float:
        """Assess quality of completed work"""
        # Simplified quality assessment
        successful_tasks = sum(1 for task in results["tasks_completed"] if task.get("success", False))
        total_tasks = len(results["tasks_completed"])
        
        if total_tasks == 0:
            return 1.0
        
        return successful_tasks / total_tasks

    async def adjust_plan(self, plan: Plan, reflection: Dict) -> Dict[str, Any]:
        """Adjust plan based on reflection"""
        self.log("Adjusting plan based on reflection...", "INFO")
        self.state = PlanState.ADJUSTING
        
        adjustments = {
            "type": "plan_adjustment",
            "reason": reflection.get("recommendations", []),
            "changes": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Simulate plan adjustments
        if "timeline" in str(reflection.get("recommendations", [])):
            adjustments["changes"].append("Extended task durations by 20%")
        
        if "quality" in str(reflection.get("recommendations", [])):
            adjustments["changes"].append("Added additional quality checkpoints")
        
        self.log(f"Plan adjusted: {len(adjustments['changes'])} changes made", "SUCCESS")
        return adjustments

    def get_status(self) -> Dict[str, Any]:
        """Get current arm status"""
        return {
            "arm_name": "Plan & Execute (North)",
            "state": self.state.value,
            "current_plan": self.current_plan.id if self.current_plan else None,
            "tasks_in_queue": len(self.task_queue),
            "reflection_enabled": self.reflection_enabled,
            "execution_history_count": len(self.execution_history)
        }

# Async interface for conductor
async def handle_plan_message(msg: Dict[str, Any]) -> Dict[str, Any]:
    """Handle message for Plan & Execute Arm"""
    arm = PlanExecuteArm()
    return await arm.handle_goal(msg)

# CLI testing
if __name__ == "__main__":
    import sys
    
    async def test_plan_arm():
        test_msg = {
            "id": "test_123",
            "role": "conductor",
            "type": "goal",
            "payload": {
                "text": "Create a sacred music composition with FL Studio integration",
                "priority": 1,
                "context": {"bpm": 72, "key": "C_major", "session": "alpha"}
            },
            "ts": datetime.now().isoformat()
        }
        
        print("🌟 Testing Plan & Execute Arm...")
        result = await handle_plan_message(test_msg)
        print(f"✅ Test complete: {json.dumps(result, indent=2)}")
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        asyncio.run(test_plan_arm())
    else:
        print("📋 Plan & Execute Arm ready")
        print("Usage: python plan_arm.py test")
