# Finding Waldo
# Name: Jacky Ly

# Sets the path and loads the pictures for use in the program
setMediaPath(getMediaPath())
waldo = makePicture('tinywaldo.jpg')
scene = makePicture('tinyscene.jpg')

# Overlays the template image onto the bigger image comparing the top-left pixel of the template to the pixel at (x1, y1)
# on the search image and calculates the sum of the differences between the luminance of the pixels
def compareOne(template, searchImage, x1, y1):
  W, H = getWidth(template), getHeight(template)
  sum = 0
  for x in range(W):
    for y in range(H):
      p1 = getPixel(template, x, y)
      p2 = getPixel(searchImage, x1 + x, y1 + y)
      L1, L2 = getRed(p1), getRed(p2)
      difference = L2 - L1
      sum += abs(difference)
  return sum

# Runs compareOne (above) for all the possible positions in the search image and
# stores the result (sum) of each search region into their respective elements of a matrix
def compareAll(template, searchImage):
  W1, W2 = getWidth(searchImage), getWidth(template)
  H1, H2 = getHeight(searchImage), getHeight(template)
  matrix = [[1000000 for i in range(W1)] for j in range(H1)]
  for x in range(W1-W2+1):
    for y in range(H1-H2+1):
      matrix[y][x] = compareOne(template, searchImage, x, y)
  return matrix

# Finds the minimum value in a matrix and returns the position of where the value is in the matrix (row, column)
def find2Dmin(matrix):
  minrow = mincol = 0
  for i in range(len(matrix)):
    for j in range(len(matrix[i])):
      current = matrix[i][j]
      minPos = matrix[mincol][minrow]
      if current < minPos:
        minrow = j
        mincol = i
  return (minrow, mincol)

# Draws a rectangle box around the region where the target is found
# starting at the position of the target (x1, y1), which has a border of 3 pixels
def displayMatch(searchImage, x1, y1, w1, h1, color):
  border = 3
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
  pixels = getPixels(picture)
  for p in pixels:
    r, g, b = getRed(p), getGreen(p), getBlue(p)
    L = (r + g + b)/3
    setColor(p, makeColor(L, L, L))
  return picture

# Finds a target given a target picture and a picture to be searched
# This is the main function which calls upon the other functions above to find an target and display the result
def findWaldo(targetJPG, searchJPG):
  W = getWidth(targetJPG)
  H = getHeight(targetJPG)
  targetJPG = grayscale(targetJPG)
  searchJPG = grayscale(searchJPG)
  matrix = compareAll(targetJPG, searchJPG)
  (x1, y1) = find2Dmin(matrix)
  displayMatch(searchJPG, x1, y1, W, H, red)
  explore(searchJPG)
