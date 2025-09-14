#!/usr/bin/env python3
"""
Main Launch Script for Deep Tree Echo

This is the primary entry point for launching Deep Tree Echo in any configuration.
It consolidates the functionality from multiple launch scripts into a single,
easy-to-use interface with clear mode selection.

Available modes:
- deep-tree-echo: Full async system with all components
- gui: GUI dashboard with full component initialization  
- gui-standalone: Simplified GUI with minimal dependencies
- web: Web dashboard only
- dashboards: Process manager for multiple dashboards

Usage examples:
    python launch.py                           # Default GUI mode
    python launch.py deep-tree-echo --gui      # Full system with GUI
    python launch.py dashboards               # Both web and GUI dashboards
    python launch.py web --port 8080          # Web dashboard on port 8080
    python launch.py gui-standalone           # Minimal GUI
"""

import sys
import argparse
import logging
from typing import List
from unified_launcher import UnifiedLauncher, create_config_from_args

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_banner():
    """Print startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                            Deep Tree Echo Launcher                           ║
║                                                                              ║
║  Unified launcher for neural architecture combining Echo State Networks,     ║
║  P-System hierarchies, and rooted trees with hypergraph-based memory        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def list_modes():
    """Display available launch modes"""
    modes_info = {
        'deep-tree-echo': 'Full async system with all components (recommended for development)',
        'gui': 'GUI dashboard with full component initialization',
        'gui-standalone': 'Simplified GUI with minimal dependencies (lightweight)',
        'web': 'Web dashboard only (browser-based interface)',
        'dashboards': 'Process manager for multiple dashboards (GUI + Web)'
    }
    
    print("\nAvailable launch modes:")
    print("─" * 80)
    for mode, description in modes_info.items():
        print(f"  {mode:<18} : {description}")
    print()

def create_main_parser() -> argparse.ArgumentParser:
    """Create the main argument parser"""
    parser = argparse.ArgumentParser(
        prog='launch.py',
        description='Unified Deep Tree Echo Launcher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch.py                           # Default GUI mode
  python launch.py deep-tree-echo --gui      # Full system with GUI
  python launch.py dashboards               # Both web and GUI dashboards
  python launch.py web --port 8080          # Web dashboard on port 8080
  python launch.py gui-standalone           # Minimal GUI

For mode-specific options, use: python launch.py <mode> --help
        """
    )
    
    parser.add_argument(
        'mode',
        nargs='?',
        default='gui',
        choices=['deep-tree-echo', 'gui', 'gui-standalone', 'web', 'dashboards'],
        help='Launch mode (default: gui)'
    )
    
    parser.add_argument(
        '--list-modes',
        action='store_true',
        help='Show available launch modes and exit'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress banner and informational output'
    )
    
    # Common arguments
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--log-file", type=str, help="Log file path")
    parser.add_argument("--storage-dir", type=str, default="echo_memory", help="Storage directory")
    
    # Deep Tree Echo specific options
    parser.add_argument("--gui", action="store_true", help="Launch GUI dashboard (for deep-tree-echo mode)")
    parser.add_argument("--browser", action="store_true", help="Initialize browser automation (for deep-tree-echo mode)")
    
    # GUI specific options
    parser.add_argument("--no-activity", action="store_true", help="Disable activity monitoring (for gui modes)")
    
    # Dashboard specific options
    parser.add_argument("--gui-only", action="store_true", help="Launch only the GUI dashboard (for dashboards mode)")
    parser.add_argument("--web-only", action="store_true", help="Launch only the Web dashboard (for dashboards mode)")
    parser.add_argument("--no-locale-fix", action="store_true", help="Don't use the locale fix for the GUI dashboard")
    parser.add_argument("--web-port", type=int, default=8080, help="Port for the Web dashboard (default: 8080)")
    parser.add_argument("--gui-port", type=int, default=5000, help="Port for the GUI dashboard (default: 5000)")
    parser.add_argument("--no-monitor", action="store_true", help="Don't monitor dashboard status")
    
    # Web specific options  
    parser.add_argument("--port", type=int, default=8080, help="Port for the web server (default: 8080)")
    
    return parser

def validate_args(args) -> List[str]:
    """Validate argument combinations and return warnings"""
    warnings = []
    
    # Check for conflicting options
    if args.gui_only and args.web_only:
        warnings.append("Cannot specify both --gui-only and --web-only")
    
    # Mode-specific validation
    if args.mode != 'deep-tree-echo':
        if args.gui and args.mode != 'dashboards':
            warnings.append("--gui option only applies to deep-tree-echo mode")
        if args.browser:
            warnings.append("--browser option only applies to deep-tree-echo mode")
    
    if args.mode not in ['gui', 'gui-standalone'] and args.no_activity:
        warnings.append("--no-activity option only applies to gui modes")
    
    if args.mode != 'dashboards':
        dashboard_opts = ['gui_only', 'web_only', 'no_locale_fix', 'gui_port', 'no_monitor']
        for opt in dashboard_opts:
            if getattr(args, opt) and (opt != 'gui_port' or getattr(args, opt) != 5000):
                warnings.append(f"--{opt.replace('_', '-')} option only applies to dashboards mode")
    
    if args.mode != 'web' and args.port != 8080:
        warnings.append("--port option only applies to web mode")
    
    return warnings

def main():
    """Main entry point"""
    parser = create_main_parser()
    args = parser.parse_args()
    
    # Handle special modes
    if args.list_modes:
        list_modes()
        return 0
    
    # Show banner unless quiet
    if not args.quiet:
        print_banner()
        print(f"Starting Deep Tree Echo in '{args.mode}' mode...")
    
    # Validate arguments
    warnings = validate_args(args)
    if warnings:
        logger.warning("Argument validation warnings:")
        for warning in warnings:
            logger.warning("  - %s", warning)
        print()
    
    try:
        # Create configuration
        config = create_config_from_args(args.mode, args)
        
        # For web mode, use the port argument
        if args.mode == 'web':
            config.web_port = args.port
        
        # Create and run launcher
        launcher = UnifiedLauncher()
        
        if not args.quiet:
            logger.info("Configuration: %s mode", config.mode.value)
            if config.debug:
                logger.info("Debug logging enabled")
            if config.log_file:
                logger.info("Logging to file: %s", config.log_file)
        
        # Launch the system
        return launcher.launch_sync(config)
        
    except KeyboardInterrupt:
        logger.info("Launch cancelled by user")
        return 0
    except (RuntimeError, ValueError, OSError) as e:
        logger.error("Launch failed: %s", e)
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1
    except Exception as e:
        logger.error("Unexpected error during launch: %s", e)
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())