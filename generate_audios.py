import sounddevice as sd
import scipy.io.wavfile
import numpy as np

tags = [
    'rey', 'reina', 'alfil', 'caballo', 'torre', 'peon',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    '1', '2', '3', '4', '5', '6', '7', '8'
]

perm = np.random.permutation(22)

fs = 16000
duration = 3

for p in perm:
    print("Say " + tags[p] + ":")
    input()
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()

    signal = audio[fs:2*fs]

    sd.play(signal, fs)
    sd.wait()

    scipy.io.wavfile.write("audios/persona4/" + tags[p] + ".wav", fs, signal)
