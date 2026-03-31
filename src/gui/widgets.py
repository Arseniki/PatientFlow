"""
Custom GUI widgets for parameter input and results display.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable

from src.utils.constants import COLORS


class ParameterPanel(tk.LabelFrame):
    """Panel for simulation parameters."""
    
    def __init__(self, parent, on_simulate: Callable):
        super().__init__(
            parent,
            text=" Paramètres ",
            font=("Helvetica", 10, "bold"),
            bg=COLORS["background"],
            fg=COLORS["accent"],
            relief="flat",
            bd=1,
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        
        self.on_simulate = on_simulate
        self._create_widgets()
    
    def _create_widgets(self):
        """Create parameter input widgets."""
        # Parameters
        self.arrival_rate = self._add_parameter("λ (arrivées/h)", 8.0, 0, 0.1, 100)
        self.service_rate = self._add_parameter("μ (services/h)", 3.0, 1, 0.1, 100)
        self.num_servers = self._add_int_parameter("c (serveurs)", 3, 2, 1, 50)
        self.capacity = self._add_int_parameter("k₀ (capacité)", 12, 3, 1, 200)
        self.simulation_time = self._add_parameter("T (heures)", 200.0, 4, 10, 5000, 10)
        self.seed = self._add_int_parameter("Graine aléatoire", 42, 5, 0, 9999)
        
        # Separator
        sep = tk.Frame(self, bg=COLORS["border"], height=1)
        sep.grid(row=6, column=0, columnspan=2, sticky="ew", padx=8, pady=6)
        
        # Optimization thresholds
        tk.Label(
            self,
            text="Seuil d'optimisation",
            font=("Helvetica", 9, "italic"),
            bg=COLORS["background"],
            fg=COLORS["text_secondary"]
        ).grid(row=7, column=0, columnspan=2, padx=8, sticky="w")
        
        self.rejection_threshold = self._add_parameter(
            "Seuil P(rejet)", 0.05, 8, 0.01, 1.0, 0.01
        )
        self.overload_threshold = self._add_parameter(
            "Seuil P(surcharge)", 0.20, 9, 0.01, 1.0, 0.01
        )
        
        # Buttons
        btn_frame = tk.Frame(self, bg=COLORS["background"])
        btn_frame.grid(row=10, column=0, columnspan=2, pady=10, padx=8, sticky="ew")
        
        tk.Button(
            btn_frame,
            text="▶ Simuler",
            font=("Helvetica", 10, "bold"),
            bg=COLORS["accent"],
            fg="white",
            activebackground="#3C3489",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.on_simulate
        ).pack(fill="x", pady=(0, 4))
        
        tk.Button(
            btn_frame,
            text="⟳ Réinitialiser",
            font=("Helvetica", 9),
            bg=COLORS["border"],
            fg=COLORS["text"],
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._reset
        ).pack(fill="x")
        
        # Status label
        self.status_label = tk.Label(
            self,
            text="Prêt",
            font=("Helvetica", 9, "italic"),
            bg=COLORS["background"],
            fg=COLORS["text_secondary"]
        )
        self.status_label.grid(row=11, column=0, columnspan=2, pady=(0, 6))
    
    def _add_parameter(self, label: str, default: float, row: int,
                       min_val: float, max_val: float, step: float = 0.1):
        """Add a float parameter with spinbox."""
        tk.Label(
            self,
            text=label,
            font=("Helvetica", 10),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        
        var = tk.DoubleVar(value=default)
        spin = ttk.Spinbox(
            self,
            from_=min_val,
            to=max_val,
            increment=step,
            textvariable=var,
            width=8,
            font=("Helvetica", 10)
        )
        spin.grid(row=row, column=1, padx=8, pady=4, sticky="w")
        
        return var
    
    def _add_int_parameter(self, label: str, default: int, row: int,
                           min_val: int, max_val: int):
        """Add an integer parameter with spinbox."""
        tk.Label(
            self,
            text=label,
            font=("Helvetica", 10),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        
        var = tk.IntVar(value=default)
        spin = ttk.Spinbox(
            self,
            from_=min_val,
            to=max_val,
            increment=1,
            textvariable=var,
            width=8,
            font=("Helvetica", 10)
        )
        spin.grid(row=row, column=1, padx=8, pady=4, sticky="w")
        
        return var
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get current parameter values."""
        return {
            "arrival_rate": self.arrival_rate.get(),
            "service_rate": self.service_rate.get(),
            "num_servers": self.num_servers.get(),
            "capacity": self.capacity.get(),
            "simulation_time": self.simulation_time.get(),
            "seed": self.seed.get(),
            "rejection_threshold": self.rejection_threshold.get(),
            "overload_threshold": self.overload_threshold.get(),
        }
    
    def set_status(self, message: str, color: str):
        """Update status message."""
        self.status_label.config(text=message, fg=color)
    
    def _reset(self):
        """Reset all parameters to defaults."""
        self.arrival_rate.set(8.0)
        self.service_rate.set(3.0)
        self.num_servers.set(3)
        self.capacity.set(12)
        self.simulation_time.set(200.0)
        self.seed.set(42)
        self.rejection_threshold.set(0.05)
        self.overload_threshold.set(0.20)
        self.set_status("Réinitialisé à leurs valeurs par défaut", COLORS["text_secondary"])


class ResultsPanel(tk.LabelFrame):
    """Panel for displaying simulation results."""
    
    def __init__(self, parent):
        super().__init__(
            parent,
            text=" Résultats ",
            font=("Helvetica", 10, "bold"),
            bg=COLORS["panel"],
            fg=COLORS["accent2"],
            relief="flat",
            bd=1,
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create result display widgets."""
        # DES section
        tk.Label(
            self,
            text="── DES ──",
            font=("Helvetica", 9, "bold"),
            bg=COLORS["panel"],
            fg=COLORS["accent2"]
        ).grid(row=0, column=0, columnspan=2, pady=(8, 2))
        
        des_metrics = [
            ("Patients arrivés", "arrivals", None),
            ("Patients rejetés", "rejections", COLORS["danger"]),
            ("P(rejet)", "rejection_probability", COLORS["danger"]),
            ("P(surcharge)", "overload_probability", COLORS["warning"]),
            ("Utilisation ρ", "utilization", None),
            ("Wq (temps d'attente)", "avg_wait_time", None),
            ("W (temps du système)", "avg_system_time", None),
            ("Lq (longueur de la file d'attente)", "avg_queue_length", None),
            ("L (taille du système)", "avg_system_size", None),
        ]
        
        self.des_labels = {}
        for i, (label, key, color) in enumerate(des_metrics, start=1):
            self._add_result_label(label, key, i, color)
        
        # Separator
        sep = tk.Frame(self, bg=COLORS["border"], height=1)
        sep.grid(row=len(des_metrics) + 1, column=0, columnspan=2, sticky="ew", padx=8, pady=4)
        
        # Analytical section
        tk.Label(
            self,
            text="── Analytical (Steady-state) ──",
            font=("Helvetica", 9, "bold"),
            bg=COLORS["panel"],
            fg=COLORS["accent"]
        ).grid(row=len(des_metrics) + 2, column=0, columnspan=2, pady=(2, 2))
        
        analytical_metrics = [
            ("P(rejection)", "rejection_probability", COLORS["danger"]),
            ("P(overload)", "overload_probability", COLORS["warning"]),
            ("Wq (queue time)", "avg_wait_time", None),
            ("W (system time)", "avg_system_time", None),
            ("Lq (queue length)", "avg_queue_length", None),
        ]
        
        self.analytical_labels = {}
        base_row = len(des_metrics) + 3
        for i, (label, key, color) in enumerate(analytical_metrics):
            self._add_result_label(label, key, base_row + i, color, is_analytical=True)
        
        # Separator
        sep2 = tk.Frame(self, bg=COLORS["border"], height=1)
        sep2.grid(row=base_row + len(analytical_metrics), column=0, columnspan=2, sticky="ew", padx=8, pady=4)
        
        # Optimal c*
        self._add_result_label("c* optimal", "optimal_c", base_row + len(analytical_metrics) + 1, COLORS["cstar"])
    
    def _add_result_label(self, label: str, key: str, row: int, color: str = None, is_analytical: bool = False):
        """Add a labeled result display."""
        tk.Label(
            self,
            text=label,
            font=("Helvetica", 10),
            bg=COLORS["panel"],
            fg=COLORS["text_secondary"]
        ).grid(row=row, column=0, sticky="w", padx=(12, 4), pady=2)
        
        lbl = tk.Label(
            self,
            text="—",
            font=("Helvetica", 10, "bold"),
            bg=COLORS["panel"],
            fg=color or COLORS["text"]
        )
        lbl.grid(row=row, column=1, sticky="w", padx=(0, 12), pady=2)
        
        if is_analytical:
            self.analytical_labels[key] = lbl
        else:
            self.des_labels[key] = lbl
    
    def update_results(self, des: Dict, ana: Dict, optimal_c: int):
        """Update result displays with new data."""
        # Format DES results
        des_formatted = {
            "arrivals": str(des["arrivals"]),
            "rejections": str(des["rejections"]),
            "rejection_probability": f"{des['rejection_probability']:.2%}",
            "overload_probability": f"{des['overload_probability']:.2%}",
            "utilization": f"{des['utilization']:.4f}",
            "avg_wait_time": f"{des['avg_wait_time']*60:.2f} min",
            "avg_system_time": f"{des['avg_system_time']*60:.2f} min",
            "avg_queue_length": f"{des['avg_queue_length']:.3f}",
            "avg_system_size": f"{des['avg_system_size']:.3f}",
        }
        
        for key, label in self.des_labels.items():
            label.config(text=des_formatted.get(key, "—"))
        
        # Format analytical results
        ana_formatted = {
            "rejection_probability": f"{ana['rejection_probability']:.2%}",
            "overload_probability": f"{ana['overload_probability']:.2%}",
            "avg_wait_time": f"{ana['avg_wait_time']*60:.2f} min",
            "avg_system_time": f"{ana['avg_system_time']*60:.2f} min",
            "avg_queue_length": f"{ana['avg_queue_length']:.3f}",
        }
        
        for key, label in self.analytical_labels.items():
            if key != "optimal_c":
                label.config(text=ana_formatted.get(key, "—"))
            else:
                label.config(text=str(optimal_c))