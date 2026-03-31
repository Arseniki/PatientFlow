"""
Simulation des files d'attente M/M/c/k₀.
"""

import math
import random
import heapq
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass(order=True)
class Event:
    """Simulation event representation."""
    time: float
    type: str = field(compare=False)
    server: Optional[int] = field(default=None, compare=False)


def _exponential(rate: float) -> float:
    """Generate exponential random variable."""
    if rate <= 0:
        return float('inf')
    return -math.log(1.0 - random.random()) / rate


def simulate(
    arrival_rate: float,
    service_rate: float,
    num_servers: int,
    capacity: int,
    simulation_time: float,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Run discrete event simulation for M/M/c/k₀ queue.
    
    Args:
        arrival_rate: λ - taux d'arrivée (patients/heure)
        service_rate: μ - taux de service (patients/heure)
        num_servers: c - nombre de serveurs
        capacity: k₀ - capacité du système (y compris le service)
        simulation_time: T - durée de la simulation (heures)
        seed: Graine aléatoire pour la reproductibilité
        
    Returns:
        Dictionnaire avec les résultats de la simulation et l'historique
    """
    
    if seed is not None:
        random.seed(seed)
    
    # State variables
    time = 0.0
    system_size = 0
    queue = []  # Arrival times for waiting patients
    server_free_times = [float('inf')] * num_servers
    event_list = []
    
    # Statistics
    arrivals = 0
    rejections = 0
    served = 0
    total_wait_time = 0.0
    total_queue_length = 0.0
    overload_time = 0.0
    previous_time = 0.0
    
    # History
    system_history = []  # (time, size)
    wait_times = []  # Waiting times in minutes
    
    # Initial event
    heapq.heappush(event_list, Event(_exponential(arrival_rate), "ARRIVAL"))
    
    while event_list:
        event = heapq.heappop(event_list)
        
        if event.time > simulation_time:
            break
        
        # Update statistics
        delta = event.time - previous_time
        total_queue_length += len(queue) * delta
        
        if system_size > capacity:
            overload_time += delta
        
        previous_time = event.time
        time = event.time
        system_history.append((time, system_size))
        
        if event.type == "ARRIVAL":
            arrivals += 1
            
            if system_size < capacity:
                system_size += 1
                
                # Find free server
                free_server = next(
                    (i for i in range(num_servers) if server_free_times[i] == float('inf')),
                    None
                )
                
                if free_server is not None:
                    # Start service immediately
                    service_time = _exponential(service_rate)
                    server_free_times[free_server] = time + service_time
                    heapq.heappush(
                        event_list,
                        Event(time + service_time, "DEPARTURE", free_server)
                    )
                else:
                    # Join queue
                    queue.append(time)
            else:
                rejections += 1
            
            # Schedule next arrival
            heapq.heappush(
                event_list,
                Event(time + _exponential(arrival_rate), "ARRIVAL")
            )
            
        elif event.type == "DEPARTURE":
            server_id = event.server
            system_size -= 1
            server_free_times[server_id] = float('inf')
            served += 1
            
            if queue:
                # Serve next waiting patient
                arrival_time = queue.pop(0)
                wait_time = time - arrival_time
                total_wait_time += wait_time
                wait_times.append(wait_time * 60)  # Convert to minutes
                
                service_time = _exponential(service_rate)
                server_free_times[server_id] = time + service_time
                heapq.heappush(
                    event_list,
                    Event(time + service_time, "DEPARTURE", server_id)
                )
    
    # Calculate performance metrics
    effective_arrival_rate = served / simulation_time if simulation_time > 0 else 0.0
    avg_wait_time = total_wait_time / served if served > 0 else 0.0
    avg_queue_length = total_queue_length / simulation_time if simulation_time > 0 else 0.0
    avg_system_time = avg_wait_time + 1.0 / service_rate
    avg_system_size = effective_arrival_rate * avg_system_time
    utilization = effective_arrival_rate / (num_servers * service_rate) if num_servers * service_rate > 0 else float('inf')
    rejection_prob = rejections / arrivals if arrivals > 0 else 0.0
    overload_prob = overload_time / simulation_time if simulation_time > 0 else 0.0
    
    return {
        "arrivals": arrivals,
        "rejections": rejections,
        "served": served,
        "effective_arrival_rate": effective_arrival_rate,
        "avg_wait_time": avg_wait_time,
        "avg_queue_length": avg_queue_length,
        "avg_system_time": avg_system_time,
        "avg_system_size": avg_system_size,
        "utilization": utilization,
        "rejection_probability": rejection_prob,
        "overload_probability": overload_prob,
        "system_history": system_history,
        "wait_times": wait_times,
        "rejection_threshold": None,  # Not applicable for simulation
        "overload_threshold": None,
    }
