# BAT Scanner - Bat-out-of-hell

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive security assessment tool designed to assist white hat ethical hackers in identifying and searching for threats and vulnerabilities.

## 🎯 Overview

BAT Scanner is a modular security scanning framework that helps ethical hackers and security professionals conduct security assessments. It includes multiple scanning modules for port scanning, vulnerability detection, threat intelligence lookups, and exploit database searches.

## ⚠️ Legal Disclaimer

**IMPORTANT**: This tool is intended for authorized security testing and educational purposes only. Always ensure you have explicit permission before scanning any systems or networks that you do not own. Unauthorized scanning or testing is illegal and unethical.

## 🚀 Features

- **Port Scanner**: Detect open ports and identify running services
- **Vulnerability Scanner**: Check for common security vulnerabilities and misconfigurations
- **Threat Intelligence**: Cross-reference targets against threat intelligence feeds
- **Exploit Database**: Search for known exploits and CVE information
- **Modular Architecture**: Easy to extend with custom scanning modules
- **Multiple Report Formats**: Generate reports in JSON, HTML, or text format
- **Configurable**: Flexible configuration via JSON or YAML files
- **Comprehensive Logging**: Detailed logging for audit trails

## 📋 Requirements

- Python 3.7 or higher
- pip (Python package manager)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/Agamble1/Bat-out-of-hell.git
cd Bat-out-of-hell
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Scanning

Perform a quick scan on a target:
```bash
python bat_scanner/cli.py -t 192.168.1.1 --scan-type quick
```

Perform a full comprehensive scan:
```bash
python bat_scanner/cli.py -t example.com --scan-type full
```

### Custom Configuration

Use a custom configuration file:
```bash
python bat_scanner/cli.py -t 192.168.1.1 -c configs/custom.json
```

### Report Generation

Generate reports in different formats:
```bash
# JSON report (default)
python bat_scanner/cli.py -t 192.168.1.1 --report-format json

# HTML report
python bat_scanner/cli.py -t 192.168.1.1 --report-format html

# Text report
python bat_scanner/cli.py -t 192.168.1.1 --report-format text
```

### Exploit Database Search

Search for exploits by keyword:
```bash
python bat_scanner/cli.py --search-exploits log4j
python bat_scanner/cli.py --search-exploits CVE-2021-44228
```

### Module Selection

Run specific modules only:
```bash
# Run only port scanner
python bat_scanner/cli.py -t 192.168.1.1 --modules port

# Run multiple specific modules
python bat_scanner/cli.py -t 192.168.1.1 --modules port,threat
```

### Advanced Options

```bash
# Set custom output directory
python bat_scanner/cli.py -t 192.168.1.1 --output-dir /path/to/reports

# Set logging level
python bat_scanner/cli.py -t 192.168.1.1 --log-level DEBUG

# Show version
python bat_scanner/cli.py --version

# Show help
python bat_scanner/cli.py --help
```

## 📁 Project Structure

```
Bat-out-of-hell/
├── bat_scanner/              # Main package directory
│   ├── __init__.py
│   ├── cli.py               # Command-line interface
│   ├── core/                # Core scanning engine
│   │   ├── __init__.py
│   │   ├── scanner.py       # Main scanner engine
│   │   └── base_module.py   # Base class for modules
│   ├── modules/             # Scanning modules
│   │   ├── __init__.py
│   │   ├── port_scanner.py  # Port scanning module
│   │   ├── vulnerability_scanner.py
│   │   ├── threat_intelligence.py
│   │   └── exploit_db.py    # Exploit database search
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── logger.py        # Logging utilities
│   │   └── config.py        # Configuration management
│   └── reports/             # Report generation
│       ├── __init__.py
│       └── report_generator.py
├── configs/                 # Configuration files
│   ├── default.json
│   └── example.yaml
├── tests/                   # Test directory
├── docs/                    # Documentation
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── README.md               # This file
```

## 🔧 Configuration

BAT Scanner can be configured using JSON or YAML files. Example configuration:

```json
{
  "scanner": {
    "timeout": 5,
    "max_threads": 10,
    "user_agent": "BAT-Scanner/1.0"
  },
  "port_scanner": {
    "timeout": 1,
    "ports": [21, 22, 23, 25, 80, 443, 3306, 3389, 8080, 8443]
  },
  "logging": {
    "level": "INFO",
    "file": "logs/bat_scanner.log"
  },
  "reports": {
    "output_dir": "reports",
    "format": "json"
  }
}
```

See the `configs/` directory for example configuration files.

## 🧩 Modules

### Port Scanner
Scans for open ports and identifies services running on those ports. Provides security recommendations for potentially risky open ports.

### Vulnerability Scanner
Checks for common vulnerabilities including:
- SQL Injection (CWE-89)
- Cross-Site Scripting (CWE-79)
- CSRF (CWE-352)
- Weak SSL/TLS configurations

### Threat Intelligence
Cross-references targets against threat intelligence feeds to identify:
- Malicious IP addresses
- Known bad domains
- Malware file hashes

### Exploit Database
Searches for known exploits and CVE information for:
- Software vulnerabilities
- Security advisories
- Available proof-of-concept exploits

## 🛠️ Extending BAT Scanner

To create a custom scanning module:

1. Create a new file in `bat_scanner/modules/`
2. Inherit from `BaseScannerModule`
3. Implement the `scan()` method
4. Register your module in the CLI

Example:
```python
from bat_scanner.core.base_module import BaseScannerModule

class CustomScanner(BaseScannerModule):
    def scan(self, target: str):
        # Your scanning logic here
        return {
            "module": "CustomScanner",
            "findings": []
        }
```

## 📊 Report Examples

### JSON Report
Reports include comprehensive scan information:
- Scan metadata (ID, target, timestamps)
- Modules executed
- Detailed findings with severity levels
- Security recommendations

### HTML Report
User-friendly HTML reports with:
- Color-coded severity indicators
- Organized findings sections
- Executive summary

### Text Report
Plain text reports suitable for:
- Terminal viewing
- Quick reviews
- Automated processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Responsible Disclosure

If you discover any security issues with BAT Scanner itself, please report them responsibly by contacting the maintainers directly rather than posting publicly.

## 🙏 Acknowledgments

- Inspired by the security research community
- Built for ethical hackers and security professionals
- Designed to support responsible security testing

## 📚 Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CVE Database](https://cve.mitre.org/)
- [Exploit Database](https://www.exploit-db.com/)

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub.

---

**Remember**: With great power comes great responsibility. Use this tool ethically and legally.