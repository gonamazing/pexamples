import numpy as np
from PIL import Image
from urllib.request import urlopen

# URL of txt file containing image URLs, one per line
input = 'https://gist.githubusercontent.com/ehmo/e736c827ca73d84581d812b3a27bb132/raw/77680b283d7db4e7447dbf8903731bb63bf43258/input.txt'

imageUrls = urlopen(input).read().decode('UTF-8').split()

try:
  # Since this is so ineffecient, just process a single image
  # A couple "random" image URLs were selected to validate
  # results from `getcolors` method, most recently the 599 image in the input list
  img = Image.open(urlopen(imageUrls[598]))
except Exception as e:
  # In case 404
  print(e)
  sys.exit(1)

imgArray = np.array(img)
imgShape = imgArray.shape

# Where the newly generated bitmap will live
newImgArray = np.full((imgArray.shape[0],imgArray.shape[1]), 0)

# The below should work, but is resouce intensive
# The geral approach is
# 1) Iterate of each pixel and RGB tuble and represent each pixel as a 24 bit value generated from RGB channels
# 2) Keep track of top 3 pixel values as you interate
# 3) Decompose pixel value back into RGB space
pixelValueFreq = {} 
topFreq = [0,0,0]
topColors = [0,0,0]
iterations = 0
for x in imgArray:
  for y in x:
    r = y[0]
    g = y[1]
    b = y[2]
    pixelValue = (r<<16)|(g<<8)|b
    newImgArray[x][y] = pixelValue
    currentFreq = 0
    if pixelValue in pixelValueFreq:
      currentFreq = pixelValueFreq[pixelValue]
    currentFreq +=1
    pixelValueFreq[pixelValue] = currentFreq
    if currentFreq >= topFreq[0]:
      topFreq[0] = currentFreq
      topColors[0] = pixelValue
    elif currentFreq >= topFreq[1]:
      topFreq[1] = currentFreq
      topColors[1] = pixelValue
    elif currentFreq > topFreq[2]:
      topFreq[2] = currentFreq
      topColors[2] = pixelValue
    iterations += 1
    if iterations % 10000 == 0:
      # Provide periodic user feedback
      print('Iterations: ', iterations, end='\r')

print('Iterations: ', iterations)
print('Color 1: ', topColors[0]>>16,(topColors[0] & 65280)>>8,topColors[0] & 255,' Frequency: ', topFreq[0])
print('Color 2: ', topColors[1]>>16,(topColors[1] & 65280)>>8,topColors[1] & 255,' Frequency: ', topFreq[1])
print('Color 3: ', topColors[2]>>16,(topColors[2] & 65280)>>8,topColors[2] & 255,' Frequency: ', topFreq[2])
