# M/M/c/k₀ Simulation des files d'attente

## Simulation à Evènement Discret pour les centres de santé

[![Python 3.13+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un outil professionnel de Simulation à Evènement Discret (DES) oour l'analyse de M/M/c/k₀ des systèmes de file d'attente avec une interface graphique. Parfait pour la planinfication de la capacité et l'optimisation des centres de santé. 


## Fonctionnalités

- **Simulation à Evènement Discret** of M/M/c/k₀ queues
- **Solution analytique** pour une comparaison à état
- **Optimisation** Pour trouver le nombre optimal de serveurs (c*)
- **Visualisation temps réels** with matplotlib
- **Professional GUI** built with Tkinter
- **Paramètres configurable** (taux d'arrivée, taux de service, capacité.)
- **Métriques multiples** (Wq, Lq, P(rejet), P(surcharge).)

## Installation

```bash
# Cloner le répositori
git clone https://github.com/yourusername/simulation-des.git
cd simulation-des

# Installer les dépendances
pip install -r requirements.txt

# Exécuter l'application
python src/main.py