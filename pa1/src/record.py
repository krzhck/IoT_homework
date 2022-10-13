import wave
import pyaudio
import numpy as np
from matplotlib import pyplot as plt


chunk = 1024
form = pyaudio.paInt16
chan = 1
#sampleRate = 48000
#duration = 3

filename = '../wav/output.wav'

if __name__ == "__main__":

	try:
		sampleRate = int(input('采样率 (默认 48000)：'))
	except Exception as e:
		sampleRate = 48000

	try:
		duration = float(input('持续时间 (s，默认 3)：'))
		if duration <= 0: raise Exception()
	except Exception as e:
		duration = 3

	p = pyaudio.PyAudio()
	stream = p.open(format = form,
		channels = chan,
		rate = sampleRate,
		input = True,
		frames_per_buffer = chunk)

	print("Recording...")

	frames = []
	for i in range(0, int(sampleRate / chunk * duration)):
		data = stream.read(chunk)
		frames.append(data)
	print(str(duration) + "s recording done.")

	stream.stop_stream()
	stream.close()

	p.terminate()

	wf = wave.open(filename, 'wb')
	wf.setnchannels(chan)
	wf.setsampwidth(p.get_sample_size(form))
	wf.setframerate(sampleRate)
	wf.writeframes(b''.join(frames))
	wf.close