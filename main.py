from bitstring import BitArray

def IP(a):
    b = BitArray(8)

    b.set(a[1], 0)
    b.set(a[5], 1)
    b.set(a[2], 2)
    b.set(a[0], 3)
    b.set(a[3], 4)
    b.set(a[7], 5)
    b.set(a[4], 6)
    b.set(a[6], 7)

    print(b.bin)
    return b

def IPi(a):
    b = BitArray(8)

    b.set(a[3], 0)
    b.set(a[0], 1)
    b.set(a[2], 2)
    b.set(a[4], 3)
    b.set(a[6], 4)
    b.set(a[1], 5)
    b.set(a[7], 6)
    b.set(a[5], 7)

    print(b.bin)
    return b

a = BitArray('0b10101010')
IPi(IP(a))
