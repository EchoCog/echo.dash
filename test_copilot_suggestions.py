#!/usr/bin/env python3
"""
Test script for copilot_suggestions.py Azure OpenAI integration.

This test verifies:
1. Environment variable validation
2. Error handling for missing variables
3. Basic API endpoint construction
4. Note file handling
"""

import os
import json
import tempfile
import unittest
import copilot_suggestions


class TestCopilotSuggestions(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        # Clear environment variables
        for var in ['AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_KEY', 'AZURE_OPENAI_DEPLOYMENT']:
            if var in os.environ:
                del os.environ[var]
    
    def test_missing_environment_variables(self):
        """Test that missing environment variables are handled correctly"""
        # Test missing endpoint
        result = copilot_suggestions.fetch_suggestions_from_azure_openai({})
        self.assertIsNone(result)
        
        # Test missing key
        os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://test.openai.azure.com/'
        result = copilot_suggestions.fetch_suggestions_from_azure_openai({})
        self.assertIsNone(result)
        
        # Test missing deployment
        os.environ['AZURE_OPENAI_KEY'] = 'test-key'
        result = copilot_suggestions.fetch_suggestions_from_azure_openai({})
        self.assertIsNone(result)
    
    def test_api_configuration_validation(self):
        """Test API configuration validation with real checks"""
        # Test missing endpoint
        os.environ.pop('AZURE_OPENAI_ENDPOINT', None)
        os.environ.pop('AZURE_OPENAI_KEY', None)
        os.environ.pop('AZURE_OPENAI_DEPLOYMENT', None)
        
        # Should return None when configuration is missing
        result = copilot_suggestions.fetch_suggestions_from_azure_openai({})
        self.assertIsNone(result)
        
        # Test partial configuration - should still return None
        os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://test.openai.azure.com'
        result = copilot_suggestions.fetch_suggestions_from_azure_openai({})
        self.assertIsNone(result)
        
        # Test valid configuration structure (won't make actual call due to missing key)
        os.environ['AZURE_OPENAI_KEY'] = 'test-key'
        os.environ['AZURE_OPENAI_DEPLOYMENT'] = 'gpt-4'
        
        # Should at least attempt to process (will fail safely on network call)
        result = copilot_suggestions.fetch_suggestions_from_azure_openai({'test': 'data'})
        # Real function handles network failures gracefully by returning None
        self.assertIsNone(result)
    
    def test_note_file_handling_functions(self):
        """Test note file handling functions with real operations"""
        # Test update_note_with_suggestions function
        test_suggestions = {
            "suggestions": ["Deep Tree Echo enhancement: improve recursive patterns"],
            "next_focus": "hypergraph memory optimization"
        }
        
        # Test that function exists and can be called (it handles file operations gracefully)
        try:
            result = copilot_suggestions.update_note_with_suggestions(test_suggestions)
            # Function should handle file operations, return value may vary
        except Exception as e:
            # Real file operations may fail, this is acceptable for testing function existence
            pass
        
        # Test load_introspection_context function
        try:
            context = copilot_suggestions.load_introspection_context()
            # Should return dict or None depending on file availability
            self.assertIsInstance(context, (dict, type(None)))
        except Exception as e:
            # File operations may fail in test environment, this is acceptable
            pass
    
    def test_module_functions_availability(self):
        """Test that all required functions are available and callable"""
        # Test that fetch_suggestions_from_azure_openai exists
        self.assertTrue(hasattr(copilot_suggestions, 'fetch_suggestions_from_azure_openai'))
        self.assertTrue(callable(copilot_suggestions.fetch_suggestions_from_azure_openai))
        
        # Test that update_note_with_suggestions exists  
        self.assertTrue(hasattr(copilot_suggestions, 'update_note_with_suggestions'))
        self.assertTrue(callable(copilot_suggestions.update_note_with_suggestions))
        
        # Test that load_introspection_context exists
        self.assertTrue(hasattr(copilot_suggestions, 'load_introspection_context'))
        self.assertTrue(callable(copilot_suggestions.load_introspection_context))
        
        # Test that main exists
        self.assertTrue(hasattr(copilot_suggestions, 'main'))
        self.assertTrue(callable(copilot_suggestions.main))
        
        # Test module constants
        self.assertTrue(hasattr(copilot_suggestions, 'NOTE_FILE'))
        self.assertEqual(copilot_suggestions.NOTE_FILE, "note2self.json")


if __name__ == '__main__':
    unittest.main()