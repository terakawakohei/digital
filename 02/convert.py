import numpy as np
import matplotlib.pyplot as plt
import math
import csv
import sys

args = sys.argv


data_axis, data_value = np.loadtxt(
    "./"+args[1]+".csv", delimiter=',', unpack=True)



#読み込んだ信号の長さ
data_size=len(data_value)


#信号を256個ずつ区切る 
r=256

#切り出した信号の個数
M=int(data_size/256)

print("Mは、{}".format(M))

#長さ256の短時間フーリエ変換がM個並んでいる
X_r=[[0 for i in range(r)] for j in range(M)]
X_i=[[0 for i in range(r)] for j in range(M)]

for m in range(M):

    for k in range(r):
        for r_i in range(r):
            #data_valueから取り出す信号は0~data_sizeで考える
            index=m*r+r_i
            X_r[m][k] += data_value[index] * math.cos(2 * math.pi * k * index / r)
            X_i[m][k] += (-1) * data_value[index] * math.sin(2 * math.pi * k * index / r)

    


#DFTの値は左右対称となるため、128次元めまでを考えれば良い
vecSize=int(r/2)

#対数パワースペクトルを求める
O=[[0 for i in range(vecSize)] for j in range(M)]

for m in range(M):
    for k in range(vecSize):

        O[m][k]=math.log(X_r[m][k] * X_r[m][k] + X_i[m][k] * X_i[m][k])

#0次元目の値を捨てる
for m in range(M):
    del O[m][0]

#対数パワースペクトルを書き出し
with open(args[1]+'_O.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(O)


#正規分布を求める

#平均値ベクトルmyu,共分散行列の対角要素sigmaを求め、書き出す
myu=[0] * (vecSize-1)

for k in range(vecSize-1):
    for m in range(M):
        myu[k]+=O[m][k]
    
    myu[k]=myu[k]/M

with open(args[1]+'_myu.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(myu)

sigma=[0] * (vecSize-1)

for k in range(vecSize-1):
    for m in range(M):
        sigma[k]+=(O[m][k]-myu[k])*(O[m][k]-myu[k])
    
    sigma[k]=sigma[k]/M

with open(args[1]+'_sigma.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(sigma)


    

