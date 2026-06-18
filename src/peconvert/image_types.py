from enum import Enum, auto

class ImageTypes(Enum):
    GRAYSCALE = auto()
    BYTECLASS = auto()
    BYTECLASS_HILBERT = auto()
    ENTROPY = auto()
    BIGRAMS = auto()
    SPIRAL = auto()
    HIT = auto()
    EMBER = auto()