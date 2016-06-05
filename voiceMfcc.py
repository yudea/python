#coding:utf-8

import numpy as np
import wave 
import matplotlib.pyplot as plt
import os
import scipy.signal

os.chdir("../voicesample")

def waveread(filename):
	waveData = wave.open(filename, "r")
	fs = waveData.getframerate()
	x = waveData.readframes(waveData.getframerate())
	x = np.frombuffer(x, dtype = "int16") / 32768.0
	waveData.close()
	return x, float(fs)

def preEmphasis(signal, p):
	"""プリエンファシスフィルタ"""
	#係数(1.0, -p)のFIRフィルタを作成
	return scipy.signal.lfilter([1.0, -p], 1, signal)

def hz2mel(freq):
	"""Hzをmelに変換"""
	return 1127.01048 * np.log(freq / 700.0 + 1.0)

def mel2hz(mel):
	return 700.0 * (np.exp(mel / 1127.01048) - 1.0)
	

def melFilterBank(fs, n, numChannel):
	"""メルフィルタバンクの作成"""
	fmax = fs / 2 #ナイキスト周波数
	melmax = hz2mel(fmax)#ナイキスト周波数のメル単位への変換
	nmax = n / 2
	df = fs / n #周波数解像度（周波数インデックス１あたりのHｚ幅）
	dmel = melmax / (numChannel + 1)
	melcenters = np.arange(1, numChannel + 1) * dmel#メル尺度における各フィルタの中心
	fcenters = mel2hz(melcenters)
	indexcenter = np.round(fcenters / df)
	indexstart = np.hstack(([0], indexcenter[0:numChannel -1]))
	indexstop = np.hstack((indexcenter[1:numChannel], [nmax]))



if __name__ == '__main__':
	#音声をロード
	wav, fs = waveread("k_ishihara_narration1_left.wav")
	t = np.arange(0.0, len(wav) / fs, 1/fs)

	#音声の切り出し（必要ならば）
	wavAnalyDate = wav
	time = t

	#波形のプロット
	plt.subplot(221)
	plt.plot(t * 1000, wavAnalyDate)
	plt.xlabel("time [ms]")
	plt.ylabel("amplitude")

	#プリエンファシスフィルタをかける
	p = 0.9 #プリエンファシス係数
	preEmphasisDate = preEmphasis(wav, p)

	plt.subplot(222)
	plt.plot(t * 1000, preEmphasisDate)
	plt.xlabel("time")
	plt.ylabel("amp")
	plt.title("preEmphasised Data")
	
	n = 2048
	dft = np.fft.fft(wavAnalyDate, n)
	Adft = np.abs(dft)
	Pdft = np.abs(dft) ** 2
	fscale = np.fft.fftfreq(n, d=1.0/fs)

	dftPreEM = np.fft.fft(preEmphasisDate, n)
	AdftPreEm = np.abs(dftPreEM)
	PdftPreEm = np.abs(dftPreEM) ** 2

	plt.subplot(223)
	plt.plot(fscale[0:n/2], Pdft[0:n/2])
	plt.title("FFT without PreEm")

	plt.subplot(224)
	plt.plot(fscale[0:n/2], PdftPreEm[0:n/2])
	plt.title("FFT with PreEm")

	plt.show()

	#ハミング窓をかける
	hammingWindow = np.hamming(len(wavAnalyDate))
	wavAnalyDateHamminged = wavAnalyDate * hammingWindow

	specOfWavHamm = np.abs(np.fft.fft(wavAnalyDateHamminged, n))

	plt.plot(fscale[0:n/2], specOfWavHamm[0:n/2])
	plt.xlabel("freqency")
	plt.ylabel("amplitude")
	plt.title("hamminged wave spec")
	plt.show()

