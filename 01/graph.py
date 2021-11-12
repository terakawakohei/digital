# import numpy as np
# import matplotlib.pyplot as plt

# data_set = np.loadtxt(
#     fname="amp.csv",
#     dtype="int",
#     delimiter=",",
# )

# # 散布図を描画 → scatterを使用する
# # 1行ずつ取り出して描画
# #plt.scatter(x座標の値, y座標の値)
# for data in data_set:
#     plt.scatter(data)

# plt.title("correlation")
# plt.xlabel("Average Temperature of SAITAMA")
# plt.ylabel("Average Temperature of IWATE")
# plt.grid()

# plt.show()
import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('amp.csv', names=['num1', 'num2'])
# plt.plot(range(0, 3999), df['num2'], marker="o", markersize=1)
# plt.xlabel('Number of Frequency Points')
# plt.show()


# 畳み込みのxとyを表示した時

# df = pd.read_csv('out_y.csv', names=['num1', 'num2'])
# plt.plot(range(0, 3999), df['num2'],
#          label="y[n]:output", marker="o", markersize=1)


# df = pd.read_csv('test.csv', names=['num1', 'num2'])
# plt.plot(range(0, 4000), df['num2'],
#          label="x[n]:input", marker="o", markersize=1)
# plt.legend()
# plt.show()

# hの振幅スペクトル

df = pd.read_csv('amp_h_cut.csv', names=['num1', 'num2'])
plt.plot(range(0, 2000), df['num2'], marker="o", markersize=1)
plt.xlabel('Frequency')
plt.legend()
plt.show()

# スペクトル全部

# df = pd.read_csv('amp_h.csv', names=['num1', 'num2'])
# plt.plot(range(0, 3999), df['num2'], label="h", marker="o", markersize=1)

# df = pd.read_csv('amp.csv', names=['num1', 'num2'])
# plt.plot(range(0, 3999), df['num2'], label="x[n]", marker="o", markersize=1)

# df = pd.read_csv('amp_y.csv', names=['num1', 'num2'])
# plt.plot(range(0, 3999), df['num2'], label="y[n]", marker="o", markersize=1)

# plt.xlabel('Number of Frequency Points')
# plt.legend()
# plt.show()
