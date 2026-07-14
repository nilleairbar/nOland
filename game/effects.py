import random
import time
import g

def rain_effect_tcod(console, duration=10):
    """
    Create an ASCII rain effect using / characters in a tcod console.

    Args:
        console: The tcod console object
        duration: How long to run the effect (seconds)
    """
    width, height = console.width, console.height

    # Initialize rain drops
    drops = []
    for _ in range(width // 3):
        drops.append({
            'x': random.randint(0, width - 1),
            'y': random.randint(-height, 0),
            'speed': random.uniform(0.5, 2.0)
        })

    start_time = time.time()

    while time.time() - start_time < duration:
        # Clear console
        console.clear()

        # Update and draw drops
        for drop in drops:
            drop['y'] += drop['speed']

            # Reset drop if it goes off bottom
            if drop['y'] >= height:
                drop['y'] = -1
                drop['x'] = random.randint(0, width - 1)
                drop['speed'] = random.uniform(0.5, 2.0)

            # Draw the drop
            y = int(drop['y'])
            if 0 <= y < height:
                x = drop['x']
                if 0 <= x < width:
                    console.print(x, y, '/')

        # Present and handle input