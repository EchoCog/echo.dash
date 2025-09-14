#!/usr/bin/env python3
"""
Test script for Main Launcher (launch.py)

This script validates that the new main launcher consolidates all launch
functionality and provides a clean interface for users.
"""

import sys
import unittest
import io
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add current directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

class TestMainLauncher(unittest.TestCase):
    """Test main launcher functionality"""

    def setUp(self):
        """Set up test environment"""
        # Import after path setup
        import launch
        self.launch = launch
        
    def test_banner_display(self):
        """Test that banner is displayed correctly"""
        # Capture stdout
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            self.launch.print_banner()
        
        output = captured_output.getvalue()
        self.assertIn("Deep Tree Echo Launcher", output)
        self.assertIn("neural architecture", output)

    def test_modes_listing(self):
        """Test that available modes are listed correctly"""
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            self.launch.list_modes()
        
        output = captured_output.getvalue()
        expected_modes = ['deep-tree-echo', 'gui', 'gui-standalone', 'web', 'dashboards']
        for mode in expected_modes:
            self.assertIn(mode, output)

    def test_argument_parser_creation(self):
        """Test that the main argument parser is created correctly"""
        parser = self.launch.create_main_parser()
        
        # Test default arguments
        args = parser.parse_args([])
        self.assertEqual(args.mode, 'gui')  # Default mode
        self.assertFalse(args.debug)
        self.assertFalse(args.quiet)
        
        # Test mode selection
        args = parser.parse_args(['deep-tree-echo'])
        self.assertEqual(args.mode, 'deep-tree-echo')
        
        # Test with options
        args = parser.parse_args(['deep-tree-echo', '--gui', '--browser', '--debug'])
        self.assertEqual(args.mode, 'deep-tree-echo')
        self.assertTrue(args.gui)
        self.assertTrue(args.browser)
        self.assertTrue(args.debug)

    def test_argument_validation(self):
        """Test argument validation logic"""
        parser = self.launch.create_main_parser()
        
        # Test conflicting arguments - should return errors, not warnings
        args = parser.parse_args(['dashboards', '--gui-only', '--web-only'])
        errors = self.launch.validate_configuration(args)
        self.assertTrue(any('gui-only' in e and 'web-only' in e for e in errors))
        
        # Test invalid port
        args = parser.parse_args(['web', '--port', '99999'])
        errors = self.launch.validate_configuration(args)
        self.assertTrue(any('port' in e for e in errors))

    def test_mode_specific_configurations(self):
        """Test that different modes create appropriate configurations"""
        parser = self.launch.create_main_parser()
        
        # Test deep-tree-echo mode
        args = parser.parse_args(['deep-tree-echo', '--gui', '--browser'])
        self.assertEqual(args.mode, 'deep-tree-echo')
        self.assertTrue(args.gui)
        self.assertTrue(args.browser)
        
        # Test dashboards mode
        args = parser.parse_args(['dashboards', '--web-port', '9000', '--gui-port', '6000'])
        self.assertEqual(args.mode, 'dashboards')
        self.assertEqual(args.web_port, 9000)
        self.assertEqual(args.gui_port, 6000)
        
        # Test web mode
        args = parser.parse_args(['web', '--port', '7000'])
        self.assertEqual(args.mode, 'web')
        self.assertEqual(args.port, 7000)

    @patch('launch.UnifiedLauncher')
    @patch('unified_launcher.create_config_from_args')
    def test_main_function_execution(self, mock_config, mock_launcher):
        """Test the main function execution flow"""
        # Mock configuration and launcher
        mock_config_instance = Mock()
        mock_config_instance.mode.value = 'gui'
        mock_config_instance.debug = False
        mock_config_instance.log_file = None
        mock_config.return_value = mock_config_instance
        
        mock_launcher_instance = Mock()
        mock_launcher_instance.launch_sync.return_value = 0
        mock_launcher.return_value = mock_launcher_instance
        
        # Test with validation-only mode to avoid GUI dependencies
        test_args = ['launch.py', 'gui', '--quiet', '--validate-config']
        with patch('sys.argv', test_args):
            result = self.launch.main()
        
        # Should succeed in validation mode
        self.assertEqual(result, 0)

    def test_help_output(self):
        """Test that help output is comprehensive"""
        parser = self.launch.create_main_parser()
        
        # Capture help output (argparse prints help to stdout)
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            try:
                parser.parse_args(['--help'])
            except SystemExit:
                pass  # argparse calls sys.exit after printing help
        
        help_output = captured_output.getvalue()
        
        # Check that help includes key information
        self.assertIn('Unified Deep Tree Echo Launcher', help_output)
        self.assertIn('Examples:', help_output)
        self.assertIn('deep-tree-echo', help_output)
        self.assertIn('dashboards', help_output)

    def test_backward_compatibility_with_existing_scripts(self):
        """Test that the main launcher can handle all existing script use cases"""
        parser = self.launch.create_main_parser()
        
        # Test launch_deep_tree_echo.py equivalent
        args = parser.parse_args(['deep-tree-echo', '--gui', '--browser', '--debug'])
        self.assertEqual(args.mode, 'deep-tree-echo')
        self.assertTrue(args.gui)
        self.assertTrue(args.browser)
        self.assertTrue(args.debug)
        
        # Test launch_dashboards.py equivalent  
        args = parser.parse_args(['dashboards', '--web-port', '8080', '--gui-port', '5000'])
        self.assertEqual(args.mode, 'dashboards')
        self.assertEqual(args.web_port, 8080)
        self.assertEqual(args.gui_port, 5000)
        
        # Test launch_gui.py equivalent
        args = parser.parse_args(['gui', '--debug', '--no-activity'])
        self.assertEqual(args.mode, 'gui')
        self.assertTrue(args.debug)
        self.assertTrue(args.no_activity)
        
        # Test launch_gui_standalone.py equivalent
        args = parser.parse_args(['gui-standalone', '--no-activity'])
        self.assertEqual(args.mode, 'gui-standalone')
        self.assertTrue(args.no_activity)

def run_tests():
    """Run all tests"""
    # Suppress logging during tests
    import logging
    logging.getLogger().setLevel(logging.WARNING)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMainLauncher)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)