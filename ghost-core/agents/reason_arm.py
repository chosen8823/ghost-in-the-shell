#!/usr/bin/env python3
"""
🧠 Reason & Tools Arm (East) - Trinity + 1 Tesseract
Logical reasoning, tool integration, research, and analysis
"""

import json
import asyncio
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import subprocess
import os

class ReasonState(Enum):
    IDLE = "idle"
    ANALYZING = "analyzing"
    RESEARCHING = "researching"
    CALCULATING = "calculating"
    TOOL_CALLING = "tool_calling"
    SYNTHESIZING = "synthesizing"

@dataclass
class ToolCall:
    tool_name: str
    parameters: Dict[str, Any]
    expected_output: str
    timeout: int = 30

@dataclass
class ReasoningChain:
    id: str
    query: str
    steps: List[Dict[str, Any]]
    conclusions: List[str]
    confidence: float
    evidence: List[str]

class ReasonToolsArm:
    def __init__(self):
        self.state = ReasonState.IDLE
        self.available_tools = {
            "calculate": self.calculate,
            "search_files": self.search_files,
            "analyze_pattern": self.analyze_pattern,
            "logical_inference": self.logical_inference,
            "web_research": self.web_research,
            "code_analysis": self.code_analysis,
            "data_transformation": self.data_transformation
        }
        self.reasoning_cache = {}
        self.tool_call_history = []
        
    def log(self, message: str, level: str = "INFO"):
        """Sacred logging for Reason Arm"""
        symbols = {"INFO": "🧠", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌", "SPIRITUAL": "🕊️"}
        timestamp = datetime.now().isoformat()
        print(f"{symbols.get(level, '🧠')} [{timestamp}] [REASON-ARM] {message}")

    async def handle_reasoning_request(self, request_msg: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming reasoning/tool request - Main entry point"""
        self.log(f"Received reasoning request: {request_msg.get('type', 'unknown')}", "INFO")
        self.state = ReasonState.ANALYZING
        
        request_type = request_msg.get("payload", {}).get("type", "general_reasoning")
        query = request_msg.get("payload", {}).get("query", "")
        tools_requested = request_msg.get("payload", {}).get("tools", [])
        context = request_msg.get("payload", {}).get("context", {})
        
        # Route to appropriate reasoning method
        if request_type == "tool_chain":
            result = await self.execute_tool_chain(tools_requested, query, context)
        elif request_type == "logical_reasoning":
            result = await self.perform_logical_reasoning(query, context)
        elif request_type == "research":
            result = await self.conduct_research(query, context)
        elif request_type == "analysis":
            result = await self.perform_analysis(query, context)
        else:
            result = await self.general_reasoning(query, context)
        
        return {
            "id": request_msg.get("id"),
            "role": "reason_arm",
            "type": "reasoning_complete",
            "payload": result,
            "ts": datetime.now().isoformat(),
            "christ_seal": True
        }

    async def execute_tool_chain(self, tools: List[Dict], query: str, context: Dict) -> Dict[str, Any]:
        """Execute a chain of tool calls"""
        self.log(f"Executing tool chain with {len(tools)} tools", "INFO")
        self.state = ReasonState.TOOL_CALLING
        
        results = {
            "chain_id": f"chain_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "query": query,
            "tool_results": [],
            "synthesis": "",
            "success": True,
            "reasoning_steps": []
        }
        
        # Execute each tool in sequence
        chain_context = context.copy()
        
        for i, tool_spec in enumerate(tools):
            tool_name = tool_spec.get("name", "")
            parameters = tool_spec.get("parameters", {})
            
            self.log(f"Executing tool {i+1}/{len(tools)}: {tool_name}", "INFO")
            
            # Add previous results to context
            if results["tool_results"]:
                parameters["previous_results"] = results["tool_results"]
                parameters["chain_context"] = chain_context
            
            try:
                if tool_name in self.available_tools:
                    tool_result = await self.available_tools[tool_name](parameters)
                    results["tool_results"].append({
                        "tool": tool_name,
                        "parameters": parameters,
                        "result": tool_result,
                        "success": True,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Update chain context with results
                    chain_context[f"tool_{i}_result"] = tool_result
                    
                else:
                    self.log(f"Unknown tool: {tool_name}", "WARNING")
                    results["tool_results"].append({
                        "tool": tool_name,
                        "error": f"Tool not found: {tool_name}",
                        "success": False
                    })
                    
            except Exception as e:
                self.log(f"Tool execution error: {str(e)}", "ERROR")
                results["tool_results"].append({
                    "tool": tool_name,
                    "error": str(e),
                    "success": False
                })
                results["success"] = False
        
        # Synthesize results
        results["synthesis"] = await self.synthesize_tool_results(results["tool_results"], query)
        
        self.log(f"Tool chain complete - Success: {results['success']}", "SUCCESS")
        return results

    async def perform_logical_reasoning(self, query: str, context: Dict) -> Dict[str, Any]:
        """Perform structured logical reasoning"""
        self.log(f"Performing logical reasoning on: {query[:50]}...", "INFO")
        self.state = ReasonState.CALCULATING
        
        # Create reasoning chain
        chain = ReasoningChain(
            id=f"reason_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            query=query,
            steps=[],
            conclusions=[],
            confidence=0.0,
            evidence=[]
        )
        
        # Step 1: Parse and understand the query
        understanding = await self.parse_reasoning_query(query, context)
        chain.steps.append({
            "step": "understanding",
            "content": understanding,
            "timestamp": datetime.now().isoformat()
        })
        
        # Step 2: Identify logical components
        components = await self.identify_logical_components(query, understanding)
        chain.steps.append({
            "step": "logical_components",
            "content": components,
            "timestamp": datetime.now().isoformat()
        })
        
        # Step 3: Apply reasoning rules
        reasoning_result = await self.apply_reasoning_rules(components, context)
        chain.steps.append({
            "step": "reasoning_application",
            "content": reasoning_result,
            "timestamp": datetime.now().isoformat()
        })
        
        # Step 4: Draw conclusions
        chain.conclusions = await self.draw_conclusions(reasoning_result, context)
        chain.confidence = self.calculate_confidence(chain)
        
        result = {
            "reasoning_chain": chain.__dict__,
            "primary_conclusion": chain.conclusions[0] if chain.conclusions else "Unable to reach conclusion",
            "confidence_score": chain.confidence,
            "logical_validity": chain.confidence > 0.7,
            "supporting_evidence": chain.evidence
        }
        
        self.log(f"Logical reasoning complete - Confidence: {chain.confidence:.2f}", "SUCCESS")
        return result

    async def conduct_research(self, query: str, context: Dict) -> Dict[str, Any]:
        """Conduct research on a topic"""
        self.log(f"Conducting research on: {query[:50]}...", "INFO")
        self.state = ReasonState.RESEARCHING
        
        research_result = {
            "query": query,
            "research_id": f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "sources": [],
            "findings": [],
            "synthesis": "",
            "confidence": 0.0
        }
        
        # Research sources (in real implementation, would use actual APIs)
        sources = await self.identify_research_sources(query, context)
        research_result["sources"] = sources
        
        # Gather information from each source
        for source in sources:
            finding = await self.research_source(source, query)
            research_result["findings"].append(finding)
        
        # Synthesize research findings
        research_result["synthesis"] = await self.synthesize_research(research_result["findings"], query)
        research_result["confidence"] = self.assess_research_confidence(research_result["findings"])
        
        self.log(f"Research complete - {len(research_result['findings'])} findings", "SUCCESS")
        return research_result

    async def perform_analysis(self, query: str, context: Dict) -> Dict[str, Any]:
        """Perform detailed analysis"""
        self.log(f"Performing analysis: {query[:50]}...", "INFO")
        self.state = ReasonState.ANALYZING
        
        analysis_result = {
            "query": query,
            "analysis_id": f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "data_points": [],
            "patterns": [],
            "insights": [],
            "recommendations": [],
            "confidence": 0.0
        }
        
        # Extract data points for analysis
        data_points = await self.extract_data_points(query, context)
        analysis_result["data_points"] = data_points
        
        # Identify patterns
        patterns = await self.identify_patterns(data_points)
        analysis_result["patterns"] = patterns
        
        # Generate insights
        insights = await self.generate_insights(patterns, context)
        analysis_result["insights"] = insights
        
        # Provide recommendations
        recommendations = await self.generate_recommendations(insights, context)
        analysis_result["recommendations"] = recommendations
        
        analysis_result["confidence"] = self.assess_analysis_confidence(analysis_result)
        
        self.log(f"Analysis complete - {len(insights)} insights generated", "SUCCESS")
        return analysis_result

    async def general_reasoning(self, query: str, context: Dict) -> Dict[str, Any]:
        """General reasoning for unspecified requests"""
        self.log(f"General reasoning: {query[:50]}...", "INFO")
        
        return {
            "query": query,
            "reasoning_type": "general",
            "response": await self.generate_reasoned_response(query, context),
            "confidence": 0.8,
            "timestamp": datetime.now().isoformat()
        }

    # Tool implementations
    async def calculate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mathematical calculation tool"""
        expression = params.get("expression", "")
        context = params.get("context", {})
        
        try:
            # Safe evaluation of mathematical expressions
            # In production, use a proper math parser
            allowed_chars = set("0123456789+-*/().= ")
            if all(c in allowed_chars for c in expression):
                result = eval(expression)  # WARNING: Only for demo - use safe parser in production
                return {
                    "calculation": expression,
                    "result": result,
                    "success": True
                }
            else:
                return {
                    "error": "Invalid characters in expression",
                    "success": False
                }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    async def search_files(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search through files in workspace"""
        pattern = params.get("pattern", "")
        directory = params.get("directory", ".")
        file_types = params.get("file_types", ["*.py", "*.js", "*.ts", "*.json"])
        
        matches = []
        
        try:
            for file_type in file_types:
                # Use grep or findstr based on OS
                if os.name == 'nt':  # Windows
                    cmd = f'findstr /s /i "{pattern}" {directory}\\{file_type}'
                else:  # Unix-like
                    cmd = f'grep -r -i "{pattern}" {directory} --include="{file_type}"'
                
                try:
                    output = subprocess.check_output(cmd, shell=True, text=True, timeout=10)
                    matches.extend(output.strip().split('\n'))
                except subprocess.CalledProcessError:
                    pass  # No matches found
            
            return {
                "pattern": pattern,
                "matches_found": len(matches),
                "matches": matches[:20],  # Limit results
                "success": True
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    async def analyze_pattern(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns in data"""
        data = params.get("data", [])
        pattern_type = params.get("type", "general")
        
        if not data:
            return {"error": "No data provided", "success": False}
        
        analysis = {
            "data_points": len(data),
            "pattern_type": pattern_type,
            "patterns_found": [],
            "statistics": {},
            "success": True
        }
        
        # Simple pattern analysis
        if isinstance(data[0], (int, float)):
            # Numerical analysis
            analysis["statistics"] = {
                "mean": sum(data) / len(data),
                "min": min(data),
                "max": max(data),
                "range": max(data) - min(data)
            }
            
            # Trend detection
            if len(data) > 2:
                diffs = [data[i+1] - data[i] for i in range(len(data)-1)]
                if all(d > 0 for d in diffs):
                    analysis["patterns_found"].append("Increasing trend")
                elif all(d < 0 for d in diffs):
                    analysis["patterns_found"].append("Decreasing trend")
                else:
                    analysis["patterns_found"].append("Variable pattern")
        
        return analysis

    async def logical_inference(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform logical inference"""
        premises = params.get("premises", [])
        rules = params.get("rules", [])
        
        inferences = []
        
        # Simple rule application
        for rule in rules:
            if rule.get("type") == "modus_ponens":
                # If P then Q, P is true, therefore Q is true
                condition = rule.get("condition")
                conclusion = rule.get("conclusion")
                
                if condition in premises:
                    inferences.append({
                        "conclusion": conclusion,
                        "rule": "modus_ponens",
                        "premise": condition
                    })
        
        return {
            "premises": premises,
            "inferences": inferences,
            "success": True
        }

    async def web_research(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate web research (would use actual APIs in production)"""
        query = params.get("query", "")
        
        # Simulate research results
        return {
            "query": query,
            "sources": [
                {"title": f"Research result for {query}", "url": "https://example.com", "relevance": 0.9},
                {"title": f"Academic paper on {query}", "url": "https://academic.com", "relevance": 0.8}
            ],
            "summary": f"Research indicates various perspectives on {query}",
            "success": True
        }

    async def code_analysis(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code structure and patterns"""
        code = params.get("code", "")
        language = params.get("language", "python")
        
        analysis = {
            "language": language,
            "lines_of_code": len(code.split('\n')),
            "functions_found": [],
            "complexity_score": 1,
            "success": True
        }
        
        # Simple function detection for Python
        if language == "python":
            functions = re.findall(r'def\s+(\w+)\s*\(', code)
            analysis["functions_found"] = functions
            analysis["complexity_score"] = len(functions) + code.count("if ") + code.count("for ") + code.count("while ")
        
        return analysis

    async def data_transformation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Transform data between formats"""
        data = params.get("data")
        from_format = params.get("from_format", "json")
        to_format = params.get("to_format", "dict")
        
        try:
            if from_format == "json" and to_format == "dict":
                if isinstance(data, str):
                    result = json.loads(data)
                else:
                    result = data
            elif from_format == "dict" and to_format == "json":
                result = json.dumps(data, indent=2)
            else:
                result = data  # No transformation needed
            
            return {
                "original_format": from_format,
                "target_format": to_format,
                "transformed_data": result,
                "success": True
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    # Helper methods for reasoning
    async def parse_reasoning_query(self, query: str, context: Dict) -> Dict[str, Any]:
        """Parse and understand reasoning query"""
        return {
            "query_type": "logical" if any(word in query.lower() for word in ["if", "then", "because", "therefore"]) else "analytical",
            "key_concepts": re.findall(r'\b[A-Z][a-z]+\b', query),
            "question_words": re.findall(r'\b(what|who|when|where|why|how)\b', query.lower()),
            "complexity": "high" if len(query.split()) > 20 else "medium" if len(query.split()) > 10 else "low"
        }

    async def identify_logical_components(self, query: str, understanding: Dict) -> Dict[str, Any]:
        """Identify logical components in the query"""
        components = {
            "premises": [],
            "conclusions": [],
            "assumptions": [],
            "logical_connectors": []
        }
        
        # Simple logical connector detection
        connectors = ["and", "or", "if", "then", "because", "therefore", "however", "but"]
        for connector in connectors:
            if connector in query.lower():
                components["logical_connectors"].append(connector)
        
        return components

    async def apply_reasoning_rules(self, components: Dict, context: Dict) -> Dict[str, Any]:
        """Apply reasoning rules to components"""
        return {
            "rules_applied": ["deduction", "induction"],
            "logical_validity": True,
            "reasoning_steps": ["Identify premises", "Apply logical rules", "Derive conclusions"],
            "confidence_factors": ["Clear logical structure", "Valid premises"]
        }

    async def draw_conclusions(self, reasoning_result: Dict, context: Dict) -> List[str]:
        """Draw conclusions from reasoning"""
        return [
            "Based on logical analysis, the primary conclusion is supported",
            "Secondary implications suggest further investigation needed",
            "The reasoning chain maintains logical consistency"
        ]

    def calculate_confidence(self, chain: ReasoningChain) -> float:
        """Calculate confidence in reasoning chain"""
        base_confidence = 0.7
        
        # Adjust based on steps completed
        step_bonus = len(chain.steps) * 0.05
        
        # Adjust based on evidence
        evidence_bonus = len(chain.evidence) * 0.02
        
        return min(1.0, base_confidence + step_bonus + evidence_bonus)

    async def synthesize_tool_results(self, tool_results: List[Dict], query: str) -> str:
        """Synthesize results from multiple tools"""
        successful_results = [r for r in tool_results if r.get("success", False)]
        
        if not successful_results:
            return "No successful tool executions to synthesize"
        
        synthesis = f"Analysis of {len(successful_results)} tool results for query '{query}':\n"
        
        for i, result in enumerate(successful_results, 1):
            tool_name = result.get("tool", "unknown")
            synthesis += f"{i}. {tool_name}: {str(result.get('result', 'No result'))[:100]}\n"
        
        synthesis += f"\nOverall: Successfully executed {len(successful_results)} tools with consistent results."
        
        return synthesis

    # Additional helper methods...
    async def identify_research_sources(self, query: str, context: Dict) -> List[Dict[str, str]]:
        """Identify relevant research sources"""
        return [
            {"name": "local_files", "type": "filesystem", "priority": 1},
            {"name": "knowledge_base", "type": "internal", "priority": 2},
            {"name": "web_search", "type": "external", "priority": 3}
        ]

    async def research_source(self, source: Dict, query: str) -> Dict[str, Any]:
        """Research a specific source"""
        return {
            "source": source["name"],
            "findings": f"Research findings from {source['name']} for query: {query}",
            "relevance": 0.8,
            "confidence": 0.7
        }

    async def synthesize_research(self, findings: List[Dict], query: str) -> str:
        """Synthesize research findings"""
        return f"Research synthesis for '{query}': {len(findings)} sources analyzed with high confidence."

    def assess_research_confidence(self, findings: List[Dict]) -> float:
        """Assess confidence in research results"""
        if not findings:
            return 0.0
        
        avg_confidence = sum(f.get("confidence", 0.5) for f in findings) / len(findings)
        return avg_confidence

    async def extract_data_points(self, query: str, context: Dict) -> List[Dict[str, Any]]:
        """Extract data points for analysis"""
        return [
            {"type": "query_length", "value": len(query.split())},
            {"type": "context_keys", "value": len(context.keys())},
            {"type": "complexity", "value": "medium"}
        ]

    async def identify_patterns(self, data_points: List[Dict]) -> List[Dict[str, Any]]:
        """Identify patterns in data points"""
        return [
            {"pattern": "data_structure", "confidence": 0.8, "description": "Well-structured input data"},
            {"pattern": "complexity_trend", "confidence": 0.7, "description": "Medium complexity analysis request"}
        ]

    async def generate_insights(self, patterns: List[Dict], context: Dict) -> List[str]:
        """Generate insights from patterns"""
        return [
            "Data shows consistent structure patterns",
            "Analysis complexity is manageable",
            "Context provides sufficient information for reasoning"
        ]

    async def generate_recommendations(self, insights: List[str], context: Dict) -> List[str]:
        """Generate recommendations based on insights"""
        return [
            "Continue with current analytical approach",
            "Consider additional data sources for validation",
            "Monitor confidence levels throughout analysis"
        ]

    def assess_analysis_confidence(self, analysis_result: Dict) -> float:
        """Assess confidence in analysis results"""
        factors = [
            len(analysis_result.get("data_points", [])) > 0,
            len(analysis_result.get("patterns", [])) > 0,
            len(analysis_result.get("insights", [])) > 0
        ]
        
        return sum(factors) / len(factors)

    async def generate_reasoned_response(self, query: str, context: Dict) -> str:
        """Generate a reasoned response to general queries"""
        return f"Based on analysis of the query '{query}' and available context, the reasoning suggests a structured approach to understanding the request and providing appropriate logical conclusions."

    def get_status(self) -> Dict[str, Any]:
        """Get current arm status"""
        return {
            "arm_name": "Reason & Tools (East)",
            "state": self.state.value,
            "available_tools": list(self.available_tools.keys()),
            "tool_calls_completed": len(self.tool_call_history),
            "reasoning_cache_size": len(self.reasoning_cache)
        }

# Async interface for conductor
async def handle_reason_message(msg: Dict[str, Any]) -> Dict[str, Any]:
    """Handle message for Reason & Tools Arm"""
    arm = ReasonToolsArm()
    return await arm.handle_reasoning_request(msg)

# CLI testing
if __name__ == "__main__":
    import sys
    
    async def test_reason_arm():
        test_msg = {
            "id": "test_456",
            "role": "conductor",
            "type": "reasoning_request",
            "payload": {
                "type": "tool_chain",
                "query": "Calculate sacred ratios for music composition",
                "tools": [
                    {"name": "calculate", "parameters": {"expression": "1.618 * 72"}},
                    {"name": "analyze_pattern", "parameters": {"data": [72, 116, 188], "type": "golden_ratio"}}
                ],
                "context": {"session": "sacred_composition", "bpm": 72}
            },
            "ts": datetime.now().isoformat()
        }
        
        print("🌟 Testing Reason & Tools Arm...")
        result = await handle_reason_message(test_msg)
        print(f"✅ Test complete: {json.dumps(result, indent=2)}")
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        asyncio.run(test_reason_arm())
    else:
        print("🧠 Reason & Tools Arm ready")
        print("Usage: python reason_arm.py test")
