"""
Basic tests for BAT Scanner infrastructure.
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bat_scanner.core.scanner import ScannerEngine
from bat_scanner.modules.port_scanner import PortScanner
from bat_scanner.modules.vulnerability_scanner import VulnerabilityScanner
from bat_scanner.modules.threat_intelligence import ThreatIntelligence
from bat_scanner.modules.exploit_db import ExploitDatabase


class TestScannerInfrastructure(unittest.TestCase):
    """Test the basic infrastructure of BAT Scanner."""
    
    def test_scanner_engine_initialization(self):
        """Test that scanner engine can be initialized."""
        engine = ScannerEngine()
        self.assertIsNotNone(engine)
        self.assertEqual(len(engine.modules), 0)
        
    def test_module_registration(self):
        """Test that modules can be registered."""
        engine = ScannerEngine()
        module = PortScanner()
        engine.register_module(module)
        self.assertEqual(len(engine.modules), 1)
        
    def test_port_scanner_module(self):
        """Test port scanner module initialization."""
        scanner = PortScanner()
        self.assertIsNotNone(scanner)
        self.assertTrue(scanner.quick_scan)
        
    def test_vulnerability_scanner_module(self):
        """Test vulnerability scanner module initialization."""
        scanner = VulnerabilityScanner()
        self.assertIsNotNone(scanner)
        self.assertFalse(scanner.quick_scan)
        
    def test_threat_intelligence_module(self):
        """Test threat intelligence module initialization."""
        scanner = ThreatIntelligence()
        self.assertIsNotNone(scanner)
        self.assertTrue(scanner.quick_scan)
        
    def test_exploit_database_module(self):
        """Test exploit database module initialization."""
        scanner = ExploitDatabase()
        self.assertIsNotNone(scanner)
        self.assertFalse(scanner.quick_scan)
        
    def test_exploit_search(self):
        """Test exploit database search functionality."""
        exploit_db = ExploitDatabase()
        results = exploit_db.scan("log4j")
        self.assertIn("findings", results)
        self.assertGreater(len(results["findings"]), 0)
        
    def test_target_validation(self):
        """Test target validation."""
        scanner = PortScanner()
        self.assertTrue(scanner.validate_target("192.168.1.1"))
        self.assertTrue(scanner.validate_target("example.com"))
        self.assertFalse(scanner.validate_target(""))
        self.assertFalse(scanner.validate_target("   "))
        
    def test_scan_execution(self):
        """Test basic scan execution."""
        engine = ScannerEngine()
        module = ThreatIntelligence()
        engine.register_module(module)
        
        # Use a test target
        results = engine.start_scan("192.0.2.1", "quick")
        
        self.assertIn("scan_id", results)
        self.assertIn("target", results)
        self.assertIn("findings", results)
        self.assertEqual(results["target"], "192.0.2.1")


if __name__ == "__main__":
    unittest.main()
