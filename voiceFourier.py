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
	plt.plot(t * 1000, wav)
	plt.xlabel("time [ms]")
	plt.ylabel("amplitude")
	plt.show()