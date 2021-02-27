# %%
import numpy as np


class ImageTransformation:
    def __init__(self, key=None, args=None):
        self.args = args
        self.Sx = 1
        self.Sy = 1
        self.mat = np.eye(3)
        self.type = 'mat'
        if key == 'TRANS':
            self.mat = self.translation_mat(*args)
        elif key == 'SCALE':
            self.mat = self.scale_mat(*args)
        elif key == 'ROT':
            self.mat = self.rotate_mat(*args)
        elif key == 'HE':
            self.type = 'histo'
        elif key == 'NTHP':
            self.type = 'nthp'
            self.n = args[0]


    def morph(self, other):
        if (other.type, self.type) == ('mat','mat'):
            self.mat = other.mat@self.mat
            self.Sx *= other.Sx
            self.Sy *= other.Sy
            return True
        else:
            return False


    def apply(self, X):
        if self.type == 'mat':
            return self.apply_mat(X)
        elif self.type == 'histo':
            return self.histogram_equalize(X)
        else:
            return self.nthp_transform(X, self.n)

    def histogram_equalize(self, X):
        Y = np.array(255*X, copy=True)
        histo, _ = np.histogram(X, bins=np.arange(257))
        histo = histo/(X.shape[0]*X.shape[1])
        #print('SUM = ' + sum(histo))
        cdf = 0.0
        he_map = list(range(256))
        for i in range(256):
            cdf += histo[i]
            new_lvl = np.floor(cdf * 255)
            he_map[i] = new_lvl
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Y[i,j] = he_map[X[i,j]]
        return Y/255.0



    def nthp_transform(self, X, n, c = 1.0):
        Y = c*pow(X, n)
        return Y

    def apply_mat(self, X):
        n, m = X.shape
        dest_shape = (int(n*self.Sy), int(m*self.Sx))
        nn, mm = dest_shape
        mat_inv = np.linalg.inv(self.mat)
        Y = np.zeros(shape=dest_shape)
        for i in range(nn):
            for j in range(mm):
                x = np.array([i, j, 1])
                ik, jk, _ = mat_inv@x
                ik, jk = int(ik), int(jk)
                if 0 <= ik < n and 0 <= jk < m:
                    Y[i, j] = X[ik, jk]
        return Y

    def translation_mat(self, tx, ty):
        return np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ])

    def scale_mat(self, Sx, Sy):
        self.Sx *= Sx
        self.Sy *= Sy
        return np.array([
            [Sx, 0, 0],
            [0, Sy, 0],
            [0, 0, 1]
        ])

    def rotate_mat(self, t, Px, Py):
        t = np.radians(t)
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

