#coding:utf-8
import numpy as np
import pylab
import matplotlib.pyplot as plt

if __name__ == "__main__":
	#波の作成
	fs = 8820.0
	time = np.arange(0.0, 0.05, 1/fs)
	sinwav1 = 1.2*np.sin(2 * np.pi * 130 * time)
	coswav1 = 0.9*np.cos(2 * np.pi * 200 * time)
	sinwav2 = 1.8*np.sin(2 * np.pi * 260 * time)
	coswav2 = 1.4*np.cos(2 * np.pi * 320 * time)
	wavedata = 1.4 + (sinwav1 + sinwav2 + coswav1 + coswav2)

	plt.plot(time * 1000, wavedata)
	plt.xlabel("time [ms]")
	plt.ylabel("amplitude")
	plt.show()

# 離散フーリエ変換
n = 2048
dft = np.fft.fft(wavedata, n)
# 振幅スペクトル
Adft = np.abs(dft)
# パワースペクトル
Pdft = np.abs(dft) ** 2
# 周波数スケール
fscale = np.fft.fftfreq(n, d = 1.0 / fs)

#振幅を周波数ごとにプロット
plt.subplot(211)
plt.plot(fscale[0:n/2], Adft[0:n/2])
plt.xlabel("frequecy [Hz]")
plt.ylabel("amplitude")
plt.xlim(0, 700)
#パワースペクトル
plt.subplot(212)
plt.plot(fscale[0:n/2], Pdft[0:n/2])
plt.xlabel("freqency [Hz]")
plt.ylabel("power spectrum")
plt.xlim(0, 700)

plt.show()

#対数スペクトル（dBで表示）
plt.subplot(211)
plt.plot(fscale[0:n/2], 20 * np.log(Adft[0: n/2]))
plt.xlabel("frequency [Hz]")
plt.ylabel("log amplitude [dB]")
plt.xlim(0, 700)

#対数パワースペクトル
plt.subplot(212)
plt.plot(fscale[0:n/2], 20 * np.log(Pdft[0: n/2]))
plt.xlabel("frequency [Hz]")
plt.ylabel("log power spectrum [dB]")
plt.xlim(0, 700)

plt.show()











