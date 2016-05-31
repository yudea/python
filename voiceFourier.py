#coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import wave
import os

os.chdir("../voicesample")


def waveread(filename):
	waveData = wave.open(filename, "r")
	fs = waveData.getframerate()
	x = waveData.readframes(waveData.getframerate())
	x = np.frombuffer(x, dtype = "int16") / 32768.0
	waveData.close()
	return x, float(fs)

if __name__ == '__main__':
	#波形の表示
	wav, fs = waveread("k_ishihara_narration1_left.wav")
	t = np.arange(0.0, len(wav) / fs, 1 / fs)

	plt.subplot(211)
	plt.plot(t * 1000, wav)
	plt.xlabel("time [ms]")
	plt.ylabel("amplitude")


	hanningWindow = np.hanning(len(wav))
	waveData = wav * hanningWindow

	plt.subplot(212)
	plt.plot(waveData)
	plt.xlabel("time [ms]")
	plt.ylabel("amplitude")
	plt.title("hanning data")
	plt.show()

	n = 2048 #FFTサンプル数
	#離散フーリエ
	dft = np.fft.fft(waveData, n)
	Adft = np.abs(dft)
	Pdft = np.abs(dft) ** 2
	fscale = np.fft.fftfreq(n, d = 1.0 / fs)

	plt.subplot(211)
	plt.plot(fscale[0:n/2], Adft[0:n/2])
	plt.xlabel("freqency [Hz]")
	plt.ylabel("amplitude")

	plt.subplot(212)
	plt.plot(fscale[0:n/2], Pdft[0:n/2])
	plt.xlabel("frequency [Hz]")
	plt.ylabel("power spectrum")
	plt.show()

	#対数スペクトル
	AdftLog = 20 * np.log10(Adft)
	PdftLog = 10 * np.log10(Pdft)

	plt.subplot(211)
	plt.plot(fscale[0:n/2], AdftLog[0:n/2])
	plt.xlabel("frequency [Hz]")
	plt.ylabel("log amplitude spectrum")

	plt.subplot(212)
	plt.plot(fscale[0:n/2], PdftLog[0:n/2])
	plt.xlabel("frequency [Hz]")
	plt.ylabel("log power spectrum")

	plt.show()

	#ケプストラム分析
	#対数スペクトルを逆フーリエ
	cps = np.real(np.fft.ifft(AdftLog))
	plt.plot(cps[0:n/2])
	plt.ylim(-5, 5)
	plt.show()

	# ローパスリフタ
    # ケプストラムの高次成分を0にして微細構造を除去し、
    # 緩やかなスペクトル包絡のみ抽出
	cepCoef = 20             # ケプストラム次数
	cpsLif = np.array(cps)   # arrayをコピー
	# 高周波成分を除く（左右対称なので注意）
	cpsLif[cepCoef:len(cpsLif) - cepCoef + 1] = 0

	# ケプストラム領域をフーリエ変換してスペクトル領域に戻す
	# リフタリング後の対数スペクトル
	dftSpc = np.fft.fft(cpsLif, n)

	plt.plot(fscale[0:n/2], AdftLog[0:n/2])
	plt.plot(fscale[0:n/2], dftSpc[0:n/2], color = "red")
	plt.xlabel("frequency [Hz]")
	plt.ylabel("log amplitude")

	plt.show()



