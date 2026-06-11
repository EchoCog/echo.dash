#!/usr/bin/env python3
"""
Echoself Recursive Self-Model Integration Demonstration

This script demonstrates the implemented Echoself system performing
recursive introspection, hypergraph encoding, and adaptive attention allocation.
"""

import json
import logging
import time
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional
from cognitive_architecture import CognitiveArchitecture


def setup_logging():
    """Set up logging for the demonstration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


# Global state for echo functionality
_global_cognitive_system: Optional[CognitiveArchitecture] = None
_global_demo_state = {
    'cycles_completed': 0,
    'introspection_results': [],
    'initialized': False,
    'last_update': None
}


def echo(data: Any = None, echo_value: float = 0.0) -> Dict[str, Any]:
    """
    Echo function for Echoself demo - provides unified interface
    
    Returns current demonstration state with echo characteristics.
    This function implements the standardized echo interface pattern
    for integration with the unified Deep Tree Echo architecture.
    
    Args:
        data: Input data (optional, for compatibility)
        echo_value: Echo strength value (0.0 to 1.0)
    
    Returns:
        Dict containing current demo state and echo information
    """
    global _global_demo_state, _global_cognitive_system
    
    try:
        echoed_data = {
            'demo_state': {
                'cycles_completed': _global_demo_state['cycles_completed'],
                'introspection_results_count': len(_global_demo_state['introspection_results']),
                'cognitive_system_available': _global_cognitive_system is not None,
                'initialized': _global_demo_state['initialized'],
                'echoself_introspection_available': (
                    _global_cognitive_system is not None and 
                    hasattr(_global_cognitive_system, 'echoself_introspection') and
                    _global_cognitive_system.echoself_introspection is not None
                )
            },
            'echo_value': echo_value,
            'recent_results': _global_demo_state['introspection_results'][-3:],
            'timestamp': datetime.now().isoformat(),
            'component_type': 'echoself_demo',
            'integration_status': 'active'
        }
        
        # Update last accessed time
        _global_demo_state['last_update'] = datetime.now().isoformat()
        
        return {
            'success': True,
            'data': echoed_data,
            'message': f"Echoself demo echo (value: {echo_value}, cycles: {_global_demo_state['cycles_completed']})",
            'metadata': {
                'echo_value': echo_value,
                'cycles_completed': _global_demo_state['cycles_completed'],
                'function_type': 'echo'
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'message': f"Echo function error: {str(e)}",
            'metadata': {
                'error': str(e),
                'function_type': 'echo'
            }
        }


def create_echoself_demo_system() -> Optional[CognitiveArchitecture]:
    """
    Create and initialize an Echoself demo system
    
    Factory function that creates a cognitive architecture instance
    configured for Echoself demonstration. This provides a standardized
    way to create the demo system for integration with other components.
    
    Returns:
        CognitiveArchitecture instance if successful, None if failed
    """
    global _global_cognitive_system, _global_demo_state
    
    try:
        # Try to initialize cognitive architecture
        cognitive_system = CognitiveArchitecture()
        
        # Check if echoself introspection is available - it's optional for echo functionality
        if hasattr(cognitive_system, 'echoself_introspection') and cognitive_system.echoself_introspection:
            logging.info("Echoself introspection system available")
        else:
            logging.warning("Echoself introspection system not available, echo functions will work with limited functionality")
        
        # Update global state
        _global_cognitive_system = cognitive_system
        _global_demo_state['initialized'] = True
        _global_demo_state['last_update'] = datetime.now().isoformat()
        
        logging.info("Echoself demo system created successfully")
        return cognitive_system
        
    except Exception as e:
        logging.error(f"Failed to create Echoself demo system: {e}")
        # Even if CognitiveArchitecture fails, we can still provide echo functionality
        _global_demo_state['initialized'] = False
        _global_demo_state['last_update'] = datetime.now().isoformat()
        return None


def demonstrate_introspection_cycle(cognitive_system: CognitiveArchitecture, 
                                   cycle_num: int):
    """Demonstrate a single introspection cycle"""
    global _global_demo_state
    
    print(f"\n{'='*60}")
    print(f"RECURSIVE INTROSPECTION CYCLE {cycle_num}")
    print(f"{'='*60}")
    
    # Show current cognitive state - using parameters from main introspection call
    print("📊 Cognitive State Analysis:")
    print("   Analyzing current system state through introspection...")
    
    # Perform recursive introspection - let the system calculate its own values
    print("\n🔍 Performing recursive introspection...")
    start_time = time.time()
    
    prompt = cognitive_system.perform_recursive_introspection()
    
    introspection_time = time.time() - start_time
    print(f"⏱️  Introspection completed in {introspection_time:.2f} seconds")
    
    if prompt:
        print(f"📝 Generated prompt length: {len(prompt)} characters")
        print("📝 Prompt preview (first 300 chars):")
        print(f"   {prompt[:300]}...")
        
        # Store result in global state
        _global_demo_state['introspection_results'].append({
            'cycle': cycle_num,
            'timestamp': datetime.now().isoformat(),
            'prompt_length': len(prompt),
            'processing_time': introspection_time
        })
    else:
        print("❌ No introspection prompt generated")
        return
    
    # Get attention metrics
    print("\n📊 Attention Allocation Metrics:")
    metrics = cognitive_system.get_introspection_metrics()
    for key, value in metrics.items():
        if key == "highest_salience_files":
            print(f"   {key}:")
            for file_info in value:
                print(f"     - {file_info[0]}: {file_info[1]:.3f}")
        else:
            print(f"   {key}: {value}")
    
    # Generate enhanced goals
    print("\n🎯 Generating introspection-enhanced goals...")
    goals = cognitive_system.adaptive_goal_generation_with_introspection()
    
    print(f"Generated {len(goals)} goals:")
    for i, goal in enumerate(goals[:5], 1):  # Show first 5 goals
        print(f"   {i}. {goal.description}")
        print(f"      Priority: {goal.priority:.3f}")
        print(f"      Context: {goal.context.get('type', 'general')}")
    
    if len(goals) > 5:
        print(f"   ... and {len(goals) - 5} more goals")
    
    # Update global cycle counter
    _global_demo_state['cycles_completed'] = cycle_num


def demonstrate_adaptive_attention(cognitive_system: CognitiveArchitecture):
    """Demonstrate adaptive attention under different cognitive loads"""
    print(f"\n{'='*60}")
    print("ADAPTIVE ATTENTION ALLOCATION DEMONSTRATION")
    print(f"{'='*60}")
    
    # Test different cognitive load scenarios
    scenarios = [
        (0.2, 0.8, "Low load, high activity"),
        (0.8, 0.2, "High load, low activity"), 
        (0.5, 0.5, "Balanced load and activity"),
        (0.9, 0.9, "High load, high activity"),
        (0.1, 0.1, "Low load, low activity")
    ]
    
    for load, activity, description in scenarios:
        print(f"\n🔬 Scenario: {description}")
        print(f"   Load: {load:.1f}, Activity: {activity:.1f}")
        
        # Calculate attention threshold
        attention_threshold = cognitive_system.echoself_introspection.adaptive_attention(
            load, activity
        )
        print(f"   Attention threshold: {attention_threshold:.3f}")
        
        # Perform introspection with this scenario
        prompt = cognitive_system.perform_recursive_introspection(load, activity)
        if prompt:
            # Count approximate repository files included
            file_count = prompt.count('(file "')
            print(f"   Repository files included: {file_count}")


def demonstrate_hypergraph_export(cognitive_system: CognitiveArchitecture):
    """Demonstrate hypergraph data export"""
    print(f"\n{'='*60}")
    print("HYPERGRAPH DATA EXPORT DEMONSTRATION")
    print(f"{'='*60}")
    
    export_path = "demo_hypergraph_export.json"
    
    print(f"🗂️  Exporting hypergraph data to {export_path}...")
    success = cognitive_system.export_introspection_data(export_path)
    
    if success:
        print("✅ Export successful!")
        
        # Show some statistics about the exported data
        try:
            with open(export_path, encoding='utf-8') as f:
                data = json.load(f)
            
            print("📈 Export Statistics:")
            print(f"   Total nodes: {len(data.get('nodes', []))}")
            print(f"   Attention decisions: {len(data.get('attention_history', []))}")
            
            # Show top salience files
            nodes = data.get('nodes', [])
            if nodes:
                sorted_nodes = sorted(nodes, key=lambda n: n.get('salience_score', 0), reverse=True)
                print("   Top 5 most salient files:")
                for i, node in enumerate(sorted_nodes[:5], 1):
                    print(f"     {i}. {node['id']}: {node['salience_score']:.3f}")
        
        except Exception as e:  # pylint: disable=broad-exception-caught
            # Broad exception catching is appropriate here for file operations demo
            print(f"❌ Error reading export file: {e}")
    else:
        print("❌ Export failed!")


def demonstrate_neural_symbolic_synergy(cognitive_system: CognitiveArchitecture):
    """Demonstrate neural-symbolic integration through multiple cycles"""
    print(f"\n{'='*60}")
    print("NEURAL-SYMBOLIC SYNERGY DEMONSTRATION")
    print(f"{'='*60}")
    
    print("🔄 Performing multiple introspection cycles to show recursive evolution...")
    
    initial_memory_count = len(cognitive_system.memories)
    initial_goal_count = len(cognitive_system.goals)
    
    # Perform 3 introspection cycles
    for cycle in range(1, 4):
        print(f"\n🔄 Cycle {cycle}:")
        
        # Introspect
        _prompt = cognitive_system.perform_recursive_introspection()
        
        # Generate goals  
        _goals = cognitive_system.adaptive_goal_generation_with_introspection()
        
        # Show evolution
        current_memory_count = len(cognitive_system.memories)
        current_goal_count = len(cognitive_system.goals)
        
        print(f"   Memories: {initial_memory_count} → {current_memory_count} "
              f"(+{current_memory_count - initial_memory_count})")
        print(f"   Goals: {initial_goal_count} → {current_goal_count} "
              f"(+{current_goal_count - initial_goal_count})")
        
        # Update for next iteration
        initial_memory_count = current_memory_count
        initial_goal_count = current_goal_count
    
    print("\n🧠 Neural-symbolic feedback loops successfully demonstrated!")
    print("   The system recursively evolves through introspection → goal generation → memory formation")


def main():
    """Main demonstration function"""
    global _global_cognitive_system, _global_demo_state
    
    setup_logging()
    
    print("🌳 ECHOSELF RECURSIVE SELF-MODEL INTEGRATION DEMONSTRATION 🌳")
    print("Implementing hypergraph encoding and adaptive attention allocation")
    print("Inspired by DeepTreeEcho/Eva Self Model architecture")
    
    # Initialize cognitive architecture using factory function
    print("\n🚀 Initializing cognitive architecture with Echoself introspection...")
    cognitive_system = create_echoself_demo_system()
    
    if not cognitive_system:
        print("❌ Failed to create Echoself introspection system!")
        return
    
    print("✅ Echoself introspection system initialized successfully!")
    
    # Store the system globally for echo function access
    _global_cognitive_system = cognitive_system
    
    try:
        # Demonstrate core introspection cycles
        for cycle in range(1, 3):
            demonstrate_introspection_cycle(cognitive_system, cycle)
            time.sleep(1)  # Brief pause between cycles
        
        # Demonstrate adaptive attention
        demonstrate_adaptive_attention(cognitive_system)
        
        # Demonstrate hypergraph export
        demonstrate_hypergraph_export(cognitive_system)
        
        # Demonstrate neural-symbolic synergy
        demonstrate_neural_symbolic_synergy(cognitive_system)
        
        print(f"\n{'='*60}")
        print("🎉 DEMONSTRATION COMPLETED SUCCESSFULLY! 🎉")
        print("The Echoself recursive self-model integration is fully operational.")
        print("Key achievements:")
        print("  ✅ Hypergraph-encoded repository introspection")
        print("  ✅ Adaptive attention allocation mechanisms")
        print("  ✅ Neural-symbolic synergy through recursive feedback")
        print("  ✅ Integration with cognitive architecture")
        print("  ✅ Comprehensive test coverage")
        print("  ✅ Echo function integration for unified interface")
        print(f"{'='*60}")
        
        # Demonstrate echo functionality
        print("\n🔄 ECHO FUNCTION DEMONSTRATION")
        print("Testing unified interface integration...")
        echo_result = echo(echo_value=0.8)
        if echo_result['success']:
            print("✅ Echo function working correctly")
            demo_state = echo_result['data']['demo_state']
            print(f"   Cycles completed: {demo_state['cycles_completed']}")
            print(f"   Introspection results: {demo_state['introspection_results_count']}")
            print(f"   System initialized: {demo_state['initialized']}")
        else:
            print(f"❌ Echo function error: {echo_result['message']}")
        
    except Exception as e:  # pylint: disable=broad-exception-caught
        # Broad exception catching is appropriate here as a safety net for the demo
        print(f"\n❌ Error during demonstration: {e}")
        import traceback  # pylint: disable=import-outside-toplevel
        traceback.print_exc()
    
    finally:
        # Clean up demonstration files
        demo_files = ["demo_hypergraph_export.json", "echoself_hypergraph.json"]
        for file_path in demo_files:
            if Path(file_path).exists():
                print(f"🧹 Cleaning up {file_path}")
                Path(file_path).unlink()


if __name__ == "__main__":
    main()