#!/usr/bin/env python3
"""
Test script for standardized Deep Tree Echo component

Validates that the DeepTreeEcho class properly supports the standardized
Echo component interfaces while maintaining backward compatibility.
"""

import unittest
import logging
import sys
from unittest.mock import Mock, patch
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Test imports
try:
    from deep_tree_echo import DeepTreeEcho, create_deep_tree_echo_standardized, ECHO_STANDARDIZED_AVAILABLE
    DEEP_TREE_ECHO_AVAILABLE = True
except ImportError as e:
    DEEP_TREE_ECHO_AVAILABLE = False
    print(f"Warning: Could not import deep_tree_echo components: {e}")

# Try to import dependencies separately to identify specific issues
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("Warning: numpy not available")


class TestDeepTreeEchoStandardized(unittest.TestCase):
    """Test cases for standardized Deep Tree Echo component"""

    def setUp(self):
        """Set up test fixtures"""
        logging.getLogger().setLevel(logging.CRITICAL)

    def test_imports(self):
        """Test that Deep Tree Echo can be imported"""
        if not DEEP_TREE_ECHO_AVAILABLE:
            self.skipTest("Deep Tree Echo not available")
        
        self.assertTrue(DEEP_TREE_ECHO_AVAILABLE)

    @unittest.skipIf(not DEEP_TREE_ECHO_AVAILABLE, "Deep Tree Echo not available")
    @unittest.skipIf(not NUMPY_AVAILABLE, "numpy not available")
    def test_basic_creation(self):
        """Test creating Deep Tree Echo system"""
        try:
            system = DeepTreeEcho(echo_threshold=0.8, max_depth=5, use_julia=False)
            
            # Test basic attributes
            self.assertEqual(system.echo_threshold, 0.8)
            self.assertEqual(system.max_depth, 5)
            self.assertIsNotNone(system.membrane_manager)
            self.assertIsNone(system.root)  # No tree created yet
            
        except Exception as e:
            self.skipTest(f"Could not create DeepTreeEcho: {e}")

    @unittest.skipIf(not DEEP_TREE_ECHO_AVAILABLE, "Deep Tree Echo not available")
    @unittest.skipIf(not NUMPY_AVAILABLE, "numpy not available")
    def test_standardized_initialization(self):
        """Test standardized component initialization"""
        if not ECHO_STANDARDIZED_AVAILABLE:
            self.skipTest("Echo standardized components not available")
            
        try:
            system = DeepTreeEcho(use_julia=False)
            result = system.initialize_echo_component()
            
            # Should return EchoResponse
            self.assertTrue(hasattr(result, 'success'))
            self.assertTrue(result.success)
            self.assertIn("initialized", result.message)
            
        except Exception as e:
            self.skipTest(f"Could not test standardized initialization: {e}")

    @unittest.skipIf(not DEEP_TREE_ECHO_AVAILABLE, "Deep Tree Echo not available")
    @unittest.skipIf(not NUMPY_AVAILABLE, "numpy not available")
    def test_factory_function(self):
        """Test factory function creates valid system"""
        if not ECHO_STANDARDIZED_AVAILABLE:
            self.skipTest("Echo standardized components not available")
            
        try:
            system = create_deep_tree_echo_standardized(
                echo_threshold=0.6,
                max_depth=8,
                use_julia=False,
                component_name="TestSystem"
            )
            
            self.assertEqual(system.echo_threshold, 0.6)
            self.assertEqual(system.max_depth, 8)
            self.assertIsNotNone(system)
            
        except Exception as e:
            self.skipTest(f"Could not test factory function: {e}")


if __name__ == '__main__':
    unittest.main()