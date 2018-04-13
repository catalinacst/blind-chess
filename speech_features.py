# ------------------------------------------------------------------------------
#
# blind chees: speech_features.py
#
# ------------------------------------------------------------------------------

import numpy as np
import fourier_transform as ft

def mel(f):
    """
    Get the Mel Scale.

    Arguments:
    f -- Frecuency.

    Return:
    M -- Mel scale.
    """
    return 1125 * np.log(1 + f / 700)

def imel(M):
    """
    Get the Inverse Mel Scale.

    Arguments:
    M -- Mel Scale.

    Return:
    f -- frecuency.
    """
    return 700 * (np.exp(M / 1125) - 1)

def melfilterbank(nfilt, nfft, samplerate):
    """
    Get the Mel Filterbank.

    Arguments:
    nfilt -- Number of filters to get.
    nfft -- Number of points in the fourier transform.
    rate -- Sample rate of the input audio.

    Return:
    H -- A numpy array with the filters to apply.
    """
    lower, upper = 300, 8000
    ml = np.linspace(mel(lower), mel(upper), num=nfilt+2)
    h = imel(ml)
    f = np.floor((nfft + 1) * h / samplerate)
    H = np.zeros([nfilt, nfft])
    for m in range(0, nfilt):
        for k in range(int(f[m]), int(f[m + 1])):
            H[m,k] = (k - f[m]) / (f[m + 1] - f[m])
        for k in range(int(f[m + 1]), int(f[m + 2])):
            H[m,k] = (f[m + 2] - k) / (f[m + 2] - f[m + 1])
    return H

def mfcc(audio, rate=16000):
    """
    Get the Mel Frecuency Cepstral Coeficients from the input audio.

    Arguments:
    rate -- Sample rate of the input audio.
    audio -- A numpy array with the info of the audio.

    Return:
    coefs -- A numpy array with the mfcc from the audio.
    """

    frame_length = 0.025                          # Frame length in mili-seconds
    frame_step = 0.01                               # Frame step in mili-seconds
    nsamples_frame = int(frame_length * rate)      # Number of samples for frame
    nsamples_step = int(frame_step * rate)          # Number of samples for step

    k = nsamples_step - (audio.shape[0] - nsamples_frame) % nsamples_step
    audio = np.append(audio, np.zeros(k))                           # Fill zeros

    coefs = np.array([])                                  # Init the array coefs

    step = 0
    while step + nsamples_frame - 1 < audio.shape[0]:           # For each frame
        frame = audio[step : step + nsamples_frame]                      # Frame
        k = int(2 ** np.ceil(np.log2(nsamples_frame)) - nsamples_frame)
        frame = np.concatenate((frame, np.zeros(k)))         # Fill power of two

        s = frame * np.hamming(frame.size)        # Multiply by a hamming window
        S = ft.fft(s)                                   # Fast Fourier Transform
        P = np.absolute(S) ** 2 / s.size                        # Power spectral

        H = melfilterbank(26, P.size, rate)             # Get the mel filterbank
        a = np.dot(P, H.T)                             # Appy the mel filterbank

        b = np.log(a)                                             # Take the log

        c = ft.dct(b)                                # Discrete Cosine Transform

        coefs = np.append(coefs, c[:c.size // 2]) # Append features of the frame

        step += nsamples_step                                       # Next Frame

    return coefs
