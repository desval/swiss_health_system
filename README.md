# Swiss Health System Simulation Project

This repository contains a small research project on the Swiss mandatory health insurance system (OKP) and the role of risk equalization (`Risikoausgleich`) in insurer solvency.

The current codebase combines:

- a Python simulation of insurer risk pools under three phases of the Swiss risk adjustment formula;
- paper drafts that explain the institutional background, economic model, and simulation results;
- referee-style guidance for developing the paper into a tighter research narrative.

## Project Scope

The project studies how progressively richer risk adjustment affects insurer financial outcomes under community rating and open enrollment.

The simulation in [code/simulation.py](code/simulation.py) models three policy phases:

1. Phase 1: age and sex only.
2. Phase 2: age, sex, and prior hospitalization.
3. Phase 3: age, sex, prior hospitalization, and 22 pharmaceutical cost groups (PCGs).

It generates synthetic insured populations, simulates realized costs, assigns individuals to insurers under varying degrees of adverse selection, and produces figures for loss ratios, expense ratios, and combined ratios.

## Repository Layout

- [code/](code/) contains the simulation code.
- [output/figures/](output/figures/) contains generated charts from simulation runs.
- [paper/](paper/) contains project notes and draft paper sections.
- [requirements.txt](requirements.txt) lists the Python packages needed to run the simulation.

## Setup

Do not commit a virtual environment directory. Create it locally and install the dependencies from [requirements.txt](requirements.txt).

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run The Simulation

From the repository root:

```powershell
python code/simulation.py
```

The script writes figures to [output/figures/](output/figures/).

## Reproducibility Notes

- Commit [requirements.txt](requirements.txt) so collaborators can install the same dependency set.
- Keep `.venv/`, `venv/`, and similar local environment folders out of Git.
- Keep local Claude settings such as `.claude/settings.local.json` out of Git.
