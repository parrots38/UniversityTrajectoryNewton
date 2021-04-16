import numpy as np


def segmentation_difference(var, func, der):
    """Метод Ньютона-Эрмита поиска таблицы разделенных разностей.

    Args:
        var - массив значений некоторых переменных;
        func - массив значений функции от этих переменных;
        der - массив значений производной от функции.

    Return:
        Объект np.array, представляющий собой таблицу
        разделенной разности в виде:
        var0 func0  0    0    0
        var0 der0  der0  0    0
        var1 func1 val  val   0
        var1 der1  der1 val  val
        var2 func2 val  val  val
        var2 der2  der2 val  val
        ...  ...   ...  ...  ...

    """

    union = lambda l1, l2: [value for tupl in zip(l1, l2) for value in tupl]
    # объединение двух списков

    assert len(var) == len(func) == len(der), 'Массивы разных размеров.'
    var = np.array(union(var, var))
    func_der = np.array(union(func, der))
    der = np.array(union([0]*len(der), der))
    size = var.size

    result = np.zeros((size + 1, size))
    result[:3] = var, func_der, der

    for i in range(2, size, 2):
        result[2, i] = (
            (result[1, i] - result[1, i-2]) /
            (result[0, i] - result[0, i-2])
        )

    for i in range(3, size+1):
        for j in range(i-1, size):
            result[i, j] = (
                (result[i-1, j] - result[i-1, j-1]) /
                (result[0, j] - result[0, j-i+1])
            )

    return result.T


def give_diagonal(array, num=0):
    """Возвращает массив диагоналей таблицы разделенных разностей.

    Args:
        array - объект np.array, представляющий таблицу разделенных
            разностей;
        num - номер возвращаемой диагонали, считая с нуля.

    Return:
        объект np.array с элементами диагонали.

    """

    size = array.shape[0]
    result = np.zeros(size)
    i = delta = num*2
    while i < size:
        result[i] = array[i, i - delta + 1]
        i += 1

    return result[delta:size]


def make_function(array, diagonals=None):
    """
    Возвращает функцию, представляющую интерполяцию по Эрмиту-Ньютону.

    Args:
        array - массив np.array, таблица разделенных разностей;
        diagonals - объект np.array, представляющий диагональные
            элементы таблицы разделенных разностей.

    Return:
        объект функции, которая выражает зависимость от некоторой
            переменной, построенную методом Ньютона.

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
