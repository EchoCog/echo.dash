#!/usr/bin/env python3
"""
Test script for Standardized Echoself Demo Component

This comprehensive test suite validates the standardized echoself_demo_standardized.py 
module to ensure it properly implements Echo component interfaces while maintaining
backward compatibility and supporting the Deep Tree Echo ecosystem integration.

The test suite covers:
- Unit testing of core functionality 
- Integration testing with cognitive architecture
- Performance benchmarking and optimization validation
- Error resilience and edge case handling
- Concurrent operation safety
- Memory usage patterns and leak detection
- Component lifecycle management
- Unified interface compliance
- Migration compatibility scenarios

Usage:
    python test_echoself_demo_standardized.py                # Run standard test suite
    python test_echoself_demo_standardized.py --integration  # Run integration tests only

This test is part of the Deep Tree Echo Fragment Analysis initiative to ensure
all components meet unified architectural standards.
"""

import unittest
import logging
import sys
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add the current directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import the modules under test
try:
    from echoself_demo_standardized import (
        EchoselfDemoStandardized, create_echoself_demo_system,
        setup_logging, demonstrate_introspection_cycle
    )
    from echo_component_base import EchoConfig, EchoResponse, validate_echo_component
    ECHOSELF_DEMO_STANDARDIZED_AVAILABLE = True
except ImportError as e:
    ECHOSELF_DEMO_STANDARDIZED_AVAILABLE = False
    print(f"Warning: Could not import echoself_demo_standardized: {e}")


class TestEchoselfDemoStandardized(unittest.TestCase):
    """Test cases for standardized Echoself demo component"""

    def setUp(self):
        """Set up test fixtures"""
        # Suppress logging output during tests
        logging.getLogger().setLevel(logging.CRITICAL)

    def test_import_standardized_module(self):
        """Test that standardized module can be imported"""
        if not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE:
            self.skipTest("echoself_demo_standardized module not available")
        
        self.assertTrue(ECHOSELF_DEMO_STANDARDIZED_AVAILABLE)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_component_creation(self):
        """Test creating the standardized component"""
        config = EchoConfig(component_name="TestEchoselfDemo", debug_mode=True)
        component = EchoselfDemoStandardized(config)
        
        # Test basic attributes
        self.assertEqual(component.config.component_name, "TestEchoselfDemo")
        self.assertIsNotNone(component.logger)
        self.assertEqual(component.demo_cycles_completed, 0)
        self.assertEqual(len(component.introspection_results), 0)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_component_validation(self):
        """Test that component passes validation"""
        config = EchoConfig(component_name="TestEchoselfDemo")
        component = EchoselfDemoStandardized(config)
        
        # Component should be valid
        self.assertTrue(validate_echo_component(component))

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    @patch('echoself_demo_standardized.CognitiveArchitecture')
    def test_initialization_success(self, mock_cognitive_arch):
        """Test successful component initialization"""
        # Mock cognitive architecture
        mock_system = Mock()
        mock_system.echoself_introspection = Mock()
        mock_cognitive_arch.return_value = mock_system
        
        config = EchoConfig(component_name="TestEchoselfDemo")
        component = EchoselfDemoStandardized(config)
        
        # Temporarily enable cognitive architecture
        import echoself_demo_standardized
        original_available = echoself_demo_standardized.COGNITIVE_ARCHITECTURE_AVAILABLE
        echoself_demo_standardized.COGNITIVE_ARCHITECTURE_AVAILABLE = True
        
        try:
            # Initialize should succeed
            result = component.initialize()
            
            self.assertTrue(result.success)
            self.assertIn("initialized", result.message)
            self.assertTrue(component._initialized)
            self.assertIsNotNone(component.cognitive_system)
        finally:
            echoself_demo_standardized.COGNITIVE_ARCHITECTURE_AVAILABLE = original_available

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_initialization_failure_no_cognitive_arch(self):
        """Test initialization failure when cognitive architecture unavailable"""
        # Test with the actual module (cognitive architecture may not be available)
        config = EchoConfig(component_name="TestEchoselfDemo")
        component = EchoselfDemoStandardized(config)
        
        # This might fail if cognitive architecture is not available
        result = component.initialize()
        
        if not result.success:
            # If it failed, should have appropriate error message
            self.assertIn("not available", result.message.lower())
            self.assertFalse(component._initialized)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_echo_operation(self):
        """Test echo operation"""
        config = EchoConfig(component_name="TestEchoselfDemo")
        component = EchoselfDemoStandardized(config)
        
        # Echo should work even without initialization
        result = component.echo("test_data", echo_value=0.75)
        
        self.assertTrue(result.success)
        self.assertEqual(result.data['echo_value'], 0.75)
        self.assertIn('demo_state', result.data)
        self.assertEqual(result.data['demo_state']['cycles_completed'], 0)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_process_without_initialization(self):
        """Test that process fails gracefully when not initialized"""
        config = EchoConfig(component_name="TestEchoselfDemo")
        component = EchoselfDemoStandardized(config)
        
        # Process should fail if not initialized
        result = component.process("test_operation")
        
        self.assertFalse(result.success)
        self.assertIn("not initialized", result.message)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    @patch('echoself_demo_standardized.CognitiveArchitecture')
    def test_process_supported_operations(self, mock_cognitive_arch):
        """Test processing of supported operations"""
        # Mock cognitive architecture
        mock_system = Mock()
        mock_system.echoself_introspection = Mock()
        mock_system.echoself_introspection.adaptive_attention.return_value = 0.5
        mock_system.perform_recursive_introspection.return_value = "test prompt"
        mock_system.get_introspection_metrics.return_value = {"test": "metrics"}
        mock_system.adaptive_goal_generation_with_introspection.return_value = []
        mock_cognitive_arch.return_value = mock_system
        
        config = EchoConfig(component_name="TestEchoselfDemo")
        component = EchoselfDemoStandardized(config)
        
        # Set up cognitive system directly for testing
        component.cognitive_system = mock_system
        component._initialized = True
        
        # Test introspection cycle operation
        result = component.process("introspection_cycle")
        self.assertTrue(result.success)
        self.assertIn("cycle", result.message)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    @patch('echoself_demo_standardized.CognitiveArchitecture')
    def test_process_invalid_operation(self, mock_cognitive_arch):
        """Test processing of invalid operation"""
        # Mock cognitive architecture
        mock_system = Mock()
        mock_system.echoself_introspection = Mock()
        mock_cognitive_arch.return_value = mock_system
        
        config = EchoConfig(component_name="TestEchoselfDemo")
        component = EchoselfDemoStandardized(config)
        
        # Set up cognitive system directly for testing
        component.cognitive_system = mock_system
        component._initialized = True
        
        # Test invalid operation
        result = component.process("invalid_operation")
        self.assertFalse(result.success)
        self.assertIn("Unknown operation", result.message)
        self.assertIn("valid_operations", result.metadata)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_cleanup_demo_files(self):
        """Test cleanup functionality"""
        config = EchoConfig(component_name="TestEchoselfDemo")
        component = EchoselfDemoStandardized(config)
        
        # Test cleanup (should work even without files)
        result = component.cleanup_demo_files()
        self.assertTrue(result.success)
        self.assertIn("cleaned_files", result.data)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_factory_function(self):
        """Test factory function for creating demo system"""
        # This test might fail if cognitive architecture is not available
        try:
            demo = create_echoself_demo_system()
            self.assertIsInstance(demo, EchoselfDemoStandardized)
            self.assertTrue(demo._initialized)
        except RuntimeError as e:
            # Expected if cognitive architecture is not available
            self.assertIn("Failed to initialize", str(e))

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_backward_compatibility_setup_logging(self):
        """Test backward compatibility function setup_logging"""
        # Should not raise an exception
        setup_logging()
        
        # Check that logging is configured
        root_logger = logging.getLogger()
        self.assertGreaterEqual(len(root_logger.handlers), 1)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_backward_compatibility_demonstrate_introspection_cycle(self):
        """Test backward compatibility function"""
        # Mock cognitive system
        mock_cognitive_system = Mock()
        mock_cognitive_system.perform_recursive_introspection.return_value = "test prompt"
        mock_cognitive_system.get_introspection_metrics.return_value = {
            "test_metric": "value",
            "highest_salience_files": [("test.py", 0.8)]
        }
        mock_cognitive_system.adaptive_goal_generation_with_introspection.return_value = [
            Mock(description="test goal", priority=0.9, context={"type": "test"})
        ]
        
        # Redirect stdout to capture output
        from io import StringIO
        import sys
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            demonstrate_introspection_cycle(mock_cognitive_system, 1)
            output = sys.stdout.getvalue()
            
            # Check that expected content is in output
            self.assertIn("RECURSIVE INTROSPECTION CYCLE 1", output)
            self.assertIn("test prompt", output)
            self.assertIn("test goal", output)
            
        finally:
            sys.stdout = old_stdout

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_standard_response_format(self):
        """Test that all operations return EchoResponse objects"""
        config = EchoConfig(component_name="TestEchoselfDemo")
        component = EchoselfDemoStandardized(config)
        
        # Test initialize
        result = component.initialize()
        self.assertIsInstance(result, EchoResponse)
        
        # Test echo
        result = component.echo("test")
        self.assertIsInstance(result, EchoResponse)
        
        # Test process (even when not initialized)
        result = component.process("test")
        self.assertIsInstance(result, EchoResponse)
        
        # Test cleanup
        result = component.cleanup_demo_files()
        self.assertIsInstance(result, EchoResponse)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_error_handling(self):
        """Test standardized error handling"""
        config = EchoConfig(component_name="TestEchoselfDemo")
        component = EchoselfDemoStandardized(config)
        
        # Mock a method to raise an exception
        original_method = component._demonstrate_introspection_cycle
        def failing_method(*args, **kwargs):
            raise ValueError("Test error")
        component._demonstrate_introspection_cycle = failing_method
        
        # Initialize with mock
        with patch('echoself_demo_standardized.CognitiveArchitecture'):
            component._initialized = True
            component.cognitive_system = Mock()
            
            # Process should handle the error gracefully
            result = component.process("introspection_cycle")
            self.assertFalse(result.success)
            self.assertIn("Test error", result.message)
            self.assertIn("error_type", result.metadata)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_component_info_compatibility(self):
        """Test that component provides expected information"""
        config = EchoConfig(component_name="TestEchoselfDemo", version="1.2.3")
        component = EchoselfDemoStandardized(config)
        
        # Test status
        status = component.get_status()
        self.assertTrue(status.success)
        self.assertIn("component_name", status.data)
        self.assertEqual(status.data["component_name"], "TestEchoselfDemo")
        self.assertEqual(status.data["version"], "1.2.3")

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_component_metadata_validation(self):
        """Test comprehensive component metadata validation"""
        config = EchoConfig(
            component_name="MetadataTestDemo", 
            version="2.0.0",
            echo_threshold=0.8,
            debug_mode=True,
            custom_params={"test_param": "test_value"}
        )
        component = EchoselfDemoStandardized(config)
        
        # Test comprehensive status information
        status = component.get_status()
        self.assertTrue(status.success)
        
        # Validate all expected metadata fields
        data = status.data
        self.assertIn("component_name", data)
        self.assertIn("version", data)
        self.assertIn("initialized", data)
        self.assertIn("state_keys", data)
        self.assertIn("config", data)
        
        # Validate config details
        config_data = data["config"]
        self.assertEqual(config_data["echo_threshold"], 0.8)
        self.assertIn("max_depth", config_data)
        self.assertTrue(config_data["debug_mode"])

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    @patch('echoself_demo_standardized.CognitiveArchitecture')
    def test_integration_with_cognitive_architecture(self, mock_cognitive_arch):
        """Test comprehensive integration scenarios with cognitive architecture"""
        # Mock a complete cognitive architecture system
        mock_system = Mock()
        mock_introspection = Mock()
        mock_system.echoself_introspection = mock_introspection
        
        # Set up realistic mock behaviors
        mock_introspection.adaptive_attention.return_value = 0.6
        mock_system.perform_recursive_introspection.return_value = "Generated introspection prompt for testing integration"
        mock_system.get_introspection_metrics.return_value = {
            "total_files_analyzed": 42,
            "highest_salience_files": [("test_file.py", 0.95), ("integration.py", 0.87)],
            "attention_threshold_used": 0.6,
            "processing_time": 1.23
        }
        mock_system.adaptive_goal_generation_with_introspection.return_value = [
            Mock(description="Enhance integration testing", priority=0.9, context={"type": "enhancement"}),
            Mock(description="Optimize performance", priority=0.8, context={"type": "optimization"})
        ]
        mock_system.export_introspection_data.return_value = True
        mock_system.memories = ["memory1", "memory2", "memory3"]
        mock_system.goals = ["goal1", "goal2"]
        
        mock_cognitive_arch.return_value = mock_system
        
        # Test full integration workflow
        config = EchoConfig(component_name="IntegrationTestDemo")
        component = EchoselfDemoStandardized(config)
        
        # Enable cognitive architecture for testing
        import echoself_demo_standardized
        original_available = echoself_demo_standardized.COGNITIVE_ARCHITECTURE_AVAILABLE
        echoself_demo_standardized.COGNITIVE_ARCHITECTURE_AVAILABLE = True
        
        try:
            # Initialize and run full demonstration
            init_result = component.initialize()
            self.assertTrue(init_result.success)
            
            # Test full demo integration
            demo_result = component.process('full_demo')
            self.assertTrue(demo_result.success)
            
            # Validate integration results
            demo_data = demo_result.data
            self.assertIn('stages', demo_data)
            self.assertIn('summary', demo_data)
            
            stages = demo_data['stages']
            self.assertIn('introspection_cycle_1', stages)
            self.assertIn('adaptive_attention', stages)
            self.assertIn('hypergraph_export', stages)
            self.assertIn('neural_symbolic_synergy', stages)
            
            # Verify all stages completed successfully
            for stage_name, stage_result in stages.items():
                self.assertTrue(stage_result['success'], 
                              f"Stage {stage_name} should have succeeded")
            
            # Test that cognitive architecture methods were called appropriately
            mock_system.perform_recursive_introspection.assert_called()
            mock_system.get_introspection_metrics.assert_called()
            mock_system.adaptive_goal_generation_with_introspection.assert_called()
            mock_system.export_introspection_data.assert_called()
            
        finally:
            echoself_demo_standardized.COGNITIVE_ARCHITECTURE_AVAILABLE = original_available

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    @patch('echoself_demo_standardized.CognitiveArchitecture')
    def test_performance_benchmarking(self, mock_cognitive_arch):
        """Test performance characteristics and benchmarking"""
        import time
        
        # Mock cognitive architecture with timing simulation
        mock_system = Mock()
        mock_system.echoself_introspection = Mock()
        mock_system.echoself_introspection.adaptive_attention.return_value = 0.5
        
        def slow_introspection(*args, **kwargs):
            time.sleep(0.01)  # Simulate processing time
            return "Performance test introspection prompt"
        
        mock_system.perform_recursive_introspection.side_effect = slow_introspection
        mock_system.get_introspection_metrics.return_value = {"test": "metrics"}
        mock_system.adaptive_goal_generation_with_introspection.return_value = []
        
        mock_cognitive_arch.return_value = mock_system
        
        config = EchoConfig(component_name="PerformanceTestDemo")
        component = EchoselfDemoStandardized(config)
        component.cognitive_system = mock_system
        component._initialized = True
        
        # Benchmark individual operations
        operations = [
            ('introspection_cycle', {}),
            ('adaptive_attention', {}),
            ('hypergraph_export', {}),
        ]
        
        performance_results = {}
        
        for operation, params in operations:
            start_time = time.time()
            result = component.process(operation, **params)
            execution_time = time.time() - start_time
            
            performance_results[operation] = {
                'success': result.success,
                'execution_time': execution_time,
                'has_timing_metadata': 'introspection_time' in result.metadata
            }
            
            # Basic performance assertions
            self.assertLess(execution_time, 5.0, f"{operation} should complete within 5 seconds")
            if operation == 'introspection_cycle':
                self.assertIn('introspection_time', result.metadata)
        
        # Verify all operations completed successfully
        for operation, perf_data in performance_results.items():
            self.assertTrue(perf_data['success'], f"{operation} should have succeeded")

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_edge_cases_and_resilience(self):
        """Test edge cases and error resilience scenarios"""
        config = EchoConfig(component_name="EdgeCaseTestDemo")
        component = EchoselfDemoStandardized(config)
        
        # Test with None input
        result = component.echo(None, 0.5)
        self.assertTrue(result.success)  # Should handle None gracefully
        
        # Test with empty string
        result = component.echo("", 0.0)
        self.assertTrue(result.success)
        
        # Test with extreme echo values
        result = component.echo("test", -1.0)
        self.assertTrue(result.success)
        
        result = component.echo("test", 2.0)
        self.assertTrue(result.success)
        
        # Test with complex data structures
        complex_data = {
            'nested': {
                'list': [1, 2, {'inner': 'value'}],
                'tuple': (1, 2, 3),
                'set': {1, 2, 3}
            },
            'unicode': 'test 🌳 unicode',
            'number': 42.5
        }
        result = component.echo(complex_data, 0.75)
        self.assertTrue(result.success)
        
        # Test process with invalid input types
        result = component.process({'invalid': 'structure', 'no_operation': True})
        self.assertFalse(result.success)  # Should fail gracefully for uninitialized component

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_concurrent_operations(self):
        """Test component behavior under concurrent access"""
        import threading
        import time
        
        config = EchoConfig(component_name="ConcurrencyTestDemo")
        component = EchoselfDemoStandardized(config)
        
        results = []
        errors = []
        
        def echo_operation(thread_id):
            try:
                for i in range(3):
                    result = component.echo(f"thread_{thread_id}_data_{i}", 0.5)
                    results.append((thread_id, i, result.success))
                    time.sleep(0.001)  # Small delay
            except Exception as e:
                errors.append((thread_id, str(e)))
        
        # Create and start multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=echo_operation, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=10)
        
        # Validate results
        self.assertEqual(len(errors), 0, f"No errors should occur during concurrent operations: {errors}")
        self.assertEqual(len(results), 9, "Should have 9 results from 3 threads * 3 operations each")
        
        # All operations should succeed
        for thread_id, op_id, success in results:
            self.assertTrue(success, f"Operation {op_id} on thread {thread_id} should succeed")

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_memory_usage_patterns(self):
        """Test memory usage and potential leaks during operations"""
        import gc
        
        config = EchoConfig(component_name="MemoryTestDemo")
        component = EchoselfDemoStandardized(config)
        
        # Get initial memory state
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        # Perform multiple operations that create and store data
        for i in range(10):
            component.echo(f"memory_test_data_{i}" * 100, 0.5)  # Create larger data
            if i % 5 == 0:
                gc.collect()  # Force garbage collection periodically
        
        # Add to introspection results (simulating real usage)
        for i in range(5):
            component.introspection_results.append({
                'cycle': i,
                'large_data': 'x' * 1000,
                'timestamp': f"2023-test-{i}"
            })
        
        # Check memory growth
        gc.collect()
        final_objects = len(gc.get_objects())
        memory_growth = final_objects - initial_objects
        
        # Memory growth should be reasonable (not excessive)
        self.assertLess(memory_growth, 1000, 
                       f"Memory growth ({memory_growth} objects) should be reasonable")
        
        # Test cleanup
        cleanup_result = component.cleanup_demo_files()
        self.assertTrue(cleanup_result.success)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_component_lifecycle_management(self):
        """Test complete component lifecycle including reset and reinitialization"""
        config = EchoConfig(component_name="LifecycleTestDemo")
        component = EchoselfDemoStandardized(config)
        
        # Initial state
        self.assertFalse(component._initialized)
        self.assertEqual(component.demo_cycles_completed, 0)
        self.assertEqual(len(component.introspection_results), 0)
        
        # Initialize
        init_result = component.initialize()
        # Will fail due to no cognitive architecture, but state should be updated
        
        # Add some data
        component.demo_cycles_completed = 5
        component.introspection_results = [{'test': 'data'}]
        
        # Test reset
        reset_result = component.reset()
        self.assertTrue(reset_result.success)
        self.assertFalse(component._initialized)
        self.assertEqual(len(component.state), 0)
        
        # Component-specific state should remain (as it's not part of base state)
        self.assertEqual(component.demo_cycles_completed, 5)  # This should remain
        self.assertEqual(len(component.introspection_results), 1)  # This should remain
        
        # Test that component can be reinitialized
        reinit_result = component.initialize()
        # Test should work regardless of cognitive architecture availability


    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_unified_interface_compliance(self):
        """Test compliance with unified Echo component interface standards"""
        config = EchoConfig(component_name="UnifiedInterfaceTestDemo")
        component = EchoselfDemoStandardized(config)
        
        # Test that all required Echo methods exist and return EchoResponse
        required_methods = ['initialize', 'process', 'echo', 'get_status', 'reset']
        
        for method_name in required_methods:
            self.assertTrue(hasattr(component, method_name), 
                          f"Component should have {method_name} method")
            method = getattr(component, method_name)
            self.assertTrue(callable(method), f"{method_name} should be callable")
        
        # Test that all methods return EchoResponse objects
        response_methods = [
            (component.initialize, []),
            (component.echo, ["test_data", 0.5]),
            (component.get_status, []),
            (component.reset, [])
        ]
        
        for method, args in response_methods:
            result = method(*args)
            self.assertIsInstance(result, EchoResponse, 
                                f"{method.__name__} should return EchoResponse")
            self.assertIsInstance(result.success, bool)
            self.assertIsInstance(result.message, str)
            self.assertIsInstance(result.metadata, dict)
        
        # Test process method with various input types
        process_inputs = [
            "string_input",
            {"operation": "introspection_cycle"},
            {"operation": "invalid_operation"}
        ]
        
        for input_data in process_inputs:
            result = component.process(input_data)
            self.assertIsInstance(result, EchoResponse)

    @unittest.skipIf(not ECHOSELF_DEMO_STANDARDIZED_AVAILABLE, "Module not available")
    def test_migration_compatibility_scenarios(self):
        """Test backward compatibility and migration scenarios"""
        # Test factory function still works
        try:
            demo = create_echoself_demo_system()
            self.assertIsInstance(demo, EchoselfDemoStandardized)
            # May fail to initialize due to missing cognitive architecture
        except RuntimeError as e:
            # Expected if cognitive architecture is not available
            self.assertIn("Failed to initialize", str(e))
        
        # Test legacy functions still work
        setup_logging()  # Should not raise exception
        
        # Test legacy demonstrate_introspection_cycle function
        mock_cognitive_system = Mock()
        mock_cognitive_system.perform_recursive_introspection.return_value = "test prompt"
        mock_cognitive_system.get_introspection_metrics.return_value = {
            "highest_salience_files": [("test.py", 0.8)]
        }
        mock_cognitive_system.adaptive_goal_generation_with_introspection.return_value = [
            Mock(description="test goal", priority=0.9, context={"type": "test"})
        ]
        
        # Capture output to verify function works
        from io import StringIO
        import sys
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            demonstrate_introspection_cycle(mock_cognitive_system, 1)
            output = sys.stdout.getvalue()
            self.assertIn("RECURSIVE INTROSPECTION CYCLE 1", output)
        finally:
            sys.stdout = old_stdout
        
        # Test that new standardized interface is preferred but old interface still works
        config = EchoConfig(component_name="MigrationTestDemo")
        component = EchoselfDemoStandardized(config)
        
        # New interface
        status = component.get_status()
        self.assertTrue(status.success)
        
        # Component should validate as proper Echo component
        self.assertTrue(validate_echo_component(component))


def run_integration_test_suite():
    """Run comprehensive integration test suite with detailed reporting"""
    import time
    
    print("🧪 Running Echoself Demo Standardized Integration Test Suite")
    print("=" * 60)
    
    # Create test suite focusing on integration tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add specific integration-focused test methods
    integration_test_methods = [
        'test_integration_with_cognitive_architecture',
        'test_performance_benchmarking', 
        'test_edge_cases_and_resilience',
        'test_concurrent_operations',
        'test_memory_usage_patterns',
        'test_component_lifecycle_management',
        'test_unified_interface_compliance',
        'test_migration_compatibility_scenarios'
    ]
    
    for method_name in integration_test_methods:
        suite.addTest(TestEchoselfDemoStandardized(method_name))
    
    # Run tests with detailed reporting
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    start_time = time.time()
    result = runner.run(suite)
    execution_time = time.time() - start_time
    
    # Print summary
    print("\n" + "=" * 60)
    print("🏁 Integration Test Suite Summary")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    print(f"Execution time: {execution_time:.2f} seconds")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n🚨 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\n✅ Success rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()


def main():
    """Run the test suite with options for integration testing"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--integration':
        # Run integration-focused test suite
        success = run_integration_test_suite()
        sys.exit(0 if success else 1)
    else:
        # Run standard test suite
        unittest.main(verbosity=2)


if __name__ == '__main__':
    main()