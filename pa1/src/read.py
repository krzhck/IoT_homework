import numpy as np
import wave
import pyaudio
from matplotlib import pyplot as plt

chunk = 1024

def playWav(path):
	wf = wave.open(path, 'rb')
	p = pyaudio.PyAudio()
	stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
		channels = wf.getnchannels(),
		rate = wf.getframerate(),
		output = True)

	data = wf.readframes(chunk)
	print('playing sound...')
	while len(data) > 0:
		stream.write(data)
		data = wf.readframes(chunk)
	stream.stop_stream()
	stream.close()
	wf.close()
	p.terminate()


if __name__ == "__main__":
	path = '../wav/' + input('file: ')
	playWav(path)
	o = np.memmap(path, dtype = 'h', mode = 'r')
	plt.plot(o)
	plt.show()