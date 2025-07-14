from random import randint


def randomColor():
    return [randint(100, 255) for _ in range(3)]
