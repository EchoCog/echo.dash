#!/usr/bin/env python3
"""
Echo Memory Demo Integration Validator

This script provides a simple validation interface that can be used by
the unified launcher system to verify that the Echo Memory Demo component
is properly integrated and ready for use.

This addresses the "Implement unified interface" requirement from the
fragment analysis by providing launcher-compatible validation.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from echo_memory_demo_standardized import create_memory_demo_system
from echo_component_base import validate_echo_component, get_echo_component_info


def validate_memory_demo_integration():
    """
    Validate that the Echo Memory Demo is properly integrated and ready for use.
    
    Returns:
        dict: Validation results with status and details
    """
    validation_results = {
        'component_name': 'EchoMemoryDemo',
        'validation_passed': False,
        'integration_ready': False,
        'launcher_compatible': False,
        'errors': [],
        'warnings': [],
        'component_info': None
    }
    
    try:
        # Step 1: Create component using factory function
        print("🔧 Creating Echo Memory Demo component...")
        demo = create_memory_demo_system()
        
        # Step 2: Validate component structure
        print("🧪 Validating component structure...")
        if not validate_echo_component(demo):
            validation_results['errors'].append("Component failed Echo validation")
            return validation_results
        
        # Step 3: Get component information
        component_info = get_echo_component_info(demo)
        validation_results['component_info'] = component_info
        print(f"✅ Component info: {component_info['component_name']} v{component_info['version']}")
        
        # Step 4: Test core operations
        print("🔍 Testing core operations...")
        
        # Test status method (required for launcher)
        status = demo.get_status()
        if not status.success:
            validation_results['errors'].append("get_status() method failed")
            return validation_results
        
        # Test basic memory operation
        store_result = demo.process({
            "action": "store",
            "key": "validation_test",
            "data": {"test": "integration validation"}
        })
        if not store_result.success:
            validation_results['errors'].append("Basic store operation failed")
            return validation_results
        
        # Test echo operation (core Echo functionality)
        echo_result = demo.echo({"validation": "test"}, echo_value=0.8)
        if not echo_result.success:
            validation_results['errors'].append("Echo operation failed")
            return validation_results
        
        # Test reset capability (required for launcher control)
        reset_result = demo.reset()
        if not reset_result.success:
            validation_results['errors'].append("Reset operation failed")
            return validation_results
        
        # Step 5: Validate launcher compatibility
        print("🚀 Checking launcher compatibility...")
        
        # Check that component can be reinitialized after reset
        init_result = demo.initialize()
        if not init_result.success:
            validation_results['warnings'].append("Component cannot be reinitialized after reset")
        else:
            validation_results['launcher_compatible'] = True
        
        # All validations passed
        validation_results['validation_passed'] = True
        validation_results['integration_ready'] = True
        
        print("✅ All validations passed!")
        
    except Exception as e:
        validation_results['errors'].append(f"Validation failed with exception: {str(e)}")
        print(f"❌ Validation failed: {e}")
    
    return validation_results


def generate_launcher_config():
    """
    Generate configuration that could be used by the unified launcher
    to integrate the Echo Memory Demo component.
    
    Returns:
        dict: Launcher configuration for the component
    """
    return {
        'component_id': 'echo_memory_demo',
        'component_name': 'EchoMemoryDemo',
        'component_class': 'EchoMemoryDemoStandardized',
        'factory_function': 'create_memory_demo_system',
        'module': 'echo_memory_demo_standardized',
        'capabilities': {
            'memory_operations': True,
            'echo_operations': True,
            'demo_modes': ['basic', 'performance'],
            'reset_support': True,
            'status_reporting': True
        },
        'integration_level': 'full',
        'initialization_required': False,  # Factory function handles initialization
        'dependencies': ['echo_component_base'],
        'launcher_commands': {
            'start': lambda: create_memory_demo_system(),
            'status': lambda component: component.get_status(),
            'reset': lambda component: component.reset(),
            'demo': lambda component: component.process({"action": "demo", "demo_type": "basic"})
        }
    }


def main():
    """Main validation routine"""
    print("🧪 Echo Memory Demo Integration Validation")
    print("=" * 60)
    
    # Run validation
    results = validate_memory_demo_integration()
    
    print(f"\n📊 Validation Results:")
    print(f"   Component: {results['component_name']}")
    print(f"   Validation Passed: {'✅' if results['validation_passed'] else '❌'}")
    print(f"   Integration Ready: {'✅' if results['integration_ready'] else '❌'}")
    print(f"   Launcher Compatible: {'✅' if results['launcher_compatible'] else '❌'}")
    
    if results['errors']:
        print(f"\n❌ Errors Found:")
        for error in results['errors']:
            print(f"   - {error}")
    
    if results['warnings']:
        print(f"\n⚠️  Warnings:")
        for warning in results['warnings']:
            print(f"   - {warning}")
    
    # Generate launcher configuration
    if results['integration_ready']:
        print(f"\n🚀 Launcher Configuration Generated:")
        launcher_config = generate_launcher_config()
        for key, value in launcher_config.items():
            if key != 'launcher_commands':  # Skip function objects in display
                print(f"   {key}: {value}")
    
    print(f"\n🎯 Integration Status: {'READY FOR UNIFIED LAUNCHER' if results['integration_ready'] else 'NEEDS ATTENTION'}")
    
    return 0 if results['validation_passed'] else 1


if __name__ == "__main__":
    sys.exit(main())