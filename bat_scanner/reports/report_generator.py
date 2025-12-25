"""
Report generation for BAT Scanner.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


class ReportGenerator:
    """Generate security scan reports in various formats."""
    
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize report generator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_report(self, scan_results: Dict[str, Any], format: str = "json") -> str:
        """
        Generate a scan report.
        
        Args:
            scan_results: Scan results dictionary
            format: Report format (json, html, text)
            
        Returns:
            Path to generated report file
        """
        if format == "json":
            return self._generate_json_report(scan_results)
        elif format == "html":
            return self._generate_html_report(scan_results)
        elif format == "text":
            return self._generate_text_report(scan_results)
        else:
            raise ValueError(f"Unsupported report format: {format}")
            
    def _generate_json_report(self, scan_results: Dict[str, Any]) -> str:
        """
        Generate JSON report.
        
        Args:
            scan_results: Scan results
            
        Returns:
            Path to report file
        """
        filename = f"scan_report_{scan_results['scan_id']}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(scan_results, f, indent=2)
            
        return str(filepath)
        
    def _generate_html_report(self, scan_results: Dict[str, Any]) -> str:
        """
        Generate HTML report.
        
        Args:
            scan_results: Scan results
            
        Returns:
            Path to report file
        """
        filename = f"scan_report_{scan_results['scan_id']}.html"
        filepath = self.output_dir / filename
        
        html_content = self._create_html_template(scan_results)
        
        with open(filepath, 'w') as f:
            f.write(html_content)
            
        return str(filepath)
        
    def _generate_text_report(self, scan_results: Dict[str, Any]) -> str:
        """
        Generate text report.
        
        Args:
            scan_results: Scan results
            
        Returns:
            Path to report file
        """
        filename = f"scan_report_{scan_results['scan_id']}.txt"
        filepath = self.output_dir / filename
        
        text_content = self._create_text_template(scan_results)
        
        with open(filepath, 'w') as f:
            f.write(text_content)
            
        return str(filepath)
        
    def _create_html_template(self, scan_results: Dict[str, Any]) -> str:
        """
        Create HTML report template.
        
        Args:
            scan_results: Scan results
            
        Returns:
            HTML content
        """
        findings_html = ""
        for finding in scan_results.get("findings", []):
            severity_class = finding.get("severity", "info")
            findings_html += f"""
            <div class="finding {severity_class}">
                <h3>{finding.get('type', 'Unknown')}</h3>
                <p><strong>Severity:</strong> {finding.get('severity', 'N/A')}</p>
                <p><strong>Description:</strong> {finding.get('description', 'N/A')}</p>
                <p><strong>Recommendation:</strong> {finding.get('recommendation', 'N/A')}</p>
            </div>
            """
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>BAT Scanner Report - {scan_results.get('scan_id', 'N/A')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .finding {{ background-color: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }}
        .finding.critical {{ border-left-color: #e74c3c; }}
        .finding.high {{ border-left-color: #e67e22; }}
        .finding.medium {{ border-left-color: #f39c12; }}
        .finding.low {{ border-left-color: #3498db; }}
        .finding h3 {{ margin-top: 0; color: #2c3e50; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>BAT Scanner Security Report</h1>
        <p>Scan ID: {scan_results.get('scan_id', 'N/A')}</p>
    </div>
    
    <div class="summary">
        <h2>Scan Summary</h2>
        <p><strong>Target:</strong> {scan_results.get('target', 'N/A')}</p>
        <p><strong>Scan Type:</strong> {scan_results.get('scan_type', 'N/A')}</p>
        <p><strong>Start Time:</strong> {scan_results.get('start_time', 'N/A')}</p>
        <p><strong>End Time:</strong> {scan_results.get('end_time', 'N/A')}</p>
        <p><strong>Total Findings:</strong> {scan_results.get('total_findings', 0)}</p>
        <p><strong>Modules Executed:</strong> {', '.join(scan_results.get('modules_executed', []))}</p>
    </div>
    
    <div class="findings">
        <h2>Findings</h2>
        {findings_html if findings_html else '<p>No findings detected.</p>'}
    </div>
</body>
</html>
        """
        return html
        
    def _create_text_template(self, scan_results: Dict[str, Any]) -> str:
        """
        Create text report template.
        
        Args:
            scan_results: Scan results
            
        Returns:
            Text content
        """
        text = f"""
================================================================================
                        BAT SCANNER SECURITY REPORT
================================================================================

Scan ID: {scan_results.get('scan_id', 'N/A')}
Target: {scan_results.get('target', 'N/A')}
Scan Type: {scan_results.get('scan_type', 'N/A')}
Start Time: {scan_results.get('start_time', 'N/A')}
End Time: {scan_results.get('end_time', 'N/A')}

--------------------------------------------------------------------------------
SUMMARY
--------------------------------------------------------------------------------
Total Findings: {scan_results.get('total_findings', 0)}
Modules Executed: {', '.join(scan_results.get('modules_executed', []))}

--------------------------------------------------------------------------------
FINDINGS
--------------------------------------------------------------------------------
"""
        
        findings = scan_results.get('findings', [])
        if findings:
            for i, finding in enumerate(findings, 1):
                text += f"""
Finding #{i}:
  Type: {finding.get('type', 'Unknown')}
  Severity: {finding.get('severity', 'N/A')}
  Description: {finding.get('description', 'N/A')}
  Recommendation: {finding.get('recommendation', 'N/A')}
  
"""
        else:
            text += "\nNo findings detected.\n"
            
        text += "\n" + "=" * 80 + "\n"
        return text
