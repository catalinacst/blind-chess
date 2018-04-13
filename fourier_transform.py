# ------------------------------------------------------------------------------
#
# blind chees: fourier_transform.py
#
# ------------------------------------------------------------------------------

import numpy as np

def dft(s):
    """
    Get the Discrete Fourier Transform from the input signal.
    Time complexity: O(n ^ 2)

    Arguments:
    s -- A numpy array representing the signal.

    Return:
    S -- A numpy array with the dft from the signal.
    """
    N = s.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    S = np.dot(M, s)
    return S

def fft(s):
    """
    Get the Discrete Fourier Transform using the fast
    Cooley - Tukey Algorithm from the input signal.
    Time complexity: O(n * log(n))
    note: n has to be a power of two

    Arguments:
    s -- A numpy array representing the signal.

    Return:
    S -- A numpy array with the fft from the signal.
    """
    n = s.shape[0]
    if n == 1:
        return s
    wi = np.exp(-2j * np.pi * np.arange(n) / n)
    s_even = fft(s[::2])
    s_odd = fft(s[1::2])
    S0 = s_even + wi[:n//2] * s_odd
    S1 = s_even + wi[n//2:] * s_odd
    S = np.concatenate((S0, S1))
    return S

def dct(s):
    """
    Get the Discrete Cosine Transform from the input signal.
    Time complexity: O(n ^ 2)

    Arguments:
    s -- A numpy array representing the signal.

    Return:
    S -- A numpy array with the dct from the signal.
    """
    S = dft(s)
    return S.real
