import torch as th
import numpy as np
from math import ceil, log2
from random import randint
from syft.frameworks.torch.he.fv.variables import security_parameter


def powmod(a, b, m):
    """ Returns the power a**b % m """
    # a^(2b) = (a^b)^2
    # a^(2b+1) = a * (a^b)^2
    if b == 0:
        return 1
    return ((a if b % 2 == 1 else 1) * powmod(a, b / 2, m) ** 2) % m


def is_prime(p):
    """ Returns whether p is probably prime """
    for _ in range(16):
        a = randint(1, p - 1)
        if powmod(a, p - 1, p) == 1:
            return False
    return True


def gen_prime(b):
    """ Returns a prime p with b bits """
    p = randint(2 ** (b - 1), 2 ** b)
    while not is_prime(p):
        p = randint(2 ** (b - 1), 2 ** b)
    return p


def generateSophieGermainPrime(k):
    """ Return a Sophie Germain prime p with k bits """
    p = gen_prime(k - 1)
    sp = 2 * p + 1
    while not is_prime(sp):
        p = gen_prime(k - 1)
        sp = 2
    return sp


def keygen():

    q = generateSophieGermainPrime(security_parameter)
    l = ceil(log2(q))

    m = q * l
    n = security_parameter

    s = np.random.randint(q, size=n - 1, dtype=np.int64)
    SK = np.append(s, 1)
    e = np.rint(np.random.normal(scale=1.0, size=m)).astype(np.int)
    A = np.random.randint(q, size=(n - 1, m), dtype=np.int64)
    PK = np.vstack((-A, np.dot(s, A) + e)) % q
    return [SK, PK]
