import re
from urllib.request import urlopen
from PIL import Image
import numpy as np

# URL of txt file containing image URLs, one per line
input = 'https://gist.githubusercontent.com/ehmo/e736c827ca73d84581d812b3a27bb132/raw/77680b283d7db4e7447dbf8903731bb63bf43258/input.txt'

imageUrls = urlopen(input).read().decode('UTF-8').split()

img = Image.open(urlopen(imageUrls[0]))
imgArray = np.array(img)
imgShape = imgArray.shape
print('The shape is: ',imgShape)
