from bitstring import BitArray
from sdes import DSDES
import time

plaintext = '4272757465'
ciphertext = '52f0be698a'

found_keys = []

print('DS-DES Brute Force Attack')
print('-------------------------\n')
print('Attacking...\n')

start_time = time.time()

# Loop through all possible 20-bit key bundle values.
for i in range(0b100000000000000000000):
    current_key = BitArray(uint=i, length=20)
    current_dsdes = DSDES(current_key.bin, 'b')
    test = ""
    # Applies the current_dsdes encryption to all plaintext blocks.
    for j in range(0, len(plaintext), 2):
        test += current_dsdes.encrypt(plaintext[j:j+2]).hex
    # Stops if the resulting ciphertext equals the desired ciphertext.
    if test == ciphertext:
        found_keys.extend([current_key[:10].bin, current_key[10:].bin])
        break

end_time = time.time() - start_time

print('Found key bundle:', found_keys)
hex_key = BitArray(bin=''.join(found_keys)).hex
print('20-bit combined key bundle as hex:', hex_key, '\n')

print('Testing the found key bundle with the given plaintext "' +
      ''.join([chr(int(plaintext[x:x+2], base=16)) for x in range(0, len(plaintext), 2)]) +
      '" (' + plaintext + '):')
print('Provided ciphertext:\n\t', ciphertext)

test_dsdes = DSDES(''.join(found_keys), 'b')
test_ciphertext = ""
for j in range(0, len(plaintext), 2):
    test_ciphertext += test_dsdes.encrypt(plaintext[j:j+2]).hex

print('Generated ciphertext with provided plaintext and found key bundle (' +
      hex_key + '):\n\t', test_ciphertext)
print('\nCompleted in', '%.2f' % end_time, 'seconds.')
