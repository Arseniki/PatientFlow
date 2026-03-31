"""
Optimisation des paramètres du système de files d'attente M/M/c/k₀.
"""

from typing import List, Dict, Any, Tuple
from .analytical import analytical_solution


def optimize_servers(
    arrival_rate: float,
    service_rate: float,
    capacity: int,
    rejection_threshold: float = 0.05,
    overload_threshold: float = 0.20,
    max_servers: int = 20
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Trouver le nombre optimal de serveurs satisfaisant les deux contraintes.
    Find optimal number of servers satisfying both constraints.
    
    Args:
        arrival_rate: λ - taux d'arrivée (patients/heure)
        service_rate: μ - taux de service (patients/heure)
        capacity: k₀ - capacité du système
        rejection_threshold: Probabilité de rejet maximale autorisée
        overload_threshold: Probabilité de surcharge maximale autorisée
        max_servers: Nombre maximum de serveurs à considérer

    Returns:
        Tuple de (liste des résultats pour chaque c, c* optimal)
    """
    
    results = []
    optimal_c = None
    
    for c in range(1, max_servers + 1):
        # Ensure capacity >= servers
        k = max(capacity, c)
        
        res = analytical_solution(arrival_rate, service_rate, c, k)
        res["c"] = c
        
        results.append(res)
        
        if optimal_c is None:
            if (res["rejection_probability"] < rejection_threshold and
                res["overload_probability"] < overload_threshold):
                optimal_c = c
    
    if optimal_c is None:
        optimal_c = max_servers
    
    return results, optimal_c