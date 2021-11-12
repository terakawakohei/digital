import csv
import numpy as np
import math
import matplotlib.pyplot as plt
import sys

args = sys.argv

#評価データを読み込む
f = open(args[1]+"_O.csv","r")
reader = csv.reader(f)
O = [ [float(s) for s in e] for e in reader ]

#読み込んだ信号の長さ
M=len(O)

#信号を256個ずつ区切る 
r=256




#DFTの値は左右対称となるため、128次元めまでを考えれば良い、かつO[m][k]のデータは捨てたので、127次元目までの値を持つ
vecSize=int(r/2)-1

#読み込む学習データファイル名
filename=['coffee','buzzer','whistle','do','mi']


#対数確率を計算する

Pr=[]

for n in filename:
    f = open(n+"_myu.csv","r")
    reader = csv.reader(f)
    myu = sum([ [float(s) for s in e]  for e in reader ],[])

    f = open(n+"_sigma.csv","r")
    reader = csv.reader(f)
    sigma = sum([ [float(s) for s in e]  for e in reader ],[])


    def log_normal_distribution(l):
        const= vecSize*math.log(2*math.pi)
        for k in range(vecSize):
            z = math.log(sigma[k])
            const += z
            sum=const
        
        for k in range(vecSize):
            xmm = O[l][k] - myu[k]
            sum += xmm*xmm/sigma[k]

        return -0.5*sum
    
    Pr.append(np.sum([log_normal_distribution(num) for num in range(M)]))
    
    
i=Pr.index(max(Pr))

for index, n in enumerate(filename):
    print(n+":"+str(Pr[index]))

print("======================")
print("this is {}".format(filename[i]))





