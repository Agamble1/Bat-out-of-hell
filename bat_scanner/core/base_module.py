"""
Base Scanner Module.
All scanner modules should inherit from this class.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging


class BaseScannerModule(ABC):
    """Abstract base class for all scanner modules."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the scanner module.
        
        Args:
            config: Configuration dictionary for the module
        """
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.quick_scan = False
        
    @abstractmethod
    def scan(self, target: str) -> Dict[str, Any]:
        """
        Perform the scan on the target.
        
        Args:
            target: Target to scan
            
        Returns:
            Dictionary containing scan results
        """
        pass
        
    def validate_target(self, target: str) -> bool:
        """
        Validate the target before scanning.
        
        Args:
            target: Target to validate
            
        Returns:
            Boolean indicating if target is valid
        """
        if not target or target.strip() == "":
            self.logger.error("Target cannot be empty")
            return False
        return True
