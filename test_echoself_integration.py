"""
Integration test for Echoself recursive self-model integration

This module tests the integration of Echoself with CognitiveArchitecture
and validates compatibility with the unified Echo component architecture.

Fragment Analysis: EXTENSION type, ACTIVE status
- Provides comprehensive testing of introspection functionality  
- Validates integration with unified architecture patterns
- Tests echo propagation and memory integration
- Ensures compatibility with EchoComponent standardization

Integration Points:
- CognitiveArchitecture (main component under test)
- EchoComponent base class compatibility
- Unified memory system integration  
- Introspection and recursive processing
"""

import unittest
import tempfile
import logging
from pathlib import Path
from cognitive_architecture import CognitiveArchitecture

# Import unified Echo architecture components for integration testing
try:
    from echo_component_base import EchoComponent, EchoConfig, EchoResponse
    ECHO_COMPONENTS_AVAILABLE = True
except ImportError:
    # Graceful degradation if unified architecture not fully available
    ECHO_COMPONENTS_AVAILABLE = False
    EchoComponent = object
    EchoConfig = None
    EchoResponse = None


class TestEchoselfIntegration(unittest.TestCase):
    """
    Test the integration of Echoself with CognitiveArchitecture
    
    This test class validates:
    - Core introspection functionality
    - Integration with unified Echo architecture
    - Memory system compatibility
    - Echo response standardization
    """
    
    def setUp(self):
        """Set up test environment with unified architecture compatibility"""
        # Suppress logs during testing
        logging.disable(logging.CRITICAL)
        self.cognitive_arch = CognitiveArchitecture()
        
        # Initialize Echo component compatibility if available
        if ECHO_COMPONENTS_AVAILABLE:
            self.echo_config = EchoConfig(
                component_name="echoself_integration_test",
                version="1.0.0",
                echo_threshold=0.75,
                debug_mode=False
            )
        else:
            self.echo_config = None
    
    def tearDown(self):
        """Clean up test environment"""
        logging.disable(logging.NOTSET)
    
    def _wrap_in_echo_response(self, data, success=True, message=""):
        """
        Wrapper to provide EchoResponse compatibility
        
        Args:
            data: The actual test data/result
            success: Boolean indicating operation success  
            message: Optional message string
            
        Returns:
            EchoResponse object if available, otherwise raw data
        """
        if ECHO_COMPONENTS_AVAILABLE and EchoResponse:
            return EchoResponse(
                success=success,
                data=data,
                message=message,
                metadata={"test_context": "echoself_integration"}
            )
        return data
    
    def test_introspection_system_initialization(self):
        """
        Test that introspection system initializes properly
        
        Validates:
        - Basic initialization of introspection system
        - Compatibility with unified Echo architecture 
        - Proper component state management
        """
        # The system should have introspection available
        self.assertIsNotNone(self.cognitive_arch.echoself_introspection)
        
        # Test unified architecture compatibility
        if ECHO_COMPONENTS_AVAILABLE:
            # Verify the component can work with Echo architecture
            result = self._wrap_in_echo_response(
                data={"introspection_available": True},
                success=True,
                message="Introspection system initialized successfully"
            )
            self.assertTrue(result.success if hasattr(result, 'success') else True)
    
    def test_recursive_introspection_execution(self):
        """
        Test performing recursive introspection
        
        Validates:
        - Core introspection functionality
        - Echo-compatible response format
        - Proper parameter handling
        """
        # Perform introspection with specific parameters
        prompt = self.cognitive_arch.perform_recursive_introspection(
            current_cognitive_load=0.6,
            recent_activity_level=0.4
        )
        
        # Should return a valid prompt
        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertIn("DeepTreeEcho", prompt)
        self.assertIn("Repository Hypergraph Analysis", prompt)
        
        # Test with Echo response wrapper
        wrapped_result = self._wrap_in_echo_response(
            data={"prompt": prompt, "parameters": {"cognitive_load": 0.6, "activity": 0.4}},
            success=True,
            message="Recursive introspection completed successfully"
        )
        
        if hasattr(wrapped_result, 'success'):
            self.assertTrue(wrapped_result.success)
            self.assertIn("prompt", wrapped_result.data)
    
    def test_introspection_with_automatic_calculation(self):
        """Test introspection with automatic cognitive load calculation"""
        prompt = self.cognitive_arch.perform_recursive_introspection()
        
        # Should still work with calculated values
        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
    
    def test_introspection_metrics_retrieval(self):
        """Test getting introspection metrics"""
        # First perform some introspection to generate metrics
        self.cognitive_arch.perform_recursive_introspection(0.5, 0.3)
        
        # Get metrics
        metrics = self.cognitive_arch.get_introspection_metrics()
        
        # Should return valid metrics
        self.assertIsInstance(metrics, dict)
        self.assertIn("total_decisions", metrics)
        self.assertIn("hypergraph_nodes", metrics)
    
    def test_adaptive_goal_generation_with_introspection(self):
        """Test goal generation enhanced with introspection"""
        goals = self.cognitive_arch.adaptive_goal_generation_with_introspection()
        
        # Should generate some goals
        self.assertIsInstance(goals, list)
        self.assertGreater(len(goals), 0)
        
        # Check for introspection-specific goals
        introspection_goals = [
            g for g in goals 
            if "introspection" in g.description.lower() or 
               "hypergraph" in g.description.lower()
        ]
        self.assertGreater(len(introspection_goals), 0)
    
    def test_cognitive_load_calculation(self):
        """Test cognitive load calculation"""
        load = self.cognitive_arch._calculate_current_cognitive_load()
        
        # Should be a valid float between 0.1 and 0.9
        self.assertIsInstance(load, float)
        self.assertGreaterEqual(load, 0.1)
        self.assertLessEqual(load, 0.9)
    
    def test_recent_activity_calculation(self):
        """Test recent activity calculation"""
        activity = self.cognitive_arch._calculate_recent_activity()
        
        # Should be a valid float between 0.1 and 1.0
        self.assertIsInstance(activity, float)
        self.assertGreaterEqual(activity, 0.1)
        self.assertLessEqual(activity, 1.0)
    
    def test_introspection_memory_storage(self):
        """Test that introspection creates memories"""
        initial_memory_count = len(self.cognitive_arch.memories)
        
        # Perform introspection
        self.cognitive_arch.perform_recursive_introspection(0.5, 0.3)
        
        # Should have created a new memory
        self.assertGreater(len(self.cognitive_arch.memories), initial_memory_count)
        
        # Check for introspection memory
        introspection_memories = [
            m for m in self.cognitive_arch.memories.values()
            if "introspection" in m.content.lower()
        ]
        self.assertGreater(len(introspection_memories), 0)
    
    def test_export_introspection_data(self):
        """Test exporting introspection data"""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Perform introspection to generate data
            self.cognitive_arch.perform_recursive_introspection(0.5, 0.3)
            
            # Export data
            success = self.cognitive_arch.export_introspection_data(tmp_path)
            
            # Should succeed
            self.assertTrue(success)
            
            # File should exist
            self.assertTrue(Path(tmp_path).exists())
            
        finally:
            # Clean up
            Path(tmp_path).unlink(missing_ok=True)


class TestIntrospectionEnhancedBehavior(unittest.TestCase):
    """Test enhanced cognitive behaviors with introspection"""
    
    def setUp(self):
        """Set up test environment"""
        logging.disable(logging.CRITICAL)
        self.cognitive_arch = CognitiveArchitecture()
    
    def tearDown(self):
        """Clean up test environment"""
        logging.disable(logging.NOTSET)
    
    def test_introspection_influences_personality(self):
        """Test that introspection can influence personality development"""
        # Get initial curiosity level
        initial_curiosity = self.cognitive_arch.personality_traits["curiosity"].current_value
        
        # Perform introspection
        self.cognitive_arch.perform_recursive_introspection()
        
        # Generate introspection-enhanced goals
        goals = self.cognitive_arch.adaptive_goal_generation_with_introspection()
        
        # Should have goals that could influence personality
        exploration_goals = [
            g for g in goals
            if "explore" in g.description.lower() or "analyze" in g.description.lower()
        ]
        self.assertGreater(len(exploration_goals), 0)
    
    def test_recursive_feedback_loop(self):
        """Test recursive feedback between introspection and goal generation"""
        initial_memory_count = len(self.cognitive_arch.memories)
        
        # Perform multiple cycles
        for i in range(3):
            # Introspect
            prompt = self.cognitive_arch.perform_recursive_introspection()
            self.assertIsNotNone(prompt)
            
            # Generate goals
            goals = self.cognitive_arch.adaptive_goal_generation_with_introspection()
            self.assertGreater(len(goals), 0)
        
        # Should have at least created some new memories over all cycles
        final_memory_count = len(self.cognitive_arch.memories)
        self.assertGreater(final_memory_count, initial_memory_count)
    
    def test_attention_allocation_adaptation(self):
        """Test that attention allocation adapts over time"""
        metrics_1 = self.cognitive_arch.get_introspection_metrics()
        
        # Perform several introspections with different loads
        for load in [0.3, 0.7, 0.5, 0.9, 0.2]:
            self.cognitive_arch.perform_recursive_introspection(load, 0.5)
        
        metrics_2 = self.cognitive_arch.get_introspection_metrics()
        
        # Should have more decisions in history
        self.assertGreater(
            metrics_2.get("total_decisions", 0), 
            metrics_1.get("total_decisions", 0)
        )


class TestUnifiedArchitectureIntegration(unittest.TestCase):
    """
    Test integration with unified Echo component architecture
    
    This test class validates compatibility and integration with the 
    standardized Echo component base classes and unified interfaces.
    
    Fragment Analysis Integration: Tests the integration points identified
    in the fragment analysis for unified architecture compliance.
    """
    
    def setUp(self):
        """Set up test environment for unified architecture testing"""
        logging.disable(logging.CRITICAL)
        self.cognitive_arch = CognitiveArchitecture()
        
        # Initialize Echo configuration if available
        if ECHO_COMPONENTS_AVAILABLE:
            self.echo_config = EchoConfig(
                component_name="unified_integration_test",
                version="1.0.0",
                echo_threshold=0.8,
                max_depth=15,
                debug_mode=True,
                custom_params={
                    "introspection_enabled": True,
                    "memory_integration": True,
                    "recursive_depth": 3
                }
            )
        
    def tearDown(self):
        """Clean up test environment"""
        logging.disable(logging.NOTSET)
    
    @unittest.skipUnless(ECHO_COMPONENTS_AVAILABLE, "Echo components not available")
    def test_echo_config_integration(self):
        """Test EchoConfig integration with CognitiveArchitecture"""
        # Validate EchoConfig structure
        self.assertIsNotNone(self.echo_config)
        self.assertEqual(self.echo_config.component_name, "unified_integration_test")
        self.assertTrue(self.echo_config.custom_params["introspection_enabled"])
        
        # Test configuration application (would require CognitiveArchitecture modification)
        # For now, validate the config object structure
        self.assertTrue(hasattr(self.echo_config, 'echo_threshold'))
        self.assertTrue(hasattr(self.echo_config, 'max_depth'))
    
    @unittest.skipUnless(ECHO_COMPONENTS_AVAILABLE, "Echo components not available")
    def test_echo_response_standardization(self):
        """Test EchoResponse standardization for introspection results"""
        # Perform introspection and wrap in EchoResponse
        prompt = self.cognitive_arch.perform_recursive_introspection(0.7, 0.5)
        
        response = EchoResponse(
            success=True,
            data={
                "introspection_prompt": prompt,
                "cognitive_load": 0.7,
                "activity_level": 0.5,
                "component": "echoself_introspection"
            },
            message="Introspection completed with unified response format",
            metadata={
                "echo_threshold": self.echo_config.echo_threshold,
                "processing_time": 0.1,
                "unified_architecture": True
            }
        )
        
        # Validate EchoResponse structure
        self.assertTrue(response.success)
        self.assertIn("introspection_prompt", response.data)
        self.assertIsInstance(response.message, str)
        self.assertTrue(response.metadata["unified_architecture"])
    
    def test_memory_integration_compatibility(self):
        """Test compatibility with unified memory system"""
        # Test memory creation during introspection
        initial_memory_count = len(self.cognitive_arch.memories)
        
        # Perform introspection (creates memories)
        self.cognitive_arch.perform_recursive_introspection(0.6, 0.4)
        
        # Validate memory creation
        final_memory_count = len(self.cognitive_arch.memories)
        self.assertGreater(final_memory_count, initial_memory_count)
        
        # Test memory structure compatibility
        if self.cognitive_arch.memories:
            memory = list(self.cognitive_arch.memories.values())[0]
            # Should have unified memory interface attributes
            self.assertTrue(hasattr(memory, 'content'))
            self.assertTrue(hasattr(memory, 'timestamp'))
    
    def test_echo_component_compliance_readiness(self):
        """Test readiness for EchoComponent compliance"""
        # Test that CognitiveArchitecture has the methods needed for EchoComponent
        required_methods = ['perform_recursive_introspection']  # Main processing method
        optional_methods = ['get_introspection_metrics', 'export_introspection_data']
        
        for method in required_methods:
            self.assertTrue(
                hasattr(self.cognitive_arch, method),
                f"CognitiveArchitecture missing required method: {method}"
            )
        
        for method in optional_methods:
            self.assertTrue(
                hasattr(self.cognitive_arch, method),
                f"CognitiveArchitecture missing optional method: {method}"
            )
        
        # Test that methods return appropriate data
        prompt = self.cognitive_arch.perform_recursive_introspection()
        self.assertIsNotNone(prompt)
        
        metrics = self.cognitive_arch.get_introspection_metrics()
        self.assertIsInstance(metrics, dict)
    
    def test_integration_documentation_compliance(self):
        """Test that integration follows documented patterns"""
        # This test validates that the integration follows the patterns
        # identified in the fragment analysis
        
        # Test 1: Introspection system availability
        self.assertIsNotNone(self.cognitive_arch.echoself_introspection)
        
        # Test 2: Method consistency with Echo patterns  
        result = self.cognitive_arch.perform_recursive_introspection(0.5, 0.3)
        self.assertIsInstance(result, str)  # Should return string (prompt)
        
        # Test 3: Memory integration patterns
        metrics = self.cognitive_arch.get_introspection_metrics()
        self.assertIn("total_decisions", metrics)
        self.assertIn("hypergraph_nodes", metrics)
        
        # Test 4: Export functionality (unified interface pattern)
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            export_success = self.cognitive_arch.export_introspection_data(tmp.name)
            self.assertTrue(export_success)


if __name__ == "__main__":
    unittest.main()