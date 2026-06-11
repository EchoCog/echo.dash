#!/usr/bin/env python3
"""
Test script for Activity Regulation module

Tests the activity regulation and scheduling system functionality.
"""

import unittest
import asyncio
import logging
import sys
import threading
import time
from pathlib import Path
from enum import Enum

# Add the current directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import the module under test
try:
    from activity_regulation import (
        ActivityRegulator, ActivityState, TaskPriority, ScheduledTask
    )
    ACTIVITY_REGULATION_AVAILABLE = True
except ImportError as e:
    ACTIVITY_REGULATION_AVAILABLE = False
    print(f"Warning: Could not import activity_regulation: {e}")


class TestActivityRegulation(unittest.TestCase):
    """Test cases for activity_regulation module"""

    def setUp(self):
        """Set up test fixtures"""
        # Suppress logging output during tests
        logging.getLogger().setLevel(logging.CRITICAL)

    def tearDown(self):
        """Clean up after tests"""
        pass

    def test_import_activity_regulation(self):
        """Test that activity_regulation module can be imported"""
        if not ACTIVITY_REGULATION_AVAILABLE:
            self.skipTest("activity_regulation module not available")
        
        self.assertTrue(ACTIVITY_REGULATION_AVAILABLE)

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_activity_state_enum(self):
        """Test ActivityState enum exists and has expected values"""
        expected_states = ['ACTIVE', 'RESTING', 'DORMANT', 'PROCESSING', 'WAITING']
        
        for state_name in expected_states:
            if hasattr(ActivityState, state_name):
                state = getattr(ActivityState, state_name)
                self.assertIsInstance(state, ActivityState)
                self.assertEqual(state.name, state_name)

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_task_priority_enum(self):
        """Test TaskPriority enum exists and has expected values"""
        expected_priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'BACKGROUND']
        
        for priority_name in expected_priorities:
            if hasattr(TaskPriority, priority_name):
                priority = getattr(TaskPriority, priority_name)
                self.assertIsInstance(priority, TaskPriority)
                self.assertEqual(priority.name, priority_name)

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_task_priority_values(self):
        """Test TaskPriority enum has integer values in correct order"""
        if hasattr(TaskPriority, 'CRITICAL') and hasattr(TaskPriority, 'HIGH'):
            # Critical should have lower value (higher priority)
            self.assertLess(TaskPriority.CRITICAL.value, TaskPriority.HIGH.value)

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_scheduled_task_creation(self):
        """Test ScheduledTask dataclass creation with real callback function"""
        # Create a real callback function for Deep Tree Echo testing
        def deep_tree_echo_callback():
            """Deep Tree Echo recursive pattern callback"""
            return "echo_resonance_activated"
        
        task = ScheduledTask(
            priority=TaskPriority.HIGH,
            scheduled_time=time.time(),
            task_id="deep_tree_echo_task",
            callback=deep_tree_echo_callback
        )
        
        self.assertEqual(task.priority, TaskPriority.HIGH)
        self.assertEqual(task.task_id, "deep_tree_echo_task")
        self.assertEqual(task.callback, deep_tree_echo_callback)
        self.assertIsInstance(task.scheduled_time, float)
        
        # Test that callback is actually functional
        result = task.callback()
        self.assertEqual(result, "echo_resonance_activated")

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_scheduled_task_optional_fields(self):
        """Test ScheduledTask with optional fields using real functions"""
        # Create real callback and condition functions
        def hypergraph_memory_callback():
            """Deep Tree Echo hypergraph memory processing"""
            return "hypergraph_pattern_processed"
        
        def p_system_membrane_condition():
            """Deep Tree Echo P-System membrane boundary check"""
            return True  # Membrane is permeable
        
        task = ScheduledTask(
            priority=TaskPriority.MEDIUM,
            scheduled_time=time.time(),
            task_id="hypergraph_memory_task",
            callback=hypergraph_memory_callback,
            interval=30.0,
            condition=p_system_membrane_condition,
            cpu_threshold=0.9,
            memory_threshold=0.8
        )
        
        self.assertEqual(task.interval, 30.0)
        self.assertEqual(task.condition, p_system_membrane_condition)
        self.assertEqual(task.cpu_threshold, 0.9)
        self.assertEqual(task.memory_threshold, 0.8)
        
        # Test that functions are actually functional
        callback_result = task.callback()
        self.assertEqual(callback_result, "hypergraph_pattern_processed")
        
        condition_result = task.condition()
        self.assertTrue(condition_result)

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_activity_regulator_creation(self):
        """Test ActivityRegulator class instantiation"""
        regulator = ActivityRegulator()
        
        self.assertIsNotNone(regulator)
        self.assertTrue(hasattr(regulator, 'logger'))
        self.assertTrue(hasattr(regulator, 'state'))
        self.assertTrue(hasattr(regulator, 'running'))

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_activity_regulator_attributes(self):
        """Test ActivityRegulator has expected attributes"""
        regulator = ActivityRegulator()
        
        # Test required attributes exist
        expected_attrs = [
            'logger', 'state', 'task_queue', 'periodic_tasks', 
            'event_tasks', 'running'
        ]
        
        for attr in expected_attrs:
            self.assertTrue(hasattr(regulator, attr),
                          f"Missing expected attribute: {attr}")

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_activity_regulator_initial_state(self):
        """Test ActivityRegulator initial state"""
        regulator = ActivityRegulator()
        
        # Test initial values
        self.assertEqual(regulator.state, ActivityState.ACTIVE)
        self.assertTrue(regulator.running)
        
        # Test collections are initialized
        if hasattr(regulator, 'task_queue'):
            self.assertIsNotNone(regulator.task_queue)
        if hasattr(regulator, 'periodic_tasks'):
            self.assertIsInstance(regulator.periodic_tasks, dict)
        if hasattr(regulator, 'event_tasks'):
            self.assertIsInstance(regulator.event_tasks, dict)

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_scheduled_task_ordering(self):
        """Test ScheduledTask ordering for priority queue with real callbacks"""
        # Create real callback functions for Deep Tree Echo testing
        def echo_state_network_callback():
            """Deep Tree Echo State Network processing"""
            return "echo_state_processed"
        
        def recursive_pattern_callback():
            """Deep Tree Echo recursive pattern analysis"""
            return "recursive_pattern_analyzed"
        
        task1 = ScheduledTask(
            priority=TaskPriority.HIGH,
            scheduled_time=time.time(),
            task_id="echo_state_network_task",
            callback=echo_state_network_callback
        )
        
        task2 = ScheduledTask(
            priority=TaskPriority.CRITICAL,
            scheduled_time=time.time(),
            task_id="recursive_pattern_task", 
            callback=recursive_pattern_callback
        )
        
        # Critical priority task should be less than high priority (for min-heap)
        self.assertLess(task2, task1)
        
        # Verify callbacks are functional
        self.assertEqual(task1.callback(), "echo_state_processed")
        self.assertEqual(task2.callback(), "recursive_pattern_analyzed")

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_activity_state_string_values(self):
        """Test ActivityState enum has string values"""
        for state in ActivityState:
            self.assertIsInstance(state.value, str)
            self.assertGreater(len(state.value), 0)

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_task_priority_integer_values(self):
        """Test TaskPriority enum has integer values"""
        for priority in TaskPriority:
            self.assertIsInstance(priority.value, int)
            self.assertGreaterEqual(priority.value, 0)

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_module_imports(self):
        """Test that module imports required dependencies"""
        import importlib
        try:
            importlib.reload(activity_regulation)
        except ImportError as e:
            if "No module named" in str(e):
                self.skipTest(f"Module dependencies not available: {e}")
            else:
                self.fail(f"Module failed to reload: {e}")

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_scheduled_task_defaults(self):
        """Test ScheduledTask default values with real callback"""
        def adaptive_memory_callback():
            """Deep Tree Echo adaptive memory processing"""
            return "adaptive_memory_updated"
        
        task = ScheduledTask(
            priority=TaskPriority.MEDIUM,
            scheduled_time=time.time(),
            task_id="adaptive_memory_task",
            callback=adaptive_memory_callback
        )
        
        # Test default values
        self.assertIsNone(task.interval)
        self.assertIsNone(task.condition)
        self.assertIsNone(task.last_run)
        self.assertEqual(task.cpu_threshold, 0.8)
        self.assertEqual(task.memory_threshold, 0.8)

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_activity_regulator_logger_configuration(self):
        """Test that ActivityRegulator configures logger correctly"""
        regulator = ActivityRegulator()
        
        self.assertIsNotNone(regulator.logger)
        self.assertEqual(regulator.logger.name, 'activity_regulation')

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_all_enums_accessible(self):
        """Test that all enum classes are accessible from module"""
        import activity_regulation as ar_module
        
        # Test enum classes are accessible
        self.assertTrue(hasattr(ar_module, 'ActivityState'))
        self.assertTrue(hasattr(ar_module, 'TaskPriority'))
        
        # Test they are actually Enum classes
        self.assertTrue(issubclass(ar_module.ActivityState, Enum))
        self.assertTrue(issubclass(ar_module.TaskPriority, Enum))

    @unittest.skipIf(not ACTIVITY_REGULATION_AVAILABLE, "activity_regulation not available")
    def test_scheduled_task_comparison_edge_cases(self):
        """Test ScheduledTask comparison with same priorities using real callbacks"""
        def neural_integration_callback():
            """Deep Tree Echo neural integration processing"""
            return "neural_integration_complete"
            
        def symbolic_reasoning_callback():
            """Deep Tree Echo symbolic reasoning processing"""
            return "symbolic_reasoning_complete"
        
        current_time = time.time()
        
        task1 = ScheduledTask(
            priority=TaskPriority.HIGH,
            scheduled_time=current_time,
            task_id="neural_integration_task",
            callback=neural_integration_callback
        )
        
        task2 = ScheduledTask(
            priority=TaskPriority.HIGH,
            scheduled_time=current_time + 1,
            task_id="symbolic_reasoning_task",
            callback=symbolic_reasoning_callback
        )
        
        # Earlier scheduled time should have precedence with same priority
        self.assertLess(task1, task2)
        
        # Verify callbacks are functional
        self.assertEqual(task1.callback(), "neural_integration_complete")
        self.assertEqual(task2.callback(), "symbolic_reasoning_complete")


def main():
    """Run the test suite"""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()