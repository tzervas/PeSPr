"""
Command-line interface for PeSPr.

Provides commands for analyzing projects and generating configurations.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
from loguru import logger

from pespr import __version__
from pespr.analyze import analyze_project
from pespr.config_generator import generate_config


def setup_logging(verbose: bool = False) -> None:
    """
    Configure logging for the CLI.

    Args:
        verbose: Enable verbose logging
    """
    logger.remove()
    log_level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, level=log_level)


def cmd_analyze(args: argparse.Namespace) -> int:
    """
    Handle the analyze command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        logger.info(f"Analyzing project: {args.project_path}")
        results = analyze_project(args.project_path)
        
        print(f"\nAnalysis Results for {args.project_path}")
        print("=" * 60)
        print(f"Exception types found: {len(results['exception_types'])}")
        print(f"Error locations found: {len(results['error_locations'])}")
        print(f"Type errors found: {len(results['type_errors'])}")
        
        return 0
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return 1


def cmd_generate_config(args: argparse.Namespace) -> int:
    """
    Handle the generate-config command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        logger.info(f"Generating config for project: {args.project_path}")
        config = generate_config(args.project_path, args.output)
        
        print(f"\nConfiguration generated successfully!")
        print(f"Output: {args.output}")
        print(f"Version: {config['version']}")
        
        return 0
    except Exception as e:
        logger.error(f"Configuration generation failed: {e}")
        return 1


def cmd_update_config(args: argparse.Namespace) -> int:
    """
    Handle the update-config command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        logger.info(f"Updating config for project: {args.project_path}")
        
        # Check if config exists
        config_path = Path(args.config or "dynel_config.yaml")
        if not config_path.exists():
            logger.warning(f"Config file not found: {config_path}")
            logger.info("Generating new config instead...")
            return cmd_generate_config(args)
        
        # TODO: Implement config update logic
        logger.info("Config update functionality coming soon!")
        print("\nConfig update is not yet implemented.")
        print("Use 'generate-config' to create a new configuration.")
        
        return 0
    except Exception as e:
        logger.error(f"Configuration update failed: {e}")
        return 1


def create_parser() -> argparse.ArgumentParser:
    """
    Create the argument parser for the CLI.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="pespr",
        description="Perihelion Signal Processor - Automate error handling and logging configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a Python project for error handling patterns",
    )
    analyze_parser.add_argument(
        "project_path",
        type=str,
        help="Path to the Python project to analyze",
    )
    
    # Generate-config command
    generate_parser = subparsers.add_parser(
        "generate-config",
        help="Generate a DynEL configuration file",
    )
    generate_parser.add_argument(
        "project_path",
        type=str,
        help="Path to the Python project to analyze",
    )
    generate_parser.add_argument(
        "-o", "--output",
        type=str,
        default="dynel_config.yaml",
        help="Output path for the configuration file (default: dynel_config.yaml)",
    )
    
    # Update-config command
    update_parser = subparsers.add_parser(
        "update-config",
        help="Update an existing DynEL configuration file",
    )
    update_parser.add_argument(
        "project_path",
        type=str,
        help="Path to the Python project to analyze",
    )
    update_parser.add_argument(
        "-c", "--config",
        type=str,
        help="Path to the existing config file (default: dynel_config.yaml)",
    )
    
    return parser


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate command handler
    if args.command == "analyze":
        return cmd_analyze(args)
    elif args.command == "generate-config":
        return cmd_generate_config(args)
    elif args.command == "update-config":
        return cmd_update_config(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
