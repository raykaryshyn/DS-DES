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

    def encrypt(self, msg, type):
        if (type == 'b'):
            msg = BitArray('0b' + msg)

        perm = self.IP(msg)
        L, R = self.splitPerm(perm)

        for round in range(4):
            L, R = R, L ^ self.F(R, round)

        L, R = R, L
        L.append(R)

        return self.IPi(L)

    def decrypt(self, cipher, type):
        if (type == 'b'):
            cipher = BitArray('0b' + cipher)

        perm = self.IP(cipher)
        L, R = self.splitPerm(perm)

        for round in range(3, -1, -1):
            L, R = R, L ^ self.F(R, round)

        L, R = R, L
        L.append(R)

        return self.IPi(L)


class DSDES:
    def __init__(self, k1, k2):
        self.sdes1 = SDES(k1)
        self.sdes2 = SDES(k2)

    def encrypt(self, msg, type):
        if type == 'b':
            pass

        return self.sdes2.encrypt(self.sdes1.encrypt(msg, 'b').bin, 'b')

    def decrypt(self, cipher, type):
        if type == 'b':
            pass

        return self.sdes1.decrypt(self.sdes2.decrypt(cipher, 'b').bin, 'b')


'''
mySDES = SDES('0000000000')
message = '10000000'
encrypted = mySDES.encrypt(message, 'b')
decrypted = mySDES.decrypt(encrypted.bin, 'b')

print("Cipher:", encrypted.bin)
print("Plain: ",decrypted.bin)
'''

'''
myDSDES = DSDES('0000000000', '1111111111')
message = '10101010'
encrypted = myDSDES.encrypt(message, 'b')
decrypted = myDSDES.decrypt(encrypted.bin, 'b')

print("Cipher:", encrypted.bin)
print("Plain: ", decrypted.bin)
'''


def VarPlainEKAT():
    key = '0000000000'
    sdes = SDES(key)
    p = BitArray(bin='10000000')
    table = []

    for _ in range(8):
        table.append([p.bin, sdes.encrypt(str(p.bin), 'b').bin])
        p.ror(1)

    return table


def VarCipherDKAT():
    key = '0000000000'
    sdes = SDES(key)
    p = BitArray(bin='10000000')
    table = []

    for _ in range(8):
        encrypted_p = sdes.encrypt(str(p.bin), 'b').bin
        table.append([p.bin, sdes.decrypt(encrypted_p, 'b').bin])
        p.ror(1)

    return table


def InvPermEKAT(tableIn):
    key = '0000000000'
    sdes = SDES(key)
    tableOut = []

    for i in range(8):
        tableOut.append([tableIn[i][1], sdes.encrypt(tableIn[i][1], 'b').bin])

    return tableOut


def InvPermDKAT(tableIn):
    key = '0000000000'
    sdes = SDES(key)
    tableOut = []

    for i in range(8):
        tableOut.append([tableIn[i][1], sdes.decrypt(tableIn[i][1], 'b').bin])

    return tableOut


def VarKeyEKAT():
    key = BitArray(bin='1000000000')
    sdes = SDES(str(key.bin))
    p = '00000000'
    table = []

    for _ in range(10):
        table.append([str(key.bin), sdes.encrypt(p, 'b').bin])
        key.ror(1)
        sdes = SDES(str(key.bin))

    return table


def VarKeyDKAT():
    key = BitArray(bin='1000000000')
    sdes = SDES(str(key.bin))
    p = '00000000'
    table = []

    for _ in range(10):
        c = sdes.encrypt(p, 'b').bin
        table.append([str(key.bin), sdes.decrypt(c, 'b').bin])
        key.ror(1)
        sdes = SDES(str(key.bin))

    return table


def PermOpEKAT():
    keys = ['0000000011', '0011001010', '0001011001', '1011001111']
    p = '00000000'
    table = []

    for i in range(4):
        sdes = SDES(keys[i])
        table.append([keys[i], sdes.encrypt(p, 'b').bin])

    return table


def PermOpDKAT():
    keys = ['0000000011', '0011001010', '0001011001', '1011001111']
    p = '00000000'
    table = []

    for i in range(4):
        sdes = SDES(keys[i])
        c = sdes.encrypt(p, 'b').bin
        table.append([keys[i], sdes.decrypt(c, 'b').bin])

    return table


def SubTableEKAT():
    keys = ['0001101101', '0001101110', '0001110000',
            '0001110001', '0001110110', '0001111000', '0001111001']
    p = '00000000'
    table = []

    for i in range(7):
        sdes = SDES(keys[i])
        table.append([keys[i], sdes.encrypt(p, 'b').bin])

    return table


def SubTableDKAT():
    keys = ['0001101101', '0001101110', '0001110000',
            '0001110001', '0001110110', '0001111000', '0001111001']
    p = '00000000'
    table = []

    for i in range(7):
        sdes = SDES(keys[i])
        c = sdes.encrypt(p, 'b').bin
        table.append([keys[i], sdes.decrypt(c, 'b').bin])

    return table


'''
print(VarPlainEKAT())
print(InvPermEKAT(VarPlainEKAT()))
print(VarKeyEKAT())
print(PermOpEKAT())
print(SubTableEKAT())
print()

print(VarCipherDKAT())
print(InvPermDKAT(VarCipherDKAT()))
print(VarKeyDKAT())
print(PermOpDKAT())
print(SubTableDKAT())
'''

plaintext = BitArray(uint=0x42, length=8).bin
ciphertext = BitArray(uint=0x52, length=8).bin
ciphertexts = []
plaintexts = []

for i in range(0b100000000000000000000):
    key = BitArray(uint=i, length=20)
    myDSDES = DSDES(key[:10].bin, key[10:].bin)
    ciphertexts.append(myDSDES.encrypt(plaintext, 'b').bin)

for i in range(0b100000000000000000000):
    key = BitArray(uint=i, length=20)
    myDSDES = DSDES(key[:10].bin, key[10:].bin)
    plaintexts.append(myDSDES.decrypt(ciphertext, 'b').bin)

for i in range(0b100000000000000000000):
    if ciphertexts[i] == plaintexts[i]:
        print(i, ciphertexts[i], plaintexts[i])
