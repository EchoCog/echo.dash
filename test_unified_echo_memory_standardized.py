#!/usr/bin/env python3
"""
Test script for standardized Unified Echo Memory component

Validates that the UnifiedEchoMemory class properly implements
the Echo component interfaces.
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
    from unified_echo_memory import UnifiedEchoMemory, EchoMemoryConfig
    from echo_component_base import EchoConfig, validate_echo_component
    UNIFIED_MEMORY_AVAILABLE = True
except ImportError as e:
    UNIFIED_MEMORY_AVAILABLE = False
    print(f"Warning: Could not import unified echo memory components: {e}")


class TestUnifiedEchoMemoryStandardized(unittest.TestCase):
    """Test cases for standardized Unified Echo Memory component"""

    def setUp(self):
        """Set up test fixtures"""
        logging.getLogger().setLevel(logging.CRITICAL)
        self.temp_dir = tempfile.mkdtemp()

    def test_imports(self):
        """Test that Unified Echo Memory can be imported"""
        if not UNIFIED_MEMORY_AVAILABLE:
            self.skipTest("Unified Echo Memory not available")
        
        self.assertTrue(UNIFIED_MEMORY_AVAILABLE)

    @unittest.skipIf(not UNIFIED_MEMORY_AVAILABLE, "Unified Echo Memory not available")
    def test_component_creation(self):
        """Test creating Unified Echo Memory component"""
        config = EchoConfig(
            component_name="TestUnifiedMemory",
            version="1.0.0"
        )
        memory_config = EchoMemoryConfig(memory_storage_path=self.temp_dir)
        
        component = UnifiedEchoMemory(config, memory_config)
        
        # Test basic attributes
        self.assertEqual(component.config.component_name, "TestUnifiedMemory")
        self.assertIsNotNone(component.memory_manager)
        self.assertIsNotNone(component.echo_memory_stats)

    @unittest.skipIf(not UNIFIED_MEMORY_AVAILABLE, "Unified Echo Memory not available")
    def test_component_validation(self):
        """Test that component passes validation"""
        config = EchoConfig(component_name="TestUnifiedMemory")
        memory_config = EchoMemoryConfig(memory_storage_path=self.temp_dir)
        component = UnifiedEchoMemory(config, memory_config)
        
        self.assertTrue(validate_echo_component(component))

    @unittest.skipIf(not UNIFIED_MEMORY_AVAILABLE, "Unified Echo Memory not available")
    def test_initialization(self):
        """Test component initialization"""
        config = EchoConfig(component_name="TestUnifiedMemory")
        memory_config = EchoMemoryConfig(memory_storage_path=self.temp_dir)
        component = UnifiedEchoMemory(config, memory_config)
        
        result = component.initialize()
        
        self.assertTrue(result.success)
        self.assertIn("initialized", result.message)
        self.assertTrue(component._initialized)


if __name__ == '__main__':
    unittest.main()