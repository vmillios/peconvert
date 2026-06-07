import numpy as np
from .helper import get_square_dimensions


def convert(data: bytearray, window_size=256, step=64):
    data_len = len(data)
    """4. ENTROPY: Sliding window Shannon entropy visualized in 2D."""
    entropies = []
    for i in range(0, data_len - window_size, step):
        window = data[i:i+window_size]
        _, counts = np.unique(window, return_counts=True)
        
        # --- Manual Shannon Entropy Calculation ---
        probabilities = counts / counts.sum()
        ent = -np.sum(probabilities * np.log2(probabilities))
        entropies.append(ent)
        
    if not entropies: 
        entropies = [0]
    
    entropies = np.array(entropies)
    width = get_square_dimensions(len(entropies))
    padded = np.pad(entropies, (0, width*width - len(entropies)), 'constant')
    return padded.reshape((width, width))