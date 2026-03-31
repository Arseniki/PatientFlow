"""
Analytical solution for M/M/c/k₀ queue (steady-state).
"""

import math
from typing import Dict, Any


def analytical_solution(
    arrival_rate: float,
    service_rate: float,
    num_servers: int,
    capacity: int
) -> Dict[str, Any]:
    """
    Compute steady-state analytical solution for M/M/c/k₀ queue.
    
    Args:
        arrival_rate: λ - taux d'arrivée (patients/heure)
        service_rate: μ - taux de service (patients/heure)
        num_servers: c - nombre de serveurs
        capacity: k₀ - capacité du système (y compris le service)
        
    Returns:
        Dictionnaire avec les résultats analytiques incluant la distribution P(n)
    """
    
    if capacity < num_servers:
        raise ValueError("la capacité du système doit être >= au nombre de serveurs")
    
    rho = arrival_rate / (num_servers * service_rate)
    traffic_intensity = arrival_rate / service_rate
    
    # Calculate normalization constant P0
    # Sum from n=0 to c
    sum_terms = sum(
        (traffic_intensity ** n) / math.factorial(n)
        for n in range(num_servers + 1)
    )
    
    # Sum from n=c+1 to capacity
    sum_terms += sum(
        (traffic_intensity ** n) / (math.factorial(num_servers) * (num_servers ** (n - num_servers)))
        for n in range(num_servers + 1, capacity + 1)
    )
    
    P0 = 1.0 / sum_terms
    
    # Calculate steady-state probabilities
    Pn = []
    for n in range(capacity + 1):
        if n <= num_servers:
            prob = P0 * (traffic_intensity ** n) / math.factorial(n)
        else:
            prob = P0 * (traffic_intensity ** n) / (math.factorial(num_servers) * (num_servers ** (n - num_servers)))
        Pn.append(prob)
    
    # Calculate performance metrics
    rejection_prob = Pn[capacity]
    overload_prob = sum(Pn[n] for n in range(num_servers, capacity + 1))
    
    avg_queue_length = sum((n - num_servers) * Pn[n] for n in range(num_servers + 1, capacity + 1))
    
    effective_arrival_rate = arrival_rate * (1 - rejection_prob)
    
    avg_wait_time = avg_queue_length / effective_arrival_rate if effective_arrival_rate > 0 else 0.0
    avg_system_time = avg_wait_time + 1.0 / service_rate
    avg_system_size = effective_arrival_rate * avg_system_time
    
    return {
        "rho": rho,
        "P0": P0,
        "Pn": Pn,
        "rejection_probability": rejection_prob,
        "overload_probability": overload_prob,
        "avg_queue_length": avg_queue_length,
        "effective_arrival_rate": effective_arrival_rate,
        "avg_wait_time": avg_wait_time,
        "avg_system_time": avg_system_time,
        "avg_system_size": avg_system_size,
    }