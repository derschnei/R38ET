#!/usr/bin/env python3
"""CLI wrapper launcher for sp0t-node."""
import sys
from pathlib import Path

# Add src/ to sys.path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sp0t_node import main

if __name__ == "__main__":
    main()
