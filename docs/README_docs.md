# EOIR-Simulaor--RPi
Python-based EO/IR simulator on Raspberry Pi with PTZ control and sensor-style menus (MX-15-like familiarization).

## Objectives
- Practice hardware/software integration on Linux
- Recreate ISR sensor workflows (PTZ, menus)
- Build a testbed for reliability improvements

## Hardware/Software
- Raspberry Pi 4, Arducam PTZ, microSD 32GB+
- Python 3.10, OpenCV, gpiozero, tkinter

## Quick Start
pip install -r requirements.txt
python src/ptz_control.py

## Repo
- `src/` PTZ control, menu UI, camera driver
- `docs/` diagrams, screenshots

## Key Learnings
- Real-time control loops
- UI/UX for operator workflows
- Debugging hardware/software interfaces

> Unclassified, educational project. No sensitive or export-controlled data.