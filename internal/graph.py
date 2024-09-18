import matplotlib.pyplot as plt
import matplotlib
from numpy.polynomial import polynomial, Polynomial
import numpy
import statistics

TEST_MAX_LENGTH = 180000
TEST_COUNT = 20
TEST_STEP = 10000

values_x = {
    1: [],
    2: []
}

values_y = {
    1: [],
    2: []
}


def get_data_from_file(file, arrx, arry):
    for i in range(0, TEST_MAX_LENGTH + 1, TEST_STEP):
        sum_1 = []
        for j in range(TEST_COUNT):
            str = file.readline()[:-1]
            val = float(str)
            sum_1.append(val)
        arrx.append(i)
        arry.append(statistics.median(sum_1))


def get_data_from_files():
    with open("./res_test_db_no_index.txt", "r") as file:
        get_data_from_file(file, values_x[1], values_y[1])

    with open("./res_test_db_index.txt", "r") as file:
        get_data_from_file(file, values_x[2], values_y[2])
    #     values_y[2] = [ i - i * 0.1 for i in values_y[2]]

    # values_y[1] = sorted(values_y[1])
    # values_y[2] = sorted(values_y[2])


def plot_time():
    matplotlib.rcParams.update({'font.size': 14})
    matplotlib.rcParams.update({'font.family': 'Times New Roman'})
    matplotlib.rcParams.update({'figure.figsize': (10, 7)})
    matplotlib.rcParams.update({'axes.prop_cycle': matplotlib.cycler(color=['black'])})

    plt.scatter(values_x[1], values_y[1], label='Индекс отсуствует')
    plt.scatter(values_x[2], values_y[2], marker='*', label='Индекс присутствует')

    plt.xlabel('Количество строк в таблице')
    plt.ylabel(r'Время выполнения запроса (миллисекунды)')

    #  for i in range(20):
    coefs, params = polynomial.polyfit(numpy.array(values_x[1]), values_y[1], 1, full=True)

    degree = 1
    approximation, _ = polynomial.polyfit(numpy.array(values_x[2]), values_y[2], degree)
    while (degree < 2):
        degree = degree + 1
        approximation = polynomial.polyfit(numpy.array(values_x[2]), values_y[2], degree)
        print(Polynomial(approximation))
    approximation = Polynomial(coefs)
    arr = approximation(numpy.array(values_x[1]))
    print(approximation)
    plt.plot(values_x[1], arr, label="Функция зависимости времени выполнения запроса от строк (без индекса)")

    coefs, params = polynomial.polyfit(numpy.array(values_x[2]), values_y[2], 1, full=True)

    # degree = 1
    # approximation = Polynomial.fit(values_x[1], values_y[1], degree)
    # arr =  approximation(numpy.array(values_x[1]))
    # while (sum([(arr[i] - values_y[1][i]) ** 2 for i in range(len(values_y[1]))]) / (len(values_y[1]) - 1) > 1e-4):
    #     degree = degree + 1
    # approximation = Polynomial.fit(values_x[1], values_y[1], degree)
    approximation = Polynomial(coefs)
    arr = approximation(numpy.array(values_x[2]))
    print(approximation)
    plt.plot(values_x[2], arr, linestyle='dashed',
             label="Функции зависимости времени выполнения запроса от строк (с индексом)")

    ax = plt.gca()

    ax.margins(0.001)

    plt.legend(fontsize=10)

    plt.tight_layout()

    plt.show()


# def plot_mem():
#     plt.plot(values_l, values_m[1], linestyle='solid', label='Сортировка Шелла')
#     plt.plot(values_l, values_m[2], 'd', linestyle='solid', label='Сортировка Перемешиванием')
#     plt.plot(values_l, values_m[3], linestyle='dashed', label='Плавная Сортировка')
#
#     plt.xlabel('Количество элементов в массиве')
#     plt.ylabel(r'Память (байт)')
#
#     ax = plt.gca()
#     ax.margins(0.001)
#
#     plt.legend(fontsize=10)
#
#     plt.loglog()
#
#     plt.tight_layout()
#
#     plt.show()


get_data_from_files()
plot_time()
# plot_mem()

for i in range(len(values_y[1])):
    print(
        f'   \\num{{{values_x[1][i]}}} & \\num{{{"{:.2f}".format(values_y[1][i])}}}  & \\num{{{"{:.2f}".format(values_y[2][i])}}}  \\\\\\hline')

# print('-------')
#
# for i in range(len(values_m[1])):
#     print(f'   \\num{{{i * TEST_STEP}}} & \\num{{{values_m[1][i]}}}  & \\num{{{values_m[2][i]}}}  & \\num{{{values_m[3][i]}}}  \\\\\\hline')
