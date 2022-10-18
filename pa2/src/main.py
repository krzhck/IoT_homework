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

def awgn(y, snr):
    snr = 10 ** (snr / 10.0)
    xpower = np.sum(y ** 2) / len(y)
    npower = xpower / snr
    return np.random.randn(len(y)) * np.sqrt(npower) + y

def modulate(codes, filename):
    fs = 48000
    f = 20000
    time = 0.001
    t = np.arange(0, time, 1 / fs)
    impulse = np.sin(2 * np.pi * f * t)
    delta = int(time*fs)
    pause0 = np.zeros(delta)
    pause1 = np.zeros(2 * delta)
    output = np.concatenate([np.zeros(3 * delta),impulse])
    for i in codes:
        if i == 0:
            output = np.concatenate([output, pause0, impulse])
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

def modulate_with_awgn(codes, filename, snr):
    sig = modulate(codes, filename)
    sig = awgn(sig, snr)
    file = wave.open(filename, mode='wb')
    file.setframerate(48000)
    file.setnchannels(1)
    file.setsampwidth(2)
    file.writeframes(sig)
    return sig


def demodulate(filename):
    sig, sample_freq = open_wave_file(filename)
    base_freq = 20000
    b, a = signal.butter(8, [base_freq * 1.95 / sample_freq, base_freq * 2.05 / sample_freq], 'bandpass')
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
    out_dict = '../wav/'
    wav_suffix = '.wav'
    while len(file_name) == 0:
        file_name = input('另存为 (.wav)：')
    file_path = out_dict + file_name + wav_suffix
    seq = []
    for d in input_seq:
        seq.append(int(d))
    print(seq)
    plt.subplot(211)
    plt.plot(seq, 'r')
    plt.title("Before pulse encode")
    sig=modulate(seq, file_path)
    ans = demodulate(file_path)
    #print(ans)
    plt.subplot(212)
    plt.plot(ans, 'r')
    plt.title("After pulse decode")
    plt.show()

    SNR = [20, 10, 0]
    for i in SNR:
        awgn_file = out_dict + str(i) + file_name + wav_suffix
        modulate_with_awgn(seq, awgn_file, i)
        ans = demodulate(awgn_file)
        #print(ans)
        diff = [1 if seq[j] == ans[j] else 0 for j in range(len(seq))]
        labels = ["Same", "Different"]
        X = [np.sum(diff), len(seq) - np.sum(diff)]
        
        plt.subplot(2, 2, int((i/10)+1))
        plt.pie(X, labels=labels, autopct='%1.2f%%')
        plt.title("SNR = " + str(i))
    plt.show()
