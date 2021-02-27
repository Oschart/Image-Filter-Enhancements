import numpy as np


class ImageTransformer():
    def __init__(self, tr_list=[]):
        self.tr_list = tr_list
        self.optimize_matrices()

    def optimize_matrices(self):
        tr_list = self.tr_list
        opt_trs = [tr_list[0]]
        for i in range(1, len(tr_list)):
            if opt_trs[-1].morph(tr_list[i]) is False:
                opt_trs.append(tr_list[i])
        self.tr_list = opt_trs


    def apply_all(self, X):
        Y = np.array(X, copy=True)
        for tr in self.tr_list:
            Y = tr.apply(Y)
        return Y