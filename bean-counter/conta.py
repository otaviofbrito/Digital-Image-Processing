# ======================================================================
# UNIFAL - Universidade Federal de Alfenas
# BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO
# Trabalho......: Contagem de feijões
# Professor.....: Luiz Eduardo da Silva
# Aluno.........: Otavio Ferreira de Brito Silveira
# Data..........: 06/05/2024
# ======================================================================

import sys


class Image:
    def __init__(self, matrix, height, width, gray_level):
        self.matrix = matrix
        self.height = height
        self.width = width
        self.gray_level = gray_level


"""
Método para carregar uma imagem .pgm
"""


def readpgm(name) -> Image:
    with open(name, "r") as f:

        assert f.readline() == 'P2\n'
        line = f.readline()
        while (line[0] == '#'):
            line = f.readline()

        (width, height) = [int(i) for i in line.split()]
        depth = int(f.readline())
        assert depth <= 255

        img = []
        row = []
        j = 0
        for line in f:
            values = line.split()
            for val in values:
                row.append(int(val))
                j = j + 1
                if j >= width:
                    img.append(row)
                    j = 0
                    row = []
        pic = Image(matrix=img, height=height, width=width, gray_level=depth)

    return pic


def find(parent: list, x: int) -> int:
    while parent[x] != x:
        return find(parent, parent[x])
    else:
        return x


def union(parent: list, x: int, y: int):
    parent[find(parent, y)] = find(parent, x)


"""
Rotulação de componentes conexos
"""


def cc_label(img: Image) -> int:
    parents = [i for i in range(1000)]
    label_id = 1
    for i in range(1, img.height):
        for j in range(1, img.width):
            p = img.matrix[i][j]
            r = img.matrix[i-1][j]
            t = img.matrix[i][j-1]
            if p != 0:
                if r == 0 and t == 0:
                    img.matrix[i][j] = label_id
                    label_id += 1
                if r != 0 and t == 0:
                    img.matrix[i][j] = r
                if r == 0 and t != 0:
                    img.matrix[i][j] = t
                if r != 0 and t != 0 and t == r:
                    img.matrix[i][j] = r
                if r != 0 and t != 0 and t != r:
                    img.matrix[i][j] = t
                    union(parents, r, t)
    sets = set()
    for i in range(img.height):
        for j in range(img.width):
            parent = find(parents, img.matrix[i][j])
            img.matrix[i][j] = parent
            sets.add(parent)

    img.gray_level = label_id
    components = len(sets)-1
    return components


"""
Transformada de distância
"""


def distance(img: Image):
    max_gl = float('-inf')
    # Step 1
    for i in range(1, img.height):
        for j in range(1, img.width):
            p = img.matrix[i][j]
            # Top and left neighbors
            a = img.matrix[i-1][j]
            b = img.matrix[i][j-1]
            if p != 0:
                img.matrix[i][j] = min(a+1, b+1)
    # Step 2
    for i in range(img.height - 2, -1, -1):
        for j in range(img.width - 2, -1, -1):
            p = img.matrix[i][j]
            # Bottom and right neighbors
            a = img.matrix[i+1][j]
            b = img.matrix[i][j+1]
            if p != 0:
                img.matrix[i][j] = min(a+1, b+1, p)
            if p > max_gl:
                max_gl = p
    img.gray_level = max_gl


"""
Método para limiarização
"""


def threshold(img: Image, limit: int):
    # Transformation vector
    T_th = []
    gl = img.gray_level
    for i in range(gl+1):
        value = 0 if i <= limit else gl
        binary_value = (gl - value)/gl
        T_th.insert(i, int(binary_value))

    for i in range(img.height):
        for j in range(img.width):
            img.matrix[i][j] = T_th[img.matrix[i][j]]


"""
Método para normalizar imagem transformada por distância
"""


def normalize(img: Image, scale):
    t = [0] * (scale + 1)
    gl = img.gray_level
    for i in range(scale+1):
        value = gl - i
        t[i] = int((value/gl)*scale)

    for i in range(img.height):
        for j in range(img.width):
            img.matrix[i][j] = t[img.matrix[i][j]]
    img.gray_level = scale


def main():
    if len(sys.argv) != 2:
        print(
            "[AVISO] : Especifique o caminho do arquivo de imagem: <python conta.py image.pbm>")
        return

    img = readpgm(sys.argv[1])
    gl = img.gray_level

    threshold(img, 100)
    distance(img)
    normalize(img, gl)
    threshold(img, 190)
    count = cc_label(img)
    print("\n#COMPONENTES =", count)


if __name__ == '__main__':
    main()
