"""
Plot management for simulation visualization.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.utils.constants import COLORS, PLOT_COLORS


class PlotManager:
    """Manage all simulation plots."""
    
    def __init__(self, parent):
        self.parent = parent
        self._create_notebook()
    
    def _create_notebook(self):
        """Create notebook with plot tabs."""
        style = ttk.Style()
        style.configure("TNotebook", background=COLORS["background"])
        style.configure("TNotebook.Tab", font=("Helvetica", 9))
        
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill="both", expand=True)
        
        # Create tabs
        self.tab1 = tk.Frame(self.notebook, bg=COLORS["background"])
        self.tab2 = tk.Frame(self.notebook, bg=COLORS["background"])
        self.tab3 = tk.Frame(self.notebook, bg=COLORS["background"])
        self.tab4 = tk.Frame(self.notebook, bg=COLORS["background"])
        
        self.notebook.add(self.tab1, text=" Vue d'ensemble ")
        self.notebook.add(self.tab2, text=" Évolution Temporelle ")
        self.notebook.add(self.tab3, text=" Distribution Stationnaire ")
        self.notebook.add(self.tab4, text=" Optimisation ")
        
        # Create figures
        self.fig1, self.canvas1 = self._create_figure(self.tab1, (9, 6))
        self.fig2, self.canvas2 = self._create_figure(self.tab2, (9, 5))
        self.fig3, self.canvas3 = self._create_figure(self.tab3, (9, 5))
        self.fig4, self.canvas4 = self._create_figure(self.tab4, (9, 5))
    
    def _create_figure(self, parent, figsize):
        """Create a matplotlib figure and canvas."""
        fig = plt.Figure(figsize=figsize, facecolor=COLORS["background"])
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)
        return fig, canvas
    
    def update_plots(self, des, ana, opt, optimal_c, arrival_rate, service_rate, num_servers, capacity, simulation_time):
        """Update all plots with new data."""
        self._plot_overview(des, ana)
        self._plot_temporal(des, capacity, num_servers, simulation_time)
        self._plot_distribution(ana, num_servers, capacity, arrival_rate, service_rate)
        self._plot_optimization(opt, optimal_c)
    
    def _plot_overview(self, des, ana):
        """Plot DES vs Analytique comparaison."""
        self.fig1.clf()
        gs = gridspec.GridSpec(2, 2, figure=self.fig1, hspace=0.45, wspace=0.35)
        
        metrics = {
            "Wq (min)": (des["avg_wait_time"]*60, ana["avg_wait_time"]*60),
            "Lq (patients)": (des["avg_queue_length"], ana["avg_queue_length"]),
            "W total (min)": (des["avg_system_time"]*60, ana["avg_system_time"]*60),
            "P(rejet)": (des["rejection_probability"], ana["rejection_probability"]),
        }
        
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        
        for (metric, (val_des, val_ana)), pos in zip(metrics.items(), positions):
            ax = self.fig1.add_subplot(gs[pos])
            bars = ax.bar(
                ["DES", "Analytique"],
                [val_des, val_ana],
                color=[PLOT_COLORS["des"], PLOT_COLORS["analytical"]],
                width=0.5,
                edgecolor="white",
                linewidth=0.5
            )
            
            # Add value labels
            for bar, val in zip(bars, [val_des, val_ana]):
                ax.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height() + max(val_des, val_ana) * 0.02,
                    f"{val:.2f}" if metric != "P(rejection)" else f"{val:.2%}",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    fontweight="bold"
                )
            
            ax.set_title(metric, fontsize=9, fontweight="bold", color=COLORS["text"])
            ax.set_facecolor(COLORS["background"])
            ax.grid(axis="y", color=PLOT_COLORS["grid"], linewidth=0.7)
            ax.spines[["top", "right", "left"]].set_visible(False)
            ax.tick_params(labelsize=8)
            ax.set_ylim(bottom=0, top=max(val_des, val_ana) * 1.25 or 0.1)
            
            if metric == "P(rejection)":
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
        
        self.fig1.suptitle(
            "DES vs Analytique — Vue d'ensemble",
            fontsize=11,
            fontweight="bold",
            color=COLORS["text"]
        )
        self.canvas1.draw()
    
    def _plot_temporal(self, des, capacity, num_servers, simulation_time):
        """Plot temporal evolution and Wq distribution."""
        self.fig2.clf()
        gs = gridspec.GridSpec(1, 2, figure=self.fig2, wspace=0.35)
        
        # Evolution plot
        ax1 = self.fig2.add_subplot(gs[0, 0])
        if des["system_history"]:
            times, sizes = zip(*des["system_history"])
            ax1.step(times, sizes, where="post", color=PLOT_COLORS["des"],
                    linewidth=1, alpha=0.8)
            ax1.axhline(capacity, color=PLOT_COLORS["rejection"],
                       linestyle="--", linewidth=1.2, label=f"k₀ = {capacity}")
            ax1.axhline(num_servers, color=PLOT_COLORS["overload"],
                       linestyle=":", linewidth=1.2, label=f"c = {num_servers}")
            ax1.fill_between(times, sizes, alpha=0.08, color=PLOT_COLORS["des"], step="post")
        
        ax1.set_xlabel("Temps (heures)", fontsize=9)
        ax1.set_ylabel("Nombre de patients", fontsize=9)
        ax1.set_title("Évolution de N(t)", fontsize=10, fontweight="bold")
        ax1.legend(fontsize=8)
        ax1.set_facecolor(COLORS["background"])
        ax1.grid(color=PLOT_COLORS["grid"], linewidth=0.5)
        ax1.spines[["top", "right"]].set_visible(False)
        ax1.set_xlim(0, simulation_time)
        
        # Histogram plot
        ax2 = self.fig2.add_subplot(gs[0, 1])
        wait_times = des["wait_times"]
        if wait_times:
            ax2.hist(wait_times, bins=30, color=PLOT_COLORS["analytical"],
                    edgecolor="white", linewidth=0.5, alpha=0.85)
            ax2.axvline(np.mean(wait_times), color=PLOT_COLORS["rejection"],
                       linestyle="--", linewidth=1.5,
                       label=f"Mean = {np.mean(wait_times):.1f} min")
        
        ax2.set_xlabel("Temps d'attente Wq (minutes)", fontsize=9)
        ax2.set_ylabel("Fréquence", fontsize=9)
        ax2.set_title("Distribution de Wq", fontsize=10, fontweight="bold")
        ax2.legend(fontsize=8)
        ax2.set_facecolor(COLORS["background"])
        ax2.grid(axis="y", color=PLOT_COLORS["grid"], linewidth=0.5)
        ax2.spines[["top", "right"]].set_visible(False)
        
        self.fig2.suptitle(
            "Analyse Temporelle",
            fontsize=11,
            fontweight="bold",
            color=COLORS["text"]
        )
        self.canvas2.draw()
    
    def _plot_distribution(self, ana, num_servers, capacity, arrival_rate, service_rate):
        """Plot stationary distribution P(n)."""
        self.fig3.clf()
        ax = self.fig3.add_subplot(111)
        
        Pn = ana["Pn"]
        ns = list(range(capacity + 1))
        
        # Color code bars
        colors = []
        for n in ns:
            if n == capacity:
                colors.append(PLOT_COLORS["rejection"])
            elif n >= num_servers:
                colors.append(PLOT_COLORS["overload"])
            else:
                colors.append(PLOT_COLORS["des"])
        
        ax.bar(ns, Pn, color=colors, edgecolor="white", linewidth=0.5)
        ax.axvline(num_servers - 0.5, color=PLOT_COLORS["analytical"],
                  linestyle="--", linewidth=1.5, label=f"c = {num_servers}")
        ax.axvline(capacity + 0.4, color=PLOT_COLORS["rejection"],
                  linestyle=":", linewidth=1.5, label=f"k₀ = {capacity}")
        
        # Legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(color=PLOT_COLORS["des"], label="Service normal (n < c)"),
            Patch(color=PLOT_COLORS["overload"], label="File non vide (c ≤ n < k₀)"),
            Patch(color=PLOT_COLORS["rejection"], label=f"Rejet (n = k₀ = {capacity})"),
        ]
        ax.legend(handles=legend_elements, fontsize=8)
        
        ax.set_xlabel("Nombre de patients n", fontsize=9)
        ax.set_ylabel("P(n)", fontsize=9)
        ax.set_title(
            f"Distribution Stationnaire — M/M/{num_servers}/{capacity}  λ={arrival_rate}, μ={service_rate}",
            fontsize=10,
            fontweight="bold",
            color=COLORS["text"]
        )
        ax.set_facecolor(COLORS["background"])
        ax.grid(axis="y", color=PLOT_COLORS["grid"], linewidth=0.5)
        ax.spines[["top", "right"]].set_visible(False)
        
        self.canvas3.draw()
    
    def _plot_optimization(self, opt, optimal_c):
        """Plot optimization results."""
        self.fig4.clf()
        gs = gridspec.GridSpec(1, 2, figure=self.fig4, wspace=0.35)
        
        cs = [r["c"] for r in opt]
        rejection_probs = [r["rejection_probability"] for r in opt]
        overload_probs = [r["overload_probability"] for r in opt]
        wait_times = [r["avg_wait_time"] * 60 for r in opt]
        
        # First subplot: probabilities
        ax1 = self.fig4.add_subplot(gs[0, 0])
        ax1.plot(cs, rejection_probs, "o-", color=PLOT_COLORS["rejection"],
                label="P(rejection)", linewidth=2, markersize=5)
        ax1.plot(cs, overload_probs, "s-", color=PLOT_COLORS["overload"],
                label="P(overload)", linewidth=2, markersize=5)
        
        ax1.axvline(optimal_c, color=PLOT_COLORS["cstar"],
                   linestyle=":", linewidth=2, label=f"c* = {optimal_c}")
        
        ax1.set_xlabel("Nombre de serveurs c", fontsize=9)
        ax1.set_ylabel("Probabilité", fontsize=9)
        ax1.set_title("P(rejet) et P(surcharge) vs c", fontsize=10, fontweight="bold")
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
        ax1.legend(fontsize=7)
        ax1.set_facecolor(COLORS["background"])
        ax1.grid(color=PLOT_COLORS["grid"], linewidth=0.5)
        ax1.spines[["top", "right"]].set_visible(False)
        ax1.set_ylim(0, 1.05)
        
        # Second subplot: waiting times
        ax2 = self.fig4.add_subplot(gs[0, 1])
        ax2.plot(cs, wait_times, "D-", color=PLOT_COLORS["analytical"],
                linewidth=2, markersize=5, label="Wq (minutes)")
        ax2.axvline(optimal_c, color=PLOT_COLORS["cstar"],
                   linestyle=":", linewidth=2, label=f"c* = {optimal_c}")
        
        ax2.set_xlabel("Nombre de serveurs c", fontsize=9)
        ax2.set_ylabel("Temps d'attente moyen (minutes)", fontsize=9)
        ax2.set_title("Temps d'attente vs c", fontsize=10, fontweight="bold")
        ax2.legend(fontsize=8)
        ax2.set_facecolor(COLORS["background"])
        ax2.grid(color=PLOT_COLORS["grid"], linewidth=0.5)
        ax2.spines[["top", "right"]].set_visible(False)
        
        self.fig4.suptitle(
            f"Optimization — Optimal c* = {optimal_c}",
            fontsize=11,
            fontweight="bold",
            color=PLOT_COLORS["cstar"]
        )
        self.canvas4.draw()