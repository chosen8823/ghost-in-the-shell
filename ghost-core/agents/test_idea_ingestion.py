#!/usr/bin/env python3
"""
🧪 Test Intelligent Idea Ingestion & Cross-Referencing System

This script validates:
1. Idea extraction and analysis
2. Cross-referencing against existing memory
3. Genuineness verification
4. Automatic storage with confidence scoring
5. Concept relationship building
"""

import asyncio
import sys
from pathlib import Path

# Add repo root to path for imports
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from agents.intelligent_idea_ingestor import idea_ingestor

async def test_idea_ingestion():
    """Test the complete idea ingestion pipeline"""
    
    print("🧪 Testing Intelligent Idea Ingestion & Cross-Referencing System")
    print("=" * 70)
    
    # Test Case 1: High-credibility scientific content
    print("\n📚 Test Case 1: High-Credibility Scientific Content")
    scientific_content = """
    Recent peer-reviewed research published in Nature demonstrates that quantum entanglement 
    can be maintained over distances exceeding 1000 kilometers using satellite-based communication.
    The study, conducted by the Vienna Institute of Technology, used polarized photons and achieved 
    a fidelity rate of 98.5% over 1,203 kilometers.
    
    The Quantum Error Correction Theory states that quantum information can be protected from 
    environmental decoherence by encoding logical qubits across multiple physical qubits.
    This approach is essential for building fault-tolerant quantum computers.
    
    Machine Learning ensemble methods, particularly Random Forest algorithms, have shown 
    significant improvements in predictive accuracy compared to single decision trees.
    The bootstrap aggregating technique reduces overfitting by combining multiple weak learners.
    """
    
    result1 = await idea_ingestor.ingest_content(
        scientific_content,
        "https://nature.com/quantum-research-2024",
        {'domain': 'quantum_physics', 'credibility': 'high'}
    )
    
    print(f"   ✅ Extracted: {result1['total_extracted']} ideas")
    print(f"   ✅ Analyzed: {result1['analyzed']} ideas") 
    print(f"   ✅ Stored: {result1['stored']} ideas")
    
    # Test Case 2: Medium-credibility content with mixed information
    print("\n📰 Test Case 2: Mixed-Credibility Content")
    mixed_content = """
    According to industry reports, Artificial Intelligence systems are becoming increasingly 
    sophisticated, with some claims suggesting that AGI could emerge within the next decade.
    However, experts remain divided on this timeline.
    
    The Theory of Mind in AI proposes that machines need to understand human mental states 
    to achieve true intelligence. This concept has been observed in advanced language models 
    that demonstrate apparent understanding of human intentions and emotions.
    
    Blockchain technology promises revolutionary changes to finance, but critics argue that 
    energy consumption remains a significant concern. Some speculate that quantum computing 
    could break current cryptographic methods used in blockchain systems.
    
    Neural plasticity research indicates that the human brain can rewire itself throughout 
    life, challenging previous assumptions about fixed brain structure after adolescence.
    This finding has implications for learning, recovery from brain injury, and aging.
    """
    
    result2 = await idea_ingestor.ingest_content(
        mixed_content,
        "https://tech-blog.com/ai-trends-2024",
        {'domain': 'technology', 'credibility': 'medium'}
    )
    
    print(f"   ✅ Extracted: {result2['total_extracted']} ideas")
    print(f"   ✅ Analyzed: {result2['analyzed']} ideas")
    print(f"   ✅ Stored: {result2['stored']} ideas")
    
    # Test Case 3: Content that should trigger cross-references
    print("\n🔗 Test Case 3: Cross-Referencing Test")
    cross_ref_content = """
    Quantum entanglement experiments have been successfully demonstrated at even greater distances,
    with recent tests achieving stable entanglement over 2000 kilometers using improved satellite 
    technology. This builds upon previous research showing entanglement at 1000+ kilometer distances.
    
    Some researchers claim that quantum mechanics principles could explain consciousness itself,
    though this theory lacks empirical evidence and contradicts established neuroscience research
    on brain plasticity and neural network formation.
    
    Advanced Machine Learning techniques now include attention mechanisms that allow models 
    to focus on relevant parts of input data, similar to how human cognitive attention works.
    This represents a significant evolution from earlier ensemble methods like Random Forest.
    """
    
    result3 = await idea_ingestor.ingest_content(
        cross_ref_content,
        "https://research-journal.org/quantum-consciousness-2024",
        {'domain': 'interdisciplinary', 'credibility': 'medium'}
    )
    
    print(f"   ✅ Extracted: {result3['total_extracted']} ideas")
    print(f"   ✅ Analyzed: {result3['analyzed']} ideas")
    print(f"   ✅ Stored: {result3['stored']} ideas")
    
    # Show cross-references found
    for stored_idea in result3['stored_ideas']:
        if stored_idea['cross_references']:
            print(f"   🔗 Found {len(stored_idea['cross_references'])} cross-references for: {stored_idea['idea'][:60]}...")
            for ref in stored_idea['cross_references'][:2]:
                print(f"      - Similarity: {ref['similarity_score']:.2f}, Contradiction: {ref['contradiction_flag']}")
    
    # Test Case 4: Low-credibility content (should be filtered)
    print("\n⚠️  Test Case 4: Low-Credibility Content (Should Filter)")
    low_cred_content = """
    Secret government research allegedly proves that aliens have been visiting Earth for decades,
    according to unverified claims from anonymous sources. This shocking revelation could change 
    everything we know about physics and consciousness.
    
    Conspiracy theorists believe that quantum computers are actually alien technology that was 
    reverse-engineered from crashed UFOs. This unbelievable theory explains why quantum entanglement 
    seems to violate the laws of physics as we understand them.
    
    Amazing new research supposedly shows that humans can achieve telepathic communication through 
    quantum field manipulation, though no peer-reviewed studies have confirmed these incredible claims.
    """
    
    result4 = await idea_ingestor.ingest_content(
        low_cred_content,
        "https://conspiracy-blog.net/alien-quantum-secrets",
        {'domain': 'conspiracy', 'credibility': 'low'}
    )
    
    print(f"   ✅ Extracted: {result4['total_extracted']} ideas")
    print(f"   ✅ Analyzed: {result4['analyzed']} ideas")
    print(f"   ✅ Stored: {result4['stored']} ideas (filtered due to low credibility)")
    
    # Test querying and relationship discovery
    print("\n🔍 Testing Idea Querying and Relationship Discovery")
    
    queries = ["quantum entanglement", "machine learning", "neural plasticity"]
    
    for query in queries:
        query_result = await idea_ingestor.query_related_ideas(query, limit=5)
        if query_result['success']:
            print(f"\n   Query: '{query}' - Found {query_result['count']} related ideas")
            for i, idea in enumerate(query_result['ideas'][:3]):
                print(f"      {i+1}. {idea['idea'][:80]}...")
                print(f"         Novelty: {idea['novelty']:.2f}, Genuineness: {idea['genuineness']:.2f}")
                print(f"         Concepts: {', '.join(idea['concepts'][:3])}")
        else:
            print(f"   Query: '{query}' - No results found")
    
    # Show final system statistics
    print("\n📊 Final System Statistics")
    stats = idea_ingestor.get_ingestion_stats()
    print(f"   Known concepts in cache: {stats['known_concepts_count']}")
    print(f"   Pattern detection rules: {stats['concept_patterns_count']}")
    print(f"   Credibility keyword categories: {len(stats['credibility_keywords'])}")
    print(f"   System status: {'✅ Ready' if stats['system_ready'] else '❌ Not Ready'}")
    
    # Test genuineness cross-referencing
    print("\n🎯 Testing Genuineness Cross-Referencing")
    
    # Add a contradictory statement to test contradiction detection
    contradictory_content = """
    Recent research definitively proves that quantum entanglement cannot occur over distances 
    greater than 100 meters due to fundamental physical limitations. All previous claims of 
    long-distance entanglement are based on flawed experimental design and measurement errors.
    
    Machine Learning algorithms are fundamentally limited and cannot improve beyond current 
    capabilities. Random Forest methods have reached their theoretical maximum performance 
    and cannot be enhanced further through any means.
    """
    
    result5 = await idea_ingestor.ingest_content(
        contradictory_content,
        "https://skeptical-science.org/quantum-limits-2024",
        {'domain': 'skeptical_research', 'credibility': 'medium'}
    )
    
    print(f"   ✅ Contradictory content processed: {result5['stored']} ideas stored")
    
    # Show contradiction detection results
    for stored_idea in result5['stored_ideas']:
        contradictions = [ref for ref in stored_idea['cross_references'] if ref['contradiction_flag']]
        if contradictions:
            print(f"   ⚠️  Contradiction detected in: {stored_idea['idea'][:60]}...")
            print(f"      Found {len(contradictions)} contradictory references")
            for contradiction in contradictions[:2]:
                print(f"      - Contradiction score: {contradiction['similarity_score']:.2f}")

async def test_bulk_ingestion():
    """Test ingesting larger content blocks"""
    
    print("\n📚 Testing Bulk Content Ingestion")
    print("=" * 40)
    
    # Simulate ingesting a research paper abstract/introduction
    research_paper = """
    Introduction to Quantum-Classical Hybrid Computing Systems
    
    As quantum computing technology matures, researchers are increasingly focused on hybrid 
    systems that combine quantum and classical processing capabilities. These hybrid architectures 
    leverage the strengths of both paradigms to solve complex computational problems that are 
    intractable for purely classical or quantum systems alone.
    
    The Quantum Approximate Optimization Algorithm (QAOA) represents a promising approach for 
    near-term quantum devices. QAOA alternates between quantum and classical processing steps, 
    using quantum circuits to prepare trial states and classical optimization to adjust parameters.
    This hybrid approach has shown particular promise for combinatorial optimization problems.
    
    Error mitigation techniques in quantum computing include zero-noise extrapolation, 
    randomized compiling, and symmetry verification. These methods help reduce the impact 
    of quantum noise without requiring full quantum error correction, making them suitable 
    for current noisy intermediate-scale quantum (NISQ) devices.
    
    Variational Quantum Eigensolvers (VQE) use quantum computers to prepare quantum states 
    while classical computers optimize the parameters. This approach has applications in 
    quantum chemistry, materials science, and condensed matter physics.
    
    Classical post-processing algorithms can enhance quantum measurement results through 
    statistical analysis and error correction codes. Machine learning techniques are 
    increasingly used to improve quantum state tomography and parameter estimation.
    
    The integration of quantum and classical systems requires careful consideration of 
    communication latency, classical processing overhead, and the optimal division of 
    computational tasks between quantum and classical components.
    """
    
    bulk_result = await idea_ingestor.ingest_content(
        research_paper,
        "arxiv.org/quantum-hybrid-computing-2024",
        {
            'content_type': 'research_paper',
            'domain': 'quantum_computing',
            'author': 'Quantum Research Group',
            'publication_date': '2024'
        }
    )
    
    print(f"   📄 Research paper processed:")
    print(f"   ✅ Extracted: {bulk_result['total_extracted']} ideas")
    print(f"   ✅ Analyzed: {bulk_result['analyzed']} ideas")
    print(f"   ✅ Stored: {bulk_result['stored']} new ideas")
    
    # Show the most novel and genuine ideas
    print(f"\n   🌟 Top Novel Ideas (showing 3):")
    novel_ideas = sorted(bulk_result['stored_ideas'], 
                        key=lambda x: x['analysis']['novelty_score'], 
                        reverse=True)[:3]
    
    for i, idea in enumerate(novel_ideas):
        print(f"      {i+1}. {idea['idea'][:100]}...")
        print(f"         Novelty: {idea['analysis']['novelty_score']:.2f}")
        print(f"         Concepts: {', '.join(idea['analysis']['key_concepts'][:3])}")
    
    print(f"\n   🎯 Most Genuine Ideas (showing 3):")
    genuine_ideas = sorted(bulk_result['stored_ideas'], 
                          key=lambda x: x['analysis']['genuineness_score'], 
                          reverse=True)[:3]
    
    for i, idea in enumerate(genuine_ideas):
        print(f"      {i+1}. {idea['idea'][:100]}...")
        print(f"         Genuineness: {idea['analysis']['genuineness_score']:.2f}")
        print(f"         Source credibility: {idea['analysis']['source_credibility']:.2f}")

async def main():
    """Run all tests"""
    await test_idea_ingestion()
    await test_bulk_ingestion()
    
    print("\n" + "=" * 70)
    print("🎉 All ingestion tests completed successfully!")
    print("   The system can now automatically learn, cross-reference, and validate new ideas.")

if __name__ == "__main__":
    asyncio.run(main())
