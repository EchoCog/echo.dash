#!/usr/bin/env python3
"""
Test script for standardized Echoself introspection component

Validates that the new EchoselfIntrospectionStandardized class properly implements
the Echo component interfaces while maintaining backward compatibility.
"""

import unittest
import logging
import sys
import tempfile
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Test imports
try:
    from echoself_introspection import (
        EchoselfIntrospectionStandardized, 
        create_echoself_introspection_standardized,
        ECHO_STANDARDIZED_AVAILABLE
    )
    from echo_component_base import EchoConfig, validate_echo_component
    ECHOSELF_INTROSPECTION_AVAILABLE = True
except ImportError as e:
    ECHOSELF_INTROSPECTION_AVAILABLE = False
    print(f"Warning: Could not import echoself introspection components: {e}")


class TestEchoselfIntrospectionStandardized(unittest.TestCase):
    """Test cases for standardized Echoself introspection component"""

    def setUp(self):
        """Set up test fixtures"""
        logging.getLogger().setLevel(logging.CRITICAL)

    def test_imports(self):
        """Test that standardized Echoself introspection can be imported"""
        if not ECHOSELF_INTROSPECTION_AVAILABLE:
            self.skipTest("Echoself introspection not available")
        
        self.assertTrue(ECHOSELF_INTROSPECTION_AVAILABLE)
        self.assertTrue(ECHO_STANDARDIZED_AVAILABLE)

    @unittest.skipIf(not ECHOSELF_INTROSPECTION_AVAILABLE, "Echoself introspection not available")
    def test_component_creation(self):
        """Test creating standardized Echoself introspection component"""
        config = EchoConfig(
            component_name="TestEchoselfIntrospection",
            custom_params={'repository_root': '/tmp/test_repo'}
        )
        component = EchoselfIntrospectionStandardized(config)
        
        # Test basic attributes
        self.assertEqual(component.config.component_name, "TestEchoselfIntrospection")
        self.assertIsNotNone(component.echoself_introspector)
        self.assertEqual(component.introspection_count, 0)

    @unittest.skipIf(not ECHOSELF_INTROSPECTION_AVAILABLE, "Echoself introspection not available")
    def test_component_validation(self):
        """Test that component passes validation"""
        config = EchoConfig(component_name="TestEchoselfIntrospection")
        component = EchoselfIntrospectionStandardized(config)
        
        self.assertTrue(validate_echo_component(component))

    @unittest.skipIf(not ECHOSELF_INTROSPECTION_AVAILABLE, "Echoself introspection not available")
    def test_initialization(self):
        """Test component initialization"""
        config = EchoConfig(component_name="TestEchoselfIntrospection")
        component = EchoselfIntrospectionStandardized(config)
        
        result = component.initialize()
        
        self.assertTrue(result.success)
        self.assertIn("initialized", result.message)
        self.assertTrue(component._initialized)
        self.assertIn("repository_root", result.data)

    @unittest.skipIf(not ECHOSELF_INTROSPECTION_AVAILABLE, "Echoself introspection not available")
    def test_factory_function(self):
        """Test factory function creates valid component"""
        component = create_echoself_introspection_standardized(
            component_name="FactoryTest"
        )
        
        self.assertTrue(validate_echo_component(component))
        self.assertTrue(component._initialized)
        self.assertEqual(component.config.component_name, "FactoryTest")


if __name__ == '__main__':
    unittest.main()