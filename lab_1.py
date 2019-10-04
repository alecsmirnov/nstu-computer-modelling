from sympy.solvers import solve
from sympy import Symbol, diff, integrate
from os.path import dirname, join, exists
from timeit import default_timer
from numpy import *
import math
import operator as op
import matplotlib.pyplot as plt
import numpy as np

# Подсчёт времени выполнения функции с аргументами
def elapsed_time(fun, *args):
    start_time = default_timer()			# Начальное время
    fun(args)
    end_time = default_timer() 				# Конечное время
    return (end_time - start_time) * 1000	# Перевод в ms

# Вывод содержимого файла на экран
def print_file(filename):
    with open(filename, 'r') as fin:
        print(fin.read())

# Решить уравнение
def solve_equation(equation):
    return solve(equation, Symbol("x"))

# Удвоить содержимое файла
def file_doubler(filename):
    current_dir = dirname(__file__)			# Искать файл в текущей директории
    file_path = join(current_dir, filename)
    if exists(file_path):					# Проверить на существование
        f = open(file_path, "r+")
        data = f.read()						# Прочитать файла
        f.write("\n")
        f.write(data)						# Записать содержимое в конец
        f.close()

# Сортировка массива пузырьком с выборо направления сортировки
def bubble_sort(array, sign="<"):
    ops = {"<": op.lt, ">": op.gt}			# Операции сравнения
    new_array = list(array)					# Создание копии массива
    array_len = len(array) - 1
    for i in range(array_len):
        for j in range(array_len - i):
            if ops[sign](new_array[j+1], new_array[j]):
                new_array[j], new_array[j+1] = new_array[j+1], new_array[j]
    return new_array

# Поиск частной производной по указанной переменной
def find_derivative(equation, var):
    return diff(equation, Symbol(var))

# Решение неопределённого/определённого интеграла
def solve_integral(integral, a=0, b=0):
    x = Symbol("x") if a == 0 or b == 0 else (Symbol("x"), a, b)
    return integrate(integral, x)

# Отрисовка графика функции по указанным значениям x
def draw_plot(fun, x):
    plt.title(fun) 
    plt.xlabel("x") 
    plt.ylabel("f(x)", rotation = 0) 
    plt.plot(x, eval(fun))
    plt.grid(True)
    plt.show()

# Отрисовка гистограммы
def draw_chart(columns):
    x = range(len(columns))
    ax = plt.gca()
    ax.set_aspect('equal')
    ax.bar(x, columns, 1, align = 'edge')
    ax.set_xticks(x)
    ax.set_xticklabels(range(0, len(columns)))
    plt.grid(True)
    plt.show()


def main():
    # Task 1
    #equation = "2 * x**3 - 11 * x**2 + 12 * x + 9"
    #print("Equation:", equation)
    #res = solve_equation(equation)
    #print("Result:", res)

    # Task 2
    #filename = "file.txt"
    #print("File content:")
    #print_file(filename)
    #file_doubler(filename)
    #print("\nFile content after doubler:")
    #print_file(filename)

    # Task 3
    #array = [8, 3, 1, 7, 0, 2, 5, 4, 6, 9]
    #print("Source array =      ", array, "\n")
    #print("Bubble sort result =", bubble_sort(array))
    #time = elapsed_time(bubble_sort, array)
    #print("Elapsed time:", time, "ms")
    #print("Sorted result =     ", sorted(array))
    #time = elapsed_time(sorted, array)
    #print("Elapsed time:", time, "ms")

    # Task 4
    #equation = "sin(x) * cos(x**2) * tan(y) - ln(x)"
    #print("Equation:   ", equation)
    #print("X derivative", find_derivative(equation, "x"))

    # Task 5
    #integral = "x**2 * (3 + 4 * x)**2"
    #print("Indefinite integral:", integral)
    #print("Result:             ", solve_integral(integral))
    #integral = "sin(x) / (cos(x)** 2 + 1)"
    #a = math.pi / 2
    #b = math.pi
    #print("\nDefinite integral:", integral)
    #print("Result:           ", solve_integral(integral, a, b))

    # Task 6
    #fun = "sin(x) / (x + 1)"
    #x = np.arange(0, 50, 0.01)
    #draw_plot(fun, x)

    # Task 7
    data = [5, 4, 2, 7, 0, 3, 3, 4, 0]
    draw_chart(data)

if __name__ == "__main__":
    main()