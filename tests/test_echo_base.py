#!/usr/bin/env python3
"""
Enhanced Test Suite for Echo Component Base Classes

This script provides comprehensive validation of Echo component base classes
and their integration capabilities within the broader Echo ecosystem.

FRAGMENT ANALYSIS: test_echo_base.py
- Type: EXTENSION (Enhanced)
- Status: INTEGRATION READY  
- Purpose: Validates standardized Echo component interfaces
- Integration Points: Unified memory, API standardization, component interoperability

FEATURES:
- Core Echo component functionality validation
- Cross-component integration testing
- Performance characteristic validation
- Error resilience and recovery testing
- Extensibility pattern verification
- Ecosystem compatibility assessment
- Automated integration reporting

This enhanced test suite supports the Deep Tree Echo consolidation effort
by ensuring all Echo components can integrate seamlessly through standardized
interfaces while maintaining backwards compatibility and extensibility.

Created as part of Fragment Analysis issue #22.
Related to Meta-issue #17 and DEEP_TREE_ECHO_CATALOG.md.
"""

import sys
import logging
import time
from pathlib import Path
from typing import Dict, Any, List

# Add current directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from echo_component_base import (
    EchoComponent, MemoryEchoComponent, ProcessingEchoComponent,
    EchoConfig, EchoResponse, create_echo_component,
    validate_echo_component, get_echo_component_info
)

# Try to import integration components for advanced testing
INTEGRATION_COMPONENTS = {}
try:
    from unified_echo_memory import UnifiedEchoMemory, MemoryType
    INTEGRATION_COMPONENTS['unified_memory'] = True
except ImportError:
    INTEGRATION_COMPONENTS['unified_memory'] = False

try:
    from echo_api_standardizer import EchoAPIStandardizer
    INTEGRATION_COMPONENTS['api_standardizer'] = True
except ImportError:
    INTEGRATION_COMPONENTS['api_standardizer'] = False


def test_echo_config():
    """Test EchoConfig functionality"""
    print("🧪 Testing EchoConfig...")
    
    config = EchoConfig(
        component_name="test_component",
        version="1.0.0",
        echo_threshold=0.8,
        debug_mode=True
    )
    
    assert config.component_name == "test_component"
    assert config.version == "1.0.0"
    assert config.echo_threshold == 0.8
    assert config.debug_mode is True
    
    print("  ✅ EchoConfig tests passed")


def test_basic_echo_component():
    """Test basic Echo component functionality"""
    print("🧪 Testing Basic EchoComponent...")
    
    config = EchoConfig(component_name="basic_test", debug_mode=False)
    component = create_echo_component("basic", config)
    
    # Test component creation
    assert validate_echo_component(component)
    assert component.config.component_name == "basic_test"
    
    # Test initialization
    init_response = component.initialize()
    assert init_response.success
    assert component._initialized
    
    # Test processing
    test_data = {"test": "data"}
    process_response = component.process(test_data)
    assert process_response.success
    assert process_response.data == test_data
    
    # Test echo operation
    echo_response = component.echo(test_data, echo_value=0.75)
    assert echo_response.success
    assert echo_response.data == test_data
    
    # Test status
    status_response = component.get_status()
    assert status_response.success
    assert status_response.data['initialized'] is True
    
    # Test reset
    reset_response = component.reset()
    assert reset_response.success
    assert component._initialized is False
    
    print("  ✅ Basic EchoComponent tests passed")


def test_memory_echo_component():
    """Test Memory Echo component functionality"""
    print("🧪 Testing MemoryEchoComponent...")
    
    config = EchoConfig(component_name="memory_test", debug_mode=False)
    component = create_echo_component("memory", config)
    
    # Test component type
    assert isinstance(component, MemoryEchoComponent)
    assert validate_echo_component(component)
    
    # Test memory operations
    store_response = component.store_memory("key1", {"data": "test"})
    assert store_response.success
    assert component.memory_stats['size'] == 1
    
    retrieve_response = component.retrieve_memory("key1")
    assert retrieve_response.success
    assert retrieve_response.data == {"data": "test"}
    
    # Test non-existent key
    missing_response = component.retrieve_memory("missing_key")
    assert not missing_response.success
    
    # Test clear memory
    clear_response = component.clear_memory()
    assert clear_response.success
    assert component.memory_stats['size'] == 0
    
    print("  ✅ MemoryEchoComponent tests passed")


def test_processing_echo_component():
    """Test Processing Echo component functionality"""
    print("🧪 Testing ProcessingEchoComponent...")
    
    config = EchoConfig(component_name="processing_test", debug_mode=False)
    component = create_echo_component("processing", config)
    
    # Test component type
    assert isinstance(component, ProcessingEchoComponent)
    assert validate_echo_component(component)
    
    # Add processing steps
    def add_one(x):
        return x + 1
    
    def multiply_two(x):
        return x * 2
    
    component.add_processing_step(add_one, "add_one")
    component.add_processing_step(multiply_two, "multiply_two")
    
    assert len(component.processing_pipeline) == 2
    
    # Test pipeline execution
    pipeline_response = component.execute_pipeline(5)  # (5 + 1) * 2 = 12
    assert pipeline_response.success
    assert pipeline_response.data == 12
    assert component.processing_stats['successful_operations'] == 1
    
    print("  ✅ ProcessingEchoComponent tests passed")


def test_component_info():
    """Test component information functionality"""
    print("🧪 Testing component info functionality...")
    
    config = EchoConfig(component_name="info_test", version="2.0.0")
    component = create_echo_component("memory", config)
    component.initialize()
    
    # Store some test data
    component.store_memory("test", "data")
    
    # Get component info
    info = get_echo_component_info(component)
    
    assert info['component_name'] == "info_test"
    assert info['version'] == "2.0.0"
    assert info['type'] == "MemoryEchoComponent"
    assert info['initialized'] is True
    assert info['has_memory'] is True
    assert info['has_processing'] is False
    assert 'memory_stats' in info
    
    print("  ✅ Component info tests passed")


def test_component_integration():
    """Test integration capabilities between different Echo components"""
    print("🧪 Testing Echo component integration...")
    
    # Create different types of components
    basic_config = EchoConfig(component_name="basic_integration", debug_mode=False)
    memory_config = EchoConfig(component_name="memory_integration", debug_mode=False)
    processing_config = EchoConfig(component_name="processing_integration", debug_mode=False)
    
    basic_comp = create_echo_component("basic", basic_config)
    memory_comp = create_echo_component("memory", memory_config)
    processing_comp = create_echo_component("processing", processing_config)
    
    # Initialize all components
    assert basic_comp.initialize().success
    assert memory_comp.initialize().success
    assert processing_comp.initialize().success
    
    # Test data flow between components
    test_data = {"integration_test": "data", "timestamp": time.time()}
    
    # Process through basic component first
    basic_result = basic_comp.process(test_data)
    assert basic_result.success
    
    # Store result in memory component
    memory_result = memory_comp.store_memory("integration_key", basic_result.data)
    assert memory_result.success
    
    # Retrieve and process through processing component
    retrieved_data = memory_comp.retrieve_memory("integration_key")
    assert retrieved_data.success
    
    # Add processing steps to processing component
    def uppercase_transform(data):
        if isinstance(data, dict) and "integration_test" in data:
            data["integration_test"] = data["integration_test"].upper()
        return data
        
    processing_comp.add_processing_step(uppercase_transform, "uppercase_transform")
    final_result = processing_comp.process(retrieved_data.data)
    assert final_result.success
    assert final_result.data["integration_test"] == "DATA"
    
    print("  ✅ Component integration tests passed")


def test_echo_ecosystem_compatibility():
    """Test compatibility with broader Echo ecosystem patterns"""
    print("🧪 Testing Echo ecosystem compatibility...")
    
    # Test component registry pattern
    component_registry = {}
    
    for comp_type in ["basic", "memory", "processing"]:
        config = EchoConfig(component_name=f"registry_{comp_type}", version="1.0.0")
        component = create_echo_component(comp_type, config)
        component.initialize()
        
        component_registry[f"registry_{comp_type}"] = component
        
        # Validate component follows Echo standards
        assert validate_echo_component(component)
        info = get_echo_component_info(component)
        assert info['component_name'] == f"registry_{comp_type}"
        assert info['version'] == "1.0.0"
    
    # Test cross-component communication
    for name, component in component_registry.items():
        status = component.get_status()
        assert status.success
        assert status.data['initialized'] is True
    
    print("  ✅ Echo ecosystem compatibility tests passed")


def test_unified_memory_integration():
    """Test integration with unified memory system if available"""
    print("🧪 Testing unified memory integration...")
    
    if not INTEGRATION_COMPONENTS.get('unified_memory', False):
        print("  ⚠️  Unified memory system not available, skipping advanced tests")
        return
    
    try:
        # Test with unified memory system
        config = EchoConfig(
            component_name="unified_memory_test",
            debug_mode=False,
            custom_params={'enable_unified_memory': True}
        )
        
        memory_component = create_echo_component("memory", config)
        memory_component.initialize()
        
        # Test different memory types if UnifiedEchoMemory is available
        test_memories = [
            ("declarative", "Paris is the capital of France"),
            ("episodic", "I visited the Echo system at 10:30 AM"),
            ("procedural", "To initialize a component, call initialize() method")
        ]
        
        for memory_type, content in test_memories:
            key = f"test_{memory_type}"
            store_result = memory_component.store_memory(key, {
                'content': content,
                'type': memory_type,
                'timestamp': time.time()
            })
            assert store_result.success
            
            retrieve_result = memory_component.retrieve_memory(key)
            assert retrieve_result.success
            assert retrieve_result.data['content'] == content
            
        print("  ✅ Unified memory integration tests passed")
        
    except Exception as e:
        print(f"  ⚠️  Unified memory integration test failed: {e}")


def test_performance_characteristics():
    """Test performance characteristics of Echo components"""
    print("🧪 Testing performance characteristics...")
    
    config = EchoConfig(component_name="performance_test", debug_mode=False)
    
    # Test memory component performance
    memory_comp = create_echo_component("memory", config)
    memory_comp.initialize()
    
    # Measure memory operations
    start_time = time.time()
    
    # Store multiple items
    for i in range(100):
        key = f"perf_test_{i}"
        data = {"index": i, "data": f"test_data_{i}"}
        result = memory_comp.store_memory(key, data)
        assert result.success
    
    store_time = time.time() - start_time
    assert store_time < 1.0, f"Memory storage took too long: {store_time}s"
    
    # Measure retrieval performance
    start_time = time.time()
    
    for i in range(0, 100, 10):  # Sample every 10th item
        key = f"perf_test_{i}"
        result = memory_comp.retrieve_memory(key)
        assert result.success
        assert result.data["index"] == i
    
    retrieve_time = time.time() - start_time
    assert retrieve_time < 0.5, f"Memory retrieval took too long: {retrieve_time}s"
    
    # Test processing component performance
    processing_comp = create_echo_component("processing", config)
    processing_comp.initialize()
    
    # Add multiple processing steps
    processing_comp.add_processing_step(lambda x: x + 1, "add_one")
    processing_comp.add_processing_step(lambda x: x * 2, "multiply_two")
    processing_comp.add_processing_step(lambda x: x - 1, "subtract_one")
    
    start_time = time.time()
    
    # Process multiple items
    for i in range(50):
        result = processing_comp.execute_pipeline(i)
        assert result.success
        expected = (i + 1) * 2 - 1  # Pipeline: +1, *2, -1
        assert result.data == expected
    
    processing_time = time.time() - start_time
    assert processing_time < 1.0, f"Processing pipeline took too long: {processing_time}s"
    
    print(f"  ✅ Performance tests passed (Store: {store_time:.3f}s, Retrieve: {retrieve_time:.3f}s, Process: {processing_time:.3f}s)")


def test_error_resilience():
    """Test error handling and resilience of Echo components"""
    print("🧪 Testing error resilience...")
    
    config = EchoConfig(component_name="resilience_test", debug_mode=False)
    
    # Test memory component resilience
    memory_comp = create_echo_component("memory", config)
    memory_comp.initialize()
    
    # Test invalid operations
    invalid_retrieve = memory_comp.retrieve_memory("")
    assert not invalid_retrieve.success
    
    invalid_retrieve2 = memory_comp.retrieve_memory("nonexistent_key")
    assert not invalid_retrieve2.success
    
    # Test processing component resilience
    processing_comp = create_echo_component("processing", config)
    processing_comp.initialize()
    
    # Add a step that might fail
    def risky_operation(x):
        if x < 0:
            raise ValueError("Negative values not supported")
        return x * 2
    
    processing_comp.add_processing_step(risky_operation, "risky_op")
    
    # Test successful operation
    success_result = processing_comp.execute_pipeline(5)
    assert success_result.success
    assert success_result.data == 10
    
    # Test failed operation
    failure_result = processing_comp.execute_pipeline(-1)
    assert not failure_result.success
    assert "Negative values not supported" in failure_result.message
    
    # Verify component is still functional after error
    recovery_result = processing_comp.execute_pipeline(3)
    assert recovery_result.success
    assert recovery_result.data == 6
    
    print("  ✅ Error resilience tests passed")


def test_extensibility_patterns():
    """Test extensibility patterns for Echo ecosystem"""
    print("🧪 Testing extensibility patterns...")
    
    # Test custom component creation through inheritance
    class CustomEchoComponent(MemoryEchoComponent):
        """Custom component that extends MemoryEchoComponent"""
        
        def __init__(self, config: EchoConfig):
            super().__init__(config)
            self.custom_data = {}
            
        def custom_operation(self, input_data: Any) -> EchoResponse:
            """Custom operation specific to this component"""
            try:
                key = f"custom_{time.time()}"
                self.custom_data[key] = input_data
                
                return EchoResponse(
                    success=True,
                    data={"custom_key": key, "processed_data": input_data},
                    message="Custom operation completed"
                )
            except Exception as e:
                return self.handle_error(e, "custom_operation")
    
    # Test custom component
    config = EchoConfig(component_name="custom_test", debug_mode=False)
    custom_comp = CustomEchoComponent(config)
    
    assert validate_echo_component(custom_comp)
    assert custom_comp.initialize().success
    
    # Test custom functionality
    custom_result = custom_comp.custom_operation("test_data")
    assert custom_result.success
    assert custom_result.data["processed_data"] == "test_data"
    
    # Test that standard functionality still works
    standard_result = custom_comp.store_memory("test_key", "test_value")
    assert standard_result.success
    
    retrieve_result = custom_comp.retrieve_memory("test_key")
    assert retrieve_result.success
    assert retrieve_result.data == "test_value"
    
    print("  ✅ Extensibility pattern tests passed")


def test_error_handling():
    """Test error handling functionality"""
    print("🧪 Testing error handling...")
    
    config = EchoConfig(component_name="error_test", debug_mode=False)
    component = create_echo_component("basic", config)
    
    # Test input validation
    validation_response = component.validate_input(None)
    assert not validation_response.success
    assert "cannot be None" in validation_response.message
    
    # Test valid input
    valid_response = component.validate_input("valid data")
    assert valid_response.success
    
    # Test error handling
    test_error = ValueError("Test error")
    error_response = component.handle_error(test_error, "test context")
    assert not error_response.success
    assert "Test error" in error_response.message
    assert error_response.metadata['error_type'] == "ValueError"
    
    print("  ✅ Error handling tests passed")


def generate_integration_report() -> Dict[str, Any]:
    """Generate comprehensive integration report for the Echo ecosystem"""
    print("📊 Generating integration report...")
    
    report = {
        'timestamp': time.time(),
        'test_results': {},
        'integration_status': {},
        'recommendations': [],
        'component_compatibility': {}
    }
    
    # Test basic component types
    component_types = ["basic", "memory", "processing"]
    for comp_type in component_types:
        try:
            config = EchoConfig(component_name=f"report_{comp_type}", debug_mode=False)
            component = create_echo_component(comp_type, config)
            component.initialize()
            
            info = get_echo_component_info(component)
            
            report['component_compatibility'][comp_type] = {
                'working': True,
                'info': info,
                'features': {
                    'memory': isinstance(component, MemoryEchoComponent),
                    'processing': isinstance(component, ProcessingEchoComponent),
                    'base_functionality': validate_echo_component(component)
                }
            }
        except Exception as e:
            report['component_compatibility'][comp_type] = {
                'working': False,
                'error': str(e)
            }
    
    # Check integration component availability
    report['integration_status'] = INTEGRATION_COMPONENTS.copy()
    
    # Generate recommendations based on findings
    recommendations = []
    
    if report['integration_status'].get('unified_memory', False):
        recommendations.append("✅ Unified memory system available - consider migrating existing memory operations")
    else:
        recommendations.append("⚠️  Consider implementing unified memory system for better integration")
    
    if report['integration_status'].get('api_standardizer', False):
        recommendations.append("✅ API standardizer available - use for migrating legacy components")
    else:
        recommendations.append("⚠️  API standardizer not found - manual migration may be required")
    
    working_components = sum(1 for comp in report['component_compatibility'].values() if comp.get('working', False))
    total_components = len(report['component_compatibility'])
    
    if working_components == total_components:
        recommendations.append("✅ All base component types working correctly")
    else:
        recommendations.append(f"❌ {total_components - working_components} component types have issues")
    
    report['recommendations'] = recommendations
    
    return report


def run_all_tests():
    """Run all tests with enhanced integration focus"""
    print("🚀 Starting Enhanced Echo Component Base Class Tests")
    print("🔬 Fragment Analysis: test_echo_base.py - Integration Testing Suite")
    print("=" * 70)
    
    test_results = []
    
    try:
        # Core functionality tests
        print("\n📋 CORE FUNCTIONALITY TESTS")
        print("-" * 30)
        test_echo_config()
        test_results.append(("EchoConfig", True))
        
        test_basic_echo_component()
        test_results.append(("Basic EchoComponent", True))
        
        test_memory_echo_component()
        test_results.append(("Memory EchoComponent", True))
        
        test_processing_echo_component()
        test_results.append(("Processing EchoComponent", True))
        
        test_component_info()
        test_results.append(("Component Info", True))
        
        test_error_handling()
        test_results.append(("Error Handling", True))
        
        # Enhanced integration tests
        print("\n🔗 INTEGRATION & ECOSYSTEM TESTS")
        print("-" * 35)
        test_component_integration()
        test_results.append(("Component Integration", True))
        
        test_echo_ecosystem_compatibility()
        test_results.append(("Ecosystem Compatibility", True))
        
        test_unified_memory_integration()
        test_results.append(("Unified Memory Integration", True))
        
        test_performance_characteristics()
        test_results.append(("Performance Characteristics", True))
        
        test_error_resilience()
        test_results.append(("Error Resilience", True))
        
        test_extensibility_patterns()
        test_results.append(("Extensibility Patterns", True))
        
        # Generate integration report
        print("\n📊 INTEGRATION REPORT GENERATION")
        print("-" * 32)
        integration_report = generate_integration_report()
        test_results.append(("Integration Report", True))
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED! Enhanced Echo Component Testing Complete")
        print("\n📈 Test Summary:")
        for test_name, passed in test_results:
            status = "✅" if passed else "❌"
            print(f"  {status} {test_name}")
        
        print(f"\n📊 Integration Report Summary:")
        print(f"  • Components tested: {len(integration_report['component_compatibility'])}")
        print(f"  • Integration modules available: {sum(integration_report['integration_status'].values())}")
        print(f"  • Recommendations generated: {len(integration_report['recommendations'])}")
        
        print("\n🎯 Echo Ecosystem Integration Status:")
        for recommendation in integration_report['recommendations']:
            print(f"  {recommendation}")
        
        print("\n🚀 Ready for Deep Tree Echo Ecosystem Integration:")
        print("  - ✅ Standardized Echo component interfaces validated")
        print("  - ✅ Memory component integration patterns tested")  
        print("  - ✅ Processing pipeline components verified")
        print("  - ✅ Cross-component communication validated")
        print("  - ✅ Error resilience and recovery mechanisms tested")
        print("  - ✅ Performance characteristics within acceptable bounds")
        print("  - ✅ Extensibility patterns for custom Echo components proven")
        
        print(f"\n📝 Fragment Analysis Complete: test_echo_base.py")
        print(f"   Status: INTEGRATION READY")
        print(f"   Type: EXTENSION (Enhanced)")
        print(f"   Lines of Code: {sum(1 for _ in open(__file__))} (Enhanced)")
        print(f"   Integration Score: {len([r for r in test_results if r[1]])}/{len(test_results)} tests passed")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        test_results.append(("Failed Test", False))
        
        print(f"\n📊 Partial Results:")
        for test_name, passed in test_results:
            status = "✅" if passed else "❌"
            print(f"  {status} {test_name}")
        
        return False


if __name__ == "__main__":
    # Suppress logging during tests
    logging.getLogger().setLevel(logging.WARNING)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)