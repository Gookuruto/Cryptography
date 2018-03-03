from __future__ import division
from fractions import gcd
import sys
from collections import deque


class prng_lcg:
    m = 302080878814014441  # the "multiplier"
    c = 3613230612905734352  # the "increment"
    n = 4611686018427387847  # the "modulus"

    def __init__(self, seed):
        self.state = seed  # the "seed"

    def next(self):
        self.state = (self.state * self.m + self.c) % self.n
        return self.state


def test(test_count):
    gen = prng_lcg(123)  # seed = 123
    x=[]
    y=[]
    result=[]
    succes=0
    all=0
    for i in range(test_count):
        x.append(gen.next())
    y=x[0:int(test_count/2)]
    del x[0:int(test_count/2)]
    for i in range(len(x)):
        all+=1
        result.append(next_random_number(y))
        y.append(result[-1])
    for i in range(len(x)):
        if x[i]==result[i]:
            succes+=1
    return succes/all


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
      return x % n


def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0] * multiplier) % modulus
    return modulus, multiplier, increment


def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)


def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2 * t0 - t1 * t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return crack_unknown_multiplier(states, modulus)


def next_random_number(states):
    while states[0]>states[1]:
        del states[0]
    last_number = states[-1]
    if(states[0]>=states[1]):
        return "to nie zadziala"
    m, a, c = crack_unknown_modulus(states)
    return (a * last_number + c) % m




print "probability of succes is:  "
print test(1000)


