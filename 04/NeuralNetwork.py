import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


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

    # 重み係数を更新した際、古くなった入出力を消去する
    def initialize_i_o(self):
        self.o_i.clear()

        self.x_h.clear()
        self.o_h.clear()

        self.x_o.clear()
        self.o_o.clear()
        return

    # 順伝搬を行う
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

    # 二乗誤差を計算し、結果を返す
    def calc_error(self, data, d):

        N = len(data)
        result = 0
        for n in range(N):
            temp_k = 0
            for k in range(self.onodes):
                temp_k += (d[n][k]-self.o_o[n][k, 0])**2
            result += temp_k

        return result

    # 順伝搬によって得られた各層の入出力のデータを用いて、重み係数を更新する
    def calc_weight_coefficient(self, data, d):
        N = len(data)
        # w(2)kjの更新
        for k in range(self.onodes):
            for j in range(self.hnodes):
                temp = 0
                for n in range(N):
                    temp += (d[n][k]-self.o_o[n][k, 0]) * \
                        self.daf(self.x_o[n][k, 0])*self.o_h[n][j, 0]

                self.w_ho[k, j] = self.w_ho[k, j]+self.myu*temp/N

        # w(1)jiの更新
        for i in range(self.inodes):
            for j in range(self.hnodes):
                temp_n = 0
                for n in range(N):
                    temp_k = 0
                    for k in range(self.onodes):
                        temp_k += (d[n][k]-self.o_o[n][k, 0]) * \
                            self.daf(
                                self.x_o[n][k, 0])*self.w_ho[k, j]

                    temp_n += temp_k*self.daf(
                        self.x_h[n][j, 0])*data[n][i]

                self.w_ih[j, i] = self.w_ih[j, i]+self.myu*temp_n/N


if __name__ == '__main__':
    # パラメータ
    inodes = 2
    hnodes = 2
    onodes = 2
    myu = 1

    class1 = np.loadtxt('./class1.csv', delimiter=',')
    class2 = np.loadtxt('./class2.csv', delimiter=',')

    # 二つの学習データを結合、dataとする
    data = np.concatenate((class1, class2), axis=0)

    # ニューラルネットワークの初期化
    nn = ThreeLayerNetwork(inodes, hnodes, onodes, myu)

    # それぞれのクラスについての教師データを作成、dとして二つを結合する
    d_class1 = np.array([[1, 0] for i in range(len(class1))])
    d_class2 = np.array([[0, 1] for i in range(len(class2))])

    d = np.concatenate((d_class1, d_class2), axis=0)

    # 誤差を格納する
    error = []

    # 一回めの順伝播での誤差を求めておく
    nn.feedforward(data)
    error.append(nn.calc_error(data, d))

    # 誤差値が一より小さくまなるまで学習を続ける
    while error[-1] > 1:
        nn.feedforward(data)
        error.append(nn.calc_error(data, d))
        nn.calc_weight_coefficient(data, d)
        nn.initialize_i_o()

    # 誤差の収束をみる
    fig_e = plt.figure(figsize=(4, 6))
    ax_e = fig_e.add_subplot(1, 1, 1)

    ax_e.plot(range(len(error)), error,
              "o-", markersize=1, label="error")

    ax_e.legend()
    ax_e.set_xlabel('Number of iterations')
    ax_e.set_ylabel('Total error')

    plt.show()

    # 学習が完了したので、テストデータの分類を行う

    test = np.loadtxt('./test.csv', delimiter=',')

    # 順伝播でクラス分類を実行、結果がo_oに格納される
    nn.feedforward(test)

    out_node1 = []
    out_node2 = []

    # グラフ出力用にデータを移し替える
    for n in range(len(nn.o_o)):
        out_node1.append(nn.o_o[n][0])
        out_node2.append(nn.o_o[n][1])

    fig = plt.figure(figsize=(4, 6))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(range(len(out_node1)), out_node1,
            "o-", markersize=1, label="out_node1")

    ax.plot(range(len(out_node2)), out_node2,
            "o-", markersize=1, label="out_node2")

    plt.xlabel('number of samples')

    ax.legend()
    plt.show()

    for n in range(len(nn.o_o)):
        if abs(out_node1[n]-out_node1[n-1]) > 0.7:
            print("node1のクラス分類の切り替わり地点 : n={}".format(n))

    for n in range(len(nn.o_o)):
        if abs(out_node2[n]-out_node2[n-1]) > 0.7:
            print("node2のクラス分類の切り替わり地点 : n={}".format(n))
