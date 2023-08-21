from mpmath import *
import matplotlib.pyplot as plt
from numpy import arange, array, linalg
from random import vonmisesvariate

accuracy = 1e-4
mp.dps = abs(log(accuracy, 10)) + 1
mp.dps = 50

def iterat(start_value, accuracy, list_num_steps = []):

    point = start_value
    old_point = [-inf, -inf]

    diff_func1_x = lambda p0, p1: float(diff(lambda x: cos(p1+0.5)+x-0.8, p0))
    diff_func1_y = lambda p0, p1: float(diff(lambda y: cos(y+0.5)+p0-0.8, p1))
    diff_func2_x = lambda p0, p1: float(diff(lambda x: sin(x)-2*p1-1.6, p0))
    diff_func2_y = lambda p0, p1: float(diff(lambda y: sin(p0)-2*y-1.6, p1))

    cnt_steps = 0

    while sqrt(power(point[0] - old_point[0], 2) + power(point[1] - old_point[1], 2)) > accuracy:

        det_Ic = linalg.det(array([[diff_func1_x(point[0], point[1]), diff_func1_y(point[0], point[1])], [diff_func2_x(point[0], point[1]), diff_func2_y(point[0], point[1])]]))
        del_x = linalg.det(array([[float(-(cos(point[1] + 0.5) + point[0] - 0.8)), diff_func1_y(point[0], point[1])], [float(-(sin(point[0]) - 2*point[1] - 1.6)), diff_func2_y(point[0], point[1])]]))/det_Ic
        del_y = linalg.det(array([[diff_func1_x(point[0], point[1]),  float(-(cos(point[1] + 0.5) + point[0] - 0.8))], [diff_func2_x(point[0], point[1]), float(-(sin(point[0]) - 2*point[1] - 1.6))]]))/det_Ic

        old_point = point

        point = [point[0] + del_x, point[1] + del_y]
        cnt_steps += 1

    list_num_steps += [cnt_steps]

    return [mpf(point[0]), mpf(point[1])]

def grafics() -> None:

    ax = arange(-5, 5, 0.01)
    ay = arange(-5, 5, 0.01)

    func1 = lambda y: 0.8 - cos(y + 0.5)
    func2 = lambda x: sin(x)/2 - 0.8

    value_func1 = [func1(y) for y in ay]
    value_func2 = [func2(x) for x in ax]
    Ox = [0 for x in ax]
    Oy = [0 for y in ay]

    start_x, start_y = -0.13, -0.86
    list_num_steps = []
    coord_x, coord_y = [], []

    '''
    for i in range(100):
        res = iterat([start_x, start_y], accuracy, list_num_steps)
        coord_x += [start_x]
        coord_y += [start_y]
        rnd = vonmisesvariate(0, 0)
        start_x = -0.13 + i*0.01*cos(rnd)
        start_y = -0.86 + i*0.01*sin(rnd)
        #nprint(res)
    '''

    lst_powers = []
    for i in range(4, 21):
        lst_powers += [-i/2]
        accuracy = power(10, -i/2)
        res = iterat([0, 0], accuracy, list_num_steps)

    plt.subplots(figsize=(15, 8))

    plt.subplot(121)
    plt.plot(value_func1, ay, "b", label = "cos(y + 0.5) + x - 0.8 = 0")
    plt.plot(ax, value_func2, "r", label = "sin(x) - 2y - 1.6 = 0")
    plt.plot(ax, Ox, "--g", )
    plt.plot(Oy, ay, "--g", )
    plt.plot([0], [0], "ok", alpha=0.8, label = "Начальная точка")
    plt.title("Исходные функции")
    plt.grid()
    plt.legend()

    """plt.subplot(122)
                plt.plot(sorted([sqrt(power(-0.13 - coord_x[i], 2) + power(-0.86 - coord_y[i], 2)) for i in range(len(list_num_steps))]), list_num_steps)
                plt.title("Зависимость количества шагов от выбора начальной точки")
                plt.xlabel("Расстояние до решения")"""
    
    plt.subplot(122)
    plt.plot(lst_powers, list_num_steps)
    plt.title("Зависимость количества шагов от требуемой точности")
    plt.xlabel("Степень требуемой точности")


    plt.subplots_adjust(bottom=0.1, left=0.05, right=0.95, top=0.90)
    plt.show()

grafics()