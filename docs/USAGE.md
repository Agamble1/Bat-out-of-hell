# BAT Scanner Usage Guide

## Quick Start

### Basic Scanning

The simplest way to use BAT Scanner is to specify a target:

```bash
python bat_scanner/cli.py -t 192.168.1.1
```

This performs a full scan using all available modules.

### Scan Types

BAT Scanner supports three scan types:

1. **Quick Scan** - Fast scan using quick-scan modules only
   ```bash
   python bat_scanner/cli.py -t example.com --scan-type quick
   ```

2. **Full Scan** - Comprehensive scan using all modules (default)
   ```bash
   python bat_scanner/cli.py -t example.com --scan-type full
   ```

3. **Custom Scan** - Run specific modules
   ```bash
   python bat_scanner/cli.py -t example.com --modules port,threat
   ```

## Modules

### Port Scanner (`port`)
Scans for open ports and identifies services.

**Use cases:**
- Network reconnaissance
- Service discovery
- Attack surface mapping

**Example:**
```bash
python bat_scanner/cli.py -t 192.168.1.1 --modules port
```

### Vulnerability Scanner (`vuln`)
Checks for common vulnerabilities and misconfigurations.

**Use cases:**
- Web application testing
- SSL/TLS configuration checks
- Security audits

**Example:**
```bash
python bat_scanner/cli.py -t example.com --modules vuln
```

### Threat Intelligence (`threat`)
Cross-references targets against threat feeds.

**Use cases:**
- IOC (Indicator of Compromise) checking
- IP/Domain reputation lookups
- Malware hash verification

**Example:**
```bash
python bat_scanner/cli.py -t 192.0.2.1 --modules threat
```

### Exploit Database (`exploit`)
Searches for known exploits and CVEs.

**Use cases:**
- Vulnerability research
- Patch verification
- Risk assessment

**Example:**
```bash
python bat_scanner/cli.py --search-exploits CVE-2021-44228
```

## Configuration

### Using Configuration Files

Create a JSON or YAML configuration file:

**JSON Example (config.json):**
```json
{
  "scanner": {
    "timeout": 10,
    "max_threads": 5
  },
  "port_scanner": {
    "timeout": 2,
    "ports": [22, 80, 443, 8080]
  }
}
```

Use the configuration:
```bash
python bat_scanner/cli.py -t example.com -c config.json
```

**YAML Example (config.yaml):**
```yaml
scanner:
  timeout: 10
  max_threads: 5

port_scanner:
  timeout: 2
  ports:
    - 22
    - 80
    - 443
    - 8080
```

### Configuration Options

#### Scanner Settings
- `timeout`: Global timeout for operations (seconds)
- `max_threads`: Maximum concurrent threads
- `user_agent`: User agent string for HTTP requests

#### Port Scanner Settings
- `timeout`: Port connection timeout (seconds)
- `ports`: List of ports to scan

#### Logging Settings
- `level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `file`: Log file path

#### Report Settings
- `output_dir`: Directory for saving reports
- `format`: Default report format (json, html, text)

## Report Formats

### JSON Reports

JSON reports are machine-readable and suitable for automation:

```bash
python bat_scanner/cli.py -t example.com --report-format json
```

**Output Structure:**
```json
{
  "scan_id": "scan_20231225_120000",
  "target": "example.com",
  "start_time": "2023-12-25T12:00:00",
  "end_time": "2023-12-25T12:05:00",
  "total_findings": 5,
  "findings": [
    {
      "type": "open_port",
      "severity": "medium",
      "description": "Port 80 (HTTP) is open",
      "recommendation": "Ensure this service is necessary"
    }
  ]
}
```

### HTML Reports

HTML reports are user-friendly with visual formatting:

```bash
python bat_scanner/cli.py -t example.com --report-format html
```

Features:
- Color-coded severity levels
- Organized sections
- Responsive design
- Easy to share with stakeholders

### Text Reports

Text reports are simple and readable in terminals:

```bash
python bat_scanner/cli.py -t example.com --report-format text
```

Suitable for:
- Quick reviews
- Terminal viewing
- Email reports

## Advanced Usage

### Custom Output Directory

Save reports to a specific directory:

```bash
python bat_scanner/cli.py -t example.com --output-dir /path/to/reports
```

### Logging Control

Adjust logging verbosity:

```bash
# Debug level (most verbose)
python bat_scanner/cli.py -t example.com --log-level DEBUG

# Info level (default)
python bat_scanner/cli.py -t example.com --log-level INFO

# Warning level (minimal output)
python bat_scanner/cli.py -t example.com --log-level WARNING
```

### Exploit Database Searches

Search for specific vulnerabilities:

```bash
# Search by CVE
python bat_scanner/cli.py --search-exploits CVE-2021-44228

# Search by software name
python bat_scanner/cli.py --search-exploits log4j

# Search by keyword
python bat_scanner/cli.py --search-exploits heartbleed
```

## Best Practices

### 1. Always Get Authorization
Ensure you have written permission before scanning any systems.

### 2. Start with Quick Scans
Use quick scans for initial reconnaissance:
```bash
python bat_scanner/cli.py -t example.com --scan-type quick
```

### 3. Use Configuration Files
Create reusable configurations for common scan scenarios:
```bash
python bat_scanner/cli.py -t example.com -c configs/web_app_scan.json
```

### 4. Save and Review Reports
Always save reports for documentation:
```bash
python bat_scanner/cli.py -t example.com --report-format html --output-dir ./audit_2023
```

### 5. Validate Findings
Review and validate all findings before taking action.

### 6. Keep Logs
Maintain detailed logs for audit trails:
```bash
python bat_scanner/cli.py -t example.com --log-level DEBUG
```

## Common Workflows

### Web Application Assessment

```bash
# 1. Quick reconnaissance
python bat_scanner/cli.py -t webapp.example.com --scan-type quick

# 2. Full vulnerability scan
python bat_scanner/cli.py -t webapp.example.com --modules vuln

# 3. Generate HTML report
python bat_scanner/cli.py -t webapp.example.com --report-format html
```

### Network Security Audit

```bash
# 1. Port scan
python bat_scanner/cli.py -t 192.168.1.0/24 --modules port

# 2. Threat intelligence check
python bat_scanner/cli.py -t 192.168.1.100 --modules threat

# 3. Full scan with custom config
python bat_scanner/cli.py -t 192.168.1.100 -c configs/network_audit.json
```

### Vulnerability Research

```bash
# 1. Search for exploits
python bat_scanner/cli.py --search-exploits log4j

# 2. Scan target for specific vulnerability
python bat_scanner/cli.py -t vulnerable-app.com --modules vuln,exploit
```

## Troubleshooting

### Issue: "Target cannot be empty"
**Solution:** Ensure you provide a target with `-t` flag:
```bash
python bat_scanner/cli.py -t example.com
```

### Issue: No results from scan
**Solution:** 
1. Check target is reachable
2. Increase timeout in configuration
3. Enable DEBUG logging to see details

### Issue: Permission denied errors
**Solution:** Some scanning operations may require elevated privileges:
```bash
sudo python bat_scanner/cli.py -t example.com
```

### Issue: Module not found
**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Getting Help

Display help message:
```bash
python bat_scanner/cli.py --help
```

Show version:
```bash
python bat_scanner/cli.py --version
```
