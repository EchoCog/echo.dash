#!/usr/bin/env python3
"""
Test script for Echo Component Integration Module

This script validates the integration capabilities and adapter functionality
for migrating legacy Echo components to the standardized base classes.
"""

import sys
import logging
from pathlib import Path

# Add current directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from echo_component_integration import (
    EchoComponentAdapter, EchoIntegrationAnalyzer, IntegrationReport,
    create_integration_adapter, analyze_integration_readiness,
    integration_decorator, demonstrate_integration
)
from echo_component_base import (
    EchoComponent, MemoryEchoComponent, ProcessingEchoComponent,
    EchoConfig, EchoResponse, validate_echo_component
)


class MockLegacyEchoComponent:
    """Mock legacy Echo component for testing"""
    def __init__(self, name="MockComponent"):
        self.name = name
        self.data_store = {}
        
    def process_data(self, data):
        """Legacy processing method"""
        return f"Legacy processed: {data}"
        
    def echo_operation(self, data, strength=0.5):
        """Legacy echo method"""
        return f"Legacy echo[{strength}]: {data}"
        
    def store_data(self, key, value):
        """Legacy memory method"""
        self.data_store[key] = value
        return True
        
    def retrieve_data(self, key):
        """Legacy retrieval method"""
        return self.data_store.get(key)


class MockProcessingComponent:
    """Mock component focused on processing"""
    def __init__(self, processor_id="proc1"):
        self.processor_id = processor_id
        
    def analyze(self, input_data):
        """Analysis method"""
        return {"analysis": f"Analyzed {input_data}", "processor": self.processor_id}
        
    def compute(self, data, operation="sum"):
        """Computation method"""
        if isinstance(data, list) and operation == "sum":
            return sum(data)
        return data


class MockBasicComponent:
    """Mock basic component with minimal functionality"""
    def __init__(self):
        self.status = "ready"
        
    def get_status(self):
        return self.status


def test_integration_analyzer():
    """Test the integration analyzer functionality"""
    print("🧪 Testing Integration Analyzer...")
    
    analyzer = EchoIntegrationAnalyzer()
    
    # Test with legacy component
    legacy_comp = MockLegacyEchoComponent("TestLegacy")
    report = analyzer.analyze_component(legacy_comp)
    
    assert isinstance(report, IntegrationReport)
    assert report.component_name == "MockLegacyEchoComponent"
    assert report.integration_status in ['needs_migration', 'compatible']
    assert report.base_class_recommendation in ['MemoryEchoComponent', 'ProcessingEchoComponent', 'EchoComponent']
    assert len(report.integration_steps) > 0
    
    # Test with processing component
    proc_comp = MockProcessingComponent()
    proc_report = analyzer.analyze_component(proc_comp)
    assert proc_report.base_class_recommendation == 'ProcessingEchoComponent'
    
    # Test with basic component
    basic_comp = MockBasicComponent()
    basic_report = analyzer.analyze_component(basic_comp)
    assert basic_report.base_class_recommendation == 'EchoComponent'
    
    print("  ✅ Integration Analyzer tests passed")


def test_component_adapter():
    """Test the component adapter functionality"""
    print("🧪 Testing Component Adapter...")
    
    # Test memory component adaptation
    legacy_comp = MockLegacyEchoComponent("AdapterTest")
    adapter = EchoComponentAdapter(legacy_comp, "TestAdapter")
    
    assert adapter.component_name == "TestAdapter"
    assert adapter._has_memory_methods() is True
    assert adapter._has_processing_methods() is True  # Has process_data method
    
    # Create adapted component
    config = EchoConfig(component_name="AdaptedMemoryComponent", debug_mode=False)
    adapted = adapter.adapt_to_echo_component(config)
    
    # Verify it's a proper Echo component
    assert validate_echo_component(adapted)
    assert isinstance(adapted, MemoryEchoComponent)
    
    # Test initialization
    init_result = adapted.initialize()
    assert init_result.success is True
    assert adapted._initialized is True
    
    # Test processing
    process_result = adapted.process("test data")
    assert process_result.success is True
    assert "Legacy processed" in str(process_result.data)
    
    # Test echo
    echo_result = adapted.echo("echo test", 0.8)
    assert echo_result.success is True
    
    print("  ✅ Component Adapter tests passed")


def test_processing_adapter():
    """Test adapter with processing-focused component"""
    print("🧪 Testing Processing Adapter...")
    
    proc_comp = MockProcessingComponent("TestProcessor")
    adapter = EchoComponentAdapter(proc_comp, "ProcessingAdapter")
    
    assert adapter._has_processing_methods() is True
    # MockProcessingComponent should not have memory methods
    
    # Create adapted component
    config = EchoConfig(component_name="AdaptedProcessingComponent")
    adapted = adapter.adapt_to_echo_component(config)
    
    # Should be processing component if no memory methods
    assert isinstance(adapted, ProcessingEchoComponent)
    assert validate_echo_component(adapted)
    
    # Test processing with different method names
    init_result = adapted.initialize()
    assert init_result.success is True
    
    # Test analysis method
    analysis_result = adapted.process("test analysis")
    assert analysis_result.success is True
    assert "Analyzed" in str(analysis_result.data)
    
    # Test compute method
    compute_result = adapted.process([1, 2, 3, 4])
    assert compute_result.success is True
    
    print("  ✅ Processing Adapter tests passed")


def test_basic_adapter():
    """Test adapter with basic component"""
    print("🧪 Testing Basic Adapter...")
    
    basic_comp = MockBasicComponent()
    adapter = EchoComponentAdapter(basic_comp, "BasicAdapter")
    
    assert adapter._has_memory_methods() is False
    assert adapter._has_processing_methods() is False
    
    # Create adapted component
    adapted = adapter.adapt_to_echo_component()
    
    assert isinstance(adapted, EchoComponent)
    assert not isinstance(adapted, MemoryEchoComponent)
    assert not isinstance(adapted, ProcessingEchoComponent)
    assert validate_echo_component(adapted)
    
    # Test basic functionality
    init_result = adapted.initialize()
    assert init_result.success is True
    
    process_result = adapted.process("basic test")
    assert process_result.success is True
    
    echo_result = adapted.echo("basic echo")
    assert echo_result.success is True
    
    print("  ✅ Basic Adapter tests passed")


def test_convenience_functions():
    """Test convenience functions"""
    print("🧪 Testing Convenience Functions...")
    
    # Test create_integration_adapter
    legacy_comp = MockLegacyEchoComponent("ConvenienceTest")
    adapted = create_integration_adapter(legacy_comp, "ConvenienceAdapter")
    
    assert validate_echo_component(adapted)
    assert adapted.config.component_name == "ConvenienceAdapter"
    
    # Test analyze_integration_readiness
    report = analyze_integration_readiness(legacy_comp)
    assert isinstance(report, IntegrationReport)
    assert report.component_name == "MockLegacyEchoComponent"
    
    print("  ✅ Convenience Functions tests passed")


def test_integration_decorator():
    """Test the integration decorator"""
    print("🧪 Testing Integration Decorator...")
    
    @integration_decorator(base_class_type='memory')
    class DecoratedMemoryComponent:
        def __init__(self, custom_param=None):
            self.custom_param = custom_param
            
        def initialize(self):
            self._initialized = True
            return EchoResponse(success=True, message="Decorated component initialized")
            
        def process(self, input_data, **kwargs):
            return EchoResponse(success=True, data=f"Decorated: {input_data}")
            
        def echo(self, data, echo_value=0.0):
            return EchoResponse(success=True, data=data, message=f"Decorated echo: {echo_value}")
    
    # Test with EchoConfig
    config = EchoConfig(component_name="DecoratedTest")
    decorated = DecoratedMemoryComponent(config, custom_param="test")
    
    assert validate_echo_component(decorated)
    assert isinstance(decorated, MemoryEchoComponent)
    assert decorated.custom_param == "test"
    
    # Test functionality
    init_result = decorated.initialize()
    assert init_result.success is True
    
    process_result = decorated.process("decorated test")
    assert process_result.success is True
    
    print("  ✅ Integration Decorator tests passed")


def test_error_handling():
    """Test error handling in adapters"""
    print("🧪 Testing Error Handling...")
    
    class BrokenComponent:
        def process_data(self, data):
            raise ValueError("Intentional test error")
            
        def echo(self, data, value):
            raise RuntimeError("Echo error")
    
    broken_comp = BrokenComponent()
    adapted = create_integration_adapter(broken_comp, "BrokenAdapter")
    
    # Test that errors are handled gracefully
    process_result = adapted.process("test")
    assert process_result.success is False
    assert "error" in process_result.message.lower()
    assert process_result.metadata.get('error_type') == "ValueError"
    
    echo_result = adapted.echo("test")
    assert echo_result.success is False
    assert "error" in echo_result.message.lower()
    
    print("  ✅ Error Handling tests passed")


def test_integration_with_existing_components():
    """Test integration with already standardized components"""
    print("🧪 Testing Integration with Existing Components...")
    
    # Create a standardized component
    config = EchoConfig(component_name="StandardTest")
    standard_comp = MemoryEchoComponent(config)
    
    # Test that analyzer recognizes it's already compatible
    report = analyze_integration_readiness(standard_comp)
    assert report.integration_status == 'compatible'
    assert report.base_class_recommendation == 'Already standardized'
    assert report.migration_complexity == 'none'
    
    # Test that adapter recognizes it doesn't need wrapping
    adapter = EchoComponentAdapter(standard_comp)
    # The adapter should still work but recognize it's already standardized
    assert validate_echo_component(standard_comp)
    
    print("  ✅ Integration with Existing Components tests passed")


def run_all_tests():
    """Run all integration tests"""
    print("🚀 Starting Echo Component Integration Tests")
    print("=" * 60)
    
    try:
        test_integration_analyzer()
        test_component_adapter()
        test_processing_adapter()
        test_basic_adapter()
        test_convenience_functions()
        test_integration_decorator()
        test_error_handling()
        test_integration_with_existing_components()
        
        print("\n" + "=" * 60)
        print("✅ All integration tests passed!")
        print("\n🎯 Integration module is ready for:")
        print("  - Migrating legacy Echo components to standardized interfaces")
        print("  - Providing adapter layer for backward compatibility")
        print("  - Analyzing integration readiness of existing components")
        print("  - Decorating new components for automatic standardization")
        
        # Run demonstration
        print("\n🎬 Running Integration Demonstration:")
        print("-" * 40)
        demonstrate_integration()
        
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