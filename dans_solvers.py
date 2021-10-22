from math import cos
from numpy import arccos, degrees, radians, square, sqrt, log2
import matplotlib.pyplot as plt


def cosLaw(angle_len='a' or 'l', a=float, b=float, c=float):
    """Computes C as a missing length, or c as a missing angle"""
    if angle_len == 'a':
        numerator = square(a) + square(b) - square(c)
        denomenator = 2 * a * b
        answer = degrees(arccos(numerator/denomenator))
    elif angle_len == 'l':
        inside_sqrt = square(a) + square(b) - (2 * a * b * cos(radians(c)))
        answer = sqrt(inside_sqrt)
    else:
        answer = "angle_len must be 'a' or 'l'"

    return answer


ans = cosLaw('a', 685.89, 1250, 800)

def Complexity_Solver():
    n = int(input("n plz: "))
    lengthx = []
    lengthy = []

    logx = []
    logy = []
    for N in range(0, n):
        lengthx.append(N)
        lengthy.append(len(bin(N)))
        # print(lengthx[N-1], lengthy[N-1])
        logx.append(N)
        logy.append(log2(N + 1))
        print(logx[N - 1], logy[N - 1])

    plt.plot(lengthx, lengthy, label="Actual Measurement")
    plt.plot(logx, logy, label="Log_2(N+1)")
    plt.legend()
    plt.show()



