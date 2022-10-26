import wave
import matplotlib.pyplot as plt
import numpy as np
from math import sin
from scipy import signal

def seq0(n, N):
    return 1

def seq1(n, N):
    return 1 - n / N

def seq2(n, N):
    return sin(2 * np.pi * n / N)

def DFT(N, seq):
    a = [seq(i, N) for i in range(N)]
    return np.abs(np.fft.fft(a) / N)

# 绘制时频图
def spectrogram(x, nperseg, sub_no):
    f, t, zxx = signal.stft(x, nperseg=nperseg)
    plt.subplot(1, 2, sub_no)
    plt.pcolormesh(t, f, np.abs(zxx))
    plt.colorbar()
    plt.title('win size ' + str(nperseg))
    plt.ylabel('Freq(Hz)')
    plt.xlabel('Time(s)')
    plt.tight_layout()

# 返回音频数据，帧数，帧率
def open_wave_file(name):
    f = wave.open(name, "rb")
    params = f.getparams()
    [nchannels, sampwidth, framerate, nframes] = params[:4]
    str_data = f.readframes(nframes)
    f.close()
    data = np.frombuffer(str_data, dtype=np.short)
    return data, nframes, framerate


if __name__ == '__main__':

    # 1
    # DFT
    seq_list = [seq0, seq1, seq2]
    N_list = [32, 128, 1024]
    for seq in seq_list:
        for N in N_list:
            plt.subplot(3, 1, N_list.index(N) + 1)
            plt.title('N = ' + str(N))
            freq = np.linspace(0, N, N)
            plt.plot(freq, DFT(N, seq))
            plt.xlabel("Freq(Hz)")
            plt.ylabel("Amplitude")
        plt.show()

    # 2
    wave_data, _, fm = open_wave_file(r"../wav/res.wav")

    # (a) 绘制信号频谱图
    nfft = len(wave_data)
    wave_data_tmp = np.concatenate(((wave_data), np.zeros(nfft - len(wave_data))))
    fx = [i * fm / nfft for i in range((nfft >> 1) - 1)]
    data = np.abs(np.fft.fft(wave_data_tmp, nfft))
    data = data[1:len(data) >> 1]
    data = data / nfft * 2
    plt.subplot(1, 2, 1)
    plt.plot(fx, data)
    plt.title('Original')
    plt.xlabel("Freq(Hz)")
    plt.ylabel("Amplitude")

    # (b) 补0
    nfft = 10 * len(wave_data)
    wave_data_tmp = np.concatenate(((wave_data), np.zeros(nfft - len(wave_data))))
    fx = [i * fm / nfft for i in range((nfft >> 1) - 1)]
    data = np.abs(np.fft.fft(wave_data_tmp, nfft))
    data = data[1:len(data) >> 1]
    data = data / nfft * 2
    plt.subplot(1, 2, 2)
    plt.plot(fx, data)
    plt.title('Zero Padding')
    plt.xlabel("Freq(Hz)")
    plt.ylabel("Amplitude")

    plt.show()
    
    # (c) 时频分析

    spectrogram(wave_data[:round(len(wave_data) / 2)], 256, 1)
    spectrogram(wave_data[:round(len(wave_data) / 2)], 48, 2)
    plt.show()
