#coding:utf-8

import scipy.io.wavfile as wio
import matplotlib.pyplot as plt


if __name__ == '__main__':
    rate, data = wio.read("kishihara_1_left.wav")
    pxx, freq, bins, t = plt.specgram(data,Fs = rate)
    plt.show()
    