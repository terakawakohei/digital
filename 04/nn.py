import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(x))


def derivative_sigmoid(x):
    return sigmoid(x) * (1.0 - sigmoid(x))


# # 3層ニューラルネットワーク


class ThreeLayerNetwork:
    # コンストラクタ
    def __init__(self, inodes, hnodes, onodes, myu):
        # 各レイヤーのノード数
        self.inodes = inodes
        self.hnodes = hnodes
        self.onodes = onodes

        # クラスインスタンスとして各層の入出力を保持（重み更新に使う）
        self.o_i = []

        self.x_h = []
        self.o_h = []

        self.x_o = []
        self.o_o = []

        # 学習係数
        self.myu = myu

        # 重みの初期化
        self.w_ih = np.random.normal(0.0, 1.0, (self.hnodes, self.inodes))
        self.w_ho = np.random.normal(0.0, 1.0, (self.onodes, self.hnodes))

        # 活性化関数
        self.af = sigmoid
        self.daf = derivative_sigmoid

    def initialize_i_o(self):
        self.o_i.clear()

        self.x_h.clear()
        self.o_h.clear()

        self.x_o.clear()
        self.o_o.clear()
        return

    # 順伝搬

    def feedforward(self, data):
        # 入力データのサンプル数N
        N = len(data)

        # 全サンプル N(全クラス分)を一まとめにしたバッチ処理を行うため、各層での入力、出力を保存しておく

        for n in range(N):
            # 入力のリストを縦ベクトルに変換
            self.o_i.append(np.array(data[n], ndmin=2).T)

            # 隠れ層
            self.x_h.append(np.dot(self.w_ih, self.o_i[n]))
            self.o_h.append(self.af(self.x_h[n]))

            # 出力層
            self.x_o.append(np.dot(self.w_ho, self.o_h[n]))
            self.o_o.append(self.af(self.x_o[n]))

        return

    def calc_error(self, data, d):
        N = len(data)
        result = 0
        for n in range(N):
            temp_k = 0
            for k in range(self.onodes):
                temp_k += (d[n][k]-self.o_o[n][k, 0])**2
            result += temp_k

        return result

    def calc_weight_coefficient(self, data, d):
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
            # print(temp_ho)
            temp_ho += np.dot((e_o * self.daf(self.o_o[n])), self.o_h[n].T)
            temp_ih += np.dot((e_h * self.daf(self.o_h[n])), self.o_i[n].T)

        # w(2)kjの更新

        # w(1)jiの更新

        # 重みの更新
        # print(temp_ih)
        self.w_ho += self.myu * temp_ho/N
        self.w_ih += self.myu * temp_ih/N


if __name__ == '__main__':
    # パラメータ
    inodes = 2
    hnodes = 2
    onodes = 2
    myu = 1

    # ニューラルネットワークの初期化
    nn = ThreeLayerNetwork(inodes, hnodes, onodes, myu)

    # print(data)
    # N = len(data)
    # d = np.zeros((N, 2))
    # d_class1 = np.array([1, 0])
    # np.append(d_class1, d_class1, axis=0)

    class1 = np.loadtxt('./class1.csv', delimiter=',')
    class2 = np.loadtxt('./class2.csv', delimiter=',')
    data = np.concatenate((class1, class2), axis=0)

    d_class1 = np.array([[1, 0] for i in range(len(class1))])
    d_class2 = np.array([[0, 1] for i in range(len(class2))])

    d = np.concatenate((d_class1, d_class2), axis=0)

    for n in range(500):
        nn.feedforward(data)
        print(nn.calc_error(data, d))
        nn.calc_weight_coefficient(data, d)
        nn.initialize_i_o()

    # test = np.loadtxt('./test.csv', delimiter=',')
    # nn.feedforward(test)
    # print(nn.o_o)

    # print(nn.w_ih)
    # nn.set_trainingdata([0, 1])
    # print("-----------------------------")
    # for n in range(500):
    #     nn.feedforward(class2)
    #     print(nn.calc_error(class2))
    #     nn.calc_weight_coefficient(class2)
    #     nn.initialize_i_o()

    # print(nn.w_ih)

    # print(nn.o_i[0][1, 0])

    # self.d_class1 = np.array([1, 0], ndmin=2).T
    # tes = np.array([1, 0], ndmin=2).T

    # print(tes[0])

    # print(nn.w_ho)
    # tes = np.random.normal(0.0, 1.0, (5, 2))
    # print(tes)

    # print(tes[4, 1])
