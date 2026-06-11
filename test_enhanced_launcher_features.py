#!/usr/bin/env python3
"""
Test script for Enhanced Unified Launcher Features

This script validates the new enhanced features added to improve the
consolidation of multiple launch scripts.
"""

import sys
import unittest
import io
import tempfile
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add current directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

class TestEnhancedLauncherFeatures(unittest.TestCase):
    """Test enhanced launcher features"""

    def setUp(self):
        """Set up test environment"""
        # Import after path setup
        import launch
        self.launch = launch
        
    def test_migration_guide_display(self):
        """Test that migration guide is displayed correctly"""
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            self.launch.show_migration_guide()
        
        output = captured_output.getvalue()
        self.assertIn("MIGRATION GUIDE", output)
        self.assertIn("launch_deep_tree_echo.py", output)
        self.assertIn("launch_dashboards.py", output)
        self.assertIn("launch_gui.py", output)
        self.assertIn("launch_gui_standalone.py", output)
        self.assertIn("python launch.py", output)

    def test_enhanced_modes_listing(self):
        """Test that enhanced modes listing includes migration info"""
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            self.launch.list_modes()
        
        output = captured_output.getvalue()
        self.assertIn("Replaces:", output)
        self.assertIn("Key options:", output)
        self.assertIn("Migration tip:", output)
        self.assertIn("Legacy scripts still work", output)

    def test_configuration_validation_valid_config(self):
        """Test configuration validation with valid configs"""
        parser = self.launch.create_main_parser()
        
        # Test valid GUI config
        args = parser.parse_args(['gui', '--debug', '--no-activity'])
        errors = self.launch.validate_configuration(args)
        self.assertEqual(len(errors), 0)
        
        # Test valid web config
        args = parser.parse_args(['web', '--port', '8080'])
        errors = self.launch.validate_configuration(args)
        self.assertEqual(len(errors), 0)
        
        # Test valid dashboards config
        args = parser.parse_args(['dashboards', '--web-port', '8080', '--gui-port', '5000'])
        errors = self.launch.validate_configuration(args)
        self.assertEqual(len(errors), 0)

    def test_configuration_validation_invalid_ports(self):
        """Test configuration validation catches invalid ports"""
        parser = self.launch.create_main_parser()
        
        # Test invalid port (too high)
        args = parser.parse_args(['web', '--port', '99999'])
        errors = self.launch.validate_configuration(args)
        self.assertTrue(any('port' in e for e in errors))
        
        # Test invalid port (negative)
        args = parser.parse_args(['web', '--port', '-1'])
        errors = self.launch.validate_configuration(args)
        self.assertTrue(any('port' in e for e in errors))
        
        # Test conflicting ports (non-default)
        args = parser.parse_args(['dashboards', '--web-port', '9000', '--gui-port', '9000'])
        errors = self.launch.validate_configuration(args)
        self.assertTrue(any('same' in e or 'cannot be' in e for e in errors))

    def test_configuration_validation_conflicting_options(self):
        """Test configuration validation catches conflicting options"""
        parser = self.launch.create_main_parser()
        
        # Test conflicting dashboard options
        args = parser.parse_args(['dashboards', '--gui-only', '--web-only'])
        errors = self.launch.validate_configuration(args)
        self.assertTrue(any('gui-only' in e and 'web-only' in e for e in errors))

    def test_enhanced_argument_parser_features(self):
        """Test new argument parser features"""
        parser = self.launch.create_main_parser()
        
        # Test migration guide option
        args = parser.parse_args(['--migration-guide'])
        self.assertTrue(hasattr(args, 'migration_guide'))
        self.assertTrue(args.migration_guide)
        
        # Test validate config option
        args = parser.parse_args(['gui', '--validate-config'])
        self.assertTrue(hasattr(args, 'validate_config'))
        self.assertTrue(args.validate_config)

    def test_enhanced_banner_content(self):
        """Test that enhanced banner includes consolidation info"""
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            self.launch.print_banner()
        
        output = captured_output.getvalue()
        self.assertIn("Unified launcher consolidating", output)
        self.assertIn("Replaces:", output)
        self.assertIn("launch_deep_tree_echo.py", output)
        self.assertIn("launch_dashboards.py", output)

    @patch('unified_launcher.create_config_from_args')
    def test_validate_config_dry_run(self, mock_config):
        """Test the --validate-config dry run functionality"""
        # Mock configuration creation
        mock_config_instance = Mock()
        mock_config.return_value = mock_config_instance
        
        # Test validation mode
        test_args = ['launch.py', 'gui', '--validate-config', '--quiet']
        with patch('sys.argv', test_args):
            result = self.launch.main()
        
        # Should succeed without launching
        self.assertEqual(result, 0)
        mock_config.assert_called_once()

    def test_help_includes_migration_examples(self):
        """Test that help output includes comprehensive migration examples"""
        parser = self.launch.create_main_parser()
        
        # Capture help output
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            try:
                parser.parse_args(['--help'])
            except SystemExit:
                pass
        
        help_output = captured_output.getvalue()
        
        # Check for migration examples
        self.assertIn("UNIFIED LAUNCHER", help_output)
        self.assertIn("Replaces Multiple Launch Scripts", help_output)
        self.assertIn("Migration Examples", help_output)
        self.assertIn("OLD:", help_output)
        self.assertIn("NEW:", help_output)

    def test_legacy_script_compatibility(self):
        """Test that legacy scripts still work and show proper warnings"""
        # Test each legacy script exists and has deprecation notice
        legacy_scripts = [
            'launch_deep_tree_echo.py',
            'launch_dashboards.py', 
            'launch_gui.py',
            'launch_gui_standalone.py'
        ]
        
        for script in legacy_scripts:
            script_path = Path(__file__).parent / script
            self.assertTrue(script_path.exists(), f"Legacy script {script} should exist")
            
            # Check that script contains deprecation notice
            content = script_path.read_text()
            self.assertIn("DEPRECATION NOTICE", content)
            self.assertIn("python launch.py", content)

    def test_mode_mapping_consistency(self):
        """Test that mode mappings are consistent across features"""
        parser = self.launch.create_main_parser()
        
        # Test that all modes mentioned in help are valid
        expected_modes = ['deep-tree-echo', 'gui', 'gui-standalone', 'web', 'dashboards']
        
        for mode in expected_modes:
            # Should parse without error
            args = parser.parse_args([mode])
            self.assertEqual(args.mode, mode)

def run_tests():
    """Run all enhanced feature tests"""
    # Suppress logging during tests
    import logging
    logging.getLogger().setLevel(logging.WARNING)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestEnhancedLauncherFeatures)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)