import numpy as np

sigmoid_range = 34.538776394910684


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -sigmoid_range, sigmoid_range)))


def derivative_sigmoid(o):
    return o * (1.0 - o)
# 3層ニューラルネットワーク


class ThreeLayerNetwork:
    # コンストラクタ
    def __init__(self, inodes, hnodes, onodes, lr):
        # 各レイヤーのノード数
        self.inodes = inodes
        self.hnodes = hnodes
        self.onodes = onodes

        self.e_o = []
        self.e_h = []

        self.o_i = []

        self.x_h = []
        self.o_h = []

        self.x_o = []
        self.o_o = []

        # 学習率
        self.lr = lr

        # 重みの初期化
        self.w_ih = np.random.normal(0.0, 1.0, (self.hnodes, self.inodes))
        self.w_ho = np.random.normal(0.0, 1.0, (self.onodes, self.hnodes))

        # 活性化関数
        self.af = sigmoid
        self.daf = derivative_sigmoid

    # 誤差逆伝搬
    def backprop(self, idata, tdata):
        # 縦ベクトルに変換
        o_i = np.array(idata, ndmin=2).T
        t = np.array(tdata, ndmin=2).T

        # 隠れ層
        x_h = np.dot(self.w_ih, o_i)
        o_h = self.af(x_h)

        # 出力層
        x_o = np.dot(self.w_ho, o_h)
        o_o = self.af(x_o)

        self.o_i.append(o_i)

        # 隠れ層
        self.x_h.append(x_h)
        self.o_h.append(o_h)

        # 出力層
        self.x_o.append(x_o)
        self.o_o.append(o_o)

        # 誤差計算
        e_o = (t - o_o)
        e_h = np.dot(self.w_ho.T, e_o)

        self.e_o.append(e_o)
        self.e_h.append(e_h)

    def calc_weight(self, data, d):
        N = len(data)

        temp_ho = 0
        temp_ih = 0
        for n in range(N):
            # 誤差計算
            e_o = (np.array(d[n], ndmin=2).T - self.o_o[n])
            e_h = np.dot(self.w_ho.T, e_o)
            # print(e_o)
            # print(self.daf(self.o_o[n]))
            # print(e_o * self.daf(self.o_o[n]))
            # print(self.o_h[n].T)
            # print(self.o_o[n])
            temp_ho += np.dot((e_o * self.daf(self.o_o[n])), self.o_h[n].T)
            temp_ih += np.dot((e_h * self.daf(self.o_h[n])), self.o_i[n].T)

        # w(2)kjの更新

        # w(1)jiの更新

        # 重みの更新
        # print(temp_ih)
        self.w_ho += self.lr * temp_ho/N
        self.w_ih += self.lr * temp_ih/N

    # 順伝搬

    def feedforward(self, idata):
        # 入力のリストを縦ベクトルに変換
        o_i = np.array(idata, ndmin=2).T

        # 隠れ層
        x_h = np.dot(self.w_ih, o_i)
        o_h = self.af(x_h)

        # 出力層
        x_o = np.dot(self.w_ho, o_h)
        o_o = self.af(x_o)

        return o_o

    def calc_error(self, data, d):
        N = len(data)
        result = 0
        for n in range(N):
            temp_k = 0
            for k in range(self.onodes):
                temp_k += (d[n][k]-self.o_o[n][k, 0])**2
            result += temp_k

        return result


if __name__ == '__main__':
    # パラメータ
    inodes = 2
    hnodes = 2
    onodes = 2
    lr = 1

    # ニューラルネットワークの初期化
    nn = ThreeLayerNetwork(inodes, hnodes, onodes, lr)

    class1 = np.loadtxt('./class1.csv', delimiter=',')
    class2 = np.loadtxt('./class2.csv', delimiter=',')
    data = np.concatenate((class1, class2), axis=0)

    d_class1 = np.array([[1, 0] for i in range(len(class1))])
    d_class2 = np.array([[0, 1] for i in range(len(class2))])

    d = np.concatenate((d_class1, d_class2), axis=0)

    # 学習
    epoch = 500
    for e in range(epoch):
        print('#epoch ', e)
        data_size = len(data)
        for n in range(data_size):

            nn.backprop(data[n], d[n])

        nn.calc_weight(data, d)
        print(nn.calc_error(data, d))

    test = np.loadtxt('./test.csv', delimiter=',')

    for n in range(len(test)):
        print(nn.feedforward(test[n]))
