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
║  Unified launcher consolidating multiple launch scripts into a single,       ║
║  configurable interface for the Deep Tree Echo neural architecture          ║
║                                                                              ║
║  🚀 Replaces: launch_deep_tree_echo.py, launch_dashboards.py,                ║
║              launch_gui.py, launch_gui_standalone.py                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def list_modes():
    """Display available launch modes"""
    modes_info = {
        'deep-tree-echo': {
            'description': 'Full async system with all components (recommended for development)',
            'replaces': 'launch_deep_tree_echo.py',
            'key_options': '--gui, --browser, --debug'
        },
        'gui': {
            'description': 'GUI dashboard with full component initialization',
            'replaces': 'launch_gui.py', 
            'key_options': '--no-activity, --debug'
        },
        'gui-standalone': {
            'description': 'Simplified GUI with minimal dependencies (lightweight)',
            'replaces': 'launch_gui_standalone.py',
            'key_options': '--no-activity'
        },
        'web': {
            'description': 'Web dashboard only (browser-based interface)',
            'replaces': 'web_gui.py (direct)',
            'key_options': '--port'
        },
        'dashboards': {
            'description': 'Process manager for multiple dashboards (GUI + Web)',
            'replaces': 'launch_dashboards.py',
            'key_options': '--gui-only, --web-only, --web-port, --gui-port'
        }
    }
    
    print("\nAvailable launch modes (replaces multiple launch scripts):")
    print("─" * 90)
    for mode, info in modes_info.items():
        print(f"  {mode:<18} : {info['description']}")
        print(f"  {'':18}   Replaces: {info['replaces']}")
        print(f"  {'':18}   Key options: {info['key_options']}")
        print()
    
    print("💡 Migration tip: Use 'python launch.py <mode> --help' for detailed options")
    print("📚 Legacy scripts still work but show deprecation warnings")

def create_main_parser() -> argparse.ArgumentParser:
    """Create the main argument parser"""
    parser = argparse.ArgumentParser(
        prog='launch.py',
        description='Unified Deep Tree Echo Launcher - Consolidates multiple launch scripts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🚀 UNIFIED LAUNCHER - Replaces Multiple Launch Scripts:

This launcher consolidates functionality from:
  • launch_deep_tree_echo.py  → use: python launch.py deep-tree-echo
  • launch_dashboards.py      → use: python launch.py dashboards  
  • launch_gui.py             → use: python launch.py gui
  • launch_gui_standalone.py  → use: python launch.py gui-standalone

📋 Migration Examples:
  OLD: python launch_deep_tree_echo.py --gui --browser
  NEW: python launch.py deep-tree-echo --gui --browser
  
  OLD: python launch_dashboards.py --web-port 8080
  NEW: python launch.py dashboards --web-port 8080
  
  OLD: python launch_gui.py --debug --no-activity  
  NEW: python launch.py gui --debug --no-activity
  
  OLD: python launch_gui_standalone.py --no-activity
  NEW: python launch.py gui-standalone --no-activity

💡 Quick Start:
  python launch.py                           # Default GUI mode
  python launch.py --list-modes             # Show all available modes
  python launch.py deep-tree-echo --gui      # Full system with GUI
  python launch.py dashboards               # Both web and GUI dashboards

🔧 For mode-specific options: python launch.py <mode> --help
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
        help='Show available launch modes with migration guidance'
    )
    
    parser.add_argument(
        '--migration-guide',
        action='store_true', 
        help='Show detailed migration guide from old launch scripts'
    )
    
    parser.add_argument(
        '--validate-config',
        action='store_true',
        help='Validate configuration without launching (dry-run mode)'
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

def show_migration_guide():
    """Display detailed migration guide from old launch scripts"""
    guide = """
📖 MIGRATION GUIDE - From Multiple Launch Scripts to Unified Launcher

┌─────────────────────────────────────────────────────────────────────────────┐
│                          SCRIPT CONSOLIDATION                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Old Script                │ New Command                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ launch_deep_tree_echo.py  │ python launch.py deep-tree-echo               │
│ launch_dashboards.py      │ python launch.py dashboards                   │
│ launch_gui.py             │ python launch.py gui                          │
│ launch_gui_standalone.py  │ python launch.py gui-standalone               │
└─────────────────────────────────────────────────────────────────────────────┘

🔄 COMMAND MIGRATION EXAMPLES:

1️⃣ Deep Tree Echo System:
   OLD: python launch_deep_tree_echo.py --gui --browser --debug
   NEW: python launch.py deep-tree-echo --gui --browser --debug

2️⃣ Dashboard Manager:
   OLD: python launch_dashboards.py --web-port 8080 --gui-port 5000 --gui-only
   NEW: python launch.py dashboards --web-port 8080 --gui-port 5000 --gui-only

3️⃣ GUI Dashboard:
   OLD: python launch_gui.py --debug --no-activity --log-file gui.log
   NEW: python launch.py gui --debug --no-activity --log-file gui.log

4️⃣ Standalone GUI:
   OLD: python launch_gui_standalone.py --no-activity
   NEW: python launch.py gui-standalone --no-activity

✅ WHAT'S IMPROVED:
• Single entry point reduces confusion
• Consistent argument parsing across all modes
• Better error messages and validation
• Comprehensive help with --help
• Mode-specific help with <mode> --help
• Configuration validation with --validate-config

⚠️ BACKWARD COMPATIBILITY:
• Old scripts still work but show deprecation warnings
• All original command-line arguments are preserved
• No breaking changes to existing workflows

🚀 RECOMMENDED MIGRATION STEPS:
1. Test new commands alongside old ones
2. Update documentation and scripts to use launch.py
3. Set up aliases if needed: alias old_cmd='python launch.py mode'
4. Remove old script calls after validation

💡 Pro Tips:
• Use 'python launch.py --list-modes' to see all options
• Use 'python launch.py <mode> --help' for mode-specific help
• Use 'python launch.py --validate-config <mode>' to test configs
"""
    print(guide)


def validate_configuration(args) -> List[str]:
    """
    Enhanced configuration validation with detailed feedback
    Returns list of errors (empty list means valid)
    """
    errors = []
    warnings = []
    
    # Port validation
    if hasattr(args, 'port') and args.port:
        if args.port < 1 or args.port > 65535:
            errors.append(f"Invalid port number: {args.port} (must be 1-65535)")
        elif args.port < 1024:
            warnings.append(f"Port {args.port} requires elevated privileges")
    
    if hasattr(args, 'web_port') and args.web_port:
        if args.web_port < 1 or args.web_port > 65535:
            errors.append(f"Invalid web port: {args.web_port} (must be 1-65535)")
        elif args.web_port < 1024:
            warnings.append(f"Web port {args.web_port} requires elevated privileges")
    
    if hasattr(args, 'gui_port') and args.gui_port:
        if args.gui_port < 1 or args.gui_port > 65535:
            errors.append(f"Invalid GUI port: {args.gui_port} (must be 1-65535)")
        elif args.gui_port < 1024:
            warnings.append(f"GUI port {args.gui_port} requires elevated privileges")
    
    # Port conflicts
    if (hasattr(args, 'web_port') and hasattr(args, 'gui_port') and 
        args.web_port == args.gui_port and args.mode == 'dashboards' and
        args.web_port != 8080):  # Only flag as error if not default and explicitly set different
        errors.append(f"Web port and GUI port cannot be the same: {args.web_port}")
    
    # Storage directory validation
    if hasattr(args, 'storage_dir') and args.storage_dir:
        from pathlib import Path
        try:
            storage_path = Path(args.storage_dir)
            if storage_path.exists() and not storage_path.is_dir():
                errors.append(f"Storage path exists but is not a directory: {args.storage_dir}")
        except Exception as e:
            errors.append(f"Invalid storage directory path: {args.storage_dir} ({e})")
    
    # Log file validation
    if hasattr(args, 'log_file') and args.log_file:
        from pathlib import Path
        try:
            log_path = Path(args.log_file)
            if log_path.exists() and not log_path.is_file():
                errors.append(f"Log path exists but is not a file: {args.log_file}")
            # Check if parent directory is writable
            if not log_path.parent.exists():
                warnings.append(f"Log directory will be created: {log_path.parent}")
        except Exception as e:
            errors.append(f"Invalid log file path: {args.log_file} ({e})")
    
    # Mode-specific validation
    if args.mode == 'dashboards':
        if args.gui_only and args.web_only:
            errors.append("Cannot specify both --gui-only and --web-only for dashboards mode")
    
    # Check for conflicting browser/gui options
    if args.mode != 'deep-tree-echo':
        if args.gui and args.mode != 'dashboards':
            warnings.append("--gui option is only relevant for deep-tree-echo mode")
        if args.browser:
            warnings.append("--browser option is only relevant for deep-tree-echo mode")
    
    if args.mode not in ['gui', 'gui-standalone'] and args.no_activity:
        warnings.append("--no-activity option is only relevant for GUI modes")
    
    # Show warnings
    if warnings:
        logger.warning("Configuration validation warnings:")
        for warning in warnings:
            logger.warning(f"  - {warning}")
    
    return errors

def main():
    """Main entry point"""
    parser = create_main_parser()
    args = parser.parse_args()
    
    # Handle special modes
    if args.list_modes:
        list_modes()
        return 0
    
    if args.migration_guide:
        show_migration_guide()
        return 0
    
    # Validate configuration first
    validation_errors = validate_configuration(args)
    if validation_errors:
        logger.error("Configuration validation failed:")
        for error in validation_errors:
            logger.error(f"  ❌ {error}")
        logger.error("\nUse 'python launch.py --help' for usage information")
        return 1
    
    # Dry-run mode for configuration validation
    if args.validate_config:
        if not args.quiet:
            print("🔍 Configuration Validation (Dry Run)")
            print("─" * 50)
        
        # Create configuration to test
        try:
            from unified_launcher import create_config_from_args
            config = create_config_from_args(args.mode, args)
            
            if not args.quiet:
                print(f"✅ Mode: {args.mode}")
                print(f"✅ Configuration: Valid")
                print(f"✅ Storage directory: {args.storage_dir}")
                if args.log_file:
                    print(f"✅ Log file: {args.log_file}")
                if args.mode == 'deep-tree-echo':
                    print(f"✅ GUI enabled: {args.gui}")
                    print(f"✅ Browser enabled: {args.browser}")
                elif args.mode == 'dashboards':
                    print(f"✅ Web port: {args.web_port}")
                    print(f"✅ GUI port: {args.gui_port}")
                    print(f"✅ GUI only: {args.gui_only}")
                    print(f"✅ Web only: {args.web_only}")
                elif args.mode == 'web':
                    print(f"✅ Web port: {args.port}")
                
                print(f"\n✅ Configuration is valid for '{args.mode}' mode")
                print("💡 Remove --validate-config to actually launch the system")
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ Configuration validation failed: {e}")
            return 1
    
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
        print(f"🚀 Starting Deep Tree Echo in '{args.mode}' mode...")
        print(f"💡 This replaces the old launch_{args.mode.replace('-', '_')}.py script")
        print()
    
    try:
        # Create configuration
        from unified_launcher import create_config_from_args
        config = create_config_from_args(args.mode, args)
        
        # For web mode, use the port argument
        if args.mode == 'web':
            config.web_port = args.port
        
        # Create and run launcher
        from unified_launcher import UnifiedLauncher
        launcher = UnifiedLauncher()
        
        if not args.quiet:
            logger.info("Configuration: %s mode", config.mode.value)
            logger.info(f"📋 Configuration: {config.mode.value} mode")
            if config.debug:
                logger.info("🐛 Debug logging enabled")
            if config.log_file:
                logger.info("Logging to file: %s", config.log_file)
                logger.info(f"📝 Logging to file: {config.log_file}")
            if args.mode == 'deep-tree-echo':
                if config.gui:
                    logger.info("🖥️  GUI dashboard will be launched")
                if config.browser:
                    logger.info("🌐 Browser automation will be initialized")
        
        # Launch the system
        result = launcher.launch_sync(config)
        
        if not args.quiet and result == 0:
            logger.info("✅ Deep Tree Echo launched successfully")
        elif not args.quiet:
            logger.error(f"❌ Launch failed with exit code: {result}")
        
        return result
        
    except KeyboardInterrupt:
        logger.info("🛑 Launch cancelled by user")
        return 0
    except (RuntimeError, ValueError, OSError) as e:
        logger.error("Launch failed: %s", e)
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1
    except Exception as e:
        logger.error("Unexpected error during launch: %s", e)
        logger.error(f"💥 Launch failed: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())