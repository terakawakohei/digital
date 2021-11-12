import csv
import numpy as np
import math
import matplotlib.pyplot as plt


f = open("coffee_O.csv","r")
reader = csv.reader(f)
coffee = [ [float(s) for s in e]  for e in reader ]

f = open("buzzer_O.csv","r")
reader = csv.reader(f)
buzzer = [ [float(s) for s in e]  for e in reader ]

f = open("whistle_O.csv","r")
reader = csv.reader(f)
whistle = [ [float(s) for s in e]  for e in reader ]

f = open("do_O.csv","r")
reader = csv.reader(f)
do = [ [float(s) for s in e]  for e in reader ]

f = open("mi_O.csv","r")
reader = csv.reader(f)
mi = [ [float(s) for s in e]  for e in reader ]

#読み込んだ信号の長さ
coffee_M=len(coffee)
buzzer_M=len(buzzer)
whistle_M=len(whistle)
do_M=len(do)
mi_M=len(mi)

#信号を256個ずつ区切る 
r=256




#DFTの値は左右対称となるため、128次元めまでを考えれば良い、かつO[m][k]のデータは捨てたので、127次元目までの値を持つ
vecSize=int(r/2)-1


#正規分布を求める
#平均値ベクトルと分散を求める

myu_coffee=[0] * vecSize

for k in range(vecSize):
    for m in range(coffee_M):
        myu_coffee[k]+=coffee[m][k]
    
    myu_coffee[k]=myu_coffee[k]/coffee_M


myu_buzzer=[0] * vecSize

for k in range(vecSize):
    for m in range(buzzer_M):
        myu_buzzer[k]+=buzzer[m][k]
    
    myu_buzzer[k]=myu_buzzer[k]/buzzer_M

myu_whistle=[0] * vecSize

for k in range(vecSize):
    for m in range(whistle_M):
        myu_whistle[k]+=whistle[m][k]
    
    myu_whistle[k]=myu_whistle[k]/whistle_M


myu_do=[0] * vecSize

for k in range(vecSize):
    for m in range(do_M):
        myu_do[k]+=do[m][k]
    
    myu_do[k]=myu_do[k]/do_M

myu_mi=[0] * vecSize

for k in range(vecSize):
    for m in range(mi_M):
        myu_mi[k]+=mi[m][k]
    
    myu_mi[k]=myu_mi[k]/mi_M



fig = plt.figure(figsize=(4, 6))
ax = fig.add_subplot(111)
ax.plot(range(vecSize), myu_coffee, "o-", markersize=1,label="coffee")
ax.plot(range(vecSize), myu_buzzer, "o-", markersize=1,label="buzzer")
ax.plot(range(vecSize), myu_whistle, "o-", markersize=1,label="whistle")
ax.plot(range(vecSize), myu_do, "o-", markersize=1,label="do")
ax.plot(range(vecSize), myu_mi, "o-", markersize=1,label="mi")

plt.xlabel('Frequency index of k')
plt.ylabel('Log-power')
plt.legend()


plt.show()
