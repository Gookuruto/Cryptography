from __future__ import division
from ctypes import c_int, c_uint

#work in python2

def srand(seed):
    srand.r = [0 for _ in range(34)]
    srand.r[0] = c_int(seed).value
    for i in range(1, 31):
        srand.r[i] = (16807 * srand.r[i - 1]) % 2147483647
    for i in range(31, 34):
        srand.r[i] = srand.r[i - 31]
    srand.k = 0
    for _ in range(34, 344):
        rand()


def rand():
    srand.r[srand.k] = srand.r[(srand.k - 31) % 34] + srand.r[(srand.k - 3) % 34]
    r = c_uint(srand.r[srand.k]).value >> 1
    srand.k = (srand.k + 1) % 34
    return r


if __name__ == '__main__':
    srand(1337)
    assert [rand() for _ in range(10)] == [
        292616681, 1638893262, 255706927, 995816787, 588263094, 1540293802, 343418821, 903681492,
        898530248, 1459533395
    ]

    srand(0xffffffff + 0xffffffff - 1)
    assert [rand() for _ in range(10)] == [
        853660264, 1568971201, 1203662233, 15207980, 1421679843, 1717493552, 811896681, 155106358,
        1156099704, 428649477
    ]

    srand(-1337)
    assert [rand() for _ in range(10)] == [
        1766598330, 413225925, 1792113474, 2120225281, 1445538174, 488114690, 1678701932,
        1108308242, 32946609, 1612248994
    ]

    srand(-0xffffffff - 0xffffffff)
    assert [rand() for _ in range(10)] == [
        1505335290, 1738766719, 190686788, 260874575, 747983061, 906156498, 1502820864, 142559277,
        1261608745, 1380759627
]

def predict_glibc_number(states):
    if len(states)<31:
        print("zbyt malo danych aby przewidziec klolejne elementy")
        return
    o31=states[len(states)-31]
    o3=states[len(states)-3]
    prediction1 = (o31 + o3) % (1 << 31)
    return prediction1


def test_glibc(ilosc_testow):
    x=[]
    succes=0
    all=0
    for i in range(ilosc_testow):
        x.append(rand())
    know_output=x[0:32]
    del x[0:32]
    for i in range(len(x)):
        all+=1
        know_output.append(predict_glibc_number(know_output))
        if know_output[-1]==x[i]:
            succes+=1
        else:
            know_output[-1]=x[i]
    return succes/all


a=[]
for i in range(60):
    a.append(rand())

print(rand())

print(predict_glibc_number(a))
print test_glibc(100)