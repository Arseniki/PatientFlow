"""
Application principale pour l'interface graphique de la simulation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading

from src.utils.constants import COLORS
from src.core.simulator import simulate
from src.core.analytical import analytical_solution
from src.core.optimizer import optimize_servers
from src.gui.widgets import ParameterPanel, ResultsPanel
from src.gui.plots import PlotManager


class SimulationApp(tk.Tk):
    """Main application class."""
    
    def __init__(self):
        super().__init__()
        
        self.title("M/M/c/k₀ Simulation de Files d'Attente")
        self.configure(bg=COLORS["background"])
        self.geometry("1280x820")
        self.resizable(True, True)
        
        # Store simulation results
        self.simulation_result = None
        self.analytical_result = None
        self.optimization_results = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Build the user interface."""
        # Header
        header = tk.Frame(self, bg=COLORS["accent"], pady=10)
        header.pack(fill="x")
        
        tk.Label(
            header,
            text= "Simulation de Files d'Attente M/M/c/k₀",
            font=("Helvetica", 14, "bold"),
            bg=COLORS["accent"],
            fg="white"
        ).pack()
        
        tk.Label(
            header,
            text="Outil de Planification de la Capacité du Centre de Santé",
            font=("Helvetica", 9),
            bg=COLORS["accent"],
            fg="#CECBF6"
        ).pack()
        
        # Main container
        main_container = tk.Frame(self, bg=COLORS["background"])
        main_container.pack(fill="both", expand=True, padx=12, pady=10)
        
        # Left panel (parameters)
        left_panel = tk.Frame(main_container, bg=COLORS["background"], width=280)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.param_panel = ParameterPanel(left_panel, self._on_simulate)
        self.param_panel.pack(fill="x")
        
        self.results_panel = ResultsPanel(left_panel)
        self.results_panel.pack(fill="both", expand=True, pady=(8, 0))
        
        # Right panel (plots)
        right_panel = tk.Frame(main_container, bg=COLORS["background"])
        right_panel.pack(side="left", fill="both", expand=True)
        
        self.plot_manager = PlotManager(right_panel)
    
    def _on_simulate(self):
        """Handle simulation button click."""
        try:
            params = self.param_panel.get_parameters()
            
            if params["capacity"] < params["num_servers"]:
                messagebox.showerror(
                    "Invalid Parameters",
                    "La capacité du système (k₀) doit être supérieure ou égale au nombre de serveurs (c)"
                )
                return
            
            self.param_panel.set_status("Execution en cours...", COLORS["accent"])
            
            # Run simulation in separate thread
            thread = threading.Thread(
                target=self._run_simulation,
                args=(params,),
                daemon=True
            )
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _run_simulation(self, params):
        """Execute simulation in background thread."""
        try:
            # Run DES
            self.simulation_result = simulate(
                arrival_rate=params["arrival_rate"],
                service_rate=params["service_rate"],
                num_servers=params["num_servers"],
                capacity=params["capacity"],
                simulation_time=params["simulation_time"],
                seed=params["seed"]
            )
            
            # Calculate analytical solution
            self.analytical_result = analytical_solution(
                arrival_rate=params["arrival_rate"],
                service_rate=params["service_rate"],
                num_servers=params["num_servers"],
                capacity=params["capacity"]
            )
            
            # Optimize
            self.optimization_results, optimal_c = optimize_servers(
                arrival_rate=params["arrival_rate"],
                service_rate=params["service_rate"],
                capacity=params["capacity"],
                rejection_threshold=params["rejection_threshold"],
                overload_threshold=params["overload_threshold"]
            )
            
            # Update UI
            self.after(0, lambda: self._update_results(
                self.simulation_result,
                self.analytical_result,
                self.optimization_results,
                optimal_c,
                params
            ))
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Simulation Error", str(e)))
            self.after(0, lambda: self.param_panel.set_status("Error", COLORS["danger"]))
    
    def _update_results(self, des, ana, opt, optimal_c, params):
        """Update UI with simulation results."""
        # Update text results
        self.results_panel.update_results(des, ana, optimal_c)
        
        # Update plots
        self.plot_manager.update_plots(
            des, ana, opt, optimal_c,
            params["arrival_rate"],
            params["service_rate"],
            params["num_servers"],
            params["capacity"],
            params["simulation_time"]
        )
        
        # Update status
        self.param_panel.set_status(
            f"Terminé — c* = {optimal_c} | Wq = {des['avg_wait_time']*60:.1f} min",
            COLORS["accent2"]
        )