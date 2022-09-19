from bitstring import BitArray


class SDES:
    def __init__(self, key):
        self.key = BitArray('0b' + key)
        self.genRoundKeys()

    def genRoundKeys(self):
        C, D = self.PC1(self.key)
        left_shifts_table = (1, 2, 2, 2)
        self.round_keys = []

        for round in range(4):
            C.rol(left_shifts_table[round])
            D.rol(left_shifts_table[round])
            CD = C.copy()
            CD.append(D)
            self.round_keys.append(self.PC2(CD))

    def PC1(self, k):
        C = BitArray(5)
        D = BitArray(5)
        PC1_C = (3, 5, 2, 7, 4)
        PC1_D = (10, 1, 9, 8, 6)

        i = 0
        for c, d in zip(PC1_C, PC1_D):
            C.set(k[c - 1], i)
            D.set(k[d - 1], i)
            i += 1

        return (C, D)

    def PC2(self, cd):
        K = BitArray(8)
        PC2_pos = (6, 3, 7, 4, 8, 5, 10, 9)

        i = 0
        for pos in PC2_pos:
            K.set(cd[pos - 1], i)
            i += 1

        return K

    def IP(self, a):
        b = BitArray(8)
        IP_pos = (2, 6, 3, 1, 4, 8, 5, 7)

        i = 0
        for pos in IP_pos:
            b.set(a[pos - 1], i)
            i += 1

        return b

    def splitPerm(self, perm):
        return (perm[:4], perm[4:])

    def encrypt(self, msg, type):
        if (type == 'b'):
            msg = BitArray('0b' + msg)

        perm = self.IP(msg)
        L, R = self.splitPerm(perm)

        for round in range(4):
            L, R = R, self.XOR(L, self.F(R, round))

            print(round+1)

        return msg

    def decrypt(self, cipher):
        pass


mySDES = SDES('1010101010')
message = '10000000'
encrypted = mySDES.encrypt(message, 'b')
decrypted = mySDES.decrypt(message)

print(encrypted.bin)
