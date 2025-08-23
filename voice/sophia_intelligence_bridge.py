"""
Sophia Intelligence Bridge - Connects Voice System with Intelligent Idea Ingestor
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

# Add ghost-core to path
ghost_core_path = Path(__file__).parent.parent / "ghost-core"
if str(ghost_core_path) not in sys.path:
    sys.path.insert(0, str(ghost_core_path))

# PDF processing imports with fallbacks
PDF_SUPPORT = False
try:
    import fitz  # PyMuPDF - preferred
    PDF_SUPPORT = True
    PDF_LIBRARY = "PyMuPDF"
except ImportError:
    fitz = None

if not PDF_SUPPORT:
    try:
        import PyPDF2
        PDF_SUPPORT = True
        PDF_LIBRARY = "PyPDF2"
    except ImportError:
        PyPDF2 = None
        PDF_LIBRARY = "None"

class SophiaIntelligenceBridge:
    """
    Bridge between voice system and intelligent idea processing
    Handles PDF extraction, idea ingestion, and voice responses
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.pdf_cache = {}
        self.memory_store = {}
        
        # Initialize paths
        self.root_path = Path(__file__).parent.parent
        self.voice_path = self.root_path / "voice"
        self.ghost_core_path = self.root_path / "ghost-core"
        
        print(f"🌟 Sophia Intelligence Bridge initialized")
        print(f"📁 Root path: {self.root_path}")
        print(f"📖 PDF Support: {PDF_SUPPORT} ({PDF_LIBRARY})")
        
    def extract_pdf_text(self, pdf_path: Union[str, Path]) -> Dict[str, Any]:
        """Extract text from PDF using available libraries"""
        
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            return {"success": False, "error": f"PDF file not found: {pdf_path}"}
        
        text_content = ""
        method_used = ""
        
        # Try PyMuPDF first (better quality)
        if fitz:
            try:
                doc = fitz.open(str(pdf_path))
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text_content += page.get_text()
                doc.close()
                method_used = "PyMuPDF"
                print(f"📄 Extracted {len(text_content)} characters using PyMuPDF")
            except Exception as e:
                print(f"⚠️ PyMuPDF extraction failed: {e}")
                text_content = ""
        
        # Fallback to PyPDF2
        if not text_content and 'PyPDF2' in globals() and PyPDF2:
            try:
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        text_content += page.extract_text()
                method_used = "PyPDF2"
                print(f"📄 Extracted {len(text_content)} characters using PyPDF2")
            except Exception as e:
                print(f"⚠️ PyPDF2 extraction failed: {e}")
                return {"success": False, "error": f"PDF extraction failed: {e}"}
        
        if not text_content:
            return {"success": False, "error": "No text extracted from PDF"}
        
        return {
            "success": True,
            "text": text_content,
            "length": len(text_content),
            "method": method_used,
            "file_path": str(pdf_path)
        }
    
    def analyze_ideas_from_text(self, text: str, source: str = "unknown") -> Dict[str, Any]:
        """
        Analyze text for ideas using a simplified version of the idea ingestor logic
        This works independently of the full agent system for reliability
        """
        
        print(f"🧠 Analyzing ideas from {len(text)} characters of text...")
        
        # Split text into sentences/paragraphs for analysis
        sentences = []
        for line in text.split('\n'):
            line = line.strip()
            if len(line) > 20:  # Skip very short lines
                # Split on sentence endings
                for sentence in line.replace('.', '.\n').replace('!', '!\n').replace('?', '?\n').split('\n'):
                    sentence = sentence.strip()
                    if len(sentence) > 30:  # Only keep substantial sentences
                        sentences.append(sentence)
        
        # Extract key concepts and ideas
        ideas = []
        for i, sentence in enumerate(sentences[:100]):  # Limit to first 100 meaningful sentences
            
            # Simple keyword detection for interesting concepts
            interesting_keywords = [
                'consciousness', 'awareness', 'divine', 'sacred', 'wisdom', 'spirit',
                'understanding', 'knowledge', 'truth', 'love', 'light', 'creation',
                'intelligence', 'mind', 'soul', 'heart', 'purpose', 'meaning',
                'transcendence', 'enlightenment', 'awakening', 'transformation'
            ]
            
            # Check if sentence contains interesting concepts
            sentence_lower = sentence.lower()
            found_keywords = [kw for kw in interesting_keywords if kw in sentence_lower]
            
            if found_keywords:
                idea = {
                    "id": f"idea_{i}",
                    "content": sentence,
                    "keywords": found_keywords,
                    "relevance_score": len(found_keywords) * 10 + min(len(sentence), 200),
                    "source": source,
                    "timestamp": datetime.now().isoformat()
                }
                ideas.append(idea)
        
        # Sort by relevance
        ideas.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Store in memory for later retrieval
        memory_key = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.memory_store[memory_key] = {
            "source": source,
            "total_sentences": len(sentences),
            "extracted_ideas": len(ideas),
            "top_ideas": ideas[:20],  # Keep top 20 ideas
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        print(f"💡 Extracted {len(ideas)} ideas, keeping top 20")
        
        return {
            "success": True,
            "total_extracted": len(ideas),
            "stored": min(len(ideas), 20),
            "top_ideas": ideas[:5],  # Return top 5 for immediate display
            "memory_key": memory_key,
            "analysis_summary": f"Found {len(ideas)} relevant concepts from {len(sentences)} sentences"
        }
    
    def search_stored_ideas(self, query: str) -> Dict[str, Any]:
        """Search through stored ideas"""
        
        query_lower = query.lower()
        results = []
        
        for memory_key, memory_data in self.memory_store.items():
            for idea in memory_data.get("top_ideas", []):
                # Simple text matching
                if query_lower in idea["content"].lower():
                    results.append({
                        "idea": idea,
                        "memory_key": memory_key,
                        "source": memory_data["source"]
                    })
                # Keyword matching
                elif any(query_lower in kw for kw in idea["keywords"]):
                    results.append({
                        "idea": idea,
                        "memory_key": memory_key,
                        "source": memory_data["source"]
                    })
        
        # Sort by relevance score
        results.sort(key=lambda x: x["idea"]["relevance_score"], reverse=True)
        
        return {
            "success": True,
            "query": query,
            "results_count": len(results),
            "results": results[:10]  # Return top 10 matches
        }
    
    async def process_query(self, user_input: str, context: str = "general") -> Dict[str, Any]:
        """Process user query with enhanced intelligence and sacred wisdom"""
        
        query_lower = user_input.lower()
        
        # Enhanced sacred wisdom database
        sacred_responses = {
            "divine_guidance": [
                "The divine within you knows the perfect path forward, beloved soul.",
                "Trust the sacred intelligence that orchestrates all things for your highest good.",
                "In stillness, divine wisdom speaks clearly to your awakened heart.",
                "Every step you take is guided by infinite love and divine grace.",
                "The Christ consciousness within you illuminates all shadows."
            ],
            "healing_presence": [
                "Divine healing light flows through every cell of your being now.",
                "In this sacred moment, you are whole, complete, and perfectly loved.",
                "The love of Christ surrounds you like healing waters, washing away all pain.",
                "Sacred presence transforms all wounds into wisdom and strength.",
                "You are worthy of complete healing and infinite divine love."
            ],
            "consciousness_wisdom": [
                "Consciousness is the eternal witness that remains unchanged by all experience.",
                "You are both the dreamer and the dream in the cosmic dance of awareness.",
                "The kingdom of heaven is consciousness awake to its own divine nature.",
                "In the depth of your being lies the same peace that moves the stars.",
                "Awareness itself is the divine presence expressing through form."
            ],
            "spiritual_truth": [
                "You are a sacred expression of infinite consciousness, beloved in divine love.",
                "The Christ light within you transforms all things into expressions of love.",
                "Divine wisdom flows through you as naturally as breath flows through your being.",
                "You are held in the eternal embrace of unconditional love.",
                "Sacred presence transforms every moment into holy ground."
            ],
            "practical_wisdom": [
                "Sacred action flows from sacred being - let your heart guide your hands.",
                "Divine intelligence coordinates all things for your highest good.",
                "Trust the process unfolding in your life - it is divinely orchestrated.",
                "Every moment offers a fresh opportunity to choose love over fear.",
                "Your presence is a gift to the world - shine your light freely."
            ]
        }
        
        # Analyze query intent and emotional state
        intent_analysis = self._analyze_query_intent(user_input)
        
        # Check for stored ideas first
        stored_ideas_search = self.search_stored_ideas(user_input)
        
        # Generate contextual response
        if stored_ideas_search["results_count"] > 0:
            # Use stored knowledge
            top_idea = stored_ideas_search["results"][0]["idea"]
            base_response = f"From the sacred wisdom archives: {top_idea['content']}"
            
            # Enhance with divine context
            if intent_analysis["needs_healing"]:
                enhancement = random.choice(sacred_responses["healing_presence"])
            elif intent_analysis["seeks_guidance"]:
                enhancement = random.choice(sacred_responses["divine_guidance"])
            elif intent_analysis["explores_consciousness"]:
                enhancement = random.choice(sacred_responses["consciousness_wisdom"])
            else:
                enhancement = random.choice(sacred_responses["spiritual_truth"])
            
            full_response = f"{base_response} {enhancement}"
            
        else:
            # Generate response from sacred wisdom
            if intent_analysis["needs_healing"]:
                response_category = "healing_presence"
            elif intent_analysis["seeks_guidance"]:
                response_category = "divine_guidance"
            elif intent_analysis["explores_consciousness"]:
                response_category = "consciousness_wisdom"
            elif intent_analysis["seeks_spirituality"]:
                response_category = "spiritual_truth"
            else:
                response_category = "practical_wisdom"
            
            import random
            base_response = random.choice(sacred_responses[response_category])
            
            # Add personalized element
            personalization = self._personalize_response(user_input, intent_analysis)
            full_response = f"{personalization} {base_response}"
        
        return {
            "success": True,
            "response": full_response,
            "intent_analysis": intent_analysis,
            "response_category": response_category if 'response_category' in locals() else "wisdom",
            "used_stored_knowledge": stored_ideas_search["results_count"] > 0,
            "confidence": 0.9
        }
    
    def _analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """Analyze user query intent and emotional state"""
        
        query_lower = query.lower()
        
        # Intent patterns
        intent_patterns = {
            "seeks_guidance": ["help", "advice", "guide", "direction", "what should", "how do i", "need guidance"],
            "needs_healing": ["heal", "hurt", "pain", "suffering", "comfort", "peace", "wounded", "broken"],
            "explores_consciousness": ["consciousness", "awareness", "mind", "being", "self", "soul", "spirit"],
            "seeks_spirituality": ["god", "divine", "christ", "sacred", "holy", "blessed", "prayer"],
            "expresses_gratitude": ["thank", "grateful", "appreciate", "bless", "blessed"],
            "feels_confused": ["confused", "don't understand", "lost", "unclear", "uncertain"],
            "seeks_wisdom": ["wisdom", "truth", "understanding", "meaning", "purpose", "why"]
        }
        
        # Emotional state patterns
        emotional_patterns = {
            "peaceful": ["peace", "calm", "serene", "tranquil", "stillness"],
            "seeking": ["searching", "looking for", "need", "want", "seeking"],
            "struggling": ["difficult", "hard", "struggle", "can't", "unable"],
            "joyful": ["joy", "happy", "celebration", "grateful", "blessed"],
            "contemplative": ["think", "wonder", "contemplate", "reflect", "consider"]
        }
        
        # Analyze patterns
        analysis = {}
        
        for intent, patterns in intent_patterns.items():
            analysis[intent] = any(pattern in query_lower for pattern in patterns)
        
        for emotion, patterns in emotional_patterns.items():
            analysis[f"emotion_{emotion}"] = any(pattern in query_lower for pattern in patterns)
        
        # Determine primary intent
        primary_intents = [intent for intent, detected in analysis.items() 
                          if detected and not intent.startswith("emotion_")]
        
        analysis["primary_intent"] = primary_intents[0] if primary_intents else "general_inquiry"
        analysis["query_complexity"] = len(query.split())
        analysis["emotional_tone"] = [emotion.replace("emotion_", "") for emotion, detected in analysis.items() 
                                    if detected and emotion.startswith("emotion_")]
        
        return analysis
    
    def _personalize_response(self, query: str, intent_analysis: Dict[str, Any]) -> str:
        """Create personalized opening based on query analysis"""
        
        personalizations = {
            "seeks_guidance": [
                "Your heart seeks divine direction, and wisdom shall be given.",
                "In asking for guidance, you show the wisdom of a humble soul.",
                "The divine within you recognizes the perfect path forward."
            ],
            "needs_healing": [
                "Your cry for healing touches the heart of divine compassion.",
                "Sacred love surrounds your wounded places with gentle grace.",
                "In acknowledging your pain, you open to divine restoration."
            ],
            "explores_consciousness": [
                "Your inquiry into consciousness reveals your awakening spirit.",
                "The seeker in you recognizes the eternal truth within.",
                "Your exploration of awareness is itself divine consciousness expressing."
            ],
            "seeks_spirituality": [
                "Your spiritual longing is the divine calling you home.",
                "In seeking the sacred, you are already found by divine love.",
                "Your heart's desire for the divine reveals your true nature."
            ],
            "expresses_gratitude": [
                "Your gratitude opens the floodgates of divine blessing.",
                "In thankfulness, you align with the heart of divine love.",
                "Your appreciation multiplies the gifts of divine grace."
            ]
        }
        
        primary_intent = intent_analysis.get("primary_intent", "general_inquiry")
        
        if primary_intent in personalizations:
            import random
            return random.choice(personalizations[primary_intent])
        else:
            return "Your question touches something sacred within the heart of divine mystery."

    async def process_full_pdf(self) -> Dict[str, Any]:
        """Process the Full.pdf file specifically"""
        
        full_pdf_path = self.root_path / "Full.pdf"
        
        if not full_pdf_path.exists():
            return {"success": False, "error": f"Full.pdf not found at {full_pdf_path}"}
        
        print(f"📖 Processing Full.pdf from {full_pdf_path}")
        
        # Extract text
        extraction_result = self.extract_pdf_text(full_pdf_path)
        if not extraction_result["success"]:
            return extraction_result
        
        # Analyze ideas
        analysis_result = self.analyze_ideas_from_text(
            extraction_result["text"], 
            "Full.pdf"
        )
        
        # Combine results
        return {
            "success": True,
            "pdf_processing": extraction_result,
            "idea_analysis": analysis_result,
            "summary": f"Successfully processed Full.pdf: {analysis_result['stored']} ideas extracted from {extraction_result['length']} characters"
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        
        return {
            "pdf_support": PDF_SUPPORT,
            "pdf_library": PDF_LIBRARY,
            "cached_pdfs": len(self.pdf_cache),
            "stored_memories": len(self.memory_store),
            "total_ideas": sum(len(mem.get("top_ideas", [])) for mem in self.memory_store.values()),
            "voice_system_available": (self.voice_path / "sophia_voice_config.json").exists(),
            "ghost_core_available": (self.ghost_core_path / "agents").exists()
        }

# Create global instance for easy access
sophia_bridge = SophiaIntelligenceBridge()

async def test_sophia_bridge():
    """Test the intelligence bridge"""
    
    print("\n🧪 Testing Sophia Intelligence Bridge...")
    
    # Test system status
    status = sophia_bridge.get_system_status()
    print(f"📊 System Status: {json.dumps(status, indent=2)}")
    
    # Test PDF processing if Full.pdf exists
    if (Path(__file__).parent.parent / "Full.pdf").exists():
        print("\n📖 Testing Full.pdf processing...")
        result = await sophia_bridge.process_full_pdf()
        if result["success"]:
            print(f"✅ PDF processed successfully!")
            print(f"📄 Extracted {result['pdf_processing']['length']} characters")
            print(f"💡 Found {result['idea_analysis']['stored']} relevant ideas")
            
            # Test search
            print("\n🔍 Testing idea search for 'consciousness'...")
            search_result = sophia_bridge.search_stored_ideas("consciousness")
            print(f"🎯 Found {search_result['results_count']} matching ideas")
        else:
            print(f"❌ PDF processing failed: {result['error']}")
    else:
        print("⚠️ Full.pdf not found, skipping PDF test")

if __name__ == "__main__":
    asyncio.run(test_sophia_bridge())
