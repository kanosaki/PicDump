

# conduit --  push/pull stream controller based on dataflow programming model

from .junction import CyclicJunction


def cyclic(*sources):
    return CyclicJunction(*sources)
