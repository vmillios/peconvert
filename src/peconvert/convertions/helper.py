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

def calculate_entropy(data):
    """Calculate Shannon entropy of data"""
    if not data:
        return 0.0
    
    entropy = 0.0
    for i in range(256):
        freq = data.count(bytes([i]))
        if freq > 0:
            p = freq / len(data)
            entropy -= p * (p and __import__('math').log2(p) or 0)
    return round(entropy, 4)

def extract_ascii_strings(data, min_length=4):
    """Extract ASCII strings from PE file"""
    strings = []
    current_string = b''
    
    for byte in data:
        if 32 <= byte <= 126:  # Printable ASCII
            current_string += bytes([byte])
        else:
            if len(current_string) >= min_length:
                try:
                    strings.append(current_string.decode('ascii'))
                except:
                    pass
            current_string = b''
    
    return strings

def extract_unicode_strings(data, min_length=4):
        """Extract Unicode (UTF-16LE) strings from PE file"""
        strings = []
        current_string = b''
        
        i = 0
        while i < len(data) - 1:
            byte1 = data[i]
            byte2 = data[i + 1]
            
            if byte1 != 0 and 32 <= byte1 <= 126 and byte2 == 0:
                current_string += bytes([byte1])
                i += 2
            else:
                if len(current_string) >= min_length:
                    try:
                        strings.append(current_string.decode('ascii'))
                    except:
                        pass
                current_string = b''
                i += 1
        
        return strings