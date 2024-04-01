class Image:
  def __init__(self, matrix, height, width, gray_level):
    self.matrix = matrix
    self.height = height
    self.width = width
    self.gray_level = gray_level


def readpgm(name) -> Image:
  with open(name, "r") as f:

    assert f.readline() ==  'P2\n'
    line = f.readline()
    while (line[0] == '#'):
      line = f.readline()

    (width, height) = [int(i) for i in line.split()]
    print (width, height)
    depth = int(f.readline())
    assert depth <= 255
    print (depth)


    img = []
    row = []
    j = 0
    for line in f:
      values = line.split()
      for val in values:
        row.append (int (val))
        j = j + 1
        if j >= width:
          img.append (row)
          j=0
          row = []
    pic = Image(matrix=img, height=height, width=width, gray_level=depth)    

  return pic