# Introspection Testing Patterns

## Overview

This document defines testing patterns and best practices for the Echoself introspection system integration. It provides guidelines for writing comprehensive tests that validate both introspection functionality and unified architecture compliance.

## Test Architecture

### Test Class Hierarchy

```
TestEchoselfIntegration
├── Core Functionality Tests (9 methods)
│   ├── test_introspection_system_initialization
│   ├── test_recursive_introspection_execution  
│   ├── test_introspection_with_automatic_calculation
│   ├── test_introspection_metrics_retrieval
│   ├── test_adaptive_goal_generation_with_introspection
│   ├── test_cognitive_load_calculation
│   ├── test_recent_activity_calculation
│   ├── test_introspection_memory_storage
│   └── test_export_introspection_data

TestIntrospectionEnhancedBehavior
├── Advanced Behavior Tests (3 methods)
│   ├── test_introspection_influences_personality
│   ├── test_recursive_feedback_loop
│   └── test_attention_allocation_adaptation

TestUnifiedArchitectureIntegration
├── Architecture Compliance Tests (5 methods)
│   ├── test_echo_config_integration
│   ├── test_echo_response_standardization
│   ├── test_memory_integration_compatibility
│   ├── test_echo_component_compliance_readiness
│   └── test_integration_documentation_compliance
```

## Testing Patterns

### Pattern 1: Unified Architecture Compatibility

```python
def test_unified_architecture_feature(self):
    """Test pattern for unified architecture compliance"""
    
    # 1. Setup with Echo configuration
    if ECHO_COMPONENTS_AVAILABLE:
        config = EchoConfig(
            component_name="test_component",
            echo_threshold=0.8,
            custom_params={"test_mode": True}
        )
    
    # 2. Execute core functionality
    result = self.cognitive_arch.some_method()
    
    # 3. Wrap in EchoResponse format
    response = self._wrap_in_echo_response(
        data=result,
        success=True,
        message="Operation completed successfully"
    )
    
    # 4. Validate both legacy and unified formats
    self.assertIsNotNone(result)  # Legacy validation
    if hasattr(response, 'success'):
        self.assertTrue(response.success)  # Unified validation
```

### Pattern 2: Memory Integration Testing

```python
def test_memory_integration_pattern(self):
    """Test pattern for memory system integration"""
    
    # 1. Capture initial state
    initial_memory_count = len(self.cognitive_arch.memories)
    
    # 2. Perform operation that should create memories
    self.cognitive_arch.perform_recursive_introspection(0.6, 0.4)
    
    # 3. Validate memory creation
    final_memory_count = len(self.cognitive_arch.memories)
    self.assertGreater(final_memory_count, initial_memory_count)
    
    # 4. Validate memory structure
    if self.cognitive_arch.memories:
        memory = list(self.cognitive_arch.memories.values())[-1]
        self.assertTrue(hasattr(memory, 'content'))
        self.assertTrue(hasattr(memory, 'timestamp'))
        self.assertIn('introspection', memory.content.lower())
```

### Pattern 3: Metrics and Performance Testing

```python
def test_metrics_pattern(self):
    """Test pattern for metrics validation"""
    
    # 1. Get baseline metrics
    metrics_before = self.cognitive_arch.get_introspection_metrics()
    
    # 2. Perform measured operations
    for i in range(3):
        self.cognitive_arch.perform_recursive_introspection(0.5, 0.3)
    
    # 3. Get updated metrics
    metrics_after = self.cognitive_arch.get_introspection_metrics()
    
    # 4. Validate metric changes
    self.assertGreater(
        metrics_after.get("total_decisions", 0),
        metrics_before.get("total_decisions", 0)
    )
    
    # 5. Validate metric structure
    expected_keys = {"total_decisions", "hypergraph_nodes"}
    self.assertTrue(expected_keys.issubset(metrics_after.keys()))
```

### Pattern 4: Echo Response Standardization

```python
def _wrap_in_echo_response(self, data, success=True, message=""):
    """Standard pattern for Echo response wrapping"""
    if ECHO_COMPONENTS_AVAILABLE and EchoResponse:
        return EchoResponse(
            success=success,
            data=data,
            message=message,
            metadata={
                "test_context": self.__class__.__name__,
                "timestamp": time.time(),
                "unified_architecture": True
            }
        )
    return data

def test_with_echo_response(self):
    """Test pattern using standardized responses"""
    
    # Execute operation
    result = self.cognitive_arch.some_operation()
    
    # Wrap in standard format
    response = self._wrap_in_echo_response(
        data={"result": result, "status": "completed"},
        success=True,
        message="Operation successful"
    )
    
    # Validate both formats
    self.assertIsNotNone(result)
    if hasattr(response, 'success'):
        self.assertTrue(response.success)
        self.assertIn("result", response.data)
```

### Pattern 5: Graceful Degradation Testing

```python
@unittest.skipUnless(ECHO_COMPONENTS_AVAILABLE, "Echo components not available")
def test_with_echo_components(self):
    """Test pattern for Echo component dependent functionality"""
    # Test only runs when unified architecture is available
    config = EchoConfig(component_name="test")
    # ... test unified functionality
    
def test_without_echo_components(self):
    """Test pattern for graceful degradation"""
    # Test runs regardless of unified architecture availability
    # Should validate core functionality works without Echo components
    result = self.cognitive_arch.perform_recursive_introspection()
    self.assertIsNotNone(result)
```

## Test Categories

### Category 1: Core Functionality Tests

**Purpose**: Validate basic introspection functionality
**Pattern**: Direct method testing with assertion validation
**Example**:

```python
def test_core_functionality(self):
    """Test core introspection functionality"""
    # Test system initialization
    self.assertIsNotNone(self.cognitive_arch.echoself_introspection)
    
    # Test method execution
    prompt = self.cognitive_arch.perform_recursive_introspection(0.6, 0.4)
    self.assertIsInstance(prompt, str)
    self.assertIn("DeepTreeEcho", prompt)
```

### Category 2: Integration Tests

**Purpose**: Validate integration with external systems
**Pattern**: Multi-component interaction testing
**Example**:

```python
def test_integration(self):
    """Test integration between components"""
    # Test introspection -> memory -> goals workflow
    self.cognitive_arch.perform_recursive_introspection(0.5, 0.3)
    goals = self.cognitive_arch.adaptive_goal_generation_with_introspection()
    
    # Validate end-to-end functionality
    self.assertGreater(len(goals), 0)
    self.assertTrue(any("introspection" in g.description.lower() for g in goals))
```

### Category 3: Architecture Compliance Tests

**Purpose**: Validate unified architecture compliance
**Pattern**: Echo component interface testing
**Example**:

```python
def test_architecture_compliance(self):
    """Test unified architecture compliance"""
    # Test component has required methods
    required_methods = ['perform_recursive_introspection']
    for method in required_methods:
        self.assertTrue(hasattr(self.cognitive_arch, method))
    
    # Test standardized response format
    result = self.cognitive_arch.perform_recursive_introspection()
    response = self._wrap_in_echo_response(result)
    if hasattr(response, 'success'):
        self.assertTrue(response.success)
```

### Category 4: Performance and Behavior Tests

**Purpose**: Validate performance and behavioral characteristics
**Pattern**: Metrics-based validation with time/resource monitoring
**Example**:

```python
def test_performance_behavior(self):
    """Test performance and behavioral characteristics"""
    import time
    
    start_time = time.time()
    self.cognitive_arch.perform_recursive_introspection(0.7, 0.5)
    execution_time = time.time() - start_time
    
    # Validate reasonable performance
    self.assertLess(execution_time, 5.0)  # Should complete within 5 seconds
```

## Best Practices

### 1. Test Isolation

```python
def setUp(self):
    """Ensure clean test environment"""
    logging.disable(logging.CRITICAL)  # Suppress test noise
    self.cognitive_arch = CognitiveArchitecture()  # Fresh instance
    
def tearDown(self):
    """Clean up test environment"""
    logging.disable(logging.NOTSET)  # Restore logging
```

### 2. Comprehensive Validation

```python
def test_comprehensive_validation(self):
    """Validate multiple aspects of functionality"""
    
    # 1. Input validation
    with self.assertRaises(ValueError):
        self.cognitive_arch.perform_recursive_introspection(-1.0, 0.5)
    
    # 2. Output validation
    result = self.cognitive_arch.perform_recursive_introspection(0.5, 0.3)
    self.assertIsInstance(result, str)
    self.assertGreater(len(result), 0)
    
    # 3. Side effect validation
    metrics = self.cognitive_arch.get_introspection_metrics()
    self.assertIn("total_decisions", metrics)
    
    # 4. State validation
    self.assertGreater(len(self.cognitive_arch.memories), 0)
```

### 3. Mock Usage for External Dependencies

```python
from unittest.mock import Mock, patch

def test_with_mocked_dependencies(self):
    """Test with mocked external dependencies"""
    
    with patch('cognitive_architecture.some_external_service') as mock_service:
        mock_service.return_value = "mocked_response"
        
        result = self.cognitive_arch.perform_recursive_introspection()
        
        # Validate interaction with mocked service
        mock_service.assert_called_once()
        self.assertIsNotNone(result)
```

### 4. Data-Driven Testing

```python
def test_data_driven_scenarios(self):
    """Test multiple scenarios with different parameters"""
    
    test_scenarios = [
        (0.3, 0.2, "low_load_scenario"),
        (0.7, 0.8, "high_load_scenario"), 
        (0.5, 0.5, "balanced_scenario")
    ]
    
    for cognitive_load, activity, scenario_name in test_scenarios:
        with self.subTest(scenario=scenario_name):
            result = self.cognitive_arch.perform_recursive_introspection(
                cognitive_load, activity
            )
            self.assertIsNotNone(result, f"Failed for {scenario_name}")
```

## Debugging Patterns

### 1. Debug Mode Testing

```python
def test_with_debug_mode(self):
    """Test with debug logging enabled"""
    
    if ECHO_COMPONENTS_AVAILABLE:
        debug_config = EchoConfig(
            component_name="debug_test",
            debug_mode=True
        )
        # Enable detailed logging for troubleshooting
    
    # Perform operation with debug info
    with self.assertLogs(level='DEBUG'):
        result = self.cognitive_arch.perform_recursive_introspection()
```

### 2. State Inspection

```python
def test_state_inspection(self):
    """Test with detailed state inspection"""
    
    # Capture initial state
    initial_state = {
        'memory_count': len(self.cognitive_arch.memories),
        'metrics': self.cognitive_arch.get_introspection_metrics()
    }
    
    # Perform operation
    self.cognitive_arch.perform_recursive_introspection(0.6, 0.4)
    
    # Inspect final state
    final_state = {
        'memory_count': len(self.cognitive_arch.memories),
        'metrics': self.cognitive_arch.get_introspection_metrics()
    }
    
    # Validate state changes
    self.assertGreater(final_state['memory_count'], initial_state['memory_count'])
```

## Continuous Integration

### Test Execution Commands

```bash
# Run all introspection tests
python -m unittest test_echoself_integration -v

# Run with coverage
python -m coverage run -m unittest test_echoself_integration
python -m coverage report

# Run specific test patterns
python -m unittest test_echoself_integration.TestUnifiedArchitectureIntegration -v

# Run with different configurations
ECHO_COMPONENTS_AVAILABLE=1 python -m unittest test_echoself_integration -v
```

### CI Configuration Example

```yaml
test_introspection:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run introspection tests
      run: |
        python -m unittest test_echoself_integration -v
    - name: Run with unified architecture
      run: |
        ECHO_COMPONENTS_AVAILABLE=1 python -m unittest test_echoself_integration -v
```

## See Also

- [Echoself Integration Guide](./ECHOSELF_INTEGRATION_GUIDE.md)
- [Echo Component Base Classes](./echo_component_base.py)
- [Cognitive Architecture Documentation](./cognitive_architecture.py)
- [Deep Tree Echo Testing Patterns](./test_deep_tree_echo.py)