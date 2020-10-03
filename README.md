# Problem Statement
Bellow is a list of links leading to an image, read this list of images and find 3 most prevalent colors in the RGB scheme in hexadecimal format (#000000 - #FFFFFF) in each image, and write the result into a CSV file in a form of url,color,color,color.

Please focus on speed and resources. The solution should be able to handle input files with more than a billion URLs, using limited resources (e.g. 1 CPU, 512MB RAM). Keep in mind that there is no limit on the execution time, but make sure you are utilizing the provided resources as much as possible at any time during the program execution.

Answer should be posted in a git repo.

# Appoach

1. Read single image data of size wxh from URL into memory.
   Expected output: 2D image data array sized wXh of hex RGB values
2. 2D FFT on image data array to bring in to frequency domainm
   Expected output: 2D frequency arrary sized 16777215x(max wxh)
3. Sort frequency array by descending ordinate
   Expected output: sorted frequency array
4. Append image url and abscissa for first 3 entries in frequency array to file in CSV format.
   Expected output: CSV file in form of url, color, color, color
5. Repeat 1-4 for each image URL
6. Testing, performance and optimization
   -Add automated tests
   -Consider parallelization - might need to consider file locking
   -Consider short circuit optimization either in sorting or even when data is in spatial domain
   -Perhaps cgroups can be used to enfource targeted resource limitiations
   -Time execution and/or i/o
   -Threading?

