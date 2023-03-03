
from math import log2, ceil

# Implementation of the universal constrained code
# Example implementation: constrained periodicity

# Construction parameters
n = 14
# Custom parameters
p = 4

# Modify the below variables and functions

# The encoding length (periodicity example)
encoding_length = p
# The window length (do not change)
l = min([pot_l for pot_l in range(n) if pot_l == ceil(log2(n - pot_l + 2)) + encoding_length + 1])


# Check if in S
def isInS(vec):

    # Periodicity example
    for p_tag in range(1, p):

        is_period = True
        for j in range(p_tag, l):
            if vec[j] != vec[j - p_tag]:
                is_period = False
                break

        if is_period:
            return True


def phi(vec):

    assert(isInS(vec))

    # Periodicity example

    # Find minimal period
    min_period = None
    for p_tag in range(1, p):

        is_period = True
        for j in range(p_tag, l):
            if vec[j] != vec[j - p_tag]:
                is_period = False
                break

        if is_period:
            min_period = p_tag
            break

    # Encode kernel, padded with one and then zeros
    return vec[:min_period] + '1' + '0' * (p - min_period - 1)


def invPhi(vec):

    # Periodicity example
    period = p - 1
    i = 1
    while vec[-i] == '0':
        period -= 1
        i += 1

    new_vec = vec[:period]
    for i in range(period, l):
        new_vec += new_vec[i - period]

    return new_vec


# Core algorithm (do not modify)

def repair(vec):

    # Find bad window
    bad_window_idx = -1

    for i in range(0, n - l + 2):
        window = vec[i:i + l]
        if isInS(window):
            bad_window_idx = i
            break

    if bad_window_idx == -1:
        return None

    window = vec[bad_window_idx:bad_window_idx + l]

    bad_window_idx_vec = ''.join(reversed([str(int(bool(bad_window_idx & (1 << j)))) for j in range(ceil(log2((n - l + 2))))]))
    phi_encoding = phi(window)
    new_vec = vec[:bad_window_idx] + vec[bad_window_idx + l:] + phi_encoding + bad_window_idx_vec + '0'
    assert (len(new_vec) == n + 1)
    return new_vec


def encode(x):
    """
    Performs the universal code encoder
    :param x: input of size n
    :return: output of size n + 1 that satisfies the constraints
    """

    y = x + '1'

    while repair(y) is not None:
        y = repair(y)

    return y


def decode(y):

    while y[-1] == '0':

        rev_y = ''.join(reversed(y))

        idx_vec = rev_y[1:1 + ceil(log2((n - l + 2)))]
        idx = sum([int(idx_vec[j]) << j for j in range(ceil(log2(n - l + 2)))])

        phi_encoding = rev_y[1 + ceil(log2((n - l + 2))): 1 + ceil(log2((n - l + 2))) + encoding_length]
        orig_window = invPhi(phi_encoding)

        y = y[:idx] + orig_window + y[idx:-(1 + ceil(log2(n - l + 2)) + encoding_length)]

    return y[:-1]


if __name__ == '__main__':

    print(encode('10001010101100'))
    print(decode(encode('10001010101100')))

