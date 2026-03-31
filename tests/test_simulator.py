"""
Unit tests for the simulation engine.
"""

import unittest
from src.core.simulator import simulate


class TestSimulator(unittest.TestCase):
    
    def test_basic_simulation(self):
        """Test basic simulation with deterministic seed."""
        result = simulate(
            arrival_rate=8.0,
            service_rate=3.0,
            num_servers=3,
            capacity=12,
            simulation_time=100.0,
            seed=42
        )
        
        self.assertGreater(result["arrivals"], 0)
        self.assertGreaterEqual(result["served"], 0)
        self.assertGreaterEqual(result["rejections"], 0)
        self.assertEqual(
            result["arrivals"],
            result["served"] + result["rejections"]
        )
    
    def test_zero_capacity(self):
        """Test simulation with zero capacity."""
        result = simulate(
            arrival_rate=8.0,
            service_rate=3.0,
            num_servers=1,
            capacity=0,
            simulation_time=10.0,
            seed=42
        )
        
        self.assertEqual(result["rejections"], result["arrivals"])
        self.assertEqual(result["served"], 0)
    
    def test_infinite_capacity(self):
        """Test simulation with large capacity."""
        result = simulate(
            arrival_rate=8.0,
            service_rate=3.0,
            num_servers=3,
            capacity=1000,
            simulation_time=100.0,
            seed=42
        )
        
        self.assertEqual(result["rejections"], 0)
        self.assertGreater(result["served"], 0)


if __name__ == "__main__":
    unittest.main()