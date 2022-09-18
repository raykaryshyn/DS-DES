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
print()





left_shifts_table = (1, 2, 2, 2)

def left_shift(a, num):
    a.rol(num)

x = C.copy()
for i in left_shifts_table:
    left_shift(x, i)
    print(x.bin)

print()







def E(a):
    b = BitArray(8)
    E_pos = (4, 1, 2, 3, 2, 3, 4, 1)

    i = 0
    for pos in E_pos:
        b.set(a[pos - 1], i)
        i += 1

    return b

R = BitArray('0b1100')
print(E(R).bin)
print()


def S1(a):
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

    return S1_box[row.uint][column.uint]

def S2(a):
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

    return S2_box[row.uint][column.uint]

xyz = BitArray('0b0110')
print(S1(xyz))
print(S2(xyz))
print()
