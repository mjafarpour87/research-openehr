
"""
Version: 0.0.1


Configuration file for setting project-wide constants and paths.


This file defines key directory paths and runtime constants used throughout
the project. It dynamically resolves the project's root directory based on the
location of this file, ensuring portability across environments.

Attributes:
    ROOT (Path): The root directory of the project (two levels up from this file).
    DATA_DIR (Path): Directory where dataset and data-related files are stored.
    DATASET_FILE (Path): Full path to the KG-CAD dataset JSON file.
    OUTPUT_DIR (Path): Directory where output files will be saved.
    SAVE_MODE (bool): If True, enables saving outputs and intermediate results.
    CLI_ALERT_POINT (int): Threshold value used for command-line alerts (e.g., log prints).

Usage:
    Import this module to access shared constants across the codebase:
        from config import DATASET_FILE, OUTPUT_DIR
"""

import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
DATASET_FILE = DATA_DIR / "dataset.json"
OUTPUT_DIR = ROOT / "output" 
SAVE_MODE = True
# CLI_ALERT_POINT = 500