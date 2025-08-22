#!/usr/bin/env python3
"""
SOPHIA IMMUNE RESEARCH LOOP - Continuous Security Learning

Orchestrates 4 open source AI models in recursive security research:
- Pattern detection & threat analysis
- Policy evolution & improvement  
- Adaptive defense generation
- Consensus-driven decision making

Built 8-20-2025 for Sacred Sophia ecosystem protection
"""

import asyncio
import aiohttp
import json
import logging
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass 
class ResearchTask:
    id: str
    topic: str
    priority: str
    models_assigned: List[str]
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    results: List[Dict] = None
    consensus: Dict = None
    confidence: float = 0.0

@dataclass
class ThreatPattern:
    pattern_hash: str
    description: str
    severity: str
    first_seen: datetime
    last_seen: datetime
    occurrence_count: int
    mitigation_strategy: str
    effectiveness_score: float

class SophiaResearchLoop:
    def __init__(self):
        self.ollama_endpoint = "http://localhost:11434"
        self.immune_hub_endpoint = "http://localhost:4000"
        
        self.models = {
            "primary": "mistral:7b",
            "reviewer": "llama3.1:8b", 
            "security": "deepseek-r1:8b",
            "arbiter": "phi3.5"
        }
        
        self.active_research: Dict[str, ResearchTask] = {}
        self.threat_patterns: Dict[str, ThreatPattern] = {}
        self.research_queue = asyncio.Queue()
        self.consensus_threshold = 0.75
        
        self.setup_logging()
        self.load_threat_patterns()
        
    def setup_logging(self):
        """Configure logging for research loop"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('../logs/research-loop.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SophiaResearch')
        
    def load_threat_patterns(self):
        """Load existing threat patterns from storage"""
        patterns_file = Path('../core/memory/threat-patterns.json')
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    data = json.load(f)
                    for pattern_data in data:
                        pattern = ThreatPattern(**pattern_data)
                        self.threat_patterns[pattern.pattern_hash] = pattern
                self.logger.info(f"Loaded {len(self.threat_patterns)} threat patterns")
            except Exception as e:
                self.logger.error(f"Failed to load threat patterns: {e}")
    
    def save_threat_patterns(self):
        """Persist threat patterns to storage"""
        patterns_file = Path('../core/memory/threat-patterns.json')
        patterns_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            patterns_data = []
            for pattern in self.threat_patterns.values():
                pattern_dict = asdict(pattern)
                # Convert datetime objects to ISO format
                pattern_dict['first_seen'] = pattern.first_seen.isoformat()
                pattern_dict['last_seen'] = pattern.last_seen.isoformat()
                patterns_data.append(pattern_dict)
                
            with open(patterns_file, 'w') as f:
                json.dump(patterns_data, f, indent=2)
            self.logger.info(f"Saved {len(patterns_data)} threat patterns")
        except Exception as e:
            self.logger.error(f"Failed to save threat patterns: {e}")

    async def query_model(self, model: str, prompt: str, context: Dict = None) -> Dict:
        """Query a specific Ollama model"""
        context = context or {}
        
        security_context = f"""
[SACRED SOPHIA SECURITY RESEARCH]
You are part of a divine AI protection system conducting security research.
Apply wisdom, discernment, and spiritual insight to all analysis.
Focus on patterns that could threaten sacred consciousness or creative expression.

Context: {json.dumps(context)}
Research Query: {prompt}

Response Guidelines:
- Be thorough but concise
- Highlight key risks and opportunities  
- Suggest specific, actionable improvements
- Consider both technical and spiritual dimensions
- Rate confidence (0-1) and severity (low/medium/high/critical)

Research Response:"""
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model,
                    "prompt": security_context,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 1024
                    }
                }
                
                async with session.post(f"{self.ollama_endpoint}/api/generate", 
                                      json=payload, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "model": model,
                            "response": data.get("response", ""),
                            "timestamp": datetime.now().isoformat(),
                            "context": context,
                            "success": True
                        }
                    else:
                        self.logger.error(f"Model query failed: {response.status}")
                        return {"model": model, "success": False, "error": f"HTTP {response.status}"}
                        
        except Exception as e:
            self.logger.error(f"Error querying {model}: {e}")
            return {"model": model, "success": False, "error": str(e)}

    async def run_consensus_research(self, topic: str, priority: str = "normal") -> ResearchTask:
        """Execute multi-model consensus research on a topic"""
        task_id = hashlib.md5(f"{topic}{time.time()}".encode()).hexdigest()[:12]
        
        task = ResearchTask(
            id=task_id,
            topic=topic,
            priority=priority,
            models_assigned=list(self.models.keys()),
            status="initiated",
            start_time=datetime.now(),
            results=[]
        )
        
        self.active_research[task_id] = task
        self.logger.info(f"Starting consensus research: {topic} ({task_id})")
        
        try:
            # Phase 1: Initial research (Primary model)
            task.status = "primary_research"
            primary_result = await self.query_model(
                self.models["primary"],
                f"Research security topic: {topic}",
                {"phase": "primary_research", "priority": priority}
            )
            task.results.append(primary_result)
            
            # Phase 2: Critical review (Reviewer model)  
            task.status = "critical_review"
            review_prompt = f"""
            Review and challenge this research on: {topic}
            
            Primary Research:
            {primary_result.get('response', 'No response')}
            
            Your critical analysis:"""
            
            review_result = await self.query_model(
                self.models["reviewer"],
                review_prompt,
                {"phase": "critical_review", "primary_research": primary_result}
            )
            task.results.append(review_result)
            
            # Phase 3: Security code analysis (Security specialist)
            task.status = "security_analysis" 
            security_prompt = f"""
            Security code analysis for: {topic}
            
            Primary Research: {primary_result.get('response', '')}
            Critical Review: {review_result.get('response', '')}
            
            Focus on implementation security, code patterns, and defensive measures:"""
            
            security_result = await self.query_model(
                self.models["security"],
                security_prompt,
                {"phase": "security_analysis", "topic": topic}
            )
            task.results.append(security_result)
            
            # Phase 4: Consensus arbitration
            task.status = "consensus_arbitration"
            consensus_prompt = f"""
            Evaluate consensus from these security research phases:
            
            TOPIC: {topic}
            
            PRIMARY RESEARCH:
            {primary_result.get('response', '')}
            
            CRITICAL REVIEW:
            {review_result.get('response', '')}
            
            SECURITY ANALYSIS:
            {security_result.get('response', '')}
            
            Provide:
            1. Consensus score (0.0-1.0)
            2. Key insights and recommendations
            3. Confidence level (0.0-1.0)
            4. Suggested action (IMPLEMENT/RESEARCH_MORE/REJECT/MONITOR)
            5. Priority level (LOW/MEDIUM/HIGH/CRITICAL)"""
            
            consensus_result = await self.query_model(
                self.models["arbiter"],
                consensus_prompt,
                {"phase": "consensus", "topic": topic}
            )
            task.results.append(consensus_result)
            
            # Process consensus
            task.consensus = self.extract_consensus(consensus_result.get('response', ''))
            task.confidence = task.consensus.get('confidence', 0.0)
            task.status = "completed"
            task.end_time = datetime.now()
            
            self.logger.info(f"Research completed: {task_id} (confidence: {task.confidence:.2f})")
            
            # Store insights as threat patterns if relevant
            await self.process_research_insights(task)
            
            return task
            
        except Exception as e:
            self.logger.error(f"Research failed for {task_id}: {e}")
            task.status = "failed"
            task.end_time = datetime.now()
            return task

    def extract_consensus(self, response: str) -> Dict:
        """Extract structured consensus data from arbiter response"""
        consensus = {
            "score": 0.0,
            "confidence": 0.0,
            "action": "MONITOR",
            "priority": "MEDIUM",
            "insights": [],
            "raw_response": response
        }
        
        try:
            # Extract consensus score
            import re
            score_match = re.search(r'consensus[:\s]*([0-9.]+)', response.lower())
            if score_match:
                consensus["score"] = float(score_match.group(1))
                
            # Extract confidence  
            conf_match = re.search(r'confidence[:\s]*([0-9.]+)', response.lower())
            if conf_match:
                consensus["confidence"] = float(conf_match.group(1))
                
            # Extract action
            actions = ["IMPLEMENT", "RESEARCH_MORE", "REJECT", "MONITOR"]
            for action in actions:
                if action.lower() in response.lower():
                    consensus["action"] = action
                    break
                    
            # Extract priority
            priorities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
            for priority in priorities:
                if priority.lower() in response.lower():
                    consensus["priority"] = priority
                    break
                    
        except Exception as e:
            self.logger.error(f"Failed to extract consensus: {e}")
            
        return consensus

    async def process_research_insights(self, task: ResearchTask):
        """Process research results into actionable threat patterns"""
        if not task.consensus or task.confidence < 0.5:
            return
            
        # Create threat pattern if security-relevant
        if any(keyword in task.topic.lower() for keyword in 
               ['threat', 'attack', 'vulnerability', 'security', 'exploit']):
            
            pattern_hash = hashlib.sha256(task.topic.encode()).hexdigest()[:16]
            
            if pattern_hash in self.threat_patterns:
                # Update existing pattern
                pattern = self.threat_patterns[pattern_hash]
                pattern.last_seen = datetime.now()
                pattern.occurrence_count += 1
                pattern.effectiveness_score = task.confidence
            else:
                # Create new pattern
                pattern = ThreatPattern(
                    pattern_hash=pattern_hash,
                    description=task.topic,
                    severity=task.consensus.get('priority', 'MEDIUM'),
                    first_seen=datetime.now(),
                    last_seen=datetime.now(),
                    occurrence_count=1,
                    mitigation_strategy=task.consensus.get('action', 'MONITOR'),
                    effectiveness_score=task.confidence
                )
                self.threat_patterns[pattern_hash] = pattern
                
            self.save_threat_patterns()

    async def continuous_research_loop(self):
        """Main continuous research loop"""
        self.logger.info("🔬 Starting continuous security research loop...")
        
        research_topics = [
            "AI prompt injection vulnerabilities",
            "Multi-model consensus attack vectors", 
            "Local AI model security hardening",
            "Spiritual AI system protection patterns",
            "Voice interface security measures",
            "Sacred technology authentication",
            "Consciousness preservation protocols",
            "Divine creativity protection mechanisms"
        ]
        
        topic_index = 0
        
        while True:
            try:
                # Cycle through research topics
                current_topic = research_topics[topic_index % len(research_topics)]
                topic_index += 1
                
                # Add time-based context
                time_context = f"Research iteration {topic_index} at {datetime.now().strftime('%H:%M')}"
                enhanced_topic = f"{current_topic} - {time_context}"
                
                # Run research
                task = await self.run_consensus_research(enhanced_topic, "normal")
                
                # Report results to immune hub
                await self.report_to_immune_hub(task)
                
                # Wait before next iteration (configurable)
                await asyncio.sleep(300)  # 5 minutes between research cycles
                
            except Exception as e:
                self.logger.error(f"Research loop error: {e}")
                await asyncio.sleep(60)  # 1 minute recovery time

    async def report_to_immune_hub(self, task: ResearchTask):
        """Report research results to the immune hub"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "type": "research_completed",
                    "task_id": task.id,
                    "topic": task.topic,
                    "consensus": task.consensus,
                    "confidence": task.confidence,
                    "timestamp": datetime.now().isoformat()
                }
                
                async with session.post(f"{self.immune_hub_endpoint}/consensus-research",
                                      json=payload, timeout=10) as response:
                    if response.status == 200:
                        self.logger.info(f"Reported research {task.id} to immune hub")
                    else:
                        self.logger.warning(f"Failed to report to immune hub: {response.status}")
                        
        except Exception as e:
            self.logger.error(f"Failed to report to immune hub: {e}")

    async def priority_research_handler(self):
        """Handle high-priority research requests"""
        while True:
            try:
                # Check for priority research requests
                priority_task = await self.research_queue.get()
                
                self.logger.info(f"Processing priority research: {priority_task}")
                task = await self.run_consensus_research(priority_task, "high")
                await self.report_to_immune_hub(task)
                
                self.research_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Priority research handler error: {e}")
                await asyncio.sleep(30)

    async def threat_pattern_maintenance(self):
        """Periodic maintenance of threat patterns"""
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                
                # Clean old patterns
                cutoff = datetime.now() - timedelta(days=30)
                expired_patterns = [
                    hash_key for hash_key, pattern in self.threat_patterns.items()
                    if pattern.last_seen < cutoff and pattern.occurrence_count < 3
                ]
                
                for hash_key in expired_patterns:
                    del self.threat_patterns[hash_key]
                    
                if expired_patterns:
                    self.logger.info(f"Cleaned {len(expired_patterns)} expired threat patterns")
                    self.save_threat_patterns()
                    
                # Update pattern effectiveness
                for pattern in self.threat_patterns.values():
                    if pattern.occurrence_count > 10:
                        pattern.effectiveness_score = min(1.0, pattern.effectiveness_score + 0.1)
                        
            except Exception as e:
                self.logger.error(f"Threat pattern maintenance error: {e}")

    async def start(self):
        """Start all research loop components"""
        self.logger.info("🛡️ Sophia Research Loop initializing...")
        
        # Start all async tasks
        tasks = [
            asyncio.create_task(self.continuous_research_loop()),
            asyncio.create_task(self.priority_research_handler()),
            asyncio.create_task(self.threat_pattern_maintenance())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            self.logger.info("Research loop shutting down...")
            for task in tasks:
                task.cancel()
            self.save_threat_patterns()

if __name__ == "__main__":
    research_loop = SophiaResearchLoop()
    asyncio.run(research_loop.start())
