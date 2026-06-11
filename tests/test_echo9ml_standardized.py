#!/usr/bin/env python3
"""
Test script for standardized Echo9ml component

Validates that the new Echo9mlStandardized class properly implements
the Echo component interfaces while maintaining backward compatibility.
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
    from echo9ml import Echo9mlStandardized, create_echo9ml_standardized, ECHO_STANDARDIZED_AVAILABLE
    from echo_component_base import EchoConfig, validate_echo_component
    ECHO9ML_AVAILABLE = True
except ImportError as e:
    ECHO9ML_AVAILABLE = False
    print(f"Warning: Could not import echo9ml components: {e}")


class TestEcho9mlStandardized(unittest.TestCase):
    """Test cases for standardized Echo9ml component"""

    def setUp(self):
        """Set up test fixtures"""
        logging.getLogger().setLevel(logging.CRITICAL)

    def test_imports(self):
        """Test that standardized Echo9ml can be imported"""
        if not ECHO9ML_AVAILABLE:
            self.skipTest("Echo9ml not available")
        
        self.assertTrue(ECHO9ML_AVAILABLE)
        self.assertTrue(ECHO_STANDARDIZED_AVAILABLE)

    @unittest.skipIf(not ECHO9ML_AVAILABLE, "Echo9ml not available")
    def test_component_creation(self):
        """Test creating standardized Echo9ml component"""
        config = EchoConfig(
            component_name="TestEcho9ml",
            custom_params={'save_path': '/tmp/test_echo9ml'}
        )
        component = Echo9mlStandardized(config)
        
        # Test basic attributes
        self.assertEqual(component.config.component_name, "TestEcho9ml")
        self.assertIsNotNone(component.echo9ml_system)
        self.assertEqual(component.experiences_processed, 0)

    @unittest.skipIf(not ECHO9ML_AVAILABLE, "Echo9ml not available")
    def test_component_validation(self):
        """Test that component passes validation"""
        config = EchoConfig(component_name="TestEcho9ml")
        component = Echo9mlStandardized(config)
        
        self.assertTrue(validate_echo_component(component))

    @unittest.skipIf(not ECHO9ML_AVAILABLE, "Echo9ml not available")
    def test_initialization(self):
        """Test component initialization"""
        config = EchoConfig(component_name="TestEcho9ml")
        component = Echo9mlStandardized(config)
        
        result = component.initialize()
        
        self.assertTrue(result.success)
        self.assertIn("initialized", result.message)
        self.assertTrue(component._initialized)
        self.assertIn("persona_name", result.data)

    @unittest.skipIf(not ECHO9ML_AVAILABLE, "Echo9ml not available")
    def test_factory_function(self):
        """Test factory function creates valid component"""
        component = create_echo9ml_standardized(component_name="FactoryTest")
        
        self.assertTrue(validate_echo_component(component))
        self.assertTrue(component._initialized)
        self.assertEqual(component.config.component_name, "FactoryTest")


if __name__ == '__main__':
    unittest.main()