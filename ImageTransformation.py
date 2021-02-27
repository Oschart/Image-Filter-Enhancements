#%%
import numpy as np

class ImageTransformation:
    def __init__(self, key, args):
        self.args = args
        if key == 'TRANS':
            self.mat = self.translation_mat(*args)
        elif key == 'SCALE':
            self.mat = self.scale_mat(*args)
        elif key == 'ROT':
            self.mat = self.rotate_mat(*args)
    
    def apply(self, X):
        Y = np.zeros(shape=X.shape)
        n, m = X.shape
        for i in range(n):
            for j in  range(m):
                x = np.array([i, j, 1])
                ik, jk, _ = self.mat@x
                ik, jk = int(ik), int(jk)
                if 0 <= ik < n and 0 <= jk < m:
                    Y[ik,jk] = X[i,j]
        return Y
    
    @staticmethod
    def translation_mat(tx, ty):
        return np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ])
    
    @staticmethod
    def scale_mat(Sx, Sy):
        return np.array([
            [Sx, 0, 0],
            [0, Sy, 0],
            [0, 0, 1]
        ])
    
    @staticmethod
    def rotate_mat(t, Px, Py):
        m1 = np.array([
            [1, 0, Px],
            [0, 1, Py],
            [0, 0, 1]
        ])
        m2 = np.array([
            [np.cos(t), np.sin(t), 0],
            [-np.sin(t), np.cos(t), 0],
            [0, 0, 1]
        ])
        m3 = np.array([
            [1, 0, -Px],
            [0, 1, -Py],
            [0, 0, 1]
        ])

        return m1@m2@m3





# %%
