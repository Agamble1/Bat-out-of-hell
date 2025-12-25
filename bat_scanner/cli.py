#!/usr/bin/env python3
"""
BAT Scanner - Command Line Interface
A tool to assist white hat ethical hackers in identifying and searching threats and vulnerabilities.
"""
import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bat_scanner.core.scanner import ScannerEngine
from bat_scanner.modules.port_scanner import PortScanner
from bat_scanner.modules.vulnerability_scanner import VulnerabilityScanner
from bat_scanner.modules.threat_intelligence import ThreatIntelligence
from bat_scanner.modules.exploit_db import ExploitDatabase
from bat_scanner.utils.logger import setup_logging
from bat_scanner.utils.config import Config
from bat_scanner.reports.report_generator import ReportGenerator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="BAT Scanner - Security Assessment Tool for Ethical Hackers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick scan of a target
  python bat_scanner/cli.py -t 192.168.1.1 --scan-type quick
  
  # Full scan with custom config
  python bat_scanner/cli.py -t example.com --scan-type full -c configs/custom.json
  
  # Search exploit database
  python bat_scanner/cli.py --search-exploits log4j
  
  # Generate HTML report
  python bat_scanner/cli.py -t 192.168.1.1 --report-format html
        """
    )
    
    parser.add_argument(
        "-t", "--target",
        help="Target to scan (IP address, domain, or hostname)",
        type=str
    )
    
    parser.add_argument(
        "--scan-type",
        choices=["quick", "full", "custom"],
        default="full",
        help="Type of scan to perform (default: full)"
    )
    
    parser.add_argument(
        "-c", "--config",
        help="Path to configuration file (JSON or YAML)",
        type=str
    )
    
    parser.add_argument(
        "--report-format",
        choices=["json", "html", "text"],
        default="json",
        help="Report output format (default: json)"
    )
    
    parser.add_argument(
        "--output-dir",
        help="Directory to save reports (default: reports)",
        default="reports",
        type=str
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--search-exploits",
        help="Search exploit database for a specific term",
        type=str,
        metavar="QUERY"
    )
    
    parser.add_argument(
        "--modules",
        help="Comma-separated list of modules to run (port,vuln,threat,exploit)",
        type=str
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="BAT Scanner 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(log_level=args.log_level)
    
    # Handle exploit search
    if args.search_exploits:
        handle_exploit_search(args.search_exploits)
        return 0
    
    # Validate target for scanning
    if not args.target:
        parser.error("Target (-t/--target) is required for scanning")
        return 1
    
    # Load configuration
    config = Config(args.config) if args.config else Config()
    
    # Initialize scanner engine
    engine = ScannerEngine(config.config)
    
    # Register modules
    register_modules(engine, args.modules, config.config)
    
    # Perform scan
    print(f"\n{'='*60}")
    print(f"BAT Scanner - Starting {args.scan_type} scan on {args.target}")
    print(f"{'='*60}\n")
    
    results = engine.start_scan(args.target, args.scan_type)
    
    # Generate report
    report_gen = ReportGenerator(args.output_dir)
    report_path = report_gen.generate_report(results, args.report_format)
    
    print(f"\n{'='*60}")
    print(f"Scan completed!")
    print(f"Total findings: {results['total_findings']}")
    print(f"Report saved to: {report_path}")
    print(f"{'='*60}\n")
    
    # Display summary of findings
    if results['findings']:
        print("\nFindings Summary:")
        severity_counts = {}
        for finding in results['findings']:
            severity = finding.get('severity', 'unknown')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        for severity, count in sorted(severity_counts.items()):
            print(f"  {severity.upper()}: {count}")
    
    return 0


def register_modules(engine: ScannerEngine, modules_arg: str, config: dict):
    """
    Register scanning modules with the engine.
    
    Args:
        engine: Scanner engine instance
        modules_arg: Comma-separated module names or None for all
        config: Configuration dictionary
    """
    available_modules = {
        "port": PortScanner,
        "vuln": VulnerabilityScanner,
        "threat": ThreatIntelligence,
        "exploit": ExploitDatabase
    }
    
    if modules_arg:
        selected = [m.strip() for m in modules_arg.split(",")]
        modules_to_register = {k: v for k, v in available_modules.items() if k in selected}
    else:
        modules_to_register = available_modules
    
    for name, module_class in modules_to_register.items():
        module_config = config.get(name + "_scanner", {})
        engine.register_module(module_class(module_config))


def handle_exploit_search(query: str):
    """
    Handle exploit database search.
    
    Args:
        query: Search query
    """
    print(f"\n{'='*60}")
    print(f"Searching exploit database for: {query}")
    print(f"{'='*60}\n")
    
    exploit_db = ExploitDatabase()
    results = exploit_db.scan(query)
    
    if results['findings']:
        for i, exploit in enumerate(results['findings'], 1):
            print(f"\nExploit #{i}:")
            print(f"  CVE ID: {exploit.get('cve_id', 'N/A')}")
            print(f"  Title: {exploit.get('title', 'N/A')}")
            print(f"  Severity: {exploit.get('severity', 'N/A')}")
            print(f"  Description: {exploit.get('description', 'N/A')}")
            print(f"  Affected Versions: {exploit.get('affected_versions', 'N/A')}")
            print(f"  Exploit Available: {exploit.get('exploit_available', 'N/A')}")
            print(f"  Recommendation: {exploit.get('recommendation', 'N/A')}")
    else:
        print("No exploits found matching your query.")
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    sys.exit(main())
