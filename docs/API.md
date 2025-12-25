# BAT Scanner - API Documentation

## Core Components

### ScannerEngine

Main scanning engine that orchestrates security assessments.

```python
from bat_scanner.core.scanner import ScannerEngine

# Initialize scanner
engine = ScannerEngine(config)

# Register modules
engine.register_module(PortScanner())
engine.register_module(VulnerabilityScanner())

# Start scan
results = engine.start_scan(target="example.com", scan_type="full")
```

#### Methods

- `register_module(module)`: Register a scanning module
- `start_scan(target, scan_type)`: Start a security scan
- `get_results()`: Get all scan results

### BaseScannerModule

Abstract base class for all scanner modules.

```python
from bat_scanner.core.base_module import BaseScannerModule

class CustomScanner(BaseScannerModule):
    def scan(self, target: str):
        # Implement scanning logic
        return {
            "module": "CustomScanner",
            "findings": []
        }
```

## Modules

### PortScanner

Scans for open ports and identifies services.

```python
from bat_scanner.modules.port_scanner import PortScanner

scanner = PortScanner(config={
    "timeout": 2,
    "ports": [80, 443, 8080]
})

results = scanner.scan("192.168.1.1")
```

**Configuration Options:**
- `timeout`: Connection timeout in seconds
- `ports`: List of ports to scan

**Output Format:**
```json
{
  "module": "PortScanner",
  "findings": [
    {
      "type": "open_port",
      "severity": "medium",
      "port": 80,
      "service": "HTTP",
      "description": "Port 80 (HTTP) is open",
      "recommendation": "Ensure this service is necessary..."
    }
  ]
}
```

### VulnerabilityScanner

Checks for common vulnerabilities and security misconfigurations.

```python
from bat_scanner.modules.vulnerability_scanner import VulnerabilityScanner

scanner = VulnerabilityScanner()
results = scanner.scan("example.com")
```

**Checks:**
- SQL Injection (CWE-89)
- Cross-Site Scripting (CWE-79)
- CSRF (CWE-352)
- Weak SSL/TLS configurations

### ThreatIntelligence

Cross-references targets against threat intelligence feeds.

```python
from bat_scanner.modules.threat_intelligence import ThreatIntelligence

scanner = ThreatIntelligence()
results = scanner.scan("192.168.1.1")
```

**Checks:**
- Malicious IP addresses
- Known bad domains
- Malware file hashes

### ExploitDatabase

Searches for known exploits and CVE information.

```python
from bat_scanner.modules.exploit_db import ExploitDatabase

scanner = ExploitDatabase()
results = scanner.scan("log4j")
```

## Utilities

### Config

Configuration management for BAT Scanner.

```python
from bat_scanner.utils.config import Config

# Load default configuration
config = Config()

# Load from file
config = Config("configs/custom.json")

# Get configuration value
timeout = config.get("scanner.timeout", default=5)

# Set configuration value
config.set("scanner.timeout", 10)

# Save configuration
config.save_to_file("configs/saved.json")
```

### Logger

Logging utilities for BAT Scanner.

```python
from bat_scanner.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(log_level="INFO", log_file="logs/scanner.log")

# Get logger
logger = get_logger(__name__)
logger.info("Starting scan...")
```

## Reports

### ReportGenerator

Generate security scan reports in various formats.

```python
from bat_scanner.reports.report_generator import ReportGenerator

# Initialize report generator
report_gen = ReportGenerator(output_dir="reports")

# Generate report
report_path = report_gen.generate_report(
    scan_results=results,
    format="html"  # json, html, or text
)
```

**Report Formats:**
- `json`: Machine-readable JSON format
- `html`: User-friendly HTML with styling
- `text`: Plain text format

## Example: Full Integration

```python
#!/usr/bin/env python3
from bat_scanner.core.scanner import ScannerEngine
from bat_scanner.modules.port_scanner import PortScanner
from bat_scanner.modules.vulnerability_scanner import VulnerabilityScanner
from bat_scanner.modules.threat_intelligence import ThreatIntelligence
from bat_scanner.modules.exploit_db import ExploitDatabase
from bat_scanner.utils.logger import setup_logging
from bat_scanner.utils.config import Config
from bat_scanner.reports.report_generator import ReportGenerator

# Setup
setup_logging(log_level="INFO")
config = Config("configs/default.json")

# Initialize scanner
engine = ScannerEngine(config.config)

# Register modules
engine.register_module(PortScanner(config.get("port_scanner")))
engine.register_module(VulnerabilityScanner())
engine.register_module(ThreatIntelligence())
engine.register_module(ExploitDatabase())

# Perform scan
results = engine.start_scan(
    target="example.com",
    scan_type="full"
)

# Generate report
report_gen = ReportGenerator(output_dir="reports")
report_path = report_gen.generate_report(results, format="html")

print(f"Scan completed. Report saved to: {report_path}")
print(f"Total findings: {results['total_findings']}")
```

## CLI Usage

See [USAGE.md](USAGE.md) for detailed CLI documentation.

```bash
# Basic scan
python bat_scanner/cli.py -t example.com

# Custom configuration
python bat_scanner/cli.py -t example.com -c configs/custom.json

# Specific modules
python bat_scanner/cli.py -t example.com --modules port,threat

# HTML report
python bat_scanner/cli.py -t example.com --report-format html

# Exploit search
python bat_scanner/cli.py --search-exploits CVE-2021-44228
```

## Error Handling

All modules implement proper error handling:

```python
try:
    results = scanner.scan(target)
except Exception as e:
    logger.error(f"Scan failed: {str(e)}")
```

## Security Considerations

1. **Authorization**: Always obtain proper authorization before scanning
2. **Rate Limiting**: Implement rate limiting for aggressive scans
3. **Logging**: All scans are logged for audit trails
4. **Target Validation**: Targets are validated before scanning
5. **Error Handling**: Errors are caught and logged without exposing sensitive information

## Extending BAT Scanner

### Creating a Custom Module

1. Create a new file in `bat_scanner/modules/`
2. Inherit from `BaseScannerModule`
3. Implement the `scan()` method
4. Register in CLI or programmatically

```python
from bat_scanner.core.base_module import BaseScannerModule

class DNSScanner(BaseScannerModule):
    """Scanner for DNS records and configuration."""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.quick_scan = True
    
    def scan(self, target: str):
        """Scan DNS records."""
        if not self.validate_target(target):
            return {"findings": []}
        
        findings = []
        
        # Implement DNS scanning logic
        # ...
        
        return {
            "module": "DNSScanner",
            "findings": findings
        }
```

### Adding to CLI

Update `bat_scanner/cli.py`:

```python
from bat_scanner.modules.dns_scanner import DNSScanner

available_modules = {
    "port": PortScanner,
    "vuln": VulnerabilityScanner,
    "threat": ThreatIntelligence,
    "exploit": ExploitDatabase,
    "dns": DNSScanner  # Add your module
}
```

## Testing

Run tests:

```bash
python -m unittest tests.test_infrastructure -v
```

## Performance Considerations

- Use `quick_scan = True` for fast modules
- Implement timeouts to prevent hanging
- Use threading for concurrent operations
- Cache results when appropriate

## License

MIT License - See LICENSE file for details.
