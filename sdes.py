from bitstring import BitArray


class SDES:
    def __init__(self, key, type=None):
        if type == 'b':
            self.key = BitArray(bin=key)
        else:
            self.key = BitArray(bin=(bin(int(key, 16))[2:]).zfill(10))
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

    def IPi(self, a):
        b = BitArray(8)
        IPi_pos = (4, 1, 3, 5, 7, 2, 8, 6)

        i = 0
        for pos in IPi_pos:
            b.set(a[pos - 1], i)
            i += 1

        return b

    def splitPerm(self, perm):
        return (perm[:4], perm[4:])

    def E(self, a):
        b = BitArray(8)
        E_pos = (4, 1, 2, 3, 2, 3, 4, 1)

        i = 0
        for pos in E_pos:
            b.set(a[pos - 1], i)
            i += 1

        return b

    def S1(self, a):
        S1_box = (
            (1, 0, 3, 2),
            (3, 2, 1, 0),
            (0, 2, 1, 3),
            (3, 1, 3, 2)
        )

        row = BitArray(2)
        column = BitArray(2)

        row.set(a[0], 0)
        row.set(a[3], 1)
        column.set(a[1], 0)
        column.set(a[2], 1)

        return BitArray(uint=S1_box[row.uint][column.uint], length=2)

    def S2(self, a):
        S2_box = (
            (0, 1, 2, 3),
            (2, 0, 1, 3),
            (3, 0, 1, 0),
            (2, 1, 0, 3)
        )

        row = BitArray(2)
        column = BitArray(2)

        row.set(a[0], 0)
        row.set(a[3], 1)
        column.set(a[1], 0)
        column.set(a[2], 1)

        return BitArray(uint=S2_box[row.uint][column.uint], length=2)

    def P(self, a):
        b = BitArray(4)
        IP_pos = (2, 4, 3, 1)

        i = 0
        for pos in IP_pos:
            b.set(a[pos - 1], i)
            i += 1

        return b

    def F(self, R, round):
        B = self.round_keys[round] ^ self.E(R)
        B1, B2 = self.S1(B[:4]), self.S2(B[4:])
        B1.append(B2)

        return self.P(B1)

    def handleInput(self, msg, type=None):
        if type == 'b':
            msg = BitArray(bin=msg)
        else:
            msg = BitArray(hex=msg)

        #out = []
        #i = 0
        # while i < msg.len:
        #    out.append(msg[i:i+8])
        #    i += 8

        # return out

        return msg

    def encrypt(self, msg, type=None):
        msg = self.handleInput(msg, type)

        perm = self.IP(msg)
        L, R = self.splitPerm(perm)

        for round in range(4):
            L, R = R, L ^ self.F(R, round)

        L, R = R, L
        L.append(R)

        return self.IPi(L)

    def decrypt(self, cipher, type=None):
        cipher = self.handleInput(cipher, type)

        perm = self.IP(cipher)
        L, R = self.splitPerm(perm)

        for round in range(3, -1, -1):
            L, R = R, L ^ self.F(R, round)

        L, R = R, L
        L.append(R)

        return self.IPi(L)


class DSDES:
    def __init__(self, k1, k2, type=None):
        self.sdes1 = SDES(k1, type)
        self.sdes2 = SDES(k2, type)

    def encrypt(self, msg, type=None):
        return self.sdes2.encrypt(self.sdes1.encrypt(msg, type).bin, type)

    def decrypt(self, cipher, type=None):
        return self.sdes1.decrypt(self.sdes2.decrypt(cipher, type).bin, type)
