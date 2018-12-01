# Finding Waldo - Version 2
# Name: Jacky Ly

# Sets the path and initializes assets for use in the program
import time
setMediaPath(getMediaPath())
bigwaldo = makePicture('waldo.jpg')
bigscene = makePicture('scene.jpg')

# Overlays the template image onto the bigger image comparing the top-left pixel of the template to the pixel at (x1, y1)
# on the search image and calculates the sum of the differences between the luminance of the pixels

# *only compares the top/middle/bottom pixels in the first/last columns and
#  the left/middle/right pixels in the first/last rows of the template image for maximum efficiency)

# Template Image Diagram (x means the pixels to be compared):
# x o x o x
# o o o o o
# x o o o x
# o o o o o
# x o x o x
 
def compareOne(template, searchImage, x1, y1):
  W, H = getWidth(template), getHeight(template)
  search_accuracy = W/2 # *read note above
  sum = 0
  for x in range(0, W, search_accuracy):
    for y in range(0, H, search_accuracy):
      p1 = getPixel(template, x, y)
      p2 = getPixel(searchImage, x1 + x, y1 + y)
      L1, L2 = getBlue(p1), getBlue(p2)
      difference = L2 - L1
      sum += abs(difference)
  return sum

# Runs compareOne (above) for all the possible positions in the search image and
# stores the result (sum) of each search region into their respective elements of a matrix  
def compareAll(template, searchImage):
  max_value = 10000000 # the initial value the elements in the matrix will be
  W1, W2 = getWidth(searchImage), getWidth(template)
  H1, H2 = getHeight(searchImage), getHeight(template)
  matrix = [[max_value for i in range(W1)] for j in range(H1)]
  for x in range(W1-W2+1):
    for y in range(H1-H2+1):
      matrix[y][x] = compareOne(template, searchImage, x, y)
  return matrix

# Finds the minimum value in a matrix and returns the position of where the value is in the matrix (row, column)
def find2Dmin(matrix):
  minrow = mincol = 0 # assumes the first element at (0, 0) is the minimum value
  for i in range(len(matrix)):
    for j in range(len(matrix[i])):
      current = matrix[i][j]
      minPos = matrix[mincol][minrow]
      if current < minPos: # if the current element value is lower then the previous minimum value
        minrow, mincol = j, i # then set the min position to the current value's position
  return (minrow, mincol)

# Draws a rectangle box around the region where the target is found
# starting at the position of the target (x1, y1), which has a border of 3 pixels
def displayMatch(searchImage, x1, y1, w1, h1, color):
  border = 3 # sets the border width to 3 pixels
  for x in range(x1, x1 + w1):
    for y in range(y1, y1 + border):
      p = getPixel(searchImage, x, y)
      setColor(p, color)
    for y in range(y1 + h1 - border - 1, y1 + h1 - 1):
      p = getPixel(searchImage, x, y)
      setColor(p, color)
  for x in range(x1, x1 + border):
    for y in range(y1 + border, y1 + h1 - border - 1):
      p = getPixel(searchImage, x, y)
      setColor(p, color)
  for x in range(x1 + w1 - border, x1 + w1):
    for y in range(y1 + border, y1 + h1 - border - 1):  
      p = getPixel(searchImage, x, y)
      setColor(p, color)

# Converts all the pixels in a picture to gray, resulting in a grayscale picture
def grayscale(picture):
  W = getWidth(picture)
  H = getHeight(picture)
  for x in range(W):
    for y in range(H):
      p = getPixel(picture, x, y)
      r, g, b = getRed(p), getGreen(p), getBlue(p)
      L = (r + g + b)/3
      setColor(p, makeColor(L, L, L))
  return picture

# Calculates the elapsed time to execute the search and output the result
def timeTaken(timeStart, timeEnd, picture):
  m, s = divmod(timeEnd, 60)
  h, m = divmod(m, 60)
  H = getHeight(picture)
  string = "Processing Time: %d:%02d:%02d" % (h, m, s)
  addText(picture, 5, H - 5, string, yellow)
  return string

# Finds a target given a target picture and a picture to be searched
# This is the main function which calls upon the other functions above to find an target and display the result
def findWaldo(targetJPG, searchJPG):
  timeStart = time.clock() # starts the timer
  W = getWidth(targetJPG)
  H = getHeight(targetJPG)
  targetJPG = grayscale(targetJPG)
  searchJPG = grayscale(searchJPG)
  matrix = compareAll(targetJPG, searchJPG)
  (x1, y1) = find2Dmin(matrix)
  displayMatch(searchJPG, x1, y1, W, H, yellow)
  timeEnd = time.clock() - timeStart # stops the timer
  print timeTaken(timeStart, timeEnd, searchJPG)
  explore(searchJPG)
