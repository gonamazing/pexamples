from collections import OrderedDict
from PIL import Image
from urllib.request import urlopen

# URL of txt file containing image URLs, one per line
input = 'https://gist.githubusercontent.com/ehmo/e736c827ca73d84581d812b3a27bb132/raw/77680b283d7db4e7447dbf8903731bb63bf43258/input.txt'

# Results file
output = 'prevalentColors.csv'

imageUrls = urlopen(input).read().decode('UTF-8').split()
# remove duplicates from ~1000 to 40 unique image URLs
imageUrls = list(OrderedDict.fromkeys(imageUrls))
results = []

for image in imageUrls:

  try:
    img = Image.open(urlopen(image))
  except Exception as e:
    # Most common exception seems to be HTTP 404
    print(image + " ", e)
    continue

  w,h = img.size
  # PILLOW library provided method that retuns [(<# of occurences>, (R,G,B)),...]
  colorFrequency = img.getcolors(w*h)
  colorFrequency.sort(reverse=True,key=lambda colors: colors[0])

  # Normally hex values would be represted with a preceeding `0x
  # Simply stripping this prefix caused issues with `0` values not displaying correctly
  # This formatting string enforces uppercase and each hex value will be 2 characters
  formatString = '{:02X}{:02X}{:02X}'

  color1 = formatString.format(*colorFrequency[0][1])
  color2 = formatString.format(*colorFrequency[1][1])
  color3 = formatString.format(*colorFrequency[2][1])
    
  result = image + ",#" + color1 + ",#" + color2 + ",#" + color3
  results.append(result)   
  print("Images processed: ",len(results), end='\r')


f = open(output, "w")
while len(results) > 0:
  f.write(results.pop() + "\n")
f.close()
