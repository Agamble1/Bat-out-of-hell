"""
Port Scanner Module.
Scans for open ports and services on target systems.
"""
import socket
from typing import Dict, Any, List
from bat_scanner.core.base_module import BaseScannerModule


class PortScanner(BaseScannerModule):
    """Scanner module for detecting open ports and services."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the port scanner.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.quick_scan = True
        self.common_ports = [21, 22, 23, 25, 80, 443, 3306, 3389, 8080, 8443]
        self.timeout = self.config.get("timeout", 1)
        
    def scan(self, target: str) -> Dict[str, Any]:
        """
        Scan target for open ports.
        
        Args:
            target: IP address or hostname to scan
            
        Returns:
            Dictionary with scan results
        """
        if not self.validate_target(target):
            return {"findings": []}
            
        self.logger.info(f"Starting port scan on {target}")
        
        ports_to_scan = self.config.get("ports", self.common_ports)
        open_ports = []
        
        for port in ports_to_scan:
            if self._check_port(target, port):
                service = self._identify_service(port)
                open_ports.append({
                    "port": port,
                    "state": "open",
                    "service": service
                })
                self.logger.info(f"Found open port: {port} ({service})")
                
        findings = []
        for port_info in open_ports:
            findings.append({
                "type": "open_port",
                "severity": self._assess_severity(port_info["port"]),
                "port": port_info["port"],
                "service": port_info["service"],
                "description": f"Port {port_info['port']} ({port_info['service']}) is open",
                "recommendation": self._get_recommendation(port_info["port"])
            })
            
        return {
            "module": "PortScanner",
            "findings": findings,
            "total_scanned": len(ports_to_scan),
            "total_open": len(open_ports)
        }
        
    def _check_port(self, target: str, port: int) -> bool:
        """
        Check if a port is open.
        
        Args:
            target: Target host
            port: Port number to check
            
        Returns:
            Boolean indicating if port is open
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            return result == 0
        except socket.error:
            return False
            
    def _identify_service(self, port: int) -> str:
        """
        Identify common service running on port.
        
        Args:
            port: Port number
            
        Returns:
            Service name
        """
        common_services = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            80: "HTTP",
            443: "HTTPS",
            3306: "MySQL",
            3389: "RDP",
            8080: "HTTP-Proxy",
            8443: "HTTPS-Alt"
        }
        return common_services.get(port, "Unknown")
        
    def _assess_severity(self, port: int) -> str:
        """
        Assess security severity of open port.
        
        Args:
            port: Port number
            
        Returns:
            Severity level
        """
        high_risk_ports = [23, 3389]  # Telnet, RDP
        medium_risk_ports = [21, 25, 3306]  # FTP, SMTP, MySQL
        
        if port in high_risk_ports:
            return "high"
        elif port in medium_risk_ports:
            return "medium"
        return "low"
        
    def _get_recommendation(self, port: int) -> str:
        """
        Get security recommendation for open port.
        
        Args:
            port: Port number
            
        Returns:
            Security recommendation
        """
        recommendations = {
            21: "Consider using SFTP instead of FTP for secure file transfers",
            23: "Telnet is insecure. Use SSH instead",
            3389: "Ensure RDP is properly secured with strong passwords and 2FA",
            3306: "MySQL should not be exposed directly. Use firewall rules"
        }
        return recommendations.get(port, "Ensure this service is necessary and properly secured")
