import numpy as np
import os

def calculate_local_population(lat, lng, pop_data_path):
    """Localized population impact (grid summation simulation)."""
    try:
        if not os.path.exists(pop_data_path):
            return 0

        grid = np.load(pop_data_path)
        impacted = grid[grid > 0]
        return int(np.sum(impacted) / 1200)
    except Exception:
        return 0
