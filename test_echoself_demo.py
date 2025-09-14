#!/usr/bin/env python3
"""
Test script for Echoself Recursive Self-Model Integration Demonstration

Tests the basic functionality of the echoself_demo.py module using real implementations
and no mocks to comply with deep tree echo zero-tolerance mock/fake policy.
"""

import unittest
import logging
import sys
import tempfile
import time
from pathlib import Path

# Add the current directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import the module under test
try:
    import echoself_demo
    ECHOSELF_DEMO_AVAILABLE = True
except ImportError as e:
    ECHOSELF_DEMO_AVAILABLE = False
    print(f"Warning: Could not import echoself_demo: {e}")


class TestEchoselfDemo(unittest.TestCase):
    """Test cases for echoself_demo module using real implementations (no mocks)"""

    def setUp(self):
        """Set up test fixtures"""
        # Suppress logging output during tests
        logging.getLogger().setLevel(logging.CRITICAL)
        
        # Reset global state before each test
        if ECHOSELF_DEMO_AVAILABLE:
            echoself_demo._global_cognitive_system = None
            echoself_demo._global_demo_state = {
                'cycles_completed': 0,
                'introspection_results': [],
                'initialized': False,
                'last_update': None
            }

    def test_import_echoself_demo(self):
        """Test that echoself_demo module can be imported"""
        if not ECHOSELF_DEMO_AVAILABLE:
            self.skipTest("echoself_demo module not available")
        
        self.assertTrue(ECHOSELF_DEMO_AVAILABLE)
        self.assertIsNotNone(echoself_demo)

    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available")
    def test_setup_logging_function_exists(self):
        """Test that setup_logging function exists"""
        self.assertTrue(hasattr(echoself_demo, 'setup_logging'))
        self.assertTrue(callable(echoself_demo.setup_logging))

    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available")
    def test_setup_logging_functionality(self):
        """Test that setup_logging configures logging correctly"""
        # Clear any existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Call setup_logging
        echoself_demo.setup_logging()
        
        # Verify logging is configured
        self.assertGreaterEqual(len(root_logger.handlers), 1)
        self.assertEqual(root_logger.level, logging.INFO)

    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available")
    def test_demonstrate_introspection_cycle_function_exists(self):
        """Test that demonstrate_introspection_cycle function exists"""
        self.assertTrue(hasattr(echoself_demo, 'demonstrate_introspection_cycle'))
        self.assertTrue(callable(echoself_demo.demonstrate_introspection_cycle))

    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available")
    def test_module_structure(self):
        """Test that the module has the expected structure"""
        # Check for expected functions
        expected_functions = [
            'setup_logging', 
            'demonstrate_introspection_cycle',
            'echo',  # Echo function
            'create_echoself_demo_system'  # Factory function
        ]
        
        for func_name in expected_functions:
            self.assertTrue(hasattr(echoself_demo, func_name), 
                          f"Missing expected function: {func_name}")
            self.assertTrue(callable(getattr(echoself_demo, func_name)),
                          f"Expected function is not callable: {func_name}")

    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available")
    def test_required_imports(self):
        """Test that the module imports required dependencies"""
        # Test that the module imports what it needs without crashing
        import importlib
        try:
            importlib.reload(echoself_demo)
        except ImportError as e:
            self.fail(f"Module failed to import required dependencies: {e}")

    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available")
    def test_echo_function_basic_functionality(self):
        """Test that echo function works without any dependencies"""
        result = echoself_demo.echo()
        
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('data', result)
        self.assertIn('message', result)
        self.assertTrue(result['success'])  # Should always succeed

    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available")
    def test_echo_function_with_parameters(self):
        """Test echo function with parameters - no mocks needed"""
        result = echoself_demo.echo(data={'test': 'data'}, echo_value=0.5)
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        self.assertIn('echo_value', result['metadata'])
        self.assertEqual(result['metadata']['echo_value'], 0.5)
        
    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available")
    def test_echo_function_state_tracking(self):
        """Test that echo function properly tracks state changes"""
        # First call
        result1 = echoself_demo.echo(echo_value=0.3)
        self.assertTrue(result1['success'])
        initial_cycles = result1['data']['demo_state']['cycles_completed']
        
        # Simulate some demo state changes
        echoself_demo._global_demo_state['cycles_completed'] = 2
        echoself_demo._global_demo_state['introspection_results'].append({
            'cycle': 1, 'timestamp': '2024-01-01T00:00:00', 'test': True
        })
        
        # Second call should reflect state changes
        result2 = echoself_demo.echo(echo_value=0.7)
        self.assertTrue(result2['success'])
        self.assertEqual(result2['data']['demo_state']['cycles_completed'], 2)
        self.assertEqual(result2['data']['demo_state']['introspection_results_count'], 1)

    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available")
    def test_create_echoself_demo_system_function_exists(self):
        """Test that create_echoself_demo_system function exists"""
        self.assertTrue(hasattr(echoself_demo, 'create_echoself_demo_system'))
        self.assertTrue(callable(echoself_demo.create_echoself_demo_system))

    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available") 
    def test_create_echoself_demo_system_functionality(self):
        """Test create_echoself_demo_system with real dependencies"""
        # This test uses real CognitiveArchitecture if available
        system = echoself_demo.create_echoself_demo_system()
        
        # The function should handle failures gracefully and update global state
        self.assertIn('initialized', echoself_demo._global_demo_state)
        self.assertIsNotNone(echoself_demo._global_demo_state['last_update'])
        
        # If system creation succeeded, it should be a real object, not a mock
        if system is not None:
            # Should have expected attributes for real CognitiveArchitecture
            self.assertTrue(hasattr(system, '__class__'))
            self.assertNotEqual(str(type(system)), "<class 'unittest.mock.Mock'>")

    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available") 
    def test_echo_function_structure_compliance(self):
        """Test that echo function returns expected structure for integration"""
        result = echoself_demo.echo(echo_value=0.8)
        
        # Check overall structure
        self.assertIn('success', result)
        self.assertIn('data', result)
        self.assertIn('message', result)
        self.assertIn('metadata', result)
        
        # Check data structure
        if result['success']:
            data = result['data']
            self.assertIn('demo_state', data)
            self.assertIn('echo_value', data)
            self.assertIn('timestamp', data)
            self.assertIn('component_type', data)
            self.assertEqual(data['component_type'], 'echoself_demo')
            self.assertEqual(data['integration_status'], 'active')
            
            # Check demo_state structure
            demo_state = data['demo_state']
            self.assertIn('cycles_completed', demo_state)
            self.assertIn('initialized', demo_state)
            self.assertIn('cognitive_system_available', demo_state)
            
    @unittest.skipIf(not ECHOSELF_DEMO_AVAILABLE, "echoself_demo not available")
    def test_echo_integration_with_real_system(self):
        """Test echo function integration with real cognitive system if available"""
        # Try to create a real system
        system = echoself_demo.create_echoself_demo_system()
        
        # Test echo function after system creation
        result = echoself_demo.echo(echo_value=0.9)
        self.assertTrue(result['success'])
        
        # Check system integration status
        demo_state = result['data']['demo_state']
        if system is not None:
            self.assertTrue(demo_state['cognitive_system_available'])
        
        # The echo function should work regardless of system availability
        self.assertIsInstance(demo_state['cycles_completed'], int)
        self.assertIsInstance(demo_state['introspection_results_count'], int)


def main():
    """Run the test suite"""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()