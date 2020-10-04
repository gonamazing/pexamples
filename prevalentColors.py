import re
from urllib.request import urlopen
from PIL import Image
import numpy as np

# URL of txt file containing image URLs, one per line
input = 'https://gist.githubusercontent.com/ehmo/e736c827ca73d84581d812b3a27bb132/raw/77680b283d7db4e7447dbf8903731bb63bf43258/input.txt'

imageUrls = urlopen(input).read().decode('UTF-8').split()

img = Image.open(urlopen(imageUrls[0]))
w,h = img.size
colorFrequency = img.getcolors(w*h)
colorFrequency.sort(reverse=True,key=lambda colors: colors[0])
color1 = colorFrequency[0]
color2 = colorFrequency[1]
color3 = colorFrequency[2]

print('Color 1: ',color1,' Color 2: ',color2,' Color 3: ',color3)

print(colorFrequency)




imgArray = np.array(img)
imgShape = imgArray.shape
####
# Using Pillow to covert to a 24 bit BITMAP doesn't seem to work; pillow reduces the color space
# to 256 colors, much fewer than the 256**3 in the RGB space.
# Using a histogram with seperate RGB channels also is problematic as shown below
#imgColorBitmap = img.convert(mode="P",palette="ADAPTIVE",colors=256**3)
#imgColorBitmap = img.convert(mode="I")
#imgColorBitmapArray = np.array(imgColorBitmap)
#print('Shape of Bitmap: ', imgColorBitmapArray.shape)
#print('Max color: ', np.amax(imgColorBitmapArray))
#print('Shape of Image Array: ', imgArray.shape)
####

newImgArray = np.full((imgArray.shape[0],imgArray.shape[1]), 0)
print('Shape of New Image Array: ', newImgArray.shape)



####
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
      print('Iterations: ', iterations)
      print('Color 1: ', topColors[0]>>16,(topColors[0] & 65280)>>8,topColors[0] & 255,' Frequency: ', topFreq[0])
      print('Color 2: ', topColors[1]>>16,(topColors[1] & 65280)>>8,topColors[1] & 255,' Frequency: ', topFreq[1])
      print('Color 3: ', topColors[2]>>16,(topColors[2] & 65280)>>8,topColors[2] & 255,' Frequency: ', topFreq[2])

print('Iterations: ', iterations)
print('Color 1: ', topColors[0]>>16,(topColors[0] & 65280)>>8,topColors[0] & 255,' Frequency: ', topFreq[0])
print('Color 2: ', topColors[1]>>16,(topColors[1] & 65280)>>8,topColors[1] & 255,' Frequency: ', topFreq[1])
print('Color 3: ', topColors[2]>>16,(topColors[2] & 65280)>>8,topColors[1] & 255,' Frequency: ', topFreq[2])

###
# This doesn't work because you loose color info when attempting to covert to bitmap in Pillow
# OR if a hitogram is performed on 3 channel RGB, RGB values are concatenated and you go from a color space of
# 256**3 to 768 colors
# imgHistogram = imgColorBitmap.histogram()
# sortedHistogram = imgHistogram.copy()
# sortedHistogram.sort(reverse=True)
# color1 = imgHistogram.index(sortedHistogram.pop(0))
# color2 = imgHistogram.index(sortedHistogram.pop(1))
# color3 = imgHistogram.index(sortedHistogram.pop(2))

#print('The 3 most prevalent colors are: ', color1, color2, color3)
#print('R: ', color1>>16, 'G: ', (color1 & 65280)>>8, 'B: ', (color1 & 255))
#print('R: ', color2>>16, 'G: ', (color2 & 65280)>>8, 'B: ', (color2 & 255))
#print('R: ', color3>>16, 'G: ', (color3 & 65280)>>8, 'B: ', (color3 & 255))
#print(imageUrls[0])
###


