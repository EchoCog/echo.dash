#!/usr/bin/env python3

import sys
import logging
from unified_launcher import UnifiedLauncher, create_config_from_args, create_argument_parser

print("⚠️  DEPRECATION NOTICE: This script is deprecated.")
print("🚀 USE INSTEAD: python launch.py gui-standalone")
print()
print("📖 Migration Guide:")
print("   OLD: python launch_gui_standalone.py --no-activity")
print("   NEW: python launch.py gui-standalone --no-activity")
print()
print("💡 Benefits of the unified launcher:")
print("   • Single entry point for all launch modes")
print("   • Better error handling and validation")
print("   • Comprehensive help: python launch.py --help")
print("   • Lightweight mode still available as gui-standalone")
print()
print("⏳ Continuing with legacy launcher (will be removed in future version)...")
print()

# Set up logging to file instead of console
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='gui_dashboard.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for standalone GUI launcher"""
    
    # Parse arguments using unified launcher's parser
    parser = create_argument_parser("gui-standalone")
    args = parser.parse_args()
    
    # Create config from arguments  
    config = create_config_from_args("gui-standalone", args)
    
    # Use unified launcher
    launcher = UnifiedLauncher()
    return launcher.launch_sync(config)

if __name__ == "__main__":
    sys.exit(main())