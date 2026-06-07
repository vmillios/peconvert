import numpy as np
import math

from .helper import generate_hilbert_curve

def convert(data: bytearray):
        data_len = len(data)
        # Get raw classes first
        classes = np.zeros(data_len, dtype=np.uint8)
        for i, b in enumerate(data):
            if b == 0x00: classes[i] = 1
            elif b == 0xFF: classes[i] = 2
            elif 32 <= b <= 126: classes[i] = 3
            else: classes[i] = 4

        # Find required Hilbert order
        order = int(math.ceil(math.log2(math.sqrt(data_len))))
        if order < 1: order = 1
        grid_size = 1 << order
        
        grid = np.zeros((grid_size, grid_size), dtype=np.uint8)
        coords = generate_hilbert_curve(order)
        
        for i in range(min(data_len, len(coords))):
            x, y = coords[i]
            grid[x, y] = classes[i]
        return grid