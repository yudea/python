#coding:utf-8
import wave
from numpy import *
from pylab import *
import os

os.chdir("../voicesample")

def prtintWaveInfo(wf):
	"""WAVEファイルの情報を取得"""
	print "チャンネル数:", wf.getnchannels()
	print "サンプル幅:", wf.getsampwidth()
	print "サンプリング周波数",wf.getframerate()
	print "フレーム数:", wf.getnframes()
	print "パラメータ:", wf.getparams()
	print "長さ（秒）:", float(wf.getnframes() / wf.getframerate())

if __name__ == '__main__':
	wf = wave.open("k_ishihara_narration1_left.wav", "r")
	prtintWaveInfo(wf)

	buffer = wf.readframes(wf.getnframes())
	print len(buffer)

	date = frombuffer(buffer, dtype = "int16")

	plot(date[0:44100])
	show()