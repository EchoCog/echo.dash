#!/usr/bin/env python3
"""
Consolidated Test Suite for Unified Echo Memory System

This consolidates all memory-related tests from the fragmented test files:
- test_echo_memory_demo_standardized.py
- test_memory_integration.py 
- test_unified_memory.py
- test_unified_echo_memory_standardized.py

This addresses the "Fragmented Memory System" issue by providing a single
comprehensive test suite for all memory functionality.
"""

import sys
import unittest
import tempfile
import logging
import json
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import all memory components
from unified_echo_memory import (
    UnifiedEchoMemory, EchoMemoryConfig, create_unified_memory_system, 
    MemoryType, MemoryNode, HypergraphMemory
)
from echo_component_base import EchoConfig, EchoResponse, validate_echo_component
from memory_adapter import MemoryAdapter, get_memory_adapter
from memory_management import memory_system
from echo_memory_demo_standardized import EchoMemoryDemoStandardized, create_memory_demo_system

# Suppress logging during tests
logging.getLogger().setLevel(logging.CRITICAL)


class TestUnifiedEchoMemoryConsolidated(unittest.TestCase):
    """
    Consolidated test suite for all memory system functionality
    
    This replaces multiple fragmented test files with a single comprehensive suite
    """
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Standard configurations for testing
        self.echo_config = EchoConfig(
            component_name="TestUnifiedMemory",
            version="1.0.0",
            echo_threshold=0.75
        )
        
        self.memory_config = EchoMemoryConfig(
            memory_storage_path=self.temp_dir,
            working_memory_capacity=5,
            auto_save_interval=60
        )
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up temp directory if needed
        import shutil
        try:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass
    
    # =========================================================================
    # CORE UNIFIED MEMORY SYSTEM TESTS
    # =========================================================================
    
    def test_unified_memory_creation(self):
        """Test creating unified memory system"""
        memory_system = UnifiedEchoMemory(self.echo_config, self.memory_config)
        
        # Test initialization
        result = memory_system.initialize()
        self.assertTrue(result.success)
        self.assertIn("initialized", result.message.lower())
        self.assertTrue(memory_system._initialized)
    
    def test_memory_storage_and_retrieval(self):
        """Test basic memory storage and retrieval operations"""
        memory_system = UnifiedEchoMemory(self.echo_config, self.memory_config)
        memory_system.initialize()
        
        # Store a memory
        store_result = memory_system.store_memory(
            content="Test memory content",
            memory_type=MemoryType.DECLARATIVE,
            echo_value=0.8,
            metadata={"test": True}
        )
        
        self.assertTrue(store_result.success)
        self.assertIsNotNone(store_result.data.get('memory_id'))
        
        # Retrieve the memory
        memory_id = store_result.data['memory_id']
        retrieve_result = memory_system.retrieve_memory(memory_id)
        
        self.assertTrue(retrieve_result.success)
        self.assertEqual(retrieve_result.data['content'], "Test memory content")
        self.assertEqual(retrieve_result.data['memory_type'], 'declarative')
        self.assertEqual(retrieve_result.data['echo_value'], 0.8)
    
    def test_memory_search(self):
        """Test memory search functionality"""
        memory_system = UnifiedEchoMemory(self.echo_config, self.memory_config)
        memory_system.initialize()
        
        # Store multiple memories
        test_memories = [
            ("Important business meeting", MemoryType.EPISODIC),
            ("Python programming concepts", MemoryType.SEMANTIC),
            ("Meeting with client tomorrow", MemoryType.EPISODIC),
            ("How to ride a bicycle", MemoryType.PROCEDURAL)
        ]
        
        for content, mem_type in test_memories:
            memory_system.store_memory(content, mem_type, echo_value=0.5)
        
        # Search for memories
        search_result = memory_system.search_memories("meeting")
        
        self.assertTrue(search_result.success)
        self.assertGreater(search_result.data['result_count'], 0)
        
        # Verify search results contain relevant memories
        results = search_result.data['results']
        meeting_results = [r for r in results if 'meeting' in r['content'].lower()]
        self.assertGreater(len(meeting_results), 0)
    
    def test_memory_echo_operations(self):
        """Test echo-specific memory operations"""
        memory_system = UnifiedEchoMemory(self.echo_config, self.memory_config)
        memory_system.initialize()
        
        # Test echo operation
        echo_result = memory_system.echo("Test echo data", echo_value=0.9)
        
        self.assertTrue(echo_result.success)
        self.assertIn('echo_memory_id', echo_result.data)
        self.assertEqual(echo_result.data['echo_value'], 0.9)
        self.assertIn('resonant_memories', echo_result.data)
    
    def test_memory_overview_and_analysis(self):
        """Test memory system analysis capabilities"""
        memory_system = UnifiedEchoMemory(self.echo_config, self.memory_config)
        memory_system.initialize()
        
        # Add some test data
        for i in range(5):
            memory_system.store_memory(
                f"Test memory {i}",
                MemoryType.DECLARATIVE,
                echo_value=i * 0.2
            )
        
        # Get overview
        overview_result = memory_system.get_memory_overview()
        
        self.assertTrue(overview_result.success)
        self.assertEqual(overview_result.data['total_memories'], 5)
        self.assertIn('memory_type_distribution', overview_result.data)
        self.assertIn('echo_statistics', overview_result.data)
    
    # =========================================================================
    # MEMORY ADAPTER TESTS
    # =========================================================================
    
    def test_memory_adapter_functionality(self):
        """Test memory adapter provides unified interface"""
        adapter = MemoryAdapter("test_adapter")
        
        # Test adapter storage
        memory_id = adapter.store_memory(
            "Test adapter memory",
            MemoryType.DECLARATIVE,
            metadata={"adapter_test": True},
            echo_value=0.7
        )
        
        self.assertIsNotNone(memory_id)
        
        # Test adapter retrieval
        retrieved = adapter.retrieve_memory(memory_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.content, "Test adapter memory")
        self.assertEqual(retrieved.echo_value, 0.7)
    
    def test_global_memory_adapter(self):
        """Test global memory adapter singleton"""
        adapter1 = get_memory_adapter("global_test")
        adapter2 = get_memory_adapter("global_test")
        
        # Should return the same instance
        self.assertIs(adapter1, adapter2)
        
        # Test functionality
        memory_id = adapter1.store_memory("Global test", MemoryType.SEMANTIC)
        retrieved = adapter2.retrieve_memory(memory_id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.content, "Global test")
    
    def test_memory_adapter_search(self):
        """Test memory adapter search capabilities"""
        adapter = MemoryAdapter("search_test")
        
        # Add test memories with adequate echo values to pass the default threshold
        test_data = [
            ("Python is a programming language", 0.8),
            ("Machine learning uses Python", 0.9),
            ("JavaScript is for web development", 0.7)
        ]
        
        for content, echo_value in test_data:
            adapter.store_memory(content, MemoryType.SEMANTIC, echo_value=echo_value)
        
        # Search for Python-related memories
        python_memories = adapter.search_memories("Python")
        self.assertGreater(len(python_memories), 0)
        
        # Verify results
        for memory in python_memories:
            self.assertIn("Python", memory.content)
    
    # =========================================================================
    # COMPATIBILITY LAYER TESTS
    # =========================================================================
    
    def test_memory_management_compatibility(self):
        """Test that memory_management.py provides backward compatibility"""
        # Test that the compatibility layer works
        self.assertIsInstance(memory_system, HypergraphMemory)
        
        # Test basic operations through compatibility layer
        test_node = MemoryNode(
            id="test_compat",
            content="Compatibility test",
            memory_type=MemoryType.DECLARATIVE
        )
        
        node_id = memory_system.add_node(test_node)
        self.assertEqual(node_id, "test_compat")
        
        retrieved = memory_system.get_node("test_compat")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.content, "Compatibility test")
    
    # =========================================================================
    # ECHO COMPONENT VALIDATION TESTS
    # =========================================================================
    
    def test_echo_component_validation(self):
        """Test that all memory components pass Echo validation"""
        # Test UnifiedEchoMemory
        memory_system = UnifiedEchoMemory(self.echo_config, self.memory_config)
        self.assertTrue(validate_echo_component(memory_system))
        
        # Test EchoMemoryDemoStandardized
        demo_config = EchoConfig(
            component_name="test_demo",
            version="1.0.0"
        )
        demo = EchoMemoryDemoStandardized(demo_config)
        self.assertTrue(validate_echo_component(demo))
    
    def test_echo_response_format(self):
        """Test that all operations return proper EchoResponse objects"""
        memory_system = UnifiedEchoMemory(self.echo_config, self.memory_config)
        
        # Test initialization response
        init_result = memory_system.initialize()
        self.assertIsInstance(init_result, EchoResponse)
        self.assertTrue(hasattr(init_result, 'success'))
        self.assertTrue(hasattr(init_result, 'message'))
        self.assertTrue(hasattr(init_result, 'data'))
        self.assertTrue(hasattr(init_result, 'metadata'))
        
        # Test process response
        process_result = memory_system.process({
            'operation': 'store',
            'content': 'Test process memory',
            'memory_type': 'declarative'
        })
        self.assertIsInstance(process_result, EchoResponse)
        self.assertTrue(process_result.success)
    
    # =========================================================================
    # FACTORY FUNCTION TESTS
    # =========================================================================
    
    def test_create_unified_memory_system(self):
        """Test the factory function for creating memory systems"""
        memory_system = create_unified_memory_system(
            component_name="FactoryTest",
            storage_path=self.temp_dir
        )
        
        self.assertIsInstance(memory_system, UnifiedEchoMemory)
        self.assertTrue(memory_system._initialized)
        
        # Test basic functionality
        store_result = memory_system.store_memory("Factory test", MemoryType.DECLARATIVE)
        self.assertTrue(store_result.success)
    
    def test_create_memory_demo_system(self):
        """Test the demo system factory function"""
        demo_system = create_memory_demo_system()  # No arguments needed
        
        self.assertIsInstance(demo_system, EchoMemoryDemoStandardized)
        
        # Test initialization
        init_result = demo_system.initialize()
        self.assertTrue(init_result.success)
    
    # =========================================================================
    # INTEGRATION TESTS
    # =========================================================================
    
    def test_memory_system_integration(self):
        """Test integration between different memory components"""
        # Create unified memory system
        unified = create_unified_memory_system("IntegrationTest", self.temp_dir)
        
        # Create memory adapter
        adapter = MemoryAdapter("integration_adapter")
        
        # Store memory through unified system
        unified_result = unified.store_memory(
            "Integration test memory",
            MemoryType.DECLARATIVE,
            echo_value=0.8
        )
        self.assertTrue(unified_result.success)
        
        # Store memory through adapter
        adapter_memory_id = adapter.store_memory(
            "Adapter integration memory",
            MemoryType.SEMANTIC,
            echo_value=0.6
        )
        self.assertIsNotNone(adapter_memory_id)
        
        # Verify both systems can access their memories
        unified_memory_id = unified_result.data['memory_id']
        unified_retrieve = unified.retrieve_memory(unified_memory_id)
        self.assertTrue(unified_retrieve.success)
        
        adapter_retrieve = adapter.retrieve_memory(adapter_memory_id)
        self.assertIsNotNone(adapter_retrieve)
    
    def test_memory_type_consistency(self):
        """Test that MemoryType is consistent across all components"""
        # All components should use the same MemoryType enum
        from unified_echo_memory import MemoryType as UnifiedMemoryType
        from memory_adapter import MemoryType as AdapterMemoryType
        from memory_management import MemoryType as ManagementMemoryType
        
        # Should be the same enum
        self.assertIs(UnifiedMemoryType, AdapterMemoryType)
        self.assertIs(UnifiedMemoryType, ManagementMemoryType)
        
        # Test that all expected memory types are present
        expected_types = {
            'DECLARATIVE', 'EPISODIC', 'PROCEDURAL', 'SEMANTIC',
            'WORKING', 'SENSORY', 'EMOTIONAL', 'ASSOCIATIVE'
        }
        
        actual_types = {mt.name for mt in UnifiedMemoryType}
        self.assertEqual(expected_types, actual_types)
    
    # =========================================================================
    # PERFORMANCE AND STRESS TESTS
    # =========================================================================
    
    def test_memory_system_performance(self):
        """Test memory system performance with larger datasets"""
        memory_system = create_unified_memory_system("PerfTest", self.temp_dir)
        
        # Store multiple memories quickly
        start_time = time.time()
        memory_ids = []
        
        for i in range(50):  # Reasonable number for testing
            result = memory_system.store_memory(
                f"Performance test memory {i}",
                MemoryType.DECLARATIVE,
                echo_value=i / 50.0
            )
            self.assertTrue(result.success)
            memory_ids.append(result.data['memory_id'])
        
        store_time = time.time() - start_time
        
        # Retrieve memories
        start_time = time.time()
        for memory_id in memory_ids:
            result = memory_system.retrieve_memory(memory_id)
            self.assertTrue(result.success)
        
        retrieve_time = time.time() - start_time
        
        # Performance should be reasonable (less than 5 seconds for 50 operations)
        self.assertLess(store_time, 5.0)
        self.assertLess(retrieve_time, 5.0)
        
        print(f"\nPerformance Test Results:")
        print(f"  Store 50 memories: {store_time:.3f}s")
        print(f"  Retrieve 50 memories: {retrieve_time:.3f}s")
    
    def test_working_memory_capacity(self):
        """Test working memory capacity limits"""
        memory_system = UnifiedEchoMemory(self.echo_config, self.memory_config)
        memory_system.initialize()
        
        # Store more memories than working memory capacity
        for i in range(10):  # More than capacity of 5
            memory_system.store_memory(
                f"Working memory test {i}",
                MemoryType.WORKING
            )
        
        # Working memory should be limited to configured capacity
        self.assertLessEqual(
            len(memory_system.echo_working_memory),
            self.memory_config.working_memory_capacity
        )


def run_consolidated_tests():
    """Run the consolidated memory test suite"""
    print("🧪 Running Consolidated Memory System Tests")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUnifiedEchoMemoryConsolidated)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ ALL TESTS PASSED' if success else '❌ SOME TESTS FAILED'}")
    
    return success


if __name__ == "__main__":
    run_consolidated_tests()