import numpy as np
from PIL import Image
from .helper import get_square_dimensions

def convert(data: bytes) -> Image.Image:
    data_len = len(data)
    width = get_square_dimensions(data_len)
    padded_len = width * width
    padded_data = np.pad(data, (0, padded_len - data_len), 'constant')
    return padded_data.reshape((width, width))