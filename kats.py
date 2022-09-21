from bitstring import BitArray
from sdes import SDES


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
