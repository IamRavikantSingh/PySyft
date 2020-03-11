import numpy as np
from syft.frameworks.torch.he.fv import variables


def decrypt(SK, CT):
    ct0 = CT[0]
    ct1 = CT[1]

    t = variables.t
    q = variables.q

    return np.round((t * (ct0 + np.dot(ct1, SK)) % q) / q) % t
