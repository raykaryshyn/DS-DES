from bitstring import BitArray
from sdes import SDES, DSDES

plaintext = [BitArray(uint=0x42, length=8).bin, BitArray(uint=0x72, length=8).bin, BitArray(
    uint=0x75, length=8).bin, BitArray(uint=0x74, length=8).bin, BitArray(uint=0x65, length=8).bin]
ciphertext = [BitArray(uint=0x52, length=8).bin, BitArray(uint=0xf0, length=8).bin, BitArray(
    uint=0xbe, length=8).bin, BitArray(uint=0x69, length=8).bin, BitArray(uint=0x8a, length=8).bin]
ciphertexts = []
plaintexts = []
found_keys = []


for i in range(0b10000000000):
    key = BitArray(uint=i, length=10)
    mySDES = SDES(key.bin, 'b')
    ans = []
    for j in plaintext:
        ans.append(mySDES.encrypt(j, 'b').bin)
    ciphertexts.append((key.bin, ''.join(ans)))

for i in range(0b10000000000):
    key = BitArray(uint=i, length=10)
    mySDES = SDES(key.bin, 'b')
    ans = []
    for j in ciphertext:
        ans.append(mySDES.decrypt(j, 'b').bin)
    for x in ciphertexts:
        if (x[1] == ''.join(ans)):
            found_keys.append(x[0])
            found_keys.append(key.bin)
            break

print(found_keys)
myDSDES = DSDES(''.join(found_keys), 'b')
test = []
for x in plaintext:
    test.append(myDSDES.encrypt(x, 'b').bin)

print(test)
print(ciphertext)
