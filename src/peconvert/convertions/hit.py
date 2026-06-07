import numpy as np

def convert(data: bytearray):
        """7. HIT: Highest Intensity Texture map / Byte occurrence map."""
        counts = np.zeros(256, dtype=np.uint32)
        for b in data:
            counts[b] += 1
        
        # Reshape the 256 histogram into a 16x16 grid grid pattern
        return counts.reshape((16, 16))