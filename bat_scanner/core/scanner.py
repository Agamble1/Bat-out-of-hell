"""
Core Scanner Engine for BAT Scanner.
Coordinates all scanning modules and manages scan lifecycle.
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime


class ScannerEngine:
    """Main scanning engine that orchestrates security assessments."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the scanner engine.
        
        Args:
            config: Configuration dictionary for the scanner
        """
        self.config = config or {}
        self.modules = []
        self.results = []
        self.logger = logging.getLogger(__name__)
        self.scan_id = None
        
    def register_module(self, module):
        """
        Register a scanning module.
        
        Args:
            module: Scanner module instance to register
        """
        self.modules.append(module)
        self.logger.info(f"Registered module: {module.__class__.__name__}")
        
    def start_scan(self, target: str, scan_type: str = "full") -> Dict[str, Any]:
        """
        Start a security scan on the target.
        
        Args:
            target: Target to scan (IP, domain, URL, etc.)
            scan_type: Type of scan to perform (quick, full, custom)
            
        Returns:
            Dictionary containing scan results
        """
        self.scan_id = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.logger.info(f"Starting {scan_type} scan on target: {target}")
        
        scan_results = {
            "scan_id": self.scan_id,
            "target": target,
            "scan_type": scan_type,
            "start_time": datetime.now().isoformat(),
            "modules_executed": [],
            "findings": []
        }
        
        for module in self.modules:
            if self._should_run_module(module, scan_type):
                self.logger.info(f"Executing module: {module.__class__.__name__}")
                try:
                    result = module.scan(target)
                    scan_results["modules_executed"].append(module.__class__.__name__)
                    if result:
                        scan_results["findings"].extend(result.get("findings", []))
                except Exception as e:
                    self.logger.error(f"Module {module.__class__.__name__} failed: {str(e)}")
                    
        scan_results["end_time"] = datetime.now().isoformat()
        scan_results["total_findings"] = len(scan_results["findings"])
        
        self.results.append(scan_results)
        self.logger.info(f"Scan completed. Found {scan_results['total_findings']} findings")
        
        return scan_results
        
    def _should_run_module(self, module, scan_type: str) -> bool:
        """
        Determine if a module should run based on scan type.
        
        Args:
            module: Module to check
            scan_type: Type of scan being performed
            
        Returns:
            Boolean indicating if module should run
        """
        if scan_type == "full":
            return True
        elif scan_type == "quick":
            return getattr(module, "quick_scan", False)
        return True
        
    def get_results(self) -> List[Dict[str, Any]]:
        """
        Get all scan results.
        
        Returns:
            List of scan result dictionaries
        """
        return self.results
