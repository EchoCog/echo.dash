#!/usr/bin/env python3
"""
Echo Component Integration Module

This module provides integration utilities to help existing Echo components
seamlessly work with the standardized base classes from echo_component_base.py.
It serves as an adapter layer and migration assistant.

Created as part of the Deep Tree Echo consolidation effort to standardize APIs
and improve system integration.
"""

import logging
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
import inspect
import functools

from echo_component_base import (
    EchoComponent, MemoryEchoComponent, ProcessingEchoComponent,
    EchoConfig, EchoResponse, create_echo_component,
    validate_echo_component, get_echo_component_info
)


@dataclass
class IntegrationReport:
    """Report on component integration status"""
    component_name: str
    integration_status: str  # 'compatible', 'needs_migration', 'incompatible'
    base_class_recommendation: str
    integration_steps: List[str] = field(default_factory=list)
    compatibility_issues: List[str] = field(default_factory=list)
    migration_complexity: str = "low"  # low, medium, high


class EchoComponentAdapter:
    """
    Adapter to wrap existing Echo components to work with standardized interfaces
    """
    
    def __init__(self, legacy_component: Any, component_name: str = None):
        self.legacy_component = legacy_component
        self.component_name = component_name or getattr(legacy_component, '__class__.__name__', 'UnknownComponent')
        self.logger = logging.getLogger(f"echo.adapter.{self.component_name}")
        
    def adapt_to_echo_component(self, config: EchoConfig = None) -> EchoComponent:
        """
        Create a standardized EchoComponent wrapper around the legacy component
        """
        if config is None:
            config = EchoConfig(component_name=self.component_name)
        
        # Detect what type of component this should be based on methods
        if self._has_processing_methods() and not self._has_memory_methods():
            return self._create_processing_adapter(config)
        elif self._has_memory_methods():
            return self._create_memory_adapter(config)
        else:
            return self._create_basic_adapter(config)
    
    def _has_memory_methods(self) -> bool:
        """Check if component has memory-related methods"""
        memory_methods = ['store', 'retrieve', 'memory', 'save', 'load']
        component_methods = [method for method in dir(self.legacy_component) if not method.startswith('_')]
        return any(any(memory_word in method.lower() for memory_word in memory_methods) 
                  for method in component_methods)
    
    def _has_processing_methods(self) -> bool:
        """Check if component has processing-related methods"""
        processing_methods = ['process', 'execute', 'run', 'compute', 'analyze']
        component_methods = [method for method in dir(self.legacy_component) if not method.startswith('_')]
        return any(any(proc_word in method.lower() for proc_word in processing_methods) 
                  for method in component_methods)
    
    def _create_memory_adapter(self, config: EchoConfig) -> MemoryEchoComponent:
        """Create a MemoryEchoComponent adapter"""
        
        class AdaptedMemoryComponent(MemoryEchoComponent):
            def __init__(self, legacy_comp, adapter_config):
                super().__init__(adapter_config)
                self.legacy_comp = legacy_comp
                
            def initialize(self) -> EchoResponse:
                try:
                    # Try to call legacy initialization
                    if hasattr(self.legacy_comp, 'initialize'):
                        result = self.legacy_comp.initialize()
                    elif hasattr(self.legacy_comp, '__init__'):
                        result = True
                    else:
                        result = True
                    
                    self._initialized = True
                    return EchoResponse(
                        success=True,
                        message=f"Adapted memory component {self.config.component_name} initialized"
                    )
                except Exception as e:
                    return self.handle_error(e, "initialize")
            
            def process(self, input_data: Any, **kwargs) -> EchoResponse:
                try:
                    # Try different processing method names
                    for method_name in ['process', 'process_data', 'run', 'execute', 'analyze']:
                        if hasattr(self.legacy_comp, method_name):
                            method = getattr(self.legacy_comp, method_name)
                            # Try calling with minimal arguments first
                            try:
                                result = method(input_data)
                            except TypeError:
                                # Try with kwargs if the method supports them
                                result = method(input_data, **kwargs)
                            
                            # Store in memory
                            key = kwargs.get('memory_key', f"process_{datetime.now().timestamp()}")
                            self.store_memory(key, result)
                            
                            return EchoResponse(
                                success=True,
                                data=result,
                                message=f"Legacy component processing completed via {method_name}",
                                metadata={'method_used': method_name, 'memory_key': key}
                            )
                    
                    # Fallback to parent implementation
                    return super().process(input_data, **kwargs)
                except Exception as e:
                    return self.handle_error(e, "process")
            
            def echo(self, data: Any, echo_value: float = 0.0) -> EchoResponse:
                try:
                    # Try to use legacy echo method if available
                    for method_name in ['echo', 'echo_operation']:
                        if hasattr(self.legacy_comp, method_name):
                            method = getattr(self.legacy_comp, method_name)
                            # Try different parameter signatures
                            try:
                                result = method(data, echo_value)
                            except TypeError:
                                try:
                                    result = method(data, strength=echo_value)
                                except TypeError:
                                    result = method(data)
                        
                            # Store in memory
                            key = f"echo_{datetime.now().timestamp()}"
                            self.store_memory(key, result)
                            
                            return EchoResponse(
                                success=True,
                                data=result,
                                message=f"Legacy echo operation completed (value: {echo_value})",
                                metadata={'echo_value': echo_value, 'memory_key': key, 'method_used': method_name}
                            )
                    
                    # Fallback to parent implementation
                    return super().echo(data, echo_value)
                except Exception as e:
                    return self.handle_error(e, "echo")
        
        return AdaptedMemoryComponent(self.legacy_component, config)
    
    def _create_processing_adapter(self, config: EchoConfig) -> ProcessingEchoComponent:
        """Create a ProcessingEchoComponent adapter"""
        
        class AdaptedProcessingComponent(ProcessingEchoComponent):
            def __init__(self, legacy_comp, adapter_config):
                super().__init__(adapter_config)
                self.legacy_comp = legacy_comp
                
            def initialize(self) -> EchoResponse:
                try:
                    if hasattr(self.legacy_comp, 'initialize'):
                        self.legacy_comp.initialize()
                    
                    self._initialized = True
                    return EchoResponse(
                        success=True,
                        message=f"Adapted processing component {self.config.component_name} initialized"
                    )
                except Exception as e:
                    return self.handle_error(e, "initialize")
            
            def process(self, input_data: Any, **kwargs) -> EchoResponse:
                try:
                    # Try different processing method names
                    for method_name in ['analyze', 'compute', 'process', 'process_data', 'run', 'execute']:
                        if hasattr(self.legacy_comp, method_name):
                            method = getattr(self.legacy_comp, method_name)
                            # Try calling with minimal arguments first
                            try:
                                result = method(input_data)
                            except TypeError:
                                # Try with kwargs if the method supports them
                                result = method(input_data, **kwargs)
                            
                            return EchoResponse(
                                success=True,
                                data=result,
                                message=f"Legacy component processing completed via {method_name}",
                                metadata={'method_used': method_name}
                            )
                    
                    # Fallback to parent implementation
                    return super().process(input_data, **kwargs)
                except Exception as e:
                    return self.handle_error(e, "process")
        
        return AdaptedProcessingComponent(self.legacy_component, config)
    
    def _create_basic_adapter(self, config: EchoConfig) -> EchoComponent:
        """Create a basic EchoComponent adapter"""
        
        class AdaptedBasicComponent(EchoComponent):
            def __init__(self, legacy_comp, adapter_config):
                super().__init__(adapter_config)
                self.legacy_comp = legacy_comp
                
            def initialize(self) -> EchoResponse:
                try:
                    if hasattr(self.legacy_comp, 'initialize'):
                        self.legacy_comp.initialize()
                    
                    self._initialized = True
                    return EchoResponse(
                        success=True,
                        message=f"Adapted basic component {self.config.component_name} initialized"
                    )
                except Exception as e:
                    return self.handle_error(e, "initialize")
            
            def process(self, input_data: Any, **kwargs) -> EchoResponse:
                try:
                    # Try to delegate to legacy component
                    for method_name in ['process', 'run', 'execute']:
                        if hasattr(self.legacy_comp, method_name):
                            method = getattr(self.legacy_comp, method_name)
                            result = method(input_data, **kwargs)
                            
                            return EchoResponse(
                                success=True,
                                data=result,
                                message=f"Legacy component processing via {method_name}"
                            )
                    
                    # Default: return input data
                    return EchoResponse(
                        success=True,
                        data=input_data,
                        message="Basic adapter processing completed"
                    )
                except Exception as e:
                    return self.handle_error(e, "process")
            
            def echo(self, data: Any, echo_value: float = 0.0) -> EchoResponse:
                try:
                    if hasattr(self.legacy_comp, 'echo'):
                        result = self.legacy_comp.echo(data, echo_value)
                        return EchoResponse(
                            success=True,
                            data=result,
                            message=f"Legacy echo operation (value: {echo_value})"
                        )
                    
                    # Default echo implementation
                    return EchoResponse(
                        success=True,
                        data=data,
                        message=f"Basic echo operation (value: {echo_value})"
                    )
                except Exception as e:
                    return self.handle_error(e, "echo")
        
        return AdaptedBasicComponent(self.legacy_component, config)


class EchoIntegrationAnalyzer:
    """
    Analyzer to assess integration readiness of existing Echo components
    """
    
    def __init__(self):
        self.logger = logging.getLogger("echo.integration.analyzer")
    
    def analyze_component(self, component: Any) -> IntegrationReport:
        """Analyze a component for integration readiness"""
        component_name = component.__class__.__name__
        
        # Check if already standardized
        if validate_echo_component(component):
            return IntegrationReport(
                component_name=component_name,
                integration_status='compatible',
                base_class_recommendation='Already standardized',
                integration_steps=['No migration needed'],
                migration_complexity='none'
            )
        
        # Analyze component structure
        methods = [method for method in dir(component) if not method.startswith('_')]
        has_echo = any('echo' in method.lower() for method in methods)
        has_process = any('process' in method.lower() or method in ['run', 'execute', 'compute'] for method in methods)
        has_memory = any('memory' in method.lower() or method in ['store', 'retrieve', 'save', 'load'] for method in methods)
        
        # Determine recommended base class
        if has_memory:
            recommendation = 'MemoryEchoComponent'
            complexity = 'medium'
        elif has_process:
            recommendation = 'ProcessingEchoComponent'
            complexity = 'low'
        else:
            recommendation = 'EchoComponent'
            complexity = 'low'
        
        # Generate integration steps
        steps = [
            f"Create EchoConfig for {component_name}",
            f"Inherit from {recommendation}",
            "Implement required abstract methods",
            "Update initialization to call parent __init__",
            "Wrap existing methods in EchoResponse objects"
        ]
        
        if not has_echo:
            steps.append("Implement echo() method")
        
        # Check for potential issues
        issues = []
        if hasattr(component, '__init__'):
            init_signature = inspect.signature(component.__init__)
            if len(init_signature.parameters) > 2:  # self + config
                issues.append("Constructor takes more parameters than standard EchoConfig")
        
        if not has_process and not has_echo:
            issues.append("Component lacks standard processing or echo methods")
            complexity = 'high'
        
        status = 'needs_migration' if issues else 'compatible'
        
        return IntegrationReport(
            component_name=component_name,
            integration_status=status,
            base_class_recommendation=recommendation,
            integration_steps=steps,
            compatibility_issues=issues,
            migration_complexity=complexity
        )


def create_integration_adapter(legacy_component: Any, component_name: str = None) -> EchoComponent:
    """
    Convenience function to create an adapter for a legacy Echo component
    
    Args:
        legacy_component: The existing component to adapt
        component_name: Optional name for the component
        
    Returns:
        Standardized EchoComponent wrapper
    """
    adapter = EchoComponentAdapter(legacy_component, component_name)
    return adapter.adapt_to_echo_component()


def analyze_integration_readiness(component: Any) -> IntegrationReport:
    """
    Convenience function to analyze a component's integration readiness
    
    Args:
        component: The component to analyze
        
    Returns:
        Integration analysis report
    """
    analyzer = EchoIntegrationAnalyzer()
    return analyzer.analyze_component(component)


def integration_decorator(base_class_type: str = 'auto'):
    """
    Decorator to automatically integrate classes with Echo base classes
    
    Args:
        base_class_type: Type of base class ('memory', 'processing', 'basic', 'auto')
    """
    def decorator(cls):
        # Determine the appropriate base class
        if base_class_type == 'memory':
            base_cls = MemoryEchoComponent
        elif base_class_type == 'processing':
            base_cls = ProcessingEchoComponent
        elif base_class_type == 'auto':
            # Auto-detect based on class name and methods
            if 'memory' in cls.__name__.lower():
                base_cls = MemoryEchoComponent
            elif 'process' in cls.__name__.lower():
                base_cls = ProcessingEchoComponent
            else:
                base_cls = EchoComponent
        else:
            base_cls = EchoComponent
        
        # Create a new class that properly inherits from the base class
        class IntegratedComponent(base_cls):
            pass
        
        # Copy all attributes from the original class
        for name, value in cls.__dict__.items():
            if not name.startswith('__') or name in ['__init__']:
                setattr(IntegratedComponent, name, value)
        
        # Set the class name
        IntegratedComponent.__name__ = cls.__name__
        IntegratedComponent.__qualname__ = cls.__qualname__
        
        # Handle initialization properly
        original_init = getattr(cls, '__init__', None)
        
        def new_init(self, *args, **kwargs):
            # If first arg is EchoConfig, use it; otherwise create one
            if args and isinstance(args[0], EchoConfig):
                config = args[0]
                remaining_args = args[1:]
            else:
                config = EchoConfig(component_name=cls.__name__)
                remaining_args = args
            
            # Initialize base class
            base_cls.__init__(self, config)
            
            # Call original init with remaining args if it exists
            if original_init and remaining_args or kwargs:
                # Create a temporary method to call the original init
                def temp_init(temp_self, *temp_args, **temp_kwargs):
                    return original_init(temp_self, *temp_args, **temp_kwargs)
                temp_init(self, *remaining_args, **kwargs)
        
        IntegratedComponent.__init__ = new_init
        return IntegratedComponent
    
    return decorator


# Example usage functions
def demonstrate_integration():
    """Demonstrate the integration capabilities"""
    print("🔗 Echo Component Integration Demonstration")
    print("=" * 50)
    
    # Example legacy component
    class LegacyEchoComponent:
        def __init__(self, name):
            self.name = name
            
        def process_data(self, data):
            return f"Processed: {data}"
            
        def echo(self, data, value=0.5):
            return f"Echo[{value}]: {data}"
    
    # Create legacy component
    legacy = LegacyEchoComponent("TestLegacy")
    
    # Analyze integration readiness
    print("📊 Analyzing integration readiness...")
    report = analyze_integration_readiness(legacy)
    print(f"   Status: {report.integration_status}")
    print(f"   Recommended base class: {report.base_class_recommendation}")
    print(f"   Migration complexity: {report.migration_complexity}")
    
    # Create adapter
    print("\n🔧 Creating integration adapter...")
    adapted_component = create_integration_adapter(legacy, "TestLegacyAdapter")
    
    # Test the adapted component
    print("\n🧪 Testing adapted component...")
    init_result = adapted_component.initialize()
    print(f"   Initialization: {'✅' if init_result.success else '❌'}")
    
    process_result = adapted_component.process("test data")
    print(f"   Processing: {'✅' if process_result.success else '❌'}")
    
    echo_result = adapted_component.echo("test echo", 0.75)
    print(f"   Echo: {'✅' if echo_result.success else '❌'}")
    
    # Show component info
    info = get_echo_component_info(adapted_component)
    print(f"\n📋 Component Info:")
    print(f"   Name: {info['component_name']}")
    print(f"   Type: {info['type']}")
    print(f"   Initialized: {info['initialized']}")
    
    return True


if __name__ == "__main__":
    demonstrate_integration()