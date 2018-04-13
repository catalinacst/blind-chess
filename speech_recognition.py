# ------------------------------------------------------------------------------
#
# blind chees: speech_recognition.py
#
# ------------------------------------------------------------------------------

# import speech_features as sf
import neuralnetwork
import numpy as np
import python_speech_features as sf
import sounddevice as sd
import scipy.io.wavfile

class Receptor():

    def __init__(self, tags):
        self.tags = tags
        self.m = 5
        self.k_tags = len(tags)
        self.m_train = self.k_tags * self.m

        X = np.zeros(self.m_train * 16000).reshape(self.m_train, 16000)

        for i in range(self.m_train):          # Load the audios of the data set
            word = self.tags[i // self.m]
            filename = 'audios/persona' + str(i % self.m) + '/' + word + '.wav'
            rate, audio = scipy.io.wavfile.read(filename)
            signal = audio.T[0]
            X[i] = signal

        self.train(X)

    def train(self, signals):
        """
        """
        X = np.zeros(self.m_train * 1287).reshape(self.m_train, 1287)

        for i in range(self.m_train):
            coefs = sf.mfcc(signals[i])
            coefs = coefs.reshape(-1)
            coefs = coefs / 20
            X[i] = coefs

        self.W = np.zeros(self.k_tags * 1287).reshape(self.k_tags, 1287)
        self.B = np.zeros(self.k_tags).reshape((1, self.k_tags))
        for i in range(self.k_tags):
            a = np.zeros(self.m * i)
            b = np.ones(self.m)
            c = np.zeros(self.m * (self.k_tags-i-1))
            Y = np.concatenate((a, b, c))
            w, b = neuralnetwork.train(X.T, Y, 50000, 0.2)
            self.W[i] = w.T
            self.B[0][i] = b

    def predict(self, signal):
        """
        """
        coefs = sf.mfcc(signal)
        coefs = coefs.reshape(-1)
        coefs = coefs / 20

        p = neuralnetwork.sigmoid(np.dot(self.W, coefs.T) + self.B)
        return p.T

class SpeechRecognition():

    tags_pieces = ['rey', 'dama', 'alfil', 'caballo', 'torre', 'peon']
    tags_col = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    tags_row = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self):
        print("1...")
        self.rec_piece = Receptor(self.tags_pieces)
        print("2...")
        self.rec_col = Receptor(self.tags_col)
        print("3...")
        self.rec_row = Receptor(self.tags_row)

    def listen(self, valid_moves):
        """
        """
        fs = 16000
        duration = 3
        dfs = int(duration * fs)

        while True:
            print("Press enter to record...")
            input()

            audio = sd.rec(dfs, samplerate=fs, channels=2)
            sd.wait()

            input_signal = audio.T[0]
            signal0 = input_signal[0:dfs//3]
            signal1 = input_signal[dfs//3:2*dfs//3]
            signal2 = input_signal[2*dfs//3:dfs]

            # sd.play(audio, fs)
            # sd.wait()

            pred_piece = self.rec_piece.predict(signal0)
            pred_col = self.rec_col.predict(signal1)
            pred_row = self.rec_row.predict(signal2)

            max_val, res = 0, -1
            for (id_move, move) in enumerate(valid_moves):
                tp, idp, r, c = move
                val = pred_piece[tp // 2] * pred_row[r] * pred_col[c]
                if val > max_val:
                    max_val = val
                    res = id_move

            a = self.tags_pieces[valid_moves[res][0] // 2]
            b = self.tags_col[valid_moves[res][3]]
            c = self.tags_row[valid_moves[res][2]]

            print("You say " + a + " " + b + " " + c + "... Is correct? y / n")
            if input() == "y":
                break

        return valid_moves[res]
