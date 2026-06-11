#!/usr/bin/env python3

import sys
import logging
from unified_launcher import UnifiedLauncher, create_config_from_args, create_argument_parser

print("⚠️  DEPRECATION NOTICE: This script is deprecated.")
print("🚀 USE INSTEAD: python launch.py gui")
print()
print("📖 Migration Guide:")
print("   OLD: python launch_gui.py --debug --no-activity")
print("   NEW: python launch.py gui --debug --no-activity")
print()
print("💡 Benefits of the unified launcher:")
print("   • Single entry point for all launch modes")
print("   • Better error handling and validation")
print("   • Comprehensive help: python launch.py --help")
print("   • Mode-specific help: python launch.py gui --help")
print()
print("⏳ Continuing with legacy launcher (will be removed in future version)...")
print()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main entry point for GUI launcher"""
    
    # Parse arguments using unified launcher's parser
    parser = create_argument_parser("gui")
    args = parser.parse_args()
    
    # Create config from arguments  
    config = create_config_from_args("gui", args)
    
    # Use unified launcher
    launcher = UnifiedLauncher()
    return launcher.launch_sync(config)

if __name__ == "__main__":
    sys.exit(main())