from math import ceil, log2
from random import randint
import numpy as np
from syft.frameworks.torch.he.fv import variables


def powmod(a, b, m):
    """ Returns the power a**b % m """
    # a^(2b) = (a^b)^2
    # a^(2b+1) = a * (a^b)^2
    if b == 0:
        return 1
    return ((a if b % 2 == 1 else 1) * powmod(a, b // 2, m) ** 2) % m


def is_prime(p):
    """ Returns whether p is probably prime """
    for _ in range(16):
        a = randint(1, p - 1)
        if powmod(a, p - 1, p) != 1:
            return False
    return True


def gen_prime(b):
    """ Returns a prime p with b bits """
    p = randint(2 ** (b - 1), 2 ** b)
    while not is_prime(p):
        p = randint(2 ** (b - 1), 2 ** b)
    return p


def generateSafePrime(k):
    """ Return a safe prime p with k bits """
    p = gen_prime(k - 1)
    sp = 2 * p + 1
    while not is_prime(sp):
        p = gen_prime(k - 1)
        sp = 2
    return sp


def keygen():
    k = variables.security_parameter
    if k > 29:
        datatype = "object"
    else:
        datatype = np.int64
    variables.datatype = datatype

    variables.q = generateSafePrime(k)
    q = variables.q
    l = ceil(log2(q))
    n = k
    variables.m = n * l
    m = variables.m
    print("q value", q)
    SK = np.random.randint(q, size=n, dtype=np.int64).astype(datatype)
    e = np.rint(np.random.normal(scale=1.0, size=m)).astype(np.int).astype(datatype)
    a = np.random.randint(q, size=(m, n), dtype=np.int64).astype(datatype)
    PK = [-(np.dot(a, SK) + e) % q, a]
    return [SK, PK]
