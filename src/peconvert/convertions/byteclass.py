import numpy as np
from .helper import get_square_dimensions

def convert(data: bytearray):
    data_len = len(data)
    classes = np.zeros(data_len, dtype=np.uint8)
    for i, b in enumerate(data):
        if b == 0x00:
            classes[i] = 0    # Null bytes
        elif b == 0xFF:
            classes[i] = 51   # Static high byte
        elif 32 <= b <= 126:
            classes[i] = 102  # Printable ASCII
        elif b < 32:
            classes[i] = 153  # Control characters
        else:
            classes[i] = 204  # Non-ASCII/Executable data
            
    width = get_square_dimensions(data_len)
    padded_classes = np.pad(classes, (0, width*width - data_len), 'constant')
    return padded_classes.reshape((width, width))