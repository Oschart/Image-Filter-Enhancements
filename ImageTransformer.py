import numpy as np
import cv2

class ImageTransformer():
    def __init__(self, tr_list=[]):
        self.tr_list = tr_list
        if tr_list:
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
    
    def apply_filter(self, X, F):
        # This function does 'same' padding
        n, m = X.shape
        nk, mk = F.shape
        pad = nk//2
        Xp = cv2.copyMakeBorder(X, pad, pad, pad, pad, borderType=cv2.BORDER_REFLECT)
        Y = np.zeros(shape=X.shape)
        for i in range(n):
            for j in range(m):
                M = Xp[i:i+nk,j:j+mk]
                #Y[i,j] = max(min((M*F).sum(), 255.0), 0.0) 
                Y[i,j] = max(min((M*F).sum(), 255.0), 0.0) 
        return Y/np.max(Y)
