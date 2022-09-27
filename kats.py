from bitstring import BitArray
from sdes import SDES


def VarPlainEKAT():
    key = '0000000000'
    sdes = SDES(key, 'b')
    p = BitArray(bin='10000000')
    table = []

    for _ in range(8):
        table.append([p.bin, sdes.encrypt(str(p.bin), 'b').bin])
        p.ror(1)

    return table


def VarCipherDKAT():
    key = '0000000000'
    sdes = SDES(key, 'b')
    p = BitArray(bin='10000000')
    table = []

    for _ in range(8):
        encrypted_p = sdes.encrypt(str(p.bin), 'b').bin
        table.append([p.bin, sdes.decrypt(encrypted_p, 'b').bin])
        p.ror(1)

    return table


def InvPermEKAT(tableIn):
    key = '0000000000'
    sdes = SDES(key, 'b')
    tableOut = []

    for i in range(8):
        tableOut.append([sdes.encrypt(tableIn[i][1], 'b').bin, tableIn[i][1]])

    return tableOut


def InvPermDKAT(tableIn):
    key = '0000000000'
    sdes = SDES(key, 'b')
    tableOut = []

    for i in range(8):
        tableOut.append([tableIn[i][1], sdes.decrypt(tableIn[i][1], 'b').bin])

    return tableOut


def VarKeyEKAT():
    key = BitArray(bin='1000000000')
    sdes = SDES(str(key.bin), 'b')
    p = '00000000'
    table = []

    for _ in range(10):
        table.append([str(key.bin), sdes.encrypt(p, 'b').bin])
        key.ror(1)
        sdes = SDES(str(key.bin), 'b')

    return table


def VarKeyDKAT():
    key = BitArray(bin='1000000000')
    sdes = SDES(str(key.bin), 'b')
    p = '00000000'
    table = []

    for _ in range(10):
        c = sdes.encrypt(p, 'b').bin
        table.append([str(key.bin), sdes.decrypt(c, 'b').bin])
        key.ror(1)
        sdes = SDES(str(key.bin), 'b')

    return table


def PermOpEKAT():
    keys = ['0000000011', '0011001010', '0001011001', '1011001111']
    p = '00000000'
    table = []

    for i in range(4):
        sdes = SDES(keys[i], 'b')
        table.append([keys[i], sdes.encrypt(p, 'b').bin])

    return table


def PermOpDKAT():
    keys = ['0000000011', '0011001010', '0001011001', '1011001111']
    p = '00000000'
    table = []

    for i in range(4):
        sdes = SDES(keys[i], 'b')
        c = sdes.encrypt(p, 'b').bin
        table.append([keys[i], sdes.decrypt(c, 'b').bin])

    return table


def SubTableEKAT():
    keys = ['0001101101', '0001101110', '0001110000',
            '0001110001', '0001110110', '0001111000', '0001111001']
    p = '00000000'
    table = []

    for i in range(7):
        sdes = SDES(keys[i], 'b')
        table.append([keys[i], sdes.encrypt(p, 'b').bin])

    return table


def SubTableDKAT():
    keys = ['0001101101', '0001101110', '0001110000',
            '0001110001', '0001110110', '0001111000', '0001111001']
    p = '00000000'
    table = []

    for i in range(7):
        sdes = SDES(keys[i], 'b')
        c = sdes.encrypt(p, 'b').bin
        table.append([keys[i], sdes.decrypt(c, 'b').bin])

    return table


def DidKATPass(desired, function, op_input=None):
    if (op_input and desired == function(op_input)) or (not op_input and desired == function()):
        print('+ PASSED:\t', function.__name__)
    else:
        print('- FAILED:\t', function.__name__)


desired_VarPlainEKAT = [
    ['10000000', '10101000'],
    ['01000000', '10111110'],
    ['00100000', '00010110'],
    ['00010000', '01001010'],
    ['00001000', '01001001'],
    ['00000100', '01001110'],
    ['00000010', '00010101'],
    ['00000001', '01101000']]
desired_VarKeyEKAT = [
    ['1000000000', '01100001'],
    ['0100000000', '00010011'],
    ['0010000000', '01001111'],
    ['0001000000', '11100101'],
    ['0000100000', '01100101'],
    ['0000010000', '01011100'],
    ['0000001000', '10101110'],
    ['0000000100', '11011001'],
    ['0000000010', '10101010'],
    ['0000000001', '01001110']]
desired_PermOpEKAT = [
    ['0000000011', '00000011'],
    ['0011001010', '00100010'],
    ['0001011001', '01000000'],
    ['1011001111', '01100000']]
desired_SubTableEKAT = [
    ['0001101101', '10000111'],
    ['0001101110', '10110110'],
    ['0001110000', '10110100'],
    ['0001110001', '00110011'],
    ['0001110110', '11011001'],
    ['0001111000', '10001101'],
    ['0001111001', '00010001']]

desired_VarCipherDKAT = [
    ['10000000', '10000000'],
    ['01000000', '01000000'],
    ['00100000', '00100000'],
    ['00010000', '00010000'],
    ['00001000', '00001000'],
    ['00000100', '00000100'],
    ['00000010', '00000010'],
    ['00000001', '00000001']]
desired_InvPermDKAT = [
    ['10000000', '10101000'],
    ['01000000', '10111110'],
    ['00100000', '00010110'],
    ['00010000', '01001010'],
    ['00001000', '01001001'],
    ['00000100', '01001110'],
    ['00000010', '00010101'],
    ['00000001', '01101000']]
desired_VarKeyDKAT = [
    ['1000000000', '00000000'],
    ['0100000000', '00000000'],
    ['0010000000', '00000000'],
    ['0001000000', '00000000'],
    ['0000100000', '00000000'],
    ['0000010000', '00000000'],
    ['0000001000', '00000000'],
    ['0000000100', '00000000'],
    ['0000000010', '00000000'],
    ['0000000001', '00000000']]
desired_PermOpDKAT = [
    ['0000000011', '00000000'],
    ['0011001010', '00000000'],
    ['0001011001', '00000000'],
    ['1011001111', '00000000']]
desired_SubTableDKAT = [
    ['0001101101', '00000000'],
    ['0001101110', '00000000'],
    ['0001110000', '00000000'],
    ['0001110001', '00000000'],
    ['0001110110', '00000000'],
    ['0001111000', '00000000'],
    ['0001111001', '00000000']]


print('DS-DES Known Answer Tests (KATs)')
print('--------------------------------\n')

print('Encryption KATs:')

DidKATPass(desired_VarPlainEKAT, VarPlainEKAT)
DidKATPass(desired_VarPlainEKAT, InvPermEKAT, VarPlainEKAT())
DidKATPass(desired_VarKeyEKAT, VarKeyEKAT)
DidKATPass(desired_PermOpEKAT, PermOpEKAT)
DidKATPass(desired_SubTableEKAT, SubTableEKAT)

print('\nDecryption KATs:')

DidKATPass(desired_VarCipherDKAT, VarCipherDKAT)
DidKATPass(desired_InvPermDKAT, InvPermDKAT, VarCipherDKAT())
DidKATPass(desired_VarKeyDKAT, VarKeyDKAT)
DidKATPass(desired_PermOpDKAT, PermOpDKAT)
DidKATPass(desired_SubTableDKAT, SubTableDKAT)
