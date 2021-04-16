import numpy as np


def segmentation_difference(var, func):
    """Метод Ньютона поиска таблицы разделенных разностей.

    Args:
         var - массив значений некоторых переменных;
         func - массив значений функции от этих переменных.

    Return:
        Объект np.array, представляющий собой таблицу
        разделенной разности в виде:
        var0 func0  0   0   0
        var1 func1 val  0   0
        var2 func2 val val  0
        ...  ...   ... ... ...
    """

    assert len(var) == len(func), 'Массивы разных размеров.'
    var = np.array(var)
    func = np.array(func)
    size = var.size

    result = np.zeros((size + 1, size))
    result[:2] = var, func

    for i in range(2, size+1):
        for j in range(i-1, size):
            result[i, j] = (
                (result[i-1, j] - result[i-1, j-1]) /
                (result[0, j] - result[0, j-i+1])
            )

    return result.T


def give_diagonal(array):
    """Возвращает массив диагоналей таблицы разделенных разностей.

    Args:
        array - объект np.array, представляющий таблицу разделенных
            разностей.

    Return:
        объект np.array с элементами диагонали.

    """

    size = array.shape[0]
    result = np.zeros(size)
    for i in range(size):
        result[i] = array[i, i+1]

    return result


def make_function(array, diagonals=None):
    """Возвращает функцию, представляющую интерполяцию по Ньютону.

    Args:
        array - массив np.array, таблица разделенных разностей;
        diagonals - объект np.array, представляющий диагональные
            элементы таблицы разделенных разностей.

    Return:
        объект функции, которая выражает зависимость от некоторой
            переменной, построенную методом Эрмита-Ньютона.

    """

    if diagonals is None:
        diagonals = give_diagonal(array)

    assert isinstance(array, np.ndarray), (
        'Массив array должен быть объектом np.ndarray.')
    assert isinstance(diagonals, np.ndarray), (
        'Массив diagonals должен быть объектом np.ndarray.')
    vars = array[:, 0]

    expression = f'{diagonals[0]:+}'
    diffs = []
    for i in range(1, diagonals.size):
        diffs += [f'(var-{vars[i-1]:+})']
        mul = '*'.join(diffs)
        expression += f'{diagonals[i]:+}*{mul}'
    expression = 'exp = ' + expression
    # print(expression) если нужно вывести получившуюся функцию

    def function(var):
        namespace = {'diagonals': diagonals, 'vars': vars, 'var': var}
        exec(expression, {'__builtins__': {}}, namespace)
        return namespace['exp']

    return function
