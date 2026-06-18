# peconvert

This package aims to take `windows portable executables` and covert them to `image` using these methods in order to be used in `ML applications` :
- grayscale
- byteclass
- byteclass hilbert
- entropy
- bigrams
- spiral
- hit

### in order to install this package run 

```bash
pip install git+https://github.com/vmillios/peconvert.git
```

### how to use this package

```py
from peconvert import convert, ImageTypes

convert("<source>", "<target>", Image.<TYPE>)
```

`<source>"` the path where you have saved you windows executable \
`target` the path where you want the image to be saved \
`<TYPE>` one of 

- GRAYSCALE
- BYTECLASS
- BYTECLASS_HILBERT
- ENTROPY
- BIGRAMS
- SPIRAL
- HIT
- EMBER

_`note:` ember is in json format I know its not an image but I need it for my thesis_

to specify what kind of method you want used

if you want all the methods you can use for loop for one file

```py
from peconvert import convert, ImageTypes

for image in ImageTypes:
    convert("<source>", f"./test{image}.png", image)
```

`<source>"` the path where you have saved you windows executable 

### LLM Disclaimer

ai was used to assist in making this package since I had no idea how to convert python code to packages it helped with:
- pyproject.yml
- setup the folder structure
- other errors that I didnt have time to look up