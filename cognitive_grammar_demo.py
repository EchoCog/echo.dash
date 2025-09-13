#!/usr/bin/env python3
"""
Deep Tree Echo Cognitive Grammar Demonstration
==============================================

Demonstrates the enhanced unified symbolic reasoning capabilities
of the Deep Tree Echo cognitive architecture.
"""

import json
from cognitive_grammar_bridge import (
    get_cognitive_grammar_bridge, 
    SymbolicExpression, 
    NeuralPattern
)

def demonstrate_unified_reasoning():
    """Demonstrate unified cognitive reasoning capabilities"""
    print("🧠 Deep Tree Echo Cognitive Grammar Demonstration")
    print("=" * 55)
    
    # Initialize the cognitive grammar system
    bridge = get_cognitive_grammar_bridge()
    status = bridge.get_status()
    print(f"📊 System Status: {status.get('status', 'unknown')} ({status.get('nodes', 0)} nodes)")
    print()
    
    # 1. Demonstrate Memory and Concept Storage
    print("1️⃣ Memory and Concept Formation")
    print("-" * 35)
    
    # Store some interrelated concepts
    concepts = {
        "ai": bridge.remember("artificial intelligence", "technology domain"),
        "ml": bridge.remember("machine learning", "AI subdomain"),
        "nn": bridge.remember("neural networks", "ML architecture"),
        "cog": bridge.remember("cognitive architecture", "AI reasoning system")
    }
    
    for name, node_id in concepts.items():
        print(f"  📝 Stored {name}: {node_id}")
    print()
    
    # 2. Demonstrate Echo Propagation
    print("2️⃣ Echo Propagation and Activation Spreading")
    print("-" * 45)
    
    echo_id = bridge.echo_create(
        "deep learning breakthrough",
        emotional_state={"excitement": 0.9, "curiosity": 0.8},
        spatial_context={"field": "AI research", "impact": "high"}
    )
    print(f"  ⚡ Created echo: {echo_id}")
    
    # Spread activation through the network
    activations = bridge.activate_spread_network([echo_id], activation_level=0.9)
    print(f"  🌊 Activation spread to {len(activations)} nodes")
    print(f"  📈 Peak activation: {max(activations.values()):.2f}")
    print()
    
    # 3. Demonstrate Neural-Symbolic Integration
    print("3️⃣ Neural-Symbolic Integration")
    print("-" * 33)
    
    # Neural to symbolic conversion
    neural_pattern = [0.9, 0.2, 0.7, 0.4, 0.8, 0.3, 0.6, 0.1]
    symbol_space = ["intelligence", "learning", "reasoning", "memory", 
                   "adaptation", "creativity", "understanding", "synthesis"]
    
    symbolic_result = bridge.neural_to_symbolic(neural_pattern, symbol_space)
    print(f"  🔄 Neural→Symbolic: {symbolic_result.expression}")
    print(f"     Symbols: {', '.join(symbolic_result.symbols)}")
    print(f"     Activation: {symbolic_result.activation_level:.2f}")
    
    # Symbolic to neural conversion
    symbolic_expr = SymbolicExpression(
        expression="(learn pattern recognition)",
        symbols=["learn", "pattern", "recognition"],
        activation_level=0.8
    )
    
    neural_result = bridge.symbolic_to_neural(symbolic_expr, neural_network_size=10)
    print(f"  🔄 Symbolic→Neural: {len(neural_result.activations)} neurons")
    print(f"     Max activation: {max(neural_result.activations):.2f}")
    print()
    
    # 4. Demonstrate Advanced Reasoning
    print("4️⃣ Advanced Reasoning Capabilities")  
    print("-" * 35)
    
    # Deductive reasoning
    hypothesis = "AI systems can exhibit creativity"
    evidence = [
        "AI generates novel art and music",
        "Creative work requires original thinking", 
        "AI demonstrates original thinking patterns"
    ]
    
    deduction = bridge.deduce(hypothesis, evidence)
    print(f"  🎯 Deduction: '{hypothesis}'")
    print(f"     Confidence: {deduction['confidence']:.2f}")
    
    # Abductive reasoning
    observations = ["AI performance improving rapidly", "New algorithms emerging", "Increased research funding"]
    explanations = ["Breakthrough in quantum computing", "Better neural architectures", "More data availability"]
    
    abduction = bridge.abduce(observations, explanations)
    print(f"  🔍 Best explanation: '{abduction['best_explanation']}'")
    
    # Hybrid reasoning
    problem = "How to achieve artificial general intelligence?"
    hybrid = bridge.hybrid_reason(problem, "neural_scaling", "symbolic_integration")
    print(f"  🔬 Hybrid solution confidence: {hybrid['confidence']:.2f}")
    print()
    
    # 5. Demonstrate Meta-Cognitive Operations
    print("5️⃣ Meta-Cognitive Operations")
    print("-" * 28)
    
    # Self-reflection
    reflection = bridge.reflect("learning_process", depth=2)
    print(f"  💭 Reflection on 'learning_process':")
    print(f"     Insights: {len(reflection['insights'])} generated")
    print(f"     Recommendations: {', '.join(reflection['recommendations'][:2])}")
    
    # Introspection
    cognitive_state = {
        "memory_load": 0.6,
        "processing_speed": 0.8, 
        "attention_focus": "problem_solving",
        "confidence_level": 0.7
    }
    
    introspection = bridge.introspect(cognitive_state, "medium")
    print(f"  🔍 Introspection: {introspection['granularity']} granularity")
    print(f"     Cognitive load: {introspection.get('cognitive_load', 'unknown')}")
    
    # Strategy adaptation
    strategy = {"exploration": 0.3, "exploitation": 0.7, "learning_rate": 0.1}
    adapted = bridge.adapt(strategy, performance=0.4)
    print(f"  🎯 Strategy adaptation: {len(adapted['improvements'])} improvements suggested")
    print()
    
    # 6. Demonstrate Learning from Experience
    print("6️⃣ Learning from Experience")
    print("-" * 27)
    
    # Supervised learning example
    supervised_exp = {
        "input": "natural language query",
        "output": "structured database query", 
        "context": "language understanding task"
    }
    
    supervised_id = bridge.learn_experience(supervised_exp, "supervised")
    print(f"  📚 Supervised learning: {supervised_id}")
    
    # Reinforcement learning example
    rl_exp = {
        "state": "chess_position_mid_game",
        "action": "queen_sacrifice",
        "reward": 1.5,
        "next_state": "winning_position"
    }
    
    rl_id = bridge.learn_experience(rl_exp, "reinforcement") 
    print(f"  🎮 Reinforcement learning: {rl_id}")
    
    # Meta-learning example
    meta_exp = {
        "learning_strategy": "gradient_descent",
        "performance": 0.85,
        "context": "neural_network_training"
    }
    
    meta_id = bridge.learn_experience(meta_exp, "meta")
    print(f"  🧠 Meta-learning: {meta_id}")
    print()
    
    # 7. Final System Status
    print("7️⃣ Final System Status")
    print("-" * 22)
    
    final_status = bridge.get_status()
    print(f"  📊 Total nodes: {final_status.get('nodes', 0)}")
    print(f"  💾 Memory usage: {final_status.get('memory_usage', 0)} bytes")
    print(f"  ✅ System status: {final_status.get('status', 'unknown')}")
    
    print()
    print("🎉 Cognitive Grammar Demonstration Complete!")
    print("   The unified symbolic reasoning layer is now fully operational.")
    print("=" * 55)

if __name__ == "__main__":
    demonstrate_unified_reasoning()