import wave
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal


def open_wave_file(name):
    f = wave.open(name, "rb")
    params = f.getparams()
    [_, _, framerate, nframes] = params[:4]
    str_sig = f.readframes(nframes)
    f.close()
    sig = np.frombuffer(str_sig, dtype=np.short)
    return sig, framerate

def encode_pulse(codes, filename):
    fs = 48000
    f = 20000
    time = 0.001
    t = np.arange(0, time, 1 / fs)
    impulse = np.sin(2 * np.pi * f * t)
    delta = int(time*fs)
    pause0 = np.zeros(delta)
    pause1 = np.zeros(2 * delta)
    output = np.concatenate([np.zeros(3 * delta),impulse])
    for i in range(len(codes)):
		# use pause0 as interval if original code is 0
        if codes[i] == 0:
            output = np.concatenate([output, pause0, impulse])
		# use pause1 as interval if original code is 1
        else:
            output = np.concatenate([output, pause1, impulse])
    output = np.concatenate([output, impulse])
    sig = np.array(output).astype(np.short)
    file = wave.open(filename, mode='wb')
    file.setframerate(fs)
    file.setnchannels(1)
    file.setsampwidth(2)
    file.writeframes(sig)
    return sig


def decode_pulse(filename):
    sig, sample_freq = open_wave_file(filename)
    base_freq = 20e3
	# bandpass [0.95*base_freq,1.05*base_freq]
    [b, a] = signal.ellip(5, 0.5, 60, (base_freq * 1.95 / sample_freq, base_freq * 2.05 / sample_freq),
                          btype='bandpass', analog=False, output='ba')
    sig = signal.filtfilt(b, a, sig)
    n = len(sig)
    window = 100
    half_window = int(window / 2)
    impulse_fft = np.zeros(n)
    for i in range(n - window):
        y = abs(np.fft.fft(sig[i:i + window - 1]))
        index_impulse = round(base_freq / sample_freq * window)
        impulse_fft[i] = max(y[index_impulse - 2:index_impulse + 2])
    impulse_fft = impulse_fft / max(impulse_fft) # normalization
    position_impulse = []
    for i in range(half_window + 1, n - half_window):
        if impulse_fft[i] > 0.5 and impulse_fft[i] == max(impulse_fft[i - half_window:i + half_window]):
            position_impulse.append(i)
    N = len(position_impulse)
    delta_impulse = [position_impulse[i + 1] - position_impulse[i] for i in range(N - 1)]
    codes = []
    for i in range(N - 1):
        if delta_impulse[i] > 130:
            codes.append(1)
        elif 70 < delta_impulse[i] < 110:
            codes.append(0)
    return codes


if __name__ == '__main__':
    input_seq = input('输入01序列：')
    file_name = ''
    while len(file_name) == 0:
        file_name = input('另存为 (.wav)：')
    file_name = file_name + '.wav'
    seq = []
    for d in input_seq:
        seq.append(int(d))
    print(seq)
    plt.subplot(211)
    plt.plot(seq, 'r')
    plt.title("Before pulse encode")
    sig=encode_pulse(seq, file_name)
    ans = decode_pulse(file_name)
    plt.subplot(212)
    plt.plot(ans, 'r')
    plt.title("After pulse decode")
    plt.show()
