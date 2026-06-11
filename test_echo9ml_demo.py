"""
Test suite for echo9ml_demo.py functionality

Tests the demonstration functions and ensures they execute properly
without requiring full system dependencies for testing.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import json
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestEcho9mlDemo(unittest.TestCase):
    """Test echo9ml_demo functionality with mocked dependencies"""

    def setUp(self):
        """Set up test environment with mocked echo9ml system"""
        self.mock_system = Mock()
        self.mock_system.persona_kernel = Mock()
        self.mock_system.persona_kernel.name = "Deep Tree Echo"
        self.mock_system.persona_kernel.traits = {
            Mock(value="memory"): 0.5,
            Mock(value="reasoning"): 0.6,
            Mock(value="creativity"): 0.4
        }
        self.mock_system.tensor_encoding = Mock()
        self.mock_system.tensor_encoding.tensor_shape = (7, 7)
        
        # Mock system methods
        self.mock_system.process_experience.return_value = {
            'persona_state': {'confidence': 0.7, 'adaptability': 0.6},
            'evolution_strategy': 'gradual_adaptation',
            'suggestions': []
        }
        self.mock_system.get_cognitive_snapshot.return_value = {
            'persona_kernel': {'traits': {'memory': 0.5, 'reasoning': 0.6}},
            'hypergraph': {'node_count': 10, 'edge_count': 15, 'active_nodes': [1, 2, 3]},
            'attention': {'top_focus': [('learning', 0.8), ('creativity', 0.6)]},
            'meta_cognitive': {'recent_suggestions': []},
            'system_stats': {'interaction_count': 5, 'total_evolution_events': 3, 'system_uptime': 10.5}
        }

    @patch('echo9ml_demo.create_echo9ml_system')
    def test_demonstrate_basic_usage(self, mock_create):
        """Test basic usage demonstration function"""
        mock_create.return_value = self.mock_system
        
        # Import and test the function
        try:
            import echo9ml_demo
            result = echo9ml_demo.demonstrate_basic_usage()
            
            # Verify system was created and used
            mock_create.assert_called_once()
            self.mock_system.process_experience.assert_called_once()
            self.assertEqual(result, self.mock_system)
            
        except ImportError as e:
            self.skipTest(f"Cannot import echo9ml_demo due to missing dependencies: {e}")

    @patch('echo9ml_demo.create_echo9ml_system')
    def test_demonstrate_learning_progression(self, mock_create):
        """Test learning progression demonstration"""
        # Setup trait mocks for learning progression
        trait_mock = Mock()
        trait_mock.value = "reasoning"
        
        self.mock_system.persona_kernel.traits = {trait_mock: 0.5}
        mock_create.return_value = self.mock_system
        
        try:
            import echo9ml_demo
            result = echo9ml_demo.demonstrate_learning_progression()
            
            # Should call process_experience multiple times (5 learning stages)
            self.assertEqual(self.mock_system.process_experience.call_count, 5)
            self.assertEqual(result, self.mock_system)
            
        except ImportError as e:
            self.skipTest(f"Cannot import echo9ml_demo due to missing dependencies: {e}")

    @patch('echo9ml_demo.create_echo9ml_system')
    def test_demonstrate_creative_exploration(self, mock_create):
        """Test creative exploration demonstration"""
        mock_create.return_value = self.mock_system
        
        try:
            import echo9ml_demo
            result = echo9ml_demo.demonstrate_creative_exploration()
            
            # Should call process_experience 4 times (4 creative activities)
            self.assertEqual(self.mock_system.process_experience.call_count, 4)
            self.assertEqual(result, self.mock_system)
            
        except ImportError as e:
            self.skipTest(f"Cannot import echo9ml_demo due to missing dependencies: {e}")

    @patch('echo9ml_demo.create_echo9ml_system')
    def test_demonstrate_stress_adaptation(self, mock_create):
        """Test stress adaptation demonstration"""
        mock_create.return_value = self.mock_system
        
        try:
            import echo9ml_demo
            result = echo9ml_demo.demonstrate_stress_adaptation()
            
            # Should call process_experience 5 times (5 stress scenarios)
            self.assertEqual(self.mock_system.process_experience.call_count, 5)
            self.assertEqual(result, self.mock_system)
            
        except ImportError as e:
            self.skipTest(f"Cannot import echo9ml_demo due to missing dependencies: {e}")

    @patch('echo9ml_demo.create_echo9ml_system')
    def test_demonstrate_cognitive_snapshot(self, mock_create):
        """Test cognitive snapshot demonstration"""
        mock_create.return_value = self.mock_system
        
        try:
            import echo9ml_demo
            system, snapshot = echo9ml_demo.demonstrate_cognitive_snapshot()
            
            # Should process 4 experiences before snapshot
            self.assertEqual(self.mock_system.process_experience.call_count, 4)
            self.mock_system.get_cognitive_snapshot.assert_called_once()
            self.assertEqual(system, self.mock_system)
            self.assertIsInstance(snapshot, dict)
            
        except ImportError as e:
            self.skipTest(f"Cannot import echo9ml_demo due to missing dependencies: {e}")

    @patch('echo9ml_demo.create_echo9ml_system')
    def test_save_demo_results(self, mock_create):
        """Test demo results saving functionality"""
        mock_create.return_value = self.mock_system
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mock Path.home() to return our temp directory
            with patch('pathlib.Path.home', return_value=Path(temp_dir)):
                try:
                    import echo9ml_demo
                    echo9ml_demo.save_demo_results(self.mock_system, "test_demo")
                    
                    # Check that file was created
                    expected_file = Path(temp_dir) / '.echo9ml' / 'demos' / 'test_demo_results.json'
                    self.assertTrue(expected_file.exists())
                    
                    # Verify content is valid JSON
                    with open(expected_file) as f:
                        data = json.load(f)
                        self.assertIsInstance(data, dict)
                        
                except ImportError as e:
                    self.skipTest(f"Cannot import echo9ml_demo due to missing dependencies: {e}")

    def test_demo_structure_analysis(self):
        """Test that demo file has expected structure"""
        demo_file = Path(__file__).parent / 'echo9ml_demo.py'
        self.assertTrue(demo_file.exists(), "echo9ml_demo.py should exist")
        
        # Read and analyze the file content
        with open(demo_file) as f:
            content = f.read()
            
        # Check for expected function definitions
        expected_functions = [
            'demonstrate_basic_usage',
            'demonstrate_learning_progression', 
            'demonstrate_creative_exploration',
            'demonstrate_stress_adaptation',
            'demonstrate_cognitive_snapshot',
            'save_demo_results',
            'main'
        ]
        
        for func_name in expected_functions:
            self.assertIn(f"def {func_name}", content, 
                         f"Function {func_name} should be defined")

    def test_line_count_verification(self):
        """Verify the actual line count of the demo file"""
        demo_file = Path(__file__).parent / 'echo9ml_demo.py'
        
        with open(demo_file) as f:
            lines = f.readlines()
            
        # Verify line count matches our analysis (320 total lines)
        self.assertEqual(len(lines), 320, 
                        "Line count should match fragment analysis report")

    def test_import_structure(self):
        """Test the expected import structure"""
        demo_file = Path(__file__).parent / 'echo9ml_demo.py'
        
        with open(demo_file) as f:
            content = f.read()
            
        # Check for expected imports
        self.assertIn("from echo9ml import", content)
        self.assertIn("create_echo9ml_system", content)
        self.assertIn("PersonaTraitType", content)


class TestDemoIntegration(unittest.TestCase):
    """Integration tests for demo functionality"""

    def test_demo_metadata_consistency(self):
        """Test that demo metadata is consistent with analysis"""
        demo_file = Path(__file__).parent / 'echo9ml_demo.py'
        
        # File should exist
        self.assertTrue(demo_file.exists())
        
        # Check basic file properties
        with open(demo_file) as f:
            content = f.read()
            lines = content.split('\n')
            
        # No class definitions (as stated in analysis)
        class_definitions = [line for line in lines if line.strip().startswith('class ')]
        self.assertEqual(len(class_definitions), 0, 
                        "Should have no class definitions")
        
        # No functions with 'echo' in the name
        function_lines = [line for line in lines if line.strip().startswith('def ')]
        echo_functions = [line for line in function_lines if 'echo' in line.lower()]
        self.assertEqual(len(echo_functions), 0, 
                        "Should have no functions with 'echo' in name")


if __name__ == '__main__':
    unittest.main()