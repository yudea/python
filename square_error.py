# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series, DataFrame
from numpy.random import normal

NumberOfData = 10 #データ数
Dimension = [0, 1, 3, 9] #多項式の次数

#学習データ、テストデータの生成
def create_dataset(num):
	dataset = DataFrame(columns = ['x','y'])
	for i in range(num):
		x = float(i)/float(num-1)
		y = np.sin(2*np.pi*x) + normal(scale=0.3)
		dataset = dataset.append(Series([x,y],index = ['x','y']), ignore_index = True)
	return dataset

#誤差関数
def error(dataset_test, f):
	err=0.0
	for index, line in dataset_test.iterrows():
		x, y = line.x, line.y
		err = err + (y - f(x))**2/2
	return np.sqrt(2*err/len(dataset_test))

#Φ行列によるベクトルwの算出
def solve(dataset, m):
	t = dataset.y
	phi = DataFrame()
	for i in range(0, m+1):
		p = dataset.x**i
		p.name = "x**%d" % i
		phi = pd.concat([phi,p], axis = 1)
	ws = np.linalg.inv(np.dot(phi.T, phi))
	ws = np.dot(np.dot(ws, phi.T), t)
	
	def f(x):
		y = 0
		for i, w in enumerate(ws):
			y = y + w * (x ** i)
		return y
	return (f, ws)

train_dataset = create_dataset(NumberOfData)
test_dataset = create_dataset(NumberOfData)
df_ws = DataFrame()

fig = plt.figure()
for c, dim in enumerate(Dimension):
	f, ws = solve(train_dataset, dim)
	df_ws = df_ws.append(Series(ws, name="Dim=%d" % dim))

	subplot = fig.add_subplot(2,2,c+1)
	subplot.set_xlim(-0.05, 1.05)
	subplot.set_ylim(-1.2,1.2)
	subplot.set_title("Dim=%d" % dim)

	subplot.scatter(train_dataset.x, train_dataset.y, color="black")

#真の曲線
	linex=np.linspace(0,1,101)
	liney=np.sin(2*np.pi*linex)
	subplot.plot(linex, liney, color="red")

#求めた曲線
	linex=np.linspace(0,1,101)
	liney=f(linex)
	label="pred"
	subplot.plot(linex, liney, color="blue", label=label)
	subplot.legend()

print "Table of coefficeint"
print df_ws.transpose()

#トレーニングセットとテストセットでの誤差の変化
df = DataFrame()
for m in range(0, 10): #多項式の次数
	f,ws = solve(train_dataset, m)
	training_error = error(train_dataset, f)
	test_error = error(test_dataset, f)
	df = df.append(Series([training_error, test_error], index = ['Training set', 'Test set']), ignore_index = True)
print df
df.plot(title='RMS Error')	
plt.show()



