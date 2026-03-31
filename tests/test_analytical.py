"""
Unit tests for analytical solution.
"""

import unittest
from src.core.analytical import analytical_solution


class TestAnalytical(unittest.TestCase):
    
    def test_basic_analytical(self):
        """Test basic analytical calculation."""
        result = analytical_solution(
            arrival_rate=8.0,
            service_rate=3.0,
            num_servers=3,
            capacity=12
        )
        
        self.assertAlmostEqual(sum(result["Pn"]), 1.0, places=5)
        self.assertGreater(result["rejection_probability"], 0)
        self.assertGreater(result["overload_probability"], 0)
    
    def test_zero_load(self):
        """Test zero arrival rate."""
        result = analytical_solution(
            arrival_rate=0.0,
            service_rate=3.0,
            num_servers=3,
            capacity=12
        )
        
        self.assertEqual(result["Pn"][0], 1.0)
        self.assertEqual(result["rejection_probability"], 0.0)
    
    def test_high_load(self):
        """Test high arrival rate."""
        result = analytical_solution(
            arrival_rate=100.0,
            service_rate=3.0,
            num_servers=10,
            capacity=20
        )
        
        self.assertGreater(result["rejection_probability"], 0.5)


if __name__ == "__main__":
    unittest.main()