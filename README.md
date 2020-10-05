# Problem Statement
Bellow is a list of links leading to an image, read this list of images and find 3 most prevalent colors in the RGB scheme in hexadecimal format (#000000 - #FFFFFF) in each image, and write the result into a CSV file in a form of url,color,color,color.

Please focus on speed and resources. The solution should be able to handle input files with more than a billion URLs, using limited resources (e.g. 1 CPU, 512MB RAM). Keep in mind that there is no limit on the execution time, but make sure you are utilizing the provided resources as much as possible at any time during the program execution.

Answer should be posted in a git repo.

# Execution and Sample Output
```
$time python3 prevalentColors.py 
https://i.redd.it/d8021b5i2moy.jpg  HTTP Error 404: Not Found
https://i.redd.it/ftd3sx5ah13z.jpg  HTTP Error 404: Not Found
https://i.redd.it/nrafqoujmety.jpg  HTTP Error 404: Not Found
Images processed:  37
real	0m17.698s
user	0m6.466s
sys	0m1.041s
$ head prevalentColors.csv 
https://i.redd.it/lsuw4p2ncyny.jpg,#FFFFFF,#A77842,#FFFFFD
https://i.redd.it/fyqzavufvjwy.jpg,#DCB083,#FEFEFE,#DAAE81
https://i.redd.it/tb5pckm6e72y.jpg,#B8B6AA,#A0A19C,#A1A29D
https://i.redd.it/m4cfqp8wfv5z.jpg,#DADADC,#D1D1D1,#D0D0D0
http://i.imgur.com/Gh2I3pq.jpg,#C7B09E,#C6AF9D,#C9B2A0
https://i.redd.it/guul6eld2soy.jpg,#6B7B94,#6D7D96,#807967
https://i.redd.it/ax4eueu0szpy.jpg,#22273A,#BCBAC8,#BCBAC7
http://i.imgur.com/qvnjbVw.jpg,#A9ACB5,#A8ABB4,#AAADB6
https://i.redd.it/c5pk0vnpg3ty.jpg,#6E81CD,#6E81CE,#FEFEFE
https://i.redd.it/ru12lvaf7jyy.jpg,#9D9996,#9C9895,#9E9A97
```

# Appoach

My initial approach was to have the image(s) represented as 24 bit color bitmap - matrix of size `width` x `height` x 24 bits - and perform an FFT to obtain frequencies of each color and then sort the corresponding array.

However I came across a `histogram()` function in the PILLOW library I was using that looked promising. After experimenting with the histogram capability for a while some issues developed:

1. By default images were represented by three RGB channels each `width` x `height` x 8 bits; the `histogram` function concatenated these channels reducing the color space to 256x3 values, much, much fewer than the 256^3 colors in the RGB space. This meant results using this method could have been inaccurate.
2. Similarly, extracting an accurate RGB value from the concattenated `histogram` results proved challenging for me. The problem was `r+g+b=value`; while `value` was know there not enough obvious additional equations to solve the system.

The difficulties above lead me to attempt to tanslate the image into a 24 bit color bitmap and attempt to execute `histogram()` on that representation. This proved challending too as the PILLOW library seem to more designed for an 8 bit bitmap use case and attempting to convert the image into a palletized format with 256^3 colors did not go smoothly. Finally, I settled on a brute-force conversion attempt, iterating over each pixel and converting the 3 RGB channels to a single `int` giving me the bitmap representation I was seeking. Although, not ideal, I was hoping performance wouldn't be too bad since the actual operations at each pixel were bitwise operations which tend to be very fast.

Initial indications were that interating through each pixel was going to be costly, so I decided since I was hitting every pixel anyway to convert to a bitmap, I might as well keep track of color frequencies while doing it. This brute force method provided accurate results, but was very, very costly (see Performance section below).

Further research into the PILLOW library led me to the `getcolors()` function which provided exactly what was needed without any image conversion or potentially problematic issues with `histogram()`. Across a couple sample images the `getcolors()` method and the brute force method produced the *exact* same results, providing confidence.

# Performance, Observations, and Optimizations

- Dev/Testing Hardware: 2.4 GHz Dual-Core Intel Core i5 8G RAM
- Sample of brute force execution time

For ***SINGLE*** 790 x 1400 image:
```
real	182m57.132s
user	129m25.609s
sys	    53m6.305s
```

For ***SINGLE*** 727,040 pixel image:
```
real  29m13.917s
user  21m22.154s
sys   7m39.153s
```
- Sample of `getcolors` execution time for ***ALL*** (~1000) images

First Sample Run:
```
real  7m26.493s
user  2m47.660s
sys   0m26.979s
```
Second Sample Run:
```
real  7m16.864s
user  2m43.056s
sys   0m25.680s
```
- While validationg results I noticed a number of duplicate images in the input ... quite a few actually. The number of unique URLs in the input turned out to be 40, with 3 URL 404. This means the number of actual images that needed to be processed was 37, down from the 1000 in the input. This had significant results:
```
Images processed:  37
real  0m18.423s
user  0m6.438s
sys   0m1.050s
```

- Given the results above and without any further optimizations, the ratio of seconds to images processed seems to be about .5. Naively extrapolating this based on the very small number of samples above for 1 billion images comes out to ~16 years. Clearly some optimizations and possibly more hardware are needed to handle input of that scale.

# TODOS and Improvements
- Thread network requests so they can be parallelized; the results above suggest that I/O accounted for up to 66%-67% of total elapsed time.
- Use virtualization, cgroups, or some other mechanism to simulate target hardware described in problem statement.
- If `getcolors()` was not available, investigate ways to get bitmap representation without interating over each pixel and then look into FFT. Another option may be to look into matrix operations to perform pixel operations without iterating over each pixel. The NUMBY library would be my first stop when investigating these options.
- Look into automated testing to validate output and/or results.
