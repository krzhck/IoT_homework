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

def modulate_qpsk(codes, filename, snr):
    if len(codes) % 2 != 0:
        codes.append(0)
    codes = 1 - 2 * codes
    size = len(codes)
    fc = 20000
    fs = 48000
    T = 0.025
    ts = np.arange(0, T, 1 / fs)
    sigI = np.sin(2 * np.pi * fc * ts)
    sigQ = np.cos(2 * np.pi * fc * ts)
    sig = np.array([])
    for i in range(int(size / 2)):
        fI = codes[i * 2] * np.sqrt(1 / 2)
        fQ = codes[i * 2 + 1] * np.sqrt(1 / 2)
        sig = np.concatenate([sig, fI * sigI + fQ * sigQ])
    sig = awgn(sig, snr)
    sig = np.array(sig).astype(np.short)
    file = wave.open(filename, mode='wb')
    file.setframerate(fs)
    file.setnchannels(1)
    file.setsampwidth(2)
    file.writeframes(sig)
    return sig

def demodulate_qpsk(filename):
    symbol_duration = 0.025
    base_freq = 20e3
    sig, sample_freq = open_wave_file(filename)
    N = int(sample_freq * symbol_duration)
    num_symb = int(np.floor(len(sig) / N))
    ts = np.arange(0, N / sample_freq, 1 / sample_freq)
    base_sig1 = np.sin(2 * np.pi * base_freq * ts)
    base_sig1 = np.tile(base_sig1, num_symb)
    base_sig2 = np.cos(2 * np.pi * base_freq * ts)
    base_sig2 = np.tile(base_sig2, num_symb)
    y1 = sig * base_sig1
    y2 = sig * base_sig2

    [b, a] = signal.ellip(5, 0.5, 60, (base_freq * 2 / sample_freq),
        btype='lowpass', analog=False, output='ba')
    y1 = signal.filtfilt(b, a, y1)
    codes1 = []
    for i in range(num_symb):
        symb = y1[i * N:(i + 1) * N]
        codes1.append(int(np.sum(symb) < 0))
    y2 = signal.filtfilt(b, a, y2)
    codes2 = []
    for i in range(num_symb):
        symb = y2[i * N:(i + 1) * N]
        codes2.append(int(np.sum(symb) < 0))
    return [codes1[i >> 1] if i % 2 == 0 else codes2[i >> 1] for i in range(len(codes1) * 2)]


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
    seq = np.array(seq)

    SNR = [20, 10, 0]
    for i in SNR:
        awgn_file = out_dict + str(i) + file_name + wav_suffix
        modulate_qpsk(seq, awgn_file, i)
        ans = demodulate_qpsk(awgn_file)
        diff = [1 if seq[j] == ans[j] else 0 for j in range(len(seq))]
        labels = ["right", "wrong"]
        X = [np.sum(diff), len(seq) - np.sum(diff)]
        plt.subplot(len(SNR), 2, SNR.index(i) * 2 + 1)
        plt.plot(ans, 'r')
        plt.title("decoded signal")

        plt.subplot(len(SNR), 2, SNR.index(i) * 2 + 2)
        plt.pie(X, labels=labels, autopct='%1.2f%%')
        plt.title('SNR = ' + str(i))
    plt.show()
