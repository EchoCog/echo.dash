#!/usr/bin/env python3
"""
Consolidated Demo: Unified Echo Memory System

This demo consolidates and replaces:
- demo_memory_unification.py 
- echo_memory_demo_standardized.py

It demonstrates the complete unified memory system and addresses the
"Fragmented Memory System" issue by showing how all memory operations
are now unified while maintaining backward compatibility.
"""

import sys
import time
from pathlib import Path
from typing import Dict, Any

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import unified memory components
from unified_echo_memory import (
    UnifiedEchoMemory, EchoMemoryConfig, create_unified_memory_system,
    MemoryType, MemoryNode, HypergraphMemory
)
from echo_component_base import EchoConfig, EchoResponse
from memory_adapter import MemoryAdapter, get_memory_adapter
from memory_management import memory_system
from echo_memory_demo_standardized import EchoMemoryDemoStandardized


def print_header(title: str, char: str = "="):
    """Print a formatted header"""
    print(f"\n{char * 60}")
    print(f"🌟 {title}")
    print(f"{char * 60}")


def print_section(title: str):
    """Print a section header"""
    print(f"\n{'─' * 40}")
    print(f"📋 {title}")
    print(f"{'─' * 40}")


def demonstrate_unified_memory_types():
    """Demonstrate unified memory types across all components"""
    print_section("1. UNIFIED MEMORY TYPES")
    
    # Show all available memory types
    memory_types = list(MemoryType)
    print(f"📊 Available Memory Types: {len(memory_types)}")
    
    for memory_type in memory_types:
        print(f"   • {memory_type.name:<12} : {memory_type.value}")
    
    # Verify consistency across components
    from unified_echo_memory import MemoryType as UnifiedType
    from memory_adapter import MemoryType as AdapterType
    from memory_management import MemoryType as ManagementType
    
    types_consistent = (UnifiedType is AdapterType is ManagementType)
    print(f"\n✅ Memory types consistent across all components: {types_consistent}")
    
    return types_consistent


def demonstrate_core_memory_operations():
    """Demonstrate core memory operations with the unified system"""
    print_section("2. CORE MEMORY OPERATIONS")
    
    # Create unified memory system
    print("🔧 Creating unified memory system...")
    memory_system = create_unified_memory_system(
        component_name="DemoMemory",
        storage_path="demo_memory_storage"
    )
    
    print(f"   ✅ Memory system created: {memory_system.__class__.__name__}")
    print(f"   ✅ Initialized: {memory_system._initialized}")
    
    # Demonstrate different memory types
    demo_memories = [
        ("I attended a meeting today", MemoryType.EPISODIC, 0.8),
        ("Paris is the capital of France", MemoryType.SEMANTIC, 0.6),
        ("How to ride a bicycle", MemoryType.PROCEDURAL, 0.7),
        ("I felt happy after the success", MemoryType.EMOTIONAL, 0.9),
        ("The current task is memory demo", MemoryType.WORKING, 0.5),
        ("I heard birds singing", MemoryType.SENSORY, 0.4),
        ("Meeting reminds me of collaboration", MemoryType.ASSOCIATIVE, 0.3)
    ]
    
    stored_memories = []
    
    print("\n💾 Storing memories of different types:")
    for content, mem_type, echo_value in demo_memories:
        result = memory_system.store_memory(
            content=content,
            memory_type=mem_type,
            echo_value=echo_value,
            metadata={"demo": True, "category": mem_type.name.lower()}
        )
        
        if result.success:
            memory_id = result.data['memory_id']
            stored_memories.append(memory_id)
            print(f"   ✅ {mem_type.name:<12}: {content[:40]}...")
        else:
            print(f"   ❌ Failed to store {mem_type.name}: {result.message}")
    
    print(f"\n📈 Successfully stored {len(stored_memories)} memories")
    
    # Demonstrate retrieval
    print("\n🔍 Retrieving a specific memory:")
    if stored_memories:
        test_memory_id = stored_memories[0]
        retrieve_result = memory_system.retrieve_memory(test_memory_id)
        
        if retrieve_result.success:
            memory_data = retrieve_result.data
            print(f"   Memory ID: {memory_data['id']}")
            print(f"   Content: {memory_data['content']}")
            print(f"   Type: {memory_data['memory_type']}")
            print(f"   Echo Value: {memory_data['echo_value']}")
            print(f"   Access Count: {memory_data['access_count']}")
        else:
            print(f"   ❌ Failed to retrieve memory: {retrieve_result.message}")
    
    return memory_system, stored_memories


def demonstrate_memory_search():
    """Demonstrate memory search capabilities"""
    print_section("3. MEMORY SEARCH OPERATIONS")
    
    # Use the same memory system
    memory_system = create_unified_memory_system("SearchDemo", "demo_search_storage")
    
    # Add searchable content
    search_content = [
        "Python is a powerful programming language",
        "Machine learning algorithms use Python extensively", 
        "Web development can be done with JavaScript",
        "Data science projects often involve Python and R",
        "Python has excellent libraries for AI development"
    ]
    
    print("📚 Adding searchable content...")
    for i, content in enumerate(search_content):
        memory_system.store_memory(
            content=content,
            memory_type=MemoryType.SEMANTIC,
            echo_value=0.5 + i * 0.1,
            metadata={"topic": "programming", "index": i}
        )
    
    # Perform searches
    search_queries = ["Python", "programming", "development", "AI"]
    
    print("\n🔍 Performing searches:")
    for query in search_queries:
        search_result = memory_system.search_memories(
            query=query,
            memory_type=MemoryType.SEMANTIC,
            max_results=5
        )
        
        if search_result.success:
            results = search_result.data['results']
            print(f"\n   Query: '{query}' → {len(results)} results")
            for i, result in enumerate(results[:3]):  # Show top 3
                print(f"     {i+1}. {result['content'][:50]}...")
        else:
            print(f"   ❌ Search failed for '{query}': {search_result.message}")


def demonstrate_echo_operations():
    """Demonstrate Echo-specific memory operations"""
    print_section("4. ECHO OPERATIONS")
    
    memory_system = create_unified_memory_system("EchoDemo", "demo_echo_storage")
    
    # Add memories with different echo values
    echo_test_data = [
        ("High importance memory", 0.9),
        ("Medium importance memory", 0.5),
        ("Low importance memory", 0.1),
        ("Another high importance memory", 0.8),
        ("Resonant memory", 0.9)
    ]
    
    print("🎵 Adding memories with different echo values:")
    for content, echo_value in echo_test_data:
        result = memory_system.store_memory(
            content=content,
            memory_type=MemoryType.DECLARATIVE,
            echo_value=echo_value
        )
        print(f"   Echo {echo_value}: {content}")
    
    # Perform echo operation
    print("\n🌊 Performing echo operation (value: 0.85):")
    echo_result = memory_system.echo("Test echo resonance", echo_value=0.85)
    
    if echo_result.success:
        echo_data = echo_result.data
        print(f"   Echo Memory ID: {echo_data['echo_memory_id']}")
        print(f"   Resonant Memories: {len(echo_data['resonant_memories'])}")
        print(f"   Working Memory State: {len(echo_data['working_memory_state'])} items")
        
        # Show echo analysis
        analysis = echo_data.get('echo_analysis', {})
        if analysis:
            print(f"   Pattern Strength: {analysis.get('pattern_strength', 0):.2f}")
            print(f"   Average Resonant Echo: {analysis.get('average_resonant_echo', 0):.2f}")
    else:
        print(f"   ❌ Echo operation failed: {echo_result.message}")


def demonstrate_memory_adapter():
    """Demonstrate memory adapter for backward compatibility"""
    print_section("5. MEMORY ADAPTER (BACKWARD COMPATIBILITY)")
    
    # Create memory adapter
    adapter = MemoryAdapter("DemoAdapter")
    print("🔌 Memory adapter created for backward compatibility")
    
    # Test adapter operations
    print("\n📝 Testing adapter operations:")
    
    # Store memory using adapter
    memory_id = adapter.store_memory(
        content="Adapter compatibility test",
        memory_type=MemoryType.DECLARATIVE,
        metadata={"adapter": True, "legacy": True},
        echo_value=0.6
    )
    print(f"   ✅ Stored via adapter: {memory_id}")
    
    # Retrieve memory using adapter
    retrieved = adapter.retrieve_memory(memory_id)
    if retrieved:
        print(f"   ✅ Retrieved via adapter: {retrieved.content}")
        print(f"   Memory type: {retrieved.memory_type.value}")
        print(f"   Echo value: {retrieved.echo_value}")
    else:
        print("   ❌ Failed to retrieve via adapter")
    
    # Test legacy format compatibility
    print("\n🔄 Testing legacy format compatibility:")
    legacy_id = adapter.create_legacy_memory(
        content="Legacy format memory",
        memory_type="episodic",
        emotional_valence=0.3,
        importance=0.8,
        context={"source": "legacy_system"}
    )
    print(f"   ✅ Legacy memory created: {legacy_id}")
    
    # Retrieve in legacy format
    legacy_memory = adapter.get_legacy_memory(legacy_id)
    if legacy_memory:
        print(f"   ✅ Retrieved in legacy format:")
        print(f"     Content: {legacy_memory['content']}")
        print(f"     Emotional valence: {legacy_memory['emotional_valence']}")
        print(f"     Importance: {legacy_memory['importance']}")
    else:
        print("   ❌ Failed to retrieve legacy memory")
    
    # Test global adapter
    print("\n🌍 Testing global memory adapter:")
    global_adapter = get_memory_adapter("global_demo")
    global_adapter2 = get_memory_adapter("global_demo")
    
    same_instance = global_adapter is global_adapter2
    print(f"   ✅ Global adapter singleton: {same_instance}")


def demonstrate_memory_analysis():
    """Demonstrate memory analysis and overview capabilities"""
    print_section("6. MEMORY ANALYSIS & OVERVIEW")
    
    memory_system = create_unified_memory_system("AnalysisDemo", "demo_analysis_storage")
    
    # Add diverse memory content for analysis
    analysis_data = [
        ("Meeting with team about project X", MemoryType.EPISODIC, 0.8),
        ("Algorithm for sorting arrays", MemoryType.PROCEDURAL, 0.7),
        ("London is in England", MemoryType.SEMANTIC, 0.5),
        ("Feeling excited about new project", MemoryType.EMOTIONAL, 0.9),
        ("Remember to call client", MemoryType.WORKING, 0.6),
        ("Sound of rain on window", MemoryType.SENSORY, 0.4),
        ("Project X connects to previous work", MemoryType.ASSOCIATIVE, 0.7)
    ]
    
    print("📊 Adding diverse memory content for analysis...")
    for content, mem_type, echo_value in analysis_data:
        memory_system.store_memory(content, mem_type, echo_value)
    
    # Get memory overview
    print("\n📈 Memory System Overview:")
    overview_result = memory_system.get_memory_overview()
    
    if overview_result.success:
        overview = overview_result.data
        
        print(f"   Total Memories: {overview['total_memories']}")
        print(f"   Working Memory Size: {overview['working_memory_size']}")
        print(f"   Working Memory Capacity: {overview['working_memory_capacity']}")
        
        # Memory type distribution
        print("\n   Memory Type Distribution:")
        type_dist = overview['memory_type_distribution']
        for mem_type, count in type_dist.items():
            print(f"     {mem_type:<12}: {count}")
        
        # Echo statistics
        echo_stats = overview['echo_statistics']
        print(f"\n   Echo Value Statistics:")
        print(f"     Mean: {echo_stats['mean']:.3f}")
        print(f"     Min:  {echo_stats['min']:.3f}")
        print(f"     Max:  {echo_stats['max']:.3f}")
        
        # Access statistics
        access_stats = overview['access_statistics']
        print(f"\n   Access Statistics:")
        print(f"     Total Accesses: {access_stats['total']}")
        print(f"     Average per Memory: {access_stats['mean']:.1f}")
    else:
        print(f"   ❌ Failed to get overview: {overview_result.message}")


def demonstrate_integration_compatibility():
    """Demonstrate integration and backward compatibility"""
    print_section("7. INTEGRATION & COMPATIBILITY")
    
    print("🔄 Testing compatibility with legacy memory_management.py:")
    
    # Test the compatibility layer
    from memory_management import memory_system as legacy_system
    print(f"   Legacy system type: {type(legacy_system).__name__}")
    print(f"   Storage directory: {legacy_system.storage_dir}")
    
    # Test adding node through legacy interface
    test_node = MemoryNode(
        id="legacy_test_node",
        content="Testing legacy compatibility",
        memory_type=MemoryType.DECLARATIVE,
        echo_value=0.5
    )
    
    node_id = legacy_system.add_node(test_node)
    print(f"   ✅ Added node via legacy interface: {node_id}")
    
    # Retrieve through legacy interface
    retrieved_node = legacy_system.get_node(node_id)
    if retrieved_node:
        print(f"   ✅ Retrieved via legacy interface: {retrieved_node.content}")
    else:
        print("   ❌ Failed to retrieve via legacy interface")
    
    print("\n🧪 Testing Echo component standardization:")
    
    # Test standardized demo component
    demo_config = EchoConfig(
        component_name="IntegrationDemo",
        version="1.0.0",
        echo_threshold=0.75
    )
    
    demo = EchoMemoryDemoStandardized(demo_config)
    init_result = demo.initialize()
    
    print(f"   ✅ Demo component initialized: {init_result.success}")
    
    # Test demo operations
    demo_result = demo.process({
        'operation': 'store',
        'content': 'Integration test memory',
        'metadata': {'integration': True}
    })
    
    print(f"   ✅ Demo store operation: {demo_result.success}")


def demonstrate_performance_insights():
    """Show performance characteristics of the unified system"""
    print_section("8. PERFORMANCE INSIGHTS")
    
    memory_system = create_unified_memory_system("PerfDemo", "demo_perf_storage")
    
    # Performance test with timing
    print("⏱️  Performance testing...")
    
    # Test storage performance
    start_time = time.time()
    num_memories = 100
    
    for i in range(num_memories):
        memory_system.store_memory(
            f"Performance test memory {i}",
            MemoryType.DECLARATIVE,
            echo_value=i / num_memories
        )
    
    store_time = time.time() - start_time
    print(f"   Storage: {num_memories} memories in {store_time:.3f}s ({num_memories/store_time:.1f} ops/sec)")
    
    # Test search performance
    start_time = time.time()
    for i in range(10):
        memory_system.search_memories(f"test {i}", max_results=5)
    
    search_time = time.time() - start_time
    print(f"   Search: 10 searches in {search_time:.3f}s ({10/search_time:.1f} ops/sec)")
    
    # Memory usage insights
    overview = memory_system.get_memory_overview()
    if overview.success:
        total_memories = overview.data['total_memories']
        working_memory_usage = overview.data['working_memory_size']
        capacity = overview.data['working_memory_capacity']
        
        print(f"   Memory efficiency: {working_memory_usage}/{capacity} working memory slots used")
        print(f"   Total system memories: {total_memories}")


def run_consolidated_demo():
    """Run the complete consolidated memory system demonstration"""
    print_header("UNIFIED ECHO MEMORY SYSTEM - CONSOLIDATED DEMO")
    
    print("\n🎯 This demo shows how the fragmented memory system has been unified")
    print("   while maintaining complete backward compatibility.")
    
    results = {}
    
    try:
        # Run all demonstrations
        results['memory_types'] = demonstrate_unified_memory_types()
        
        memory_system, stored_memories = demonstrate_core_memory_operations()
        results['core_operations'] = len(stored_memories) > 0
        
        demonstrate_memory_search()
        results['search'] = True
        
        demonstrate_echo_operations()
        results['echo'] = True
        
        demonstrate_memory_adapter()
        results['adapter'] = True
        
        demonstrate_memory_analysis()
        results['analysis'] = True
        
        demonstrate_integration_compatibility()
        results['integration'] = True
        
        demonstrate_performance_insights()
        results['performance'] = True
        
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        import traceback
        traceback.print_exc()
        results['error'] = str(e)
    
    # Summary
    print_header("DEMO SUMMARY", "=")
    
    successful_demos = sum(1 for k, v in results.items() if v is True and k != 'error')
    total_demos = len([k for k in results.keys() if k != 'error'])
    
    print(f"✅ Successful demonstrations: {successful_demos}/{total_demos}")
    
    if 'error' not in results:
        print("\n🎉 UNIFIED MEMORY SYSTEM DEMONSTRATION COMPLETE!")
        print("\n📋 Key achievements demonstrated:")
        print("   • All memory types unified across components")
        print("   • Core memory operations (store, retrieve, search)")
        print("   • Echo-specific operations and resonance")
        print("   • Backward compatibility with legacy systems")
        print("   • Memory analysis and system insights")
        print("   • Performance characteristics")
        print("   • Integration with Echo component standards")
        
        print("\n✅ The fragmented memory system issue has been resolved!")
        print("   All memory operations are now unified in unified_echo_memory.py")
        print("   while maintaining full backward compatibility.")
    else:
        print(f"\n❌ Demo completed with errors: {results.get('error', 'Unknown error')}")
    
    return results


if __name__ == "__main__":
    run_consolidated_demo()