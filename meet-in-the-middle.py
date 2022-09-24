from pydoc import plain
from bitstring import BitArray
from sdes import SDES, DSDES
import time

plaintext = '4272757465'
ciphertext = '52f0be698a'

possible_ciphertexts = []
found_keys = []
saved_sdes = []

print('DS-DES Meet-in-the-Middle Attack')
print('--------------------------------\n')
print('Attacking...\n')

start_time = time.time()

for i in range(0b10000000000):
    current_key = BitArray(uint=i, length=10)
    current_sdes = SDES(current_key.bin, 'b')
    current_ciphertext = []
    for j in range(0, len(plaintext), 2):
        current_ciphertext.append(current_sdes.encrypt(plaintext[j:j+2]).bin)
    possible_ciphertexts.append((current_key.bin, ''.join(current_ciphertext)))
    saved_sdes.append(current_sdes)

for i in range(0b10000000000):
    current_key = BitArray(uint=i, length=10)
    current_sdes = saved_sdes[i]
    current_plaintext = []
    for j in range(0, len(ciphertext), 2):
        current_plaintext.append(current_sdes.decrypt(ciphertext[j:j+2]).bin)
    for x in possible_ciphertexts:
        if (x[1] == ''.join(current_plaintext)):
            found_keys.append(x[0])
            found_keys.append(current_key.bin)
            break

end_time = time.time() - start_time

print('Found keys:', found_keys)
hex_key = BitArray(bin=''.join(found_keys)).hex
print('20-bit combined key as hex:', hex_key, '\n')

print('Testing the found key with the given plaintext "' +
      ''.join([chr(int(plaintext[x:x+2], base=16)) for x in range(0, len(plaintext), 2)]) +
      '" (' + plaintext + '):')
print('Provided ciphertext:\n\t', ciphertext)

test_dsdes = DSDES(''.join(found_keys), 'b')
test_ciphertext = ""
for j in range(0, len(plaintext), 2):
    test_ciphertext += test_dsdes.encrypt(plaintext[j:j+2]).hex

print('Generated ciphertext with provided plaintext and found key (' +
      hex_key + '):\n\t', test_ciphertext)
print('\nCompleted in', '%.2f' % end_time, 'seconds.')
