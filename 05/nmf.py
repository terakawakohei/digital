import numpy as np
import matplotlib.pyplot as plt
import csv
import random
import matplotlib as mpl
mpl.rcParams['font.family'] = 'AppleGothic'

# s毎にdataに対してDFTを適用する


def STFT(data, sample_freq, s):
    # s内でのサンプルポイント数をsample_pointsとする
    sample_points = sample_freq*s
    I_dim = int(sample_points)//2
    Z = np.empty((I_dim, 0), dtype=int)
    N = len(data)
    for i in range(int(N // sample_points)):
        # print("{}〜{}".format(int(i*sample_points),
        #                      int(i*sample_points + sample_points-1)))
        tmp = data[int(i*sample_points): int(i*sample_points + sample_points)]
        tmp = np.fft.fft(tmp)  # get fft data [i*step:i*step+window]
        amp = np.abs(tmp)
        # print(len(amp))
        Z = np.append(Z, np.array(amp[:I_dim]).reshape(
            I_dim, 1), axis=1)

    return Z

# ユークリッド距離の二乗誤差を求める


def calc_error(X, W, H):
    error = np.square(X-np.dot(W, H))
    return np.sum(error)

# ユークリッド距離の二乗誤差を評価関数とし、Hを更新する


def update_H(X, W, H):
    H_error = []
    J = len(X[0, :])
    K = len(W[0, :])

    H_error.append(calc_error(X, W, H))

    for i in range(100):

        Wt_X = np.dot(W.T, X)
        Wt_W_H = np.dot(np.dot(W.T, W), H)

        for a in range(K):
            for myu in range(J):
                if Wt_W_H[a, myu] == 0:
                    H[a, myu] = 0
                else:
                    H[a, myu] = H[a, myu]*Wt_X[a, myu]/Wt_W_H[a, myu]

        H_error.append(calc_error(X, W, H))

    return H_error

# 時刻毎に10個のベクトルに対する重みを加算してゆく


def calc_weight(H):

    J = len(H[0, :])
    K = len(H[:, 0])

    sounds = np.empty((int(K/10), 0))
    for j in range(J):
        # １フレームのにおける各音の合計値が入ってゆく（18個の要素が存在）
        frame = []
        temp = 0

        for k in range(K):
            if k % 10 == 9:
                temp += H[k, j]
                if temp <= 0.1:
                    frame.append(0)
                else:
                    frame.append(temp)
                temp = 0
            else:
                temp += H[k, j]

        # 縦ベクトルにして、soundsに入れる
        np_frame = np.array(frame).reshape(int(K/10), 1)
        sounds = np.append(sounds,  np_frame, axis=1)
        frame.clear()

    return sounds


# em = np.loadtxt('em_chord.csv', delimiter=',', dtype='int64')
training_sounds = np.loadtxt(
    'all_training_sounds.csv', delimiter=',', dtype='int64')
test = np.loadtxt('test.csv', delimiter=',', dtype='int64')

X = STFT(test, 8000, 0.032)
W = STFT(training_sounds, 8000, 0.032)


J = len(X[0, :])
K = len(W[0, :])


# Hを次元だけ定義、乱数を代入
H = np.zeros((K, J))

for k in range(K):
    for j in range(J):
        H[k, j] = random.random()*0.1


# 誤差をプロット
H_error = update_H(X, W, H)


fig_e = plt.figure(figsize=(4, 6))
ax_e = fig_e.add_subplot(1, 1, 1)

ax_e.plot(range(len(H_error)), H_error, "o-", markersize=1, label="error")


ax_e.legend()
ax_e.grid()
ax_e.set_xlabel('Number of iterations')
ax_e.set_ylabel('Error')

plt.show()


# 18個の各音に対するH成分を計算してプロットする
sounds = calc_weight(H)

scale = ["ド(C3)", "ド#(C#3)", "レ(D3)", "レ#(D#3)", "ミ(E3)", "ファ(F3)", "ファ#(F#3)", "ソ(G3)", "ソ#(G#3)",
         "ラ(A3)", "ラ#(A#3)", "シ(B3)", "ド(C4)", "ド#(C#4)", "レ(D4)", "レ#(D#4)", "ミ(E4)", "ファ(F4)"]
fig = plt.figure(figsize=(4, 6))
ax = fig.add_subplot(1, 1, 1)

for i in range(len(sounds[:, 0])):
    # ラベルに使う数字

    if i in {0, 4, 8, 12, 16}:
        ax.plot(range(len(sounds[i, :])), sounds[i, :],
                "o-", markersize=5, label="{}".format(scale[i]))
    elif i in {2, 6, 10, 14}:
        ax.plot(range(len(sounds[i, :])), sounds[i, :],
                "*-", markersize=5, label="{}".format(scale[i]))
    elif i in {3, 7, 11, 15}:
        ax.plot(range(len(sounds[i, :])), sounds[i, :],
                "v-", markersize=5, label="{}".format(scale[i]))
    elif i in {1, 5, 9, 13, 17}:
        ax.plot(range(len(sounds[i, :])), sounds[i, :],
                "^-", markersize=5, label="{}".format(scale[i]))

ax.legend(bbox_to_anchor=(1, 1), loc='upper left',
          borderaxespad=0, fontsize=8)
ax.grid()
ax.set_xlabel('Frame ID')
ax.set_ylabel('H')

plt.show()
