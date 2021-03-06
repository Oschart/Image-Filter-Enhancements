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

    def apply_filter(self, X, F, clip=True, padding='same'):
        """[Apply filter F to image X with 'same' padding]

        Args:
            X ([2d numpy array]): [Normalized gray image]
            F ([2d numpy array]): [Filter]

        Returns:
            [2d numpy array]: [Filtered image]
        """
        n, m = X.shape
        nk, mk = F.shape
        if padding == 'same':
            padv, padh = nk//2, mk//2
            nn, mm = n, m
            Xp = cv2.copyMakeBorder(X, padv, padv, padh,
                                    padh, borderType=cv2.BORDER_REFLECT)
        else:
            nn, mm = n-nk+1, m-mk+1
            Xp = X

        Y = np.zeros(shape=X.shape)
        for i in range(nn):
            for j in range(mm):
                M = Xp[i:i+nk, j:j+mk]
                Y[i, j] = (M*F).sum()

        if clip:
            #Y = Y/np.max(Y)
            Y = np.clip(Y, 0.0, 1.0)
        return Y
