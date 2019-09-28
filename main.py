from random import random
from antsystem import AntColonySystem


def main():
    n = 10
    c = [[10*random(), 10*random()] for i in range(n)]
    a = AntColonySystem(n, c)
    a.findSolution()


if __name__ == '__main__':
    main()
