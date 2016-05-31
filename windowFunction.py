#coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import wave
import scipy.fftpack

N = 512



if __name__ == '__main__':
	start = 0
	N = 300 # FFTのサンプル数

	hammingWindow = np.hamming(N)
	hanningWindow = np.hanning(N)
	bartlettWindow = np.bartlett(N)
	balckmanWindow = np.blackman(N)

	waveFile = wave.open("../voicesample/k_ishihara_narration1_left.wav", "r")
	freqSampling = waveFile.getframerate() #サンプリング周波数
	x = waveFile.readframes(waveFile.getnframes())
	x = np.frombuffer(x, dtype = "int16") / 32768.0 # 0-1に正規化

	originalData = x
	windowedData = hammingWindow * x[start:start+N]

	originalDFT = np.fft.fft(originalData)
	windowedDFT = np.fft.fft(hammingWindow)


	plt.subplot(211)
	plt.plot(originalData)


	plt.show()





