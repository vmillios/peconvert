import numpy as np
import math

def get_square_dimensions(length):
        """Calculates a balanced width and height for 2D reshaping."""
        width = int(math.ceil(math.sqrt(length)))
        if width == 0: width = 1
        return width

def generate_hilbert_curve(order):
    if order == 0:
        return np.zeros((1, 2), dtype=int)
    
    prev = generate_hilbert_curve(order - 1)
    size = 1 << (order - 1)
    
    # Rotate and translate for the 4 quadrants
    q0 = np.array([prev[:, 1], prev[:, 0]]).T
    q1 = prev + np.array([0, size])
    q2 = prev + np.array([size, size])
    q3 = np.array([size - 1 - prev[:, 1], size - 1 - prev[:, 0]]).T + np.array([size, 0])
    
    return np.vstack((q0, q1, q2, q3))