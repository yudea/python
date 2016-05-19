import os
import scipy
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
from scipy import io
from scipy.io import wavfile

os.chdir("../voicesample")

sample_rate, X = scipy.io.wavfile.read("k_ishihara_narration1_left.wav")
print sample_rate, X.shape
specgram(X, Fs=sample_rate, xextent=(0,30))

pxx, freq, bing, t = plt.specgram(X, Fs=sample_rate, xextent=(0,30))
plt.show()