
import scipy.optimize
import numpy as np
import torch

from ..abstract import ExtendedTorchModule
from ._abstract_recurrent_cell import AbstractRecurrentCell

class LinearNACLayer(ExtendedTorchModule):
    """Implements the RegualizedLinearNAC

    Arguments:
        in_features: number of ingoing features
        out_features: number of outgoing features
    """

    def __init__(self, in_features, out_features, **kwargs):
        super().__init__('nac', **kwargs)
        self.in_features = in_features
        self.out_features = out_features

        self.W = torch.nn.Parameter(torch.Tensor(out_features, in_features))
        self.register_parameter('bias', None)

    def reset_parameters(self):
        torch.nn.init.xavier_uniform_(self.W)

    def forward(self, input, reuse=False):
        self.writer.add_histogram('W', self.W)
        return torch.nn.functional.linear(input, self.W, self.bias)

    def extra_repr(self):
        return 'in_features={}, out_features={}'.format(
            self.in_features, self.out_features
        )

class LinearNACCell(AbstractRecurrentCell):
    """Implements the RegualizedLinearNAC as a recurrent cell

    Arguments:
        input_size: number of ingoing features
        hidden_size: number of outgoing features
    """
    def __init__(self, input_size, hidden_size, **kwargs):
        super().__init__(RegualizedLinearNACLayer, input_size, hidden_size, **kwargs)
