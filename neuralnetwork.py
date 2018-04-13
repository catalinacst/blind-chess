# ------------------------------------------------------------------------------
#
# blind chees: neuralnetwork.py
#
# ------------------------------------------------------------------------------

import numpy as np

def sigmoid(z):
    """
    sigmoid(z) = 1 / (1 + e ^ -z)

    Arguments:
    z -- A numpy array representing the data.

    Return:
    s -- A numpy array with the sigmoid function from the input array.
    """
    s = 1 / (1 + np.exp(-z))
    return s

def initialize_with_zeros(dim):
    """
    Initialize the weights with zeros

    Arguments:
    dim -- Number of features

    Return:
    w -- A numpy array of zeros with dimension dim
    b -- Variable with zero
    """
    w = np.zeros(dim).reshape((dim, 1))
    b = 0
    return w, b

def propagate(w, b, X, Y):
    """
    Get the gradient of the current weights

    Arguments:
    w -- Numpy array with the current weights
    b -- Variable with the current bias
    X -- Input training set
    Y -- Input training set

    Return:
    dw -- A numpy array with the gradient of the current w
    db -- Variable with the gradient of the current b
    """
    m = Y.size
    A = sigmoid(np.dot(w.T, X) + b)
    dw = np.dot(X, (A - Y).T) / m + (0 / m) * w
    db = (A - Y).sum() / m
    return dw, db

def train(X, Y, num_iterations = 2000, learning_rate = 0.5):
    """
    Train a neural network with the input
    X, Y using gradient descendent algorithm

    Arguments:
    X -- Input features training set
    Y -- Input tags training set
    num_iterations -- Integer number of iterations of the algorithm
    learning_rate -- Float number of the learning rate of the algorithm

    Return:
    w -- A numpy array with the weights of the features
    b -- Variable with the weights of the bias
    """
    w, b = initialize_with_zeros(X.shape[0])
    for i in range(num_iterations):
        dw, db = propagate(w, b, X, Y)
        w = w - learning_rate * dw
        b = b - learning_rate * db
    return w, b
