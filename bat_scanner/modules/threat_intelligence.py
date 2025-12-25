"""
Threat Intelligence Module.
Checks targets against threat intelligence databases and indicators of compromise.
"""
from typing import Dict, Any, List
from bat_scanner.core.base_module import BaseScannerModule


class ThreatIntelligence(BaseScannerModule):
    """Scanner module for threat intelligence lookups."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the threat intelligence module.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.quick_scan = True
        self.threat_feeds = self._load_threat_feeds()
        
    def scan(self, target: str) -> Dict[str, Any]:
        """
        Check target against threat intelligence sources.
        
        Args:
            target: Target to check (IP, domain, hash, etc.)
            
        Returns:
            Dictionary with scan results
        """
        if not self.validate_target(target):
            return {"findings": []}
            
        self.logger.info(f"Checking threat intelligence for {target}")
        
        findings = []
        
        # Check IP reputation
        if self._is_ip_address(target):
            ip_threats = self._check_ip_reputation(target)
            findings.extend(ip_threats)
            
        # Check domain reputation
        if self._is_domain(target):
            domain_threats = self._check_domain_reputation(target)
            findings.extend(domain_threats)
            
        # Check for malicious indicators
        ioc_matches = self._check_indicators_of_compromise(target)
        findings.extend(ioc_matches)
        
        return {
            "module": "ThreatIntelligence",
            "findings": findings,
            "total_threats": len(findings)
        }
        
    def _load_threat_feeds(self) -> Dict[str, List[str]]:
        """
        Load threat intelligence feeds.
        
        Returns:
            Dictionary of threat feeds
        """
        # In a real implementation, this would load from actual threat feeds
        return {
            "malicious_ips": [
                "192.0.2.1",  # Example IPs (documentation ranges)
                "198.51.100.1"
            ],
            "malicious_domains": [
                "malicious-example.com",
                "phishing-site.net"
            ],
            "malware_hashes": [
                "d41d8cd98f00b204e9800998ecf8427e"
            ]
        }
        
    def _check_ip_reputation(self, ip: str) -> List[Dict[str, Any]]:
        """
        Check IP address reputation.
        
        Args:
            ip: IP address to check
            
        Returns:
            List of findings
        """
        findings = []
        
        if ip in self.threat_feeds["malicious_ips"]:
            findings.append({
                "type": "threat_intel",
                "threat_type": "malicious_ip",
                "severity": "critical",
                "target": ip,
                "description": f"IP {ip} identified in threat intelligence feeds",
                "recommendation": "Block this IP and investigate any connections"
            })
            
        return findings
        
    def _check_domain_reputation(self, domain: str) -> List[Dict[str, Any]]:
        """
        Check domain reputation.
        
        Args:
            domain: Domain to check
            
        Returns:
            List of findings
        """
        findings = []
        
        if domain in self.threat_feeds["malicious_domains"]:
            findings.append({
                "type": "threat_intel",
                "threat_type": "malicious_domain",
                "severity": "high",
                "target": domain,
                "description": f"Domain {domain} identified as malicious in threat feeds",
                "recommendation": "Block access to this domain and investigate any connections"
            })
            
        return findings
        
    def _check_indicators_of_compromise(self, target: str) -> List[Dict[str, Any]]:
        """
        Check for indicators of compromise.
        
        Args:
            target: Target to check
            
        Returns:
            List of findings
        """
        findings = []
        
        # Check if target could be a file hash
        if len(target) == 32 and all(c in '0123456789abcdef' for c in target.lower()):
            if target.lower() in self.threat_feeds["malware_hashes"]:
                findings.append({
                    "type": "threat_intel",
                    "threat_type": "malware_hash",
                    "severity": "critical",
                    "target": target,
                    "description": f"File hash {target} matches known malware signature",
                    "recommendation": "Quarantine file immediately and perform full system scan"
                })
                
        return findings
        
    def _is_ip_address(self, target: str) -> bool:
        """
        Check if target is an IP address.
        
        Args:
            target: Target to check
            
        Returns:
            Boolean indicating if target is an IP
        """
        parts = target.split('.')
        if len(parts) == 4:
            try:
                return all(0 <= int(part) <= 255 for part in parts)
            except ValueError:
                return False
        return False
        
    def _is_domain(self, target: str) -> bool:
        """
        Check if target is a domain name.
        
        Args:
            target: Target to check
            
        Returns:
            Boolean indicating if target is a domain
        """
        return '.' in target and not self._is_ip_address(target)
