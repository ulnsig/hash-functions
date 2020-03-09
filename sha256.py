# -*- coding: utf-8 -*-

from codecs import encode, decode
import struct

H = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
     0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
     0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
     0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

MOD = 0xFFFFFFFF

MAX_LENGTH = 18446744073709551615

BLOCK_LENGTH = 64

rotr = lambda x, n: ((x >> n) | (x << (32 - n))) & MOD

sigma0 = lambda a: rotr(a, 7) ^ rotr(a, 18) ^ (a >> 3)

sig0 = lambda a: rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)

sigma1 = lambda e: rotr(e, 19) ^ rotr(e, 17) ^ (e >> 10)

sig1 = lambda x: rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)

ch = lambda e, f, g: (e & f) ^ ((MOD ^ e) & g)

ma = lambda a, b, c: (a & b) ^ (a & c) ^ (b & c)

add_mod32 = lambda *args: sum(args) & MOD

transf_word = lambda w, k: (sigma1(w[k - 2]) + w[k - 7] + sigma0(w[k - 15]) + w[k - 16]) & MOD

word32 = lambda w: [w.append(transf_word(w, k)) for k in range(16, 64)]


def mod_arr(arr):
    for i in range(len(arr)):
        arr[i] = arr[i] & MOD
    return arr


def sum_str(arr):
    res = b''
    for i in arr:
        res += i
    return res


def pad(message):
    length = len(message)
    message += decode('80', 'hex_codec')
    assert length < MAX_LENGTH
    padding = (length + 72) // 64 * 64 - 9 - length
    message += padding * decode('00', 'hex_codec')
    message += decode('%016X' % (length * 8), 'hex_codec')
    return message


def sep_blocks(message):
    blocks = []
    for i in range(len(message))[::BLOCK_LENGTH]:
        blocks.append(message[i:i + BLOCK_LENGTH])
    return blocks


class sha256():
    def __init__(self, message):
        message = pad(message)
        h_arr = H
        k_arr = K
        w = []

        for block in sep_blocks(message):
            for i in range(BLOCK_LENGTH)[::4]:
                n = struct.unpack('>I', block[i:i + 4])
                w.append(n[0])

            word32(w)

            a = h_arr[0]
            b = h_arr[1]
            c = h_arr[2]
            d = h_arr[3]
            e = h_arr[4]
            f = h_arr[5]
            g = h_arr[6]
            h = h_arr[7]

            for i in range(64):
                temp0 = (sig0(a) + ma(a, b, c)) & MOD
                temp1 = (h + sig1(e) + ch(e, f, g) + k_arr[i] + w[i]) & MOD

                h = g
                g = f
                f = e
                e = (d + temp1) & MOD
                d = c
                c = b
                b = a
                a = (temp0 + temp1) & MOD

            h_arr[0] += a
            h_arr[1] += b
            h_arr[2] += c
            h_arr[3] += d
            h_arr[4] += e
            h_arr[5] += f
            h_arr[6] += g
            h_arr[7] += h

            h_arr = mod_arr(h_arr)
        self.hash = sum_str([struct.pack(">I", i) for i in h_arr])

    def hexdigest(self):
        return decode(encode(self.hash, 'hex_codec'), 'utf-8')



def main():
    print('sha256("abc")', sha256('abc'.encode('utf-8')).hexdigest())


if __name__ == '__main__':
    main()
