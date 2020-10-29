import syft as sy

# import numpy as np
# import torch as th

from syft.generic.abstract.tensor import AbstractTensor

# from syft.generic.frameworks.hook import hook_args
from syft.generic.frameworks.hook.hook_args import (
    get_child,
    register_backward_func,
    register_forward_func,
    register_type_rule,
    one,
)
from syft.generic.frameworks.overload import overloaded
from syft.workers.abstract import AbstractWorker


class BFVTensor(AbstractTensor):
    def __init__(self, **kwargs):
        """Initializes a BFVTensor.

        Args:
            owner: An optional BaseWorker object to specify the worker on which
                the tensor is located.
            id: An optional string or integer id of the BFVTensor.
        """
        super().__init__(**kwargs)

    def encrypt(self, public_key):
        """This method will encrypt each value in the tensor using BFV
        homomorphic encryption scheme.
        """
        print("encrypt called!")
        pass

    def decrypt(self, private_key):
        """This method will decrypt each value in the tensor, returning a normal
        torch tensor.
        """
        print("decrypt called!")
        pass

    def __add__(self, *args, **kwargs):
        """
        Here is the version of the add method without the decorator: as you can see
        it is much more complicated. However you might need sometimes to specify
        some particular behaviour: so here what to start from :)
        """
        print("custom add called!")
        pass

    def __sub__(self, *args, **kwargs):
        """
        Here is the version of the sub method without the decorator: as you can see
        it is much more complicated. However you might need sometimes to specify
        some particular behaviour: so here what to start from :)
        """
        print("custom sub called!")
        pass

    def __mul__(self, *args, **kwargs):
        """
        Here is the version of the mul method without the decorator: as you can see
        it is much more complicated. However you might need sometimes to specify
        some particular behaviour: so here what to start from :)
        """
        print("custom mul called!")
        pass

    def mm(self, *args, **kwargs):
        """
        Here is matrix multiplication between an encrypted and unencrypted tensor. Note that
        we cannot matrix multiply two encrypted tensors because Paillier does not support
        the multiplication of two encrypted values.
        """
        print("custom mm called!")
        pass

    # Method overloading
    @overloaded.method
    def add(self, _self, *args, **kwargs):
        """
        Here is an example of how to use the @overloaded.method decorator. To see
        what this decorator do, just look at the next method manual_add: it does
        exactly the same but without the decorator.

        Note the subtlety between self and _self: you should use _self and NOT self.
        """

        return self + args[0]

    # Method overloading
    @overloaded.method
    def sub(self, _self, *args, **kwargs):
        """
        Here is an example of how to use the @overloaded.method decorator. To see
        what this decorator do, just look at the next method manual_add: it does
        exactly the same but without the decorator.

        Note the subtlety between self and _self: you should use _self and NOT self.
        """

        return self - args[0]

    # Method overloading
    @overloaded.method
    def mul(self, _self, *args, **kwargs):
        """
        Here is an example of how to use the @overloaded.method decorator. To see
        what this decorator do, just look at the next method manual_add: it does
        exactly the same but without the decorator.

        Note the subtlety between self and _self: you should use _self and NOT self.
        """

        return self * args[0]

    # Module & Function overloading

    # We overload two torch functions:
    # - torch.add
    # - torch.nn.functional.relu

    @staticmethod
    @overloaded.module
    def torch(module):
        """
        We use the @overloaded.module to specify we're writing here
        a function which should overload the function with the same
        name in the <torch> module
        :param module: object which stores the overloading functions

        Note that we used the @staticmethod decorator as we're in a
        class
        """

        def add(x, y):
            """
            You can write the function to overload in the most natural
            way, so this will be called whenever you call torch.add on
            Logging Tensors, and the x and y you get are also Logging
            Tensors, so compared to the @overloaded.method, you see
            that the @overloaded.module does not hook the arguments.
            """
            pass

        # Just register it using the module variable
        module.add = add

        def mul(x, y):
            """
            You can write the function to overload in the most natural
            way, so this will be called whenever you call torch.add on
            Logging Tensors, and the x and y you get are also Logging
            Tensors, so compared to the @overloaded.method, you see
            that the @overloaded.module does not hook the arguments.
            """
            pass

        # Just register it using the module variable
        module.mul = mul

    @staticmethod
    def simplify(worker: AbstractWorker, tensor: "BFVTensor") -> tuple:
        """
        This function takes the attributes of a BFVTensor and saves them in a tuple
        Args:
            tensor (BFVTensor): # TODO
        Returns:
            tuple: a tuple holding the unique attributes of the log tensor
        Examples:
            data = _simplify(tensor)
        """

        chain = None
        if hasattr(tensor, "child"):
            chain = sy.serde.msgpack.serde._simplify(worker, tensor.child)
        return tensor.id, chain

    @staticmethod
    def detail(worker: AbstractWorker, tensor_tuple: tuple) -> "BFVTensor":
        """
        This function reconstructs a BFVTensor given it's attributes in form of a tuple.
        Args:
            worker: the worker doing the deserialization
            tensor_tuple: a tuple holding the attributes of the BFVTensor
        Returns:
            BFVTensor: # TODO
        """
        obj_id, chain = tensor_tuple

        tensor = BFVTensor(owner=worker, id=obj_id)

        if chain is not None:
            chain = sy.serde.msgpack.serde._detail(worker, chain)
            tensor.child = chain

        return tensor


register_type_rule({BFVTensor: one})
register_forward_func({BFVTensor: get_child})
register_backward_func({BFVTensor: lambda i, **kwargs: BFVTensor().on(i, wrap=False)})
