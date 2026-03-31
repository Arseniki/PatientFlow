"""
Point d'entrée principal pour l'application de Simulation d'Événements Discrets.
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from src.gui.app import SimulationApp


def main():
    """Main application entry point."""
    try:
        app = SimulationApp()
        app.mainloop()
    except Exception as e:
        print(f"Erreur lors du démarrage de l'application: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()