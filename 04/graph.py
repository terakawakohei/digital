import matplotlib.pyplot as plt
import numpy as np
# #バイナリデータをcsvファイルに変換したものを読み込む
# with open('class1.csv') as f:
#     reader = csv.reader(f)
#     l = [row for row in reader]


# class1_data=[[float(v) for v in row] for row in l]

# with open('class2.csv') as f:
#     reader = csv.reader(f)
#     l = [row for row in reader]


# class2_data=[[float(v) for v in row] for row in l]


class1_x1, class1_x2 = np.genfromtxt(
    "./class1.csv", delimiter=',', unpack=True)
class2_x1, class2_x2 = np.genfromtxt(
    "./class2.csv", delimiter=',', unpack=True)

# test_x1, test_x2 = np.genfromtxt(
#     "./test.csv", delimiter=',', unpack=True)


fig = plt.figure(figsize=(4, 6))
ax = fig.add_subplot(111)

ax.scatter(class1_x1, class1_x2, s=10)


ax.scatter(class2_x1, class2_x2, s=10)


# ax.scatter(test_x1, test_x2, s=10)


plt.xlabel('1st order')
plt.ylabel('2nd orderr')
plt.legend()
plt.grid()

plt.show()
