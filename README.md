# M/M/c/k₀ Simulation des files d'attente

## Simulation à Evènement Discret pour les centres de santé

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un outil professionnel de Simulation à Evènement Discret (DES) pour l'analyse de M/M/c/k₀ des systèmes de file d'attente avec une interface graphique. Parfait pour la planification de la capacité et l'optimisation des centres de santé. 


## Fonctionnalités

- **Simulation à Evènement Discret** de M/M/c/k₀ queues
- **Solution analytique** pour une comparaison en régime stationnaire
- **Optimisation** Pour trouver le nombre optimal de serveurs (c*)
- **Visualisation temps réel** avec matplotlib
- **Une interface utilisateur graphique Professionnelle** conçue avec Tkinter
- **Paramètres configurable** (taux d'arrivée, taux de service, capacité.)
- **Métriques multiples** (Wq, Lq, P(rejet), P(surcharge).)

## Les interfaces
![Screenshot](./interfaces/interface_vue_d_ensemble.png)
![Screenshot](./interfaces/interface_evolution_temporelle.png)
![Screenshot](./interfaces/interface_distribution_pn.png)
![Screenshot](./interfaces/interface_optimisation.png)

## Installation


```bash
# Cloner le répositori
git clone https://github.com/Arseniki/PatientFlow.git
cd PATIENTFLOW

# Installer les dépendances
pip install -r requirements.txt

# Exécuter l'application
python src/main.py
