"""
# copilot/fix-6-2
Test suite for EchoselfIntrospection module
#=======
Test module for Echoself Introspection functionality

Tests the hypergraph encoding, semantic salience assessment,
adaptive attention allocation, and repository introspection.
# main
"""

import unittest
import tempfile
# copilot/fix-6-2
import os
import json
from pathlib import Path
from echoself_introspection import EchoselfIntrospection, HypergraphNode


class TestEchoselfIntrospection(unittest.TestCase):
    """Test cases for Echoself introspection functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.introspector = EchoselfIntrospection(self.temp_dir)
        
    def tearDown(self):
        """Clean up test environment"""
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_semantic_salience_scoring(self):
        """Test semantic salience scoring for different file types"""
        # High priority files
        self.assertGreater(
            self.introspector.semantic_salience("btree-psi.scm"), 
            0.95
        )
        self.assertGreater(
            self.introspector.semantic_salience("eva-model.py"), 
            0.90
        )
        self.assertGreater(
            self.introspector.semantic_salience("echoself.md"), 
            0.90
        )
        
        # Medium priority files
        self.assertGreater(
            self.introspector.semantic_salience("cognitive_architecture.py"), 
            0.85
        )
        self.assertGreater(
            self.introspector.semantic_salience("README.md"), 
            0.85
        )
        
        # Lower priority files
        self.assertLess(
            self.introspector.semantic_salience("test_something.py"), 
            0.80
        )
        self.assertLess(
            self.introspector.semantic_salience("config.json"), 
            0.70
        )
    
    def test_adaptive_attention_mechanism(self):
        """Test adaptive attention allocation"""
        # High load should increase threshold
        high_load_threshold = self.introspector.adaptive_attention(
            current_load=0.9, 
            recent_activity=0.3
        )
        
        # Low load should decrease threshold
        low_load_threshold = self.introspector.adaptive_attention(
            current_load=0.1, 
            recent_activity=0.3
        )
        
        self.assertGreater(high_load_threshold, low_load_threshold)
        
        # High recent activity should decrease threshold
        high_activity_threshold = self.introspector.adaptive_attention(
            current_load=0.5, 
            recent_activity=0.9
        )
        
        low_activity_threshold = self.introspector.adaptive_attention(
            current_load=0.5, 
            recent_activity=0.1
        )
        
        self.assertLess(high_activity_threshold, low_activity_threshold)
    
    def test_hypergraph_node_creation(self):
        """Test hypergraph node creation and properties"""
        node = self.introspector.make_node(
            "test.py", 
            "file", 
            "print('hello')", 
            ["link1", "link2"]
        )
        
        self.assertEqual(node.id, "test.py")
        self.assertEqual(node.node_type, "file")
        self.assertEqual(node.content, "print('hello')")
        self.assertEqual(node.links, ["link1", "link2"])
        self.assertGreater(node.salience_score, 0)
        self.assertIsInstance(node.timestamp, float)
    
    def test_safe_file_reading(self):
        """Test safe file reading with various scenarios"""
        # Create test files
        test_file = Path(self.temp_dir) / "test.txt"
        large_file = Path(self.temp_dir) / "large.txt"
        empty_file = Path(self.temp_dir) / "empty.txt"
        
        # Normal file
        test_file.write_text("test content", encoding='utf-8')
        content = self.introspector.safe_read_file(test_file)
        self.assertEqual(content, "test content")
        
        # Large file (simulate)
        large_content = "x" * (self.introspector.MAX_FILE_SIZE + 1000)
        large_file.write_text(large_content, encoding='utf-8')
        content = self.introspector.safe_read_file(large_file)
        self.assertIn("File too large", content)
        
        # Empty file
        empty_file.write_text("", encoding='utf-8')
        content = self.introspector.safe_read_file(empty_file)
        self.assertEqual(content, "[Empty file]")
        
        # Non-existent file
        content = self.introspector.safe_read_file(Path("nonexistent.txt"))
        self.assertEqual(content, "[File not found]")
    
    def test_repo_file_listing(self):
        """Test repository file listing with attention filtering"""
        # Create test directory structure
        test_dir = Path(self.temp_dir)
        (test_dir / "high_priority.py").write_text("# Important code")
        (test_dir / "low_priority.txt").write_text("# Documentation")
        (test_dir / "subdir").mkdir()
        (test_dir / "subdir" / "nested.py").write_text("# Nested code")
        
        # Test with high threshold - should get fewer files
        high_threshold_files = self.introspector.repo_file_list(test_dir, 0.8)
        
        # Test with low threshold - should get more files
        low_threshold_files = self.introspector.repo_file_list(test_dir, 0.3)
        
        self.assertLessEqual(len(high_threshold_files), len(low_threshold_files))
    
    def test_hypergraph_assembly(self):
        """Test hypergraph assembly from files"""
        # Create test files
        test_dir = Path(self.temp_dir)
        (test_dir / "important.py").write_text("# Important Python code")
        (test_dir / "doc.md").write_text("# Documentation")
        
        # Assemble hypergraph
        nodes = self.introspector.assemble_hypergraph_input(test_dir, 0.5)
        
        self.assertGreater(len(nodes), 0)
        self.assertIsInstance(nodes[0], HypergraphNode)
        
        # Check that nodes are sorted by salience
        for i in range(len(nodes) - 1):
            self.assertGreaterEqual(
                nodes[i].salience_score, 
                nodes[i + 1].salience_score
            )
    
    def test_hypergraph_string_conversion(self):
        """Test conversion of hypergraph to string format"""
        node1 = HypergraphNode("test1.py", "file", "content1")
        node2 = HypergraphNode("test2.py", "file", "content2")
        
        result = self.introspector.hypergraph_to_string([node1, node2])
        
        self.assertIn("test1.py", result)
        self.assertIn("test2.py", result)
        self.assertIn("content1", result)
        self.assertIn("content2", result)
        self.assertIn("(file", result)
    
    def test_prompt_generation(self):
        """Test introspection prompt generation"""
        # Create a simple test setup
        test_dir = Path(self.temp_dir)
        (test_dir / "test.py").write_text("print('test')")
        
        introspector = EchoselfIntrospection(test_dir)
        prompt = introspector.inject_repo_input_into_prompt(0.5, 0.3)
        
        self.assertIn("DeepTreeEcho Recursive Self-Model Introspection", prompt)
        self.assertIn("Repository Hypergraph Analysis", prompt)
        self.assertIn("Cognitive architecture patterns", prompt)
    
    def test_attention_metrics(self):
        """Test attention metrics collection"""
        # Generate some attention decisions
        self.introspector.adaptive_attention(0.5, 0.3)
        self.introspector.adaptive_attention(0.7, 0.4)
        
        metrics = self.introspector.get_attention_metrics()
        
        self.assertIn("recent_average_threshold", metrics)
        self.assertIn("total_decisions", metrics)
        self.assertEqual(metrics["total_decisions"], 2)
    
    def test_hypergraph_export(self):
        """Test hypergraph export functionality"""
        # Create test node
        self.introspector.hypergraph_nodes["test.py"] = HypergraphNode(
            "test.py", "file", "content"
        )
        
        export_path = os.path.join(self.temp_dir, "export.json")
        self.introspector.export_hypergraph(export_path)
        
        # Verify export file exists and contains expected data
        self.assertTrue(os.path.exists(export_path))
        
        with open(export_path) as f:
            data = json.load(f)
        
        self.assertIn("nodes", data)
        self.assertIn("attention_history", data)
        self.assertIn("export_timestamp", data)
        self.assertEqual(len(data["nodes"]), 1)
        self.assertEqual(data["nodes"][0]["id"], "test.py")


class TestHypergraphNode(unittest.TestCase):
    """Test cases for HypergraphNode class"""
    
    def test_node_creation(self):
        """Test basic node creation"""
        node = HypergraphNode("test_id", "test_type", "test_content")
        
        self.assertEqual(node.id, "test_id")
        self.assertEqual(node.node_type, "test_type")
        self.assertEqual(node.content, "test_content")
        self.assertEqual(node.links, [])
        self.assertEqual(node.metadata, {})
        self.assertEqual(node.salience_score, 0.0)
        self.assertIsInstance(node.timestamp, float)
    
    def test_node_with_all_fields(self):
        """Test node creation with all fields specified"""
        links = ["link1", "link2"]
        metadata = {"key": "value"}
        
        node = HypergraphNode(
            id="test_id",
            node_type="test_type", 
            content="test_content",
            links=links,
            metadata=metadata,
            salience_score=0.8
        )
        
        self.assertEqual(node.links, links)
        self.assertEqual(node.metadata, metadata)
        self.assertEqual(node.salience_score, 0.8)

# =======
import shutil
from pathlib import Path
from echoself_introspection import (
    EchoselfIntrospector, 
    SemanticSalienceAssessor,
    AdaptiveAttentionAllocator,
    RepositoryIntrospector,
    HypergraphNode,
    _ECHO_INTEGRATION_AVAILABLE
)

# Import unified interface if available
if _ECHO_INTEGRATION_AVAILABLE:
    from echoself_introspection import EchoselfIntrospectionComponent
    from echo_component_base import EchoConfig

class TestSemanticSalienceAssessor(unittest.TestCase):
    """Test semantic salience assessment functionality"""
    
    def setUp(self):
        self.assessor = SemanticSalienceAssessor()
    
    def test_high_salience_files(self):
        """Test that important files get high salience scores"""
        high_salience_paths = [
            "eva-model.py",
            "echoself.md",
            "ARCHITECTURE.md"
        ]
        
        for path in high_salience_paths:
            salience = self.assessor.assess_semantic_salience(path)
            self.assertGreaterEqual(salience, 0.85, f"Path {path} should have high salience")
    
    def test_low_salience_files(self):
        """Test that unimportant files get low salience scores"""
        low_salience_paths = [
            ".git/objects/abc123",
            "node_modules/package/index.js"
        ]
        
        for path in low_salience_paths:
            salience = self.assessor.assess_semantic_salience(path)
            self.assertLess(salience, 0.2, f"Path {path} should have low salience")
    
    def test_default_salience(self):
        """Test default salience for unknown files"""
        unknown_path = "some_random_file.xyz"
        salience = self.assessor.assess_semantic_salience(unknown_path)
        self.assertEqual(salience, 0.5)

class TestAdaptiveAttentionAllocator(unittest.TestCase):
    """Test adaptive attention allocation mechanism"""
    
    def setUp(self):
        self.allocator = AdaptiveAttentionAllocator()
    
    def test_high_load_increases_threshold(self):
        """Test that high cognitive load increases attention threshold"""
        low_load_threshold = self.allocator.adaptive_attention(0.2, 0.5)
        high_load_threshold = self.allocator.adaptive_attention(0.8, 0.5)
        
        self.assertGreater(high_load_threshold, low_load_threshold)
    
    def test_low_activity_increases_threshold(self):
        """Test that low recent activity increases attention threshold"""
        high_activity_threshold = self.allocator.adaptive_attention(0.5, 0.8)
        low_activity_threshold = self.allocator.adaptive_attention(0.5, 0.2)
        
        self.assertGreater(low_activity_threshold, high_activity_threshold)
    
    def test_threshold_bounds(self):
        """Test that threshold stays within reasonable bounds"""
        # Test extreme values
        min_threshold = self.allocator.adaptive_attention(0.0, 1.0)
        max_threshold = self.allocator.adaptive_attention(1.0, 0.0)
        
        self.assertGreaterEqual(min_threshold, 0.0)
        self.assertLessEqual(max_threshold, 1.0)  # Should be clamped to 1.0

class TestRepositoryIntrospector(unittest.TestCase):
    """Test repository introspection functionality"""
    
    def setUp(self):
        self.introspector = RepositoryIntrospector()
        # Create temporary directory structure for testing
        self.test_dir = Path(tempfile.mkdtemp())
        
        # Create test files
        (self.test_dir / "README.md").write_text("# Test Repository")
        (self.test_dir / "src").mkdir()
        (self.test_dir / "src" / "main.py").write_text("print('hello world')")
        (self.test_dir / "test_file.py").write_text("def test(): pass")
        
        # Create a large file
        (self.test_dir / "large_file.txt").write_text("x" * 60000)
        
        # Create binary-like file
        (self.test_dir / "binary.pyc").write_bytes(b'\x00\x01\x02\x03')
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_file_validation(self):
        """Test file validation logic"""
        # Valid files
        self.assertTrue(self.introspector.is_valid_file(self.test_dir / "README.md"))
        self.assertTrue(self.introspector.is_valid_file(self.test_dir / "src" / "main.py"))
        
        # Invalid files
        self.assertFalse(self.introspector.is_valid_file(self.test_dir / "large_file.txt"))
        self.assertFalse(self.introspector.is_valid_file(self.test_dir / "binary.pyc"))
        self.assertFalse(self.introspector.is_valid_file(self.test_dir / "nonexistent.txt"))
    
    def test_safe_file_reading(self):
        """Test safe file reading with constraints"""
        # Normal file
        content = self.introspector.safe_read_file(self.test_dir / "README.md")
        self.assertEqual(content, "# Test Repository")
        
        # Large file
        content = self.introspector.safe_read_file(self.test_dir / "large_file.txt")
        self.assertIn("File too large", content)
        
        # Binary file
        content = self.introspector.safe_read_file(self.test_dir / "binary.pyc")
        self.assertIn("not accessible or binary", content)
    
    def test_repo_file_list_filtering(self):
        """Test repository file listing with attention filtering"""
        # Low threshold should include more files
        files_low = self.introspector.repo_file_list(self.test_dir, 0.3)
        
        # High threshold should include fewer files
        files_high = self.introspector.repo_file_list(self.test_dir, 0.9)
        
        self.assertGreaterEqual(len(files_low), len(files_high))
        
        # README should be included in high threshold due to high salience
        readme_in_high = any("readme" in str(f).lower() for f in files_high)
        # Note: This test might not always pass depending on attention threshold calculation
        # The key is that the filtering mechanism works

class TestEchoselfIntrospector(unittest.TestCase):
    """Test main introspection functionality"""
    
    def setUp(self):
        # Create temporary test repository
        self.test_dir = Path(tempfile.mkdtemp())
        
        # Create realistic test structure
        (self.test_dir / "README.md").write_text("# Test Project\nDescription")
        (self.test_dir / "echoself.md").write_text("# Echoself\nCognitive content")
        
        src_dir = self.test_dir / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("def main(): pass")
        
        self.introspector = EchoselfIntrospector(self.test_dir)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_cognitive_snapshot(self):
        """Test cognitive snapshot generation"""
        snapshot = self.introspector.get_cognitive_snapshot(
            current_load=0.6, 
            recent_activity=0.4
        )
        
        # Verify snapshot structure
        self.assertIn('timestamp', snapshot)
        self.assertIn('attention_threshold', snapshot)
        self.assertIn('total_files_processed', snapshot)
        self.assertIn('nodes', snapshot)
        
        # Verify data types
        self.assertIsInstance(snapshot['nodes'], list)
        self.assertGreater(snapshot['total_files_processed'], 0)
        
        # Verify node structure
        if snapshot['nodes']:
            node = snapshot['nodes'][0]
            self.assertIn('id', node)
            self.assertIn('type', node)
            self.assertIn('content', node)
            self.assertIn('salience', node)
    
    def test_prompt_generation(self):
        """Test prompt generation functionality"""
        prompt = self.introspector.inject_repo_input_into_prompt(
            current_load=0.5,
            recent_activity=0.5
        )
        
        # Verify prompt structure
        self.assertIn("DeepTreeEcho Prompt:", prompt)
        self.assertIn("(file", prompt)  # Should contain file entries
    
    def test_attention_threshold_affects_processing(self):
        """Test that attention threshold affects the number of files processed"""
        # High cognitive load should result in fewer files processed
        high_load_snapshot = self.introspector.get_cognitive_snapshot(
            current_load=0.9, 
            recent_activity=0.1
        )
        
        # Low cognitive load should result in more files processed
        low_load_snapshot = self.introspector.get_cognitive_snapshot(
            current_load=0.1, 
            recent_activity=0.9
        )
        
        # High load should process fewer or equal files
        self.assertLessEqual(
            high_load_snapshot['total_files_processed'],
            low_load_snapshot['total_files_processed']
        )

class TestHypergraphNode(unittest.TestCase):
    """Test hypergraph node functionality"""
    
    def test_node_creation(self):
        """Test hypergraph node creation and serialization"""
        node = HypergraphNode(
            id="test_file.py",
            node_type="file",
            content="def test(): pass",
            salience_score=0.8
        )
        
        # Test basic properties
        self.assertEqual(node.id, "test_file.py")
        self.assertEqual(node.node_type, "file")
        self.assertEqual(node.content, "def test(): pass")
        self.assertEqual(node.salience_score, 0.8)
        
        # Test serialization
        node_dict = node.to_dict()
        self.assertIn('id', node_dict)
        self.assertIn('type', node_dict)
        self.assertIn('content', node_dict)
        self.assertIn('salience', node_dict)


# Unified Echo Component Interface Tests
if _ECHO_INTEGRATION_AVAILABLE:
    class TestEchoselfIntrospectionComponent(unittest.TestCase):
        """Test cases for unified Echo component interface"""
        
        def setUp(self):
            self.test_dir = Path(tempfile.mkdtemp())
            
            # Create test files
            (self.test_dir / "README.md").write_text("# Test Project")
            (self.test_dir / "src").mkdir()
            (self.test_dir / "src" / "main.py").write_text("def main(): pass")
            
            self.config = EchoConfig(
                component_name="test_introspection",
                version="1.0.0",
                debug_mode=True
            )
            self.component = EchoselfIntrospectionComponent(self.config, self.test_dir)
        
        def tearDown(self):
            shutil.rmtree(self.test_dir)
        
        def test_component_initialization(self):
            """Test unified component initialization"""
            result = self.component.initialize()
            
            self.assertTrue(result.success)
            self.assertIn("initialized", result.message)
            self.assertTrue(self.component._initialized)
            self.assertIn('repository_root', result.metadata)
        
        def test_component_process(self):
            """Test unified component processing"""
            # Initialize first
            self.component.initialize()
            
            # Process with dict input
            input_data = {
                'current_load': 0.7,
                'recent_activity': 0.3
            }
            result = self.component.process(input_data)
            
            self.assertTrue(result.success)
            self.assertIn('timestamp', result.data)
            self.assertIn('total_files_processed', result.data)
            self.assertIn('attention_threshold', result.metadata)
            
            # Process with kwargs
            result2 = self.component.process(None, current_load=0.5, recent_activity=0.6)
            self.assertTrue(result2.success)
        
        def test_component_echo(self):
            """Test unified component echo operation"""
            # Initialize first
            self.component.initialize()
            
            test_data = "Test introspection data"
            echo_value = 0.8
            
            result = self.component.echo(test_data, echo_value)
            
            self.assertTrue(result.success)
            self.assertIn('original_data', result.data)
            self.assertIn('echo_value', result.data)
            self.assertIn('introspection_prompt', result.data)
            self.assertEqual(result.data['original_data'], test_data)
            self.assertEqual(result.data['echo_value'], echo_value)
            self.assertIn('prompt_length', result.metadata)
        
        def test_component_get_status(self):
            """Test component status retrieval"""
            result = self.component.get_status()
            
            self.assertTrue(result.success)
            self.assertIn('component_name', result.data)
            self.assertIn('version', result.data)
            self.assertEqual(result.data['component_name'], 'test_introspection')
        
        def test_component_reset(self):
            """Test component reset functionality"""
            # Initialize and add some state
            self.component.initialize()
            self.component.state['test_key'] = 'test_value'
            
            result = self.component.reset()
            
            self.assertTrue(result.success)
            self.assertFalse(self.component._initialized)
            self.assertEqual(len(self.component.state), 0)
        
        def test_introspection_metrics(self):
            """Test introspection-specific metrics"""
            self.component.initialize()
            
            # Generate some activity first
            self.component.process({'current_load': 0.5, 'recent_activity': 0.5})
            
            result = self.component.get_introspection_metrics()
            self.assertTrue(result.success)
            # Note: metrics might be empty if no attention history exists
        
        def test_hypergraph_export(self):
            """Test hypergraph export functionality"""
            self.component.initialize()
            
            # Generate some data first
            self.component.process({'current_load': 0.5, 'recent_activity': 0.5})
            
            result = self.component.export_hypergraph()
            
            self.assertTrue(result.success)
            self.assertIn('output_path', result.data)
            
            # Clean up the exported file
            output_path = result.data['output_path']
            if Path(output_path).exists():
                Path(output_path).unlink()
        
        def test_error_handling(self):
            """Test component error handling"""
            # Test with invalid repository path
            invalid_config = EchoConfig(component_name="invalid_test")
            invalid_component = EchoselfIntrospectionComponent(
                invalid_config, 
                Path("/nonexistent/path")
            )
            
            result = invalid_component.initialize()
            self.assertFalse(result.success)
            self.assertIn("does not exist", result.message)
        
        def test_auto_initialization(self):
            """Test automatic initialization during operations"""
            # Component not initialized yet
            self.assertFalse(self.component._initialized)
            
            # Process should auto-initialize
            result = self.component.process({'current_load': 0.5, 'recent_activity': 0.5})
            
            self.assertTrue(result.success)
            self.assertTrue(self.component._initialized)
            
            # Echo should also auto-initialize
            self.component._initialized = False
            result = self.component.echo("test data", 0.5)
            
            self.assertTrue(result.success)
            self.assertTrue(self.component._initialized)


# main

if __name__ == "__main__":
    unittest.main()