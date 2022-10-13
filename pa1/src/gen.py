from ast import Str
import math
import struct
import wave

def sinewave(limit: int, a: int, omega: float, phase: float):
	for n in range(limit):
		yield int(a*math.sin(omega*n + phase*math.pi))


def generateSineWaveFile(file: Str, sampleRate: int, frequency: int, phase: float, duration: float):

	amplitude = 10000
	file = '../wav/' + file
	# 样本数
	totalSamples = int(duration*sampleRate)

	# 创建波形文件并循环写入采样数据。
	with wave.open(file, 'wb') as wf:
		# 单声道
		wf.setnchannels(1)
		# 设置采样量化位数为双字节16位。
		wf.setsampwidth(2)
		# 设置采样率
		wf.setframerate(sampleRate)
		# 样本间隔角旋转量
		omega = 2*math.pi/(sampleRate/frequency)
		# 遍历每一个采样点
		swave = sinewave(totalSamples, amplitude, omega, phase)
		for s in swave:
			# 将采样数据打包成字节数据写入波形文件。
			data = struct.pack('<h', int(s))
			wf.writeframes(data)
			# 以脚本运行时根据用户提示生成一个示例文件。


if __name__ == "__main__":

	info = ''

	filename = ''
	while len(filename) == 0:
		filename = input('文件名 (不能为空)：')
	filename = filename + '.wav'
	info = info + 'filename: ' + filename

	try:
		sampleRate = int(input('采样率 (默认 48000)：'))
	except Exception as e:
		sampleRate = 48000
	info = info + '\nsample rate: ' + str(sampleRate)

	try:
		frequency = int(input('频率 (Hz，默认 1000)：'))
		if frequency == 0: raise Exception()
	except Exception as e:
		frequency = 1000
	info = info + '\nfrequency: ' + str(frequency) + 'Hz'

	try:
		phase = float(input('初始相位 (* pi，默认 0)：'))
	except Exception as e:
		phase = 0
	info = info + '\nphase: ' + str(phase) + 'pi'

	try:
		duration = float(input('持续时间 (s，默认 3)：'))
		if duration <= 0: raise Exception()
	except Exception as e:
		duration = 3
	info = info + '\nduration: ' + str(duration) + 's'

	print('\ngenerating...')
	generateSineWaveFile(filename, sampleRate, frequency, phase, duration)

	print(info)