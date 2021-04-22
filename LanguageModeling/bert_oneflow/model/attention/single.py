import oneflow.nn as nn
import oneflow as flow
import math
import oneflow.nn as nn
import numpy as np

class Attention(nn.Module):
    """
    Compute 'Scaled Dot Product Attention
    """

    def __init__(self):
        super().__init__()
        self.matmul = flow.nn.MatMul()
        self.softmax = flow.nn.Softmax(axis = -1)
        self.masked_fill = flow.MaskedFill()
 
    def forward(self, query, key, value, mask=None, dropout=None): # q k v shape >> flow.Size([16, 8, 20, 32])
        # flow.matmul(dim>2的多维情况下和torch行为没对齐)
        # scores = flow.matmul(query, key.transpose(-2, -1)) \
        #          / math.sqrt(query.size()[-1])
        x = flow.tmp.transpose(key, perm=[0, 1, 3, 2])
        x = self.matmul(query, x)
        scores = x / math.sqrt(query.size()[3])

        if mask is not None:
            # scores = scores.masked_fill(mask == 0, -1e9)
            mask = flow.Tensor((mask.numpy() == 0).astype(np.int8), dtype=flow.int)
            scores = self.masked_fill(scores, mask, -1e9)

        p_attn = self.softmax(scores)

        if dropout is not None:
            p_attn = dropout(p_attn)

        return self.matmul(p_attn, value), p_attn