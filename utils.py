import collections

import numpy as np


def give_data():
    """Возвращает кортеж с дано.

    Return:
        объект именованного кортежа со атрибутами fig1, fig2, fig3,
        fig4, start, stop:
            figN - кортеж из двух кортежей, элементы первого кортежа -
                это координаты по оси Х фигуры, элементы второго
                кортежа - координаты по оси Y;
            start - кортеж из двух значений: координат X и Y точки
                начала;
            stop - кортеж из двух значений: координат X и Y точки
                конца.

    """

    with open('given.txt', 'r') as f:
        lines = f.readlines()

    values = []
    for line in lines:
        if line[0].strip():
            vals = line.strip().split(' ')
            values.append(tuple(float(num) for num in vals))

    give = collections.namedtuple('give', (
        'fig1', 'fig2', 'fig3', 'fig4', 'start', 'stop'))

    data = give(
        (values[0], values[1]),
        (values[2], values[3]),
        (values[4], values[5]),
        (values[6], values[7]),
        values[8],
        values[9]
    )

    return data


def give_lines(dots):
    """Возвращает массивы для построения фигуры на графике.

    Args:
        dots - кортеж из двух кортежей, первый из которых
        представляет точки по оси X, а второй - по оси Y.

    Return:
        список из кортежей из двух массивов np.array, представляющих
        собой точки X и Y для построения линии на графике.

    """

    x, y = dots[0], dots[1]
    size = len(x)

    result = []
    for i in range(size):
        j = (i + 1) if i != (size - 1) else 0
        line = (
            np.linspace(x[i], x[j], 100), np.linspace(y[i], y[j], 100)
        )
        result.append(line)

    return result


def plot_fig(ax, lines):
    """Рисует фигуру.

    Args:
        ax - объект графика;
        lines - список из двойных кортежей, каждый элемент которых
            является объект np.array с точками для построения линии.

    Return:
        None

    """

    for line in lines:
        x = line[0]
        y = line[1]
        ax.plot(x, y, color='red')


def give_array_with_func(func, array):
    """Возвращает массив значений функции для переданных точек.

    Args:
        func - функция, принимающая единственный аргумент;
        array - массив np.array из значений, которые будут
            переданы функции.

    Return:
        объект np.array значений функции.

    """

    result = np.empty(array.size)
    for i, value in enumerate(array):
        result[i] = func(value)

    return result
