from bitstring import BitArray

def IP(a):
    b = BitArray(8)
    IP_pos = (2, 6, 3, 1, 4, 8, 5, 7)

    i = 0
    for pos in IP_pos:
        b.set(a[pos - 1], i)
        i += 1

    return b

def IPi(a):
    b = BitArray(8)
    IPi_pos = (4, 1, 3, 5, 7, 2, 8, 6)

    i = 0
    for pos in IPi_pos:
        b.set(a[pos - 1], i)
        i += 1

    return b

a = BitArray('0b11110000')
print(IP(a).bin)
print(IPi(IP(a)).bin)
print()





def PC1(k):
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

k = BitArray('0b1111100000')
C, D = PC1(k)
print(C.bin, D.bin)

def PC2(cd):
    K = BitArray(8)
    PC2_pos = (6, 3, 7, 4, 8, 5, 10, 9)

    i = 0
    for pos in PC2_pos:
        K.set(cd[pos - 1], i)
        i += 1

    return K

C.append(D)
print(PC2(C).bin)
