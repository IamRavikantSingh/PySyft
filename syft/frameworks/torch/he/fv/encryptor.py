import numpy as np
from random import randint
from syft.frameworks.torch.he.fv import variables


def encrypt(PK, message):
    datatype = variables.datatype
    n = variables.security_parameter
    p0 = PK[0]
    p1 = PK[1]

    q = variables.q
    variables.t = randint(2, n - 1)
    t = variables.t

    delta = q // t  # floor of q/t
    u = np.random.randint(q, size=(n, n), dtype=np.int64).astype(datatype)
    e1 = np.random.randint(q, size=n, dtype=np.int64).astype(datatype)
    e2 = np.random.randint(q, size=n, dtype=np.int64).astype(datatype)

    ct0 = (np.dot(p0, u) + e1 + delta * message) % q
    ct1 = (np.dot(p1, u) + e2) % q

    return [ct0, ct1]
