#!/usr/bin/env python3
"""
Test script for Deep Tree Echo Standardized Integration Example

This script validates that the Deep Tree Echo integration example works correctly
and demonstrates the migration pattern for complex Echo components.
"""

import sys
import logging
from pathlib import Path

# Add current directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from deep_tree_echo_standardized_example import (
    DeepTreeEchoStandardized, create_deep_tree_echo_standardized,
    create_legacy_compatible_echo, DEEP_TREE_ECHO_AVAILABLE
)
from echo_component_base import (
    EchoConfig, EchoResponse, validate_echo_component, get_echo_component_info
)


def test_component_creation():
    """Test creating the standardized component"""
    print("🧪 Testing Component Creation...")
    
    # Test factory function
    component = create_deep_tree_echo_standardized(
        echo_threshold=0.8,
        max_depth=15,
        component_name="TestDeepTreeEcho"
    )
    
    assert validate_echo_component(component)
    assert isinstance(component, DeepTreeEchoStandardized)
    assert component.config.component_name == "TestDeepTreeEcho"
    assert component.config.echo_threshold == 0.8
    assert component.echo_threshold == 0.8
    assert component.tree_max_depth == 15
    
    print("  ✅ Component Creation tests passed")


def test_initialization():
    """Test component initialization"""
    print("🧪 Testing Initialization...")
    
    component = create_deep_tree_echo_standardized(component_name="InitTest")
    
    # Test initialization
    init_result = component.initialize()
    
    if DEEP_TREE_ECHO_AVAILABLE:
        assert init_result.success is True
        assert component._initialized is True
        assert component.legacy_echo is not None
        assert "initialized successfully" in init_result.message
    else:
        # Should fail gracefully if dependencies not available
        assert init_result.success is False
        assert "dependencies not available" in init_result.message
    
    print("  ✅ Initialization tests passed")


def test_tree_operations():
    """Test tree creation and manipulation operations"""
    print("🧪 Testing Tree Operations...")
    
    if not DEEP_TREE_ECHO_AVAILABLE:
        print("  ⚠️  Skipping tree operations tests - dependencies not available")
        return
    
    component = create_deep_tree_echo_standardized(component_name="TreeTest")
    init_result = component.initialize()
    assert init_result.success is True
    
    # Test tree creation
    tree_result = component.process(
        "Root of knowledge",
        operation="create_tree",
        tree_id="test_tree"
    )
    assert tree_result.success is True
    assert tree_result.data['tree_id'] == "test_tree"
    assert tree_result.data['root_content'] == "Root of knowledge"
    
    # Test adding child
    child_result = component.process(
        "Branch of understanding",
        operation="add_child",
        tree_id="test_tree"
    )
    assert child_result.success is True
    assert child_result.data['child_content'] == "Branch of understanding"
    
    # Test tree analysis
    analysis_result = component.process(
        None,
        operation="analyze_tree",
        tree_id="test_tree"
    )
    assert analysis_result.success is True
    assert 'content' in analysis_result.data
    assert 'child_count' in analysis_result.data
    
    # Test tree list
    list_result = component.get_tree_list()
    assert list_result.success is True
    assert len(list_result.data) >= 1
    
    print("  ✅ Tree Operations tests passed")


def test_echo_operations():
    """Test echo operations"""
    print("🧪 Testing Echo Operations...")
    
    if not DEEP_TREE_ECHO_AVAILABLE:
        print("  ⚠️  Skipping echo operations tests - dependencies not available")
        return
    
    component = create_deep_tree_echo_standardized(component_name="EchoTest")
    init_result = component.initialize()
    assert init_result.success is True
    
    # Test echo operation
    echo_result = component.echo("Test echo content", echo_value=0.75)
    assert echo_result.success is True
    assert echo_result.data is not None
    assert echo_result.metadata['echo_value'] == 0.75
    
    # Verify echo created a temporary tree and stored results
    assert 'tree_id' in echo_result.metadata
    assert 'memory_key' in echo_result.metadata
    
    print("  ✅ Echo Operations tests passed")


def test_memory_integration():
    """Test memory storage and retrieval"""
    print("🧪 Testing Memory Integration...")
    
    component = create_deep_tree_echo_standardized(component_name="MemoryTest")
    
    # Test memory operations directly
    store_result = component.store_memory("test_key", {"test": "data"})
    assert store_result.success is True
    
    retrieve_result = component.retrieve_memory("test_key")
    assert retrieve_result.success is True
    assert retrieve_result.data == {"test": "data"}
    
    # Test memory stats
    assert component.memory_stats['size'] >= 1
    
    print("  ✅ Memory Integration tests passed")


def test_error_handling():
    """Test error handling capabilities"""
    print("🧪 Testing Error Handling...")
    
    component = create_deep_tree_echo_standardized(component_name="ErrorTest")
    
    if not DEEP_TREE_ECHO_AVAILABLE:
        # Test that operations fail gracefully without initialization
        error_result = component.process(
            "test content",
            operation="add_child", 
            tree_id="non_existent_tree"
        )
        assert error_result.success is False
        assert "dependencies not available" in error_result.message
    else:
        # Initialize for full testing
        init_result = component.initialize()
        assert init_result.success is True
        
        # Test operation on non-existent tree
        error_result = component.process(
            "test content",
            operation="add_child",
            tree_id="non_existent_tree"
        )
        assert error_result.success is False
        assert "not found" in error_result.message
        
        # Test invalid operation
        invalid_result = component.process(
            "test content",
            operation="invalid_operation"
        )
        assert invalid_result.success is False
        assert "Unknown operation" in invalid_result.message
    
    print("  ✅ Error Handling tests passed")


def test_legacy_compatibility():
    """Test legacy compatibility features"""
    print("🧪 Testing Legacy Compatibility...")
    
    # Test legacy-compatible factory
    legacy_component = create_legacy_compatible_echo(echo_threshold=0.9, max_depth=20)
    assert validate_echo_component(legacy_component)
    assert legacy_component.echo_threshold == 0.9
    assert legacy_component.tree_max_depth == 20
    
    print("  ✅ Legacy Compatibility tests passed")


def test_component_info():
    """Test component information functionality"""
    print("🧪 Testing Component Info...")
    
    component = create_deep_tree_echo_standardized(
        component_name="InfoTest",
        echo_threshold=0.85
    )
    
    # Get component info
    info = get_echo_component_info(component)
    
    assert info['component_name'] == "InfoTest"
    assert info['type'] == "DeepTreeEchoStandardized"
    assert info['has_memory'] is True
    assert info['has_processing'] is False
    assert info['config']['echo_threshold'] == 0.85
    
    print("  ✅ Component Info tests passed")


def test_configuration_handling():
    """Test custom configuration handling"""
    print("🧪 Testing Configuration Handling...")
    
    config = EchoConfig(
        component_name="CustomConfigTest",
        version="2.0.0",
        echo_threshold=0.95,
        max_depth=25,
        custom_params={
            'echo_threshold': 0.88,  # Override
            'tree_max_depth': 30,    # Override
            'use_julia': True,
            'spatial_awareness': False
        }
    )
    
    component = DeepTreeEchoStandardized(config)
    
    # Verify custom parameters are used
    assert component.echo_threshold == 0.88  # From custom_params
    assert component.tree_max_depth == 30    # From custom_params
    assert component.use_julia is True
    assert component.spatial_awareness is False
    
    print("  ✅ Configuration Handling tests passed")


def test_cleanup_operations():
    """Test cleanup and reset operations"""
    print("🧪 Testing Cleanup Operations...")
    
    if not DEEP_TREE_ECHO_AVAILABLE:
        print("  ⚠️  Skipping cleanup tests - dependencies not available")
        return
    
    component = create_deep_tree_echo_standardized(component_name="CleanupTest")
    init_result = component.initialize()
    assert init_result.success is True
    
    # Create some trees
    component.process("Tree 1", operation="create_tree", tree_id="tree1")
    component.process("Tree 2", operation="create_tree", tree_id="tree2")
    
    # Verify trees exist
    list_result = component.get_tree_list()
    assert len(list_result.data) == 2
    
    # Clear all trees
    clear_result = component.clear_trees()
    assert clear_result.success is True
    
    # Verify trees are cleared
    list_result = component.get_tree_list()
    assert len(list_result.data) == 0
    
    print("  ✅ Cleanup Operations tests passed")


def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Deep Tree Echo Integration Example Tests")
    print("=" * 65)
    
    if not DEEP_TREE_ECHO_AVAILABLE:
        print("⚠️  Warning: Deep Tree Echo dependencies not available")
        print("   Some tests will be skipped, but basic integration tests will run")
        print("")
    
    try:
        test_component_creation()
        test_initialization()
        test_tree_operations()
        test_echo_operations()
        test_memory_integration()
        test_error_handling()
        test_legacy_compatibility()
        test_component_info()
        test_configuration_handling()
        test_cleanup_operations()
        
        print("\n" + "=" * 65)
        print("✅ All integration example tests passed!")
        print("\n🎯 Deep Tree Echo integration example is ready for:")
        print("  - Standardized API usage across Echo ecosystem")
        print("  - Memory-based tree storage and retrieval")
        print("  - Complex multi-operation processing workflows")
        print("  - Backward compatibility with existing code")
        print("  - Enhanced error handling and logging")
        
        if DEEP_TREE_ECHO_AVAILABLE:
            print("\n🌟 Full functionality available with Deep Tree Echo dependencies")
        else:
            print("\n📦 Install Deep Tree Echo dependencies for full functionality")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Suppress logging during tests
    logging.getLogger().setLevel(logging.WARNING)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)