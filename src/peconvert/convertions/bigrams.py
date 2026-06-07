import numpy as np

def convert(data: bytearray):
    data_len = len(data)
    matrix = np.zeros((256, 256), dtype=np.uint32)
    for i in range(data_len - 1):
        matrix[data[i], data[i+1]] += 1
    # Log transform to make variations visible
    return np.log1p(matrix)