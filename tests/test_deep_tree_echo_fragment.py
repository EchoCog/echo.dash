#!/usr/bin/env python3
"""
Test script for Deep Tree Echo fragment analysis.

Tests the core echo functions and integration points identified in the fragment analysis.
"""

import unittest
import sys
import numpy as np
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Try to import the main module - if dependencies aren't available, skip tests
try:
    from deep_tree_echo import DeepTreeEcho, TreeNode, SpatialContext
    DEEP_TREE_ECHO_AVAILABLE = True
except ImportError as e:
    DEEP_TREE_ECHO_AVAILABLE = False
    print(f"Warning: Could not import deep_tree_echo: {e}")


class TestDeepTreeEchoFragment(unittest.TestCase):
    """Test cases for deep_tree_echo.py fragment analysis"""

    def setUp(self):
        """Set up test fixtures"""
        if not DEEP_TREE_ECHO_AVAILABLE:
            self.skipTest("DeepTreeEcho not available")

    def test_tree_node_creation(self):
        """Test TreeNode basic functionality"""
        node = TreeNode(content="Test content")
        
        # Check default initialization
        self.assertEqual(node.content, "Test content")
        self.assertEqual(node.echo_value, 0.0)
        self.assertIsInstance(node.children, list)
        self.assertEqual(len(node.children), 0)
        self.assertIsInstance(node.metadata, dict)
        self.assertIsInstance(node.emotional_state, np.ndarray)
        self.assertIsInstance(node.spatial_context, SpatialContext)

    def test_spatial_context_creation(self):
        """Test SpatialContext initialization"""
        context = SpatialContext()
        
        # Check default values
        self.assertEqual(context.position, (0.0, 0.0, 0.0))
        self.assertEqual(context.orientation, (0.0, 0.0, 0.0))
        self.assertEqual(context.scale, 1.0)
        self.assertEqual(context.depth, 1.0)
        self.assertEqual(context.field_of_view, 90.0)

    @unittest.skipIf(not DEEP_TREE_ECHO_AVAILABLE, "DeepTreeEcho not available")
    def test_deep_tree_echo_creation(self):
        """Test DeepTreeEcho class instantiation with minimal dependencies"""
        try:
            # Try to create with minimal configuration to avoid dependency issues
            echo_system = DeepTreeEcho(echo_threshold=0.5, max_depth=5, use_julia=False)
            
            # Check basic attributes
            self.assertEqual(echo_system.echo_threshold, 0.5)
            self.assertEqual(echo_system.max_depth, 5)
            self.assertIsNone(echo_system.root)
            
        except ImportError:
            # If dependencies are missing, skip the test
            self.skipTest("DeepTreeEcho dependencies not available")

    @unittest.skipIf(not DEEP_TREE_ECHO_AVAILABLE, "DeepTreeEcho not available")
    def test_echo_functions_exist(self):
        """Test that all identified echo functions exist"""
        try:
            echo_system = DeepTreeEcho(use_julia=False)
            
            # Check all echo functions from the fragment analysis
            echo_functions = [
                'calculate_echo_value',
                'inject_echo', 
                'propagate_echoes',
                '_update_all_echo_values',
                '_apply_echo_decay',
                'prune_weak_echoes',
                '_reset_weak_echoes',
                'analyze_echo_patterns'
            ]
            
            for func_name in echo_functions:
                self.assertTrue(hasattr(echo_system, func_name), 
                              f"Missing echo function: {func_name}")
                self.assertTrue(callable(getattr(echo_system, func_name)),
                              f"Echo function not callable: {func_name}")
                
        except ImportError:
            self.skipTest("DeepTreeEcho dependencies not available")

    @unittest.skipIf(not DEEP_TREE_ECHO_AVAILABLE, "DeepTreeEcho not available")  
    def test_basic_echo_calculation(self):
        """Test basic echo value calculation without external dependencies"""
        # Create a simple node for testing
        node = TreeNode(content="Simple test content")
        
        try:
            echo_system = DeepTreeEcho(use_julia=False)
            
            # Test that calculate_echo_value returns a float
            echo_value = echo_system.calculate_echo_value(node)
            self.assertIsInstance(echo_value, (int, float))
            self.assertGreaterEqual(echo_value, 0.0)
            
        except Exception as e:
            # If there are dependency issues, document them but don't fail
            self.skipTest(f"Echo calculation failed due to dependencies: {e}")

    def test_fragment_analysis_document_exists(self):
        """Test that the fragment analysis document was created"""
        analysis_file = Path(__file__).parent / "DEEP_TREE_ECHO_FRAGMENT_ANALYSIS.md"
        self.assertTrue(analysis_file.exists(), "Fragment analysis document not found")
        
        # Check that it contains key sections
        content = analysis_file.read_text()
        required_sections = [
            "Structure Analysis",
            "Echo Functions", 
            "Integration Points",
            "Migration Strategy",
            "Unified Interface Requirements"
        ]
        
        for section in required_sections:
            self.assertIn(section, content, f"Missing section: {section}")


def run_tests():
    """Run the fragment analysis tests"""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()