from .image_types import ImageTypes
from .convertions import (
    grayscale, 
    byteclass, 
    byteclass_hilbert, 
    entropy, 
    bigrams,
    spiral,
    hit,
    ember
)
import matplotlib.pyplot as plt
import json

def convert(source: str, target: str, image_type: ImageTypes = ImageTypes.GRAYSCALE):
    with open(source, 'rb') as f:
        data = bytearray(f.read())

    img = None
    cmap = None
    match image_type:
        case ImageTypes.GRAYSCALE:
            cmap = "gray"
            img = grayscale.convert(data)

        case ImageTypes.BYTECLASS:
            cmap = 'prism'
            img = byteclass.convert(data)

        case ImageTypes.BYTECLASS_HILBERT:
            cmap = 'gnuplot'
            img = byteclass_hilbert.convert(data)
        case ImageTypes.ENTROPY:
            cmap = 'jet'
            img = entropy.convert(data)
        case ImageTypes.BIGRAMS:
            cmap = 'hot'
            img = bigrams.convert(data)
        case ImageTypes.SPIRAL:
            cmap = "spiral"
            img = spiral.convert(data)
            plt.imsave(target, img)

        case ImageTypes.HIT:
            cmap = 'magma'
            img = hit.convert(data)

        case ImageTypes.EMBER:
            cmap = "ember"
            img = ember.convert(data, source)
            if img:
                json_data = json.dumps(img, indent=2)
                with open(target, 'w') as f:
                    f.write(json_data)
            else: 
                raise SystemError()
        case _:
            raise NotImplementedError()

    if img is None or cmap is None:
        raise ValueError(f"Conversion failed for {image_type}")
    if cmap != 'spiral' and cmap != "ember": plt.imsave(target, img, cmap=cmap)