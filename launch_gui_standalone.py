#!/usr/bin/env python3

import sys
import logging
from unified_launcher import UnifiedLauncher, create_config_from_args, create_argument_parser

print("⚠️  NOTICE: This script is deprecated. Use 'python launch.py gui-standalone' for the same functionality.")
print("   The unified launcher provides better error handling and comprehensive help.")
print("   Run 'python launch.py --help' to see all available options.\n")

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