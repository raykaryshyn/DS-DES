from bitstring import BitArray

def IP(a):
    b = BitArray(8)
    IP_pos = (2, 6, 3, 1, 4, 8, 5, 7)

    i = 0
    for pos in IP_pos:
        b.set(a[pos - 1], i)
        i += 1

    print(b.bin)
    return b

def IPi(a):
    b = BitArray(8)
    IPi_pos = (4, 1, 3, 5, 7, 2, 8, 6)

    i = 0
    for pos in IPi_pos:
        b.set(a[pos - 1], i)
        i += 1

    print(b.bin)
    return b

a = BitArray('0b11110000')
IPi(IP(a))
