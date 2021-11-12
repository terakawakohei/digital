import csv
import numpy as np
import math
import matplotlib.pyplot as plt


f = open("log_likelihood_class1.csv","r")
reader = csv.reader(f)
log_likelihood_class1 = sum([ [float(s) for s in e]  for e in reader ],[])

f = open("log_likelihood_class2.csv","r")
reader = csv.reader(f)
log_likelihood_class2 = sum([ [float(s) for s in e]  for e in reader ],[])


#読み込んだデータの長さ
iteration_class1=len(log_likelihood_class1)
iteration_class2=len(log_likelihood_class2)









fig = plt.figure(figsize=(4, 6))
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2, 1,2)

ax1.plot(range(iteration_class1), log_likelihood_class1, "o-", markersize=1)
ax1.set_title("class1")


ax2.plot(range(iteration_class2), log_likelihood_class2, "o-", markersize=1)
ax2.set_title("class2")

plt.xlabel('iteration')
plt.ylabel('Log-likelihood')
ax1.legend()
ax2.legend()



plt.show()
