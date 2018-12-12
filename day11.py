import numpy as np


def get_matrix_argmax(m):
    return np.unravel_index(m.argmax(), m.shape)


def get_hundreds_digit(powerLevel):
    paddedPowerLevel = str(powerLevel).rjust(3, '0')
    return int(paddedPowerLevel[-3])


def get_power_level(x, y, serial_number):
    rackId = x + 10
    powerLevel = rackId * y
    powerLevel += serial_number
    powerLevel *= rackId
    powerLevel = get_hundreds_digit(powerLevel)
    return powerLevel - 5

assert get_power_level(3, 5, 8) == 4
assert get_power_level(122, 79, 57) == -5
assert get_power_level(217, 196, 39) == 0
assert get_power_level(101, 153, 71) == 4


def get_power_val_matrix(N, puzzle_input):
    vals = np.zeros(shape=(N, N))
    for i in range(N):
        for j in range(N):
            vals[i, j] = get_power_level(i+1, j+1, puzzle_input)
    return vals


def get_convolution_matrix(vals, M):
    N = vals.shape[0]
    sumVals = np.zeros(shape=(N-M+1, N-M+1))
    for i in range(N - M + 1):
        for j in range(N - M + 1):
            sumVals[i, j] = np.sum(vals[i:(i+M), j:(j+M)])
    return sumVals


def get_max_x_y(N, M, power_matrix):
    sumVals = get_convolution_matrix(power_matrix, M)
    max_x, max_y = get_matrix_argmax(sumVals)
    return ( (max_x + 1, max_y + 1),  sumVals[max_x, max_y])


def get_max_x_y_m(N,  power_matrix):
    max_val = -999
    max_coord = (None, None, None)
    for m in range(1, N):
        c, v = get_max_x_y(N, m, power_matrix)
        if v > max_val:
            max_val = v
            max_coord = (c[0], c[1], m)
    return max_coord


puzzle_input = 9995
N =  300
M = 3

power_matrix = get_power_val_matrix(N, puzzle_input)
part_a, _ = get_max_x_y(N, 3, power_matrix)
print(part_a)
a_x, a_y = part_a
assert a_x == 33 and a_y == 45


# this bit takes a few minutes at the moment, not optimised
part_b = get_max_x_y_m(N, power_matrix)
print(part_b)
x, y, m = part_b
assert x == 233 and y == 116 and m == 15



