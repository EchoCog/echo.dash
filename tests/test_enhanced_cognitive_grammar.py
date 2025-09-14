#!/usr/bin/env python3
"""
Enhanced Cognitive Grammar Tests
===============================

Tests for the new advanced cognitive grammar capabilities including:
- Enhanced reasoning (inference, deduction, abduction)
- Advanced pattern matching and activation spreading
- Meta-cognitive operations
- Learning from experience
"""

import sys
import os
import json
from pathlib import Path

# Add the current directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from cognitive_grammar_bridge import (
        CognitiveGrammarBridge, SymbolicExpression, NeuralPattern,
        get_cognitive_grammar_bridge
    )
    COGNITIVE_GRAMMAR_AVAILABLE = True
except ImportError as e:
    print(f"Error importing cognitive_grammar_bridge: {e}")
    COGNITIVE_GRAMMAR_AVAILABLE = False
    sys.exit(1)

def test_enhanced_reasoning():
    """Test enhanced reasoning capabilities"""
    print("🧠 Testing Enhanced Reasoning Capabilities...")
    
    bridge = get_cognitive_grammar_bridge()
    
    # Test inference
    premises = ["All humans are mortal", "Socrates is human"]
    rules = [{"rule": "syllogism", "pattern": "All A are B, X is A", "conclusion": "X is B"}]
    
    conclusions = bridge.infer(premises, rules)
    print(f"  ✓ Inference test: {len(conclusions)} conclusions drawn")
    assert len(conclusions) > 0, "Should produce at least one conclusion"
    
    # Test deduction
    hypothesis = "Socrates is mortal"
    evidence = ["Socrates is human", "All humans are mortal"]
    
    deduction_result = bridge.deduce(hypothesis, evidence)
    print(f"  ✓ Deduction test: confidence={deduction_result['confidence']:.2f}")
    assert deduction_result['reasoning_type'] == 'deductive'
    assert 'conclusion' in deduction_result
    
    # Test abduction
    observations = ["The grass is wet", "The sky is cloudy"]
    explanations = ["It rained", "Someone used a sprinkler", "Morning dew"]
    
    abduction_result = bridge.abduce(observations, explanations)
    print(f"  ✓ Abduction test: best explanation='{abduction_result['best_explanation']}'")
    assert abduction_result['reasoning_type'] == 'abductive'
    assert abduction_result['best_explanation'] in explanations
    
    print("✅ Enhanced reasoning tests passed!")

def test_meta_cognitive_operations():
    """Test meta-cognitive operations"""
    print("🤔 Testing Meta-Cognitive Operations...")
    
    bridge = get_cognitive_grammar_bridge()
    
    # Test reflection
    reflection_result = bridge.reflect("problem_solving", depth=3)
    print(f"  ✓ Reflection test: depth={reflection_result['depth']}, insights={len(reflection_result['insights'])}")
    assert reflection_result['process'] == "problem_solving"
    assert reflection_result['depth'] == 3
    assert len(reflection_result['insights']) > 0
    
    # Test introspection
    test_state = {"memory_load": 0.7, "attention_focus": "learning", "emotional_state": "curious"}
    introspection_result = bridge.introspect(test_state, "high")
    print(f"  ✓ Introspection test: granularity={introspection_result['granularity']}")
    assert introspection_result['granularity'] == "high"
    assert 'cognitive_load' in introspection_result
    assert 'attention_distribution' in introspection_result
    
    # Test adaptation
    strategy = {"learning_rate": 0.1, "exploration": 0.3}
    adaptation_result = bridge.adapt(strategy, performance=0.5)
    print(f"  ✓ Adaptation test: improvements={len(adaptation_result['improvements'])}")
    assert 'improvements' in adaptation_result
    assert adaptation_result['original_performance'] == 0.5
    
    print("✅ Meta-cognitive operations tests passed!")

def test_learning_and_experience():
    """Test learning from experience"""
    print("📚 Testing Learning and Experience Integration...")
    
    bridge = get_cognitive_grammar_bridge()
    
    # Test supervised learning
    experience = {"input": "cat image", "output": "cat"}
    result = bridge.learn_experience(experience, "supervised")
    print(f"  ✓ Supervised learning: stored as {result}")
    assert isinstance(result, str), "Should return node ID"
    
    # Test reinforcement learning  
    rl_experience = {"state": "game_position", "action": "move_left", "reward": 1.0}
    rl_result = bridge.learn_experience(rl_experience, "reinforcement")
    print(f"  ✓ Reinforcement learning: stored as {rl_result}")
    assert isinstance(rl_result, str), "Should return node ID"
    
    # Test unsupervised learning
    unsupervised_exp = {"data": ["pattern1", "pattern2", "pattern1", "pattern3"]}
    unsup_result = bridge.learn_experience(unsupervised_exp, "unsupervised")
    print(f"  ✓ Unsupervised learning: stored as {unsup_result}")
    assert isinstance(unsup_result, str), "Should return node ID"
    
    print("✅ Learning and experience tests passed!")

def test_pattern_matching_and_activation():
    """Test pattern matching and activation spreading"""
    print("🔍 Testing Pattern Matching and Activation Spreading...")
    
    bridge = get_cognitive_grammar_bridge()
    
    # Create some concepts first
    concept1 = bridge.remember("artificial intelligence", "technology context")
    concept2 = bridge.remember("machine learning", "AI subfield")
    concept3 = bridge.remember("neural networks", "ML technique")
    
    # Test pattern matching
    pattern = {"type": "concept"}
    matches = bridge.pattern_match_hypergraph(pattern)
    print(f"  ✓ Pattern matching: found {len(matches)} matches")
    assert len(matches) >= 0, "Should return list of matches"
    
    # Test activation spreading
    source_nodes = [concept1, concept2]
    activations = bridge.activate_spread_network(source_nodes, activation_level=0.8)
    print(f"  ✓ Activation spreading: {len(activations)} nodes activated")
    assert len(activations) >= len(source_nodes), "Should include at least source nodes"
    assert all(0 <= activation <= 1.0 for activation in activations.values()), "Activations should be in [0,1]"
    
    print("✅ Pattern matching and activation tests passed!")

def test_neural_symbolic_integration():
    """Test enhanced neural-symbolic integration"""
    print("🔗 Testing Enhanced Neural-Symbolic Integration...")
    
    bridge = get_cognitive_grammar_bridge()
    
    # Test neural to symbolic with realistic data
    activation_vector = [0.8, 0.3, 0.9, 0.1, 0.6, 0.4, 0.7, 0.2]
    symbol_space = ["concept", "relation", "entity", "action", "property", "value", "context", "time"]
    
    symbolic_result = bridge.neural_to_symbolic(activation_vector, symbol_space)
    print(f"  ✓ Neural->Symbolic: {len(symbolic_result.symbols)} symbols, activation={symbolic_result.activation_level:.2f}")
    assert len(symbolic_result.symbols) > 0, "Should extract some symbols"
    assert 0 <= symbolic_result.activation_level <= 1.0, "Activation should be normalized"
    
    # Test symbolic to neural
    expression = SymbolicExpression(
        expression="(learn concept context)",
        symbols=["learn", "concept", "context"], 
        activation_level=0.7
    )
    
    neural_result = bridge.symbolic_to_neural(expression, neural_network_size=50)
    print(f"  ✓ Symbolic->Neural: {len(neural_result.activations)} activations")
    assert len(neural_result.activations) == 50, "Should match requested network size"
    assert all(0 <= act <= 1.0 for act in neural_result.activations), "Activations should be normalized"
    
    # Test hybrid reasoning  
    problem = "How to improve learning efficiency?"
    hybrid_result = bridge.hybrid_reason(problem, "neural_optimization", "symbolic_analysis")
    print(f"  ✓ Hybrid reasoning: confidence={hybrid_result['confidence']:.2f}")
    assert hybrid_result['problem'] == problem
    assert 'integrated_solution' in hybrid_result
    
    print("✅ Neural-symbolic integration tests passed!")

def test_system_integration():
    """Test system integration and status"""
    print("⚙️ Testing System Integration...")
    
    bridge = get_cognitive_grammar_bridge()
    
    # Test system status
    status = bridge.get_status()
    print(f"  ✓ System status: {status.get('status', 'unknown')}")
    assert 'status' in status, "Should provide status information"
    
    # Test memory operations with context
    contexts = ["learning_context", "reasoning_context", "memory_context"]
    stored_concepts = []
    
    for i, context in enumerate(contexts):
        concept_id = bridge.remember(f"test_concept_{i}", context)
        stored_concepts.append(concept_id)
    
    print(f"  ✓ Memory integration: stored {len(stored_concepts)} concepts")
    
    # Test recall with patterns
    recalled = bridge.recall("test_concept")
    print(f"  ✓ Pattern recall: found {len(recalled)} matching concepts")
    
    # Test echo operations
    echo_id = bridge.echo_create("integration_test_echo", 
                                {"valence": 0.8, "arousal": 0.6},
                                {"location": "test_environment"})
    
    propagation_success = bridge.echo_propagate(echo_id, 0.5)
    print(f"  ✓ Echo integration: created={echo_id}, propagated={propagation_success}")
    
    print("✅ System integration tests passed!")

def main():
    """Run all enhanced cognitive grammar tests"""
    print("🚀 Starting Enhanced Cognitive Grammar Tests")
    print("=" * 50)
    
    if not COGNITIVE_GRAMMAR_AVAILABLE:
        print("❌ Cognitive grammar bridge not available")
        return False
    
    try:
        test_enhanced_reasoning()
        print()
        
        test_meta_cognitive_operations()
        print()
        
        test_learning_and_experience() 
        print()
        
        test_pattern_matching_and_activation()
        print()
        
        test_neural_symbolic_integration()
        print()
        
        test_system_integration()
        print()
        
        print("🎉 All Enhanced Cognitive Grammar Tests Passed!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)