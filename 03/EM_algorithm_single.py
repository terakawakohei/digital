import numpy as np
import matplotlib.pyplot as plt
import math
import csv

#バイナリデータをcsvファイルに変換したものを読み込む
with open('class1.csv') as f:
    reader = csv.reader(f)
    l = [row for row in reader]


class1_data=[[float(v) for v in row] for row in l]

with open('class2.csv') as f:
    reader = csv.reader(f)
    l = [row for row in reader]


class2_data=[[float(v) for v in row] for row in l]



#x:列ベクトル   myu:列ベクトル
def func_normal_distribution(x_n,myu,sigma):

    const=1/(2*math.pi*np.linalg.det(sigma))
    exponent=-0.5*((x_n-myu).T*sigma.I*(x_n-myu))

    return const*math.exp(exponent)


def calc_gamma(k,w,x_n,myu,sigma):


    numerator=w[k]*func_normal_distribution(x_n,myu[k],sigma[k])

    denominator=0

    for l in range(len(w)):
      
        denominator+=w[l]*func_normal_distribution(x_n,myu[l],sigma[l])

    # print("{}/{},={}".format(numerator,denominator,numerator/denominator))

    return float(numerator/denominator)



def calc_log_likelihood(data,myu,sigma,w):

    sum_log=0
    for n in range(N):
        sum=0
        for k in range(K):
            x=np.matrix(data[n]).T
            sum+=w[k]*func_normal_distribution(x,myu[k],sigma[k])
        
        sum_log+=math.log(sum)

    return sum_log


def estimate_param(class_name,data,myu,sigma,w,gamma):
    #対数尤度の初期値を計算

    next=calc_log_likelihood(data,myu,sigma,w)


    #2.Eステップ

    prev=0

    iteration=0

    #対数尤度のグラフを作成するため、対数尤度を保存しておく

    #初期値を追加
    log_likelihood=[next]


    while abs(prev-next) > 1.0e-2:
    # while iteration<200:

        for n in range(N):
            for k in range(K):
                x=np.matrix(data[n]).T
                # if(iteration<5):
                #     print("before=={}".format(gamma[n][k]))

                # if(n==1):
                #     print("myu={}".format(myu))
                #     print("sigma={}".format(sigma))
                #     print("-------")
                gamma[n][k]=calc_gamma(k,w,x,myu,sigma)
           
                # if(iteration<20):
                #     print("after=={}".format(gamma[n][k]))
                #     print("--------")

           
        for k in range(K):

            N_k=[0]*K
            for n in range(N):
                N_k[k]+=gamma[n][k]

            new_myu=0
            new_sigma=0
            for n in range(N):
                x=np.matrix(data[n]).T

                new_myu+=gamma[n][k]*x
                new_sigma+=gamma[n][k]*(x-myu[k])*(x-myu[k]).T


            #myuパラメータの更新
            myu[k]=new_myu/N_k[k]
            #sigmaパラメータの更新
            sigma[k]=new_sigma/N_k[k]

            w[k]=N_k[k]/N

    

        prev=next
        next=calc_log_likelihood(data,myu,sigma,w)

        log_likelihood.append(next)

        iteration+=1

    with open('log_likelihood_'+class_name+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(log_likelihood)

    print("-----------------------")
    print(class_name+" : 結果")
    print("-----------------------")

    print(class_name+"の平均値ベクトルは,\nmyu[0]=\n{}".format(myu[0]))
    print(class_name+"の共分散行列は,\nsigma[0]=\n{}".format(sigma[0]))

    return myu,sigma,next

def combined_normal_distribution(x,myu,sigma,w):
    result=0
    for k in range(K):
        result+=w[k]*func_normal_distribution(x,myu[k],sigma[k])
    
    return result

def distinguish(data,myu,sigma):

    for n in range(N):
        temp=[]
        x=np.matrix(data[n]).T
        



#初期化

N=len(class1_data)
print('サンプル数Nは、{}'.format(N))

#重ね合わせは２
K=1

#class1のパラメータ推定のための初期化
class1_myu=[np.matrix([[1],[1]])]


class1_sigma=[np.matrix([[1,0], [0,1]])]

class1_w=[1]

class1_gamma = [[0] * K for n in range(N)]

#class1のパラメータ推定を行う
class1_myu,class1_sigma,class1_log_likelihood=estimate_param("class1",class1_data,class1_myu,class1_sigma,class1_w,class1_gamma)


#class2のパラメータ推定のための初期化
class2_myu=[np.matrix([[1],[1]])]


class2_sigma=[np.matrix([[1,0], [0,1]])]

class2_w=[1]

class2_gamma = [[0] * K for n in range(N)]

#class2のパラメータ推定を行う
class2_myu,class2_sigma,class2_log_likelihood=estimate_param("class2",class2_data,class2_myu,class2_sigma,class2_w,class2_gamma)

print("-----------------------")
print("クラス識別")
print("")
print("class1,class2の学習データから求めた単一の正規分布を用いて識別を行う")
print("-----------------------")
#混合正規分布を用いたクラス識別

#class1を判別
print("class1.datのデータを識別する")

print("class1の対数尤度は、{}".format(class1_log_likelihood))

class1_result=[]
for n in range(N):
    x=np.matrix(class1_data[n]).T
    class1=combined_normal_distribution(x,class1_myu,class1_sigma,class1_w)
    class2=combined_normal_distribution(x,class2_myu,class2_sigma,class1_w)

    if class1>class2:
        #与えたデータがclass1.datなので、xのデータがclass1に識別されるなら1(true)をappend
        class1_result.append(1)
    else:
        #与えたデータがclass1.datなので、xのデータがclass2に識別されるなら0(false)をappend
        class1_result.append(0)
    
class1_rate=(sum(class1_result)/len(class1_result))*100
print("class1.datのデータの、class1に対する識別率は{}%".format(class1_rate))


print("-----------------------")

#class2を判別
print("class2.datのデータを識別する")
class2_result=[]
for n in range(N):
    x=np.matrix(class2_data[n]).T
    class1=combined_normal_distribution(x,class1_myu,class1_sigma,class1_w)
    class2=combined_normal_distribution(x,class2_myu,class2_sigma,class1_w)

    if class1<class2:
        #与えたデータがclass2.datなので、xのデータがclass2に識別されるなら1(true)をappend
        class2_result.append(1)
    else:
        #与えたデータがclass2.datなので、xのデータがclass1に識別されるなら0(false)をappend
        class2_result.append(0)
    
class2_rate=(sum(class2_result)/len(class2_result))*100
print("class2.datのデータの、class2に対する識別率は{}%".format(class2_rate))




class1_x1, class1_x2 = np.genfromtxt("./class1.csv", delimiter=',', unpack=True)
class2_x1, class2_x2 = np.genfromtxt("./class2.csv", delimiter=',', unpack=True)







fig = plt.figure(figsize=(4, 6))
ax = fig.add_subplot(111)

ax.scatter(class1_x1, class1_x2,s=10)
ax.scatter(float(class1_myu[0][0][0]),float(class1_myu[0][1][0]),s=50,c='red',marker="x",label="class1")

ax.scatter(class2_x1, class2_x2,s=10)
ax.scatter(float(class2_myu[0][0][0]),float(class2_myu[0][1][0]),s=50,c='green',marker="x",label="class2")


ax.set_xlim(0.4, 2.2)
ax.set_ylim(0.6, 2)

plt.xlabel('1st order')
plt.ylabel('2nd orderr')
plt.legend()
plt.grid()

plt.show()








        




