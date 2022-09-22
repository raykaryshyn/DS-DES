from bitstring import BitArray
from sdes import DSDES

plaintext = [BitArray(uint=0x42, length=8).bin, BitArray(uint=0x72, length=8).bin, BitArray(
    uint=0x75, length=8).bin, BitArray(uint=0x74, length=8).bin, BitArray(uint=0x65, length=8).bin]
ciphertext = [BitArray(uint=0x52, length=8).bin, BitArray(uint=0xf0, length=8).bin, BitArray(
    uint=0xbe, length=8).bin, BitArray(uint=0x69, length=8).bin, BitArray(uint=0x8a, length=8).bin]
ciphertexts = []
plaintexts = []
found_keys = []

ans = []
for j in ciphertext:
    ans.append(j)
cipher = ''.join(ans)
for i in range(0b100000000000000000000):
    key = BitArray(uint=i, length=20)
    myDSDES = DSDES(key.bin, 'b')
    test = []
    for j in plaintext:
        test.append(myDSDES.encrypt(j, 'b').bin)
    if ''.join(test) == cipher:
        print(key[:10].bin, key[10:].bin)
        break
