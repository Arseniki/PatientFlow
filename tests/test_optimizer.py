"""
Unit tests for optimization module.
"""

import unittest
from src.core.optimizer import optimize_servers


class TestOptimizer(unittest.TestCase):
    
    def test_optimization(self):
        """Test server optimization."""
        results, optimal_c = optimize_servers(
            arrival_rate=8.0,
            service_rate=3.0,
            capacity=12,
            rejection_threshold=0.05,
            overload_threshold=0.20,
            max_servers=10
        )
        
        self.assertIsInstance(optimal_c, int)
        self.assertGreaterEqual(optimal_c, 1)
        self.assertLessEqual(optimal_c, 10)
        self.assertEqual(len(results), 10)
    
    def test_optimization_high_demand(self):
        """Test optimization with high demand."""
        results, optimal_c = optimize_servers(
            arrival_rate=50.0,
            service_rate=3.0,
            capacity=50,
            rejection_threshold=0.05,
            overload_threshold=0.20,
            max_servers=20
        )
        
        self.assertEqual(optimal_c, 20)  # Should hit max


if __name__ == "__main__":
    unittest.main()