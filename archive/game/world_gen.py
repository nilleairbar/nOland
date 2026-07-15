from random import random

import numpy as np
import tcod


def generate_perlin_noise(width, height, scale=10.0, octaves=3, persistence=0.5, lacunarity=2.0):
    """
    Generate a 2D Perlin Noise grid.

    Parameters:
        width (int): Width of the grid.
        height (int): Height of the grid.
        scale (float): Controls "zoom" (smaller = more detail, larger = bigger features).
        octaves (int): Number of noise layers (more = more complexity).
        persistence (float): How much each octave contributes (0.0-1.0; lower = less detail).
        lacunarity (float): How much octave frequency increases (usually >1; higher = more detail).
    Returns:
        2D numpy array of noise values (range: ~-1 to 1).
    """
    # Create empty grid
    noise_grid = np.zeros((height, width))

    # Generate noise for each (x, y) coordinate
            # Generate Perlin Noise value
            noise_value = tcod.noise.Noise(
                dimensions=2,
                algorithm=tcod.noise.Algorithm.PERLIN,
                lacunarity=2,
                seed=random  # Seed (change for different maps)
            )
            noise_grid = noise_value

    return noise_grid