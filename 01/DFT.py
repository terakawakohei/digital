import numpy as np
import matplotlib.pyplot as plt


# f = open(r"filter_h.dat", "rb")  # バイナリファイル読み込み。
# tmp = f.read()  # ファイルの中身をread()メソッドで一気に読み込み。
# for idx in range(len(tmp)):  # ファイルのバイト数をlen()で取り出して、その回数for文で回す、

#     print(tmp[idx])  # 1バイトづつデータを出力

# print(type(tmp[10]))


# with open('oto.raw', mode='rb') as fin:
#     content = fin.read()
#     print(content)

data03_axis1, data03_value1 = np.loadtxt(
    "./test.txt", delimiter=',', unpack=True)

data04_axis1, data04_value1 = np.loadtxt(
    "./test_h.txt", delimiter=',', unpack=True)


# fig = plt.figure(figsize=(4, 6))
# ax = fig.add_subplot(111)
# # ax.plot(data03_axis1, data03_value1, "o-", color="k", label="value1 of data01")
# ax.plot(data04_axis1, data04_value1, "o-", color="r", label="value1 of data04")

# ax.set_xlabel("axis1")
# ax.set_ylabel("value1")
# ax.legend(loc="upper left")
# plt.show()

# print(data03_value1)

# for i in range(31, 4000):
#     data04_value1.append([0])

z = np.zeros(3969)

a = np.append(data04_value1, z)

freq = np.fft.fft(a)
Amp = np.abs(freq)


plt.plot(Amp, label='|F(k)|')
plt.show()
