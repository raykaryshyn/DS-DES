from pydoc import plain
from bitstring import BitArray
from sdes import SDES, DSDES
import time

plaintext = '4272757465'
ciphertext = '52f0be698a'

possible_ciphertexts = []
possible_cipher_keys = []
found_keys = []
saved_sdes = []

print('DS-DES Meet-in-the-Middle Attack')
print('--------------------------------\n')
print('Attacking...\n')

start_time = time.time()

# Loops over all possible keys for the first S-DES (encryption).
for i in range(0b10000000000):
    current_key = BitArray(uint=i, length=10)
    current_sdes = SDES(current_key.bin, 'b')
    # Applies the current_sdes encryption to all plaintext blocks.
    current_ciphertext = ''
    for j in range(0, len(plaintext), 2):
        current_ciphertext += current_sdes.encrypt(plaintext[j:j+2]).bin
    # Saves the current key and encryption result.
    possible_ciphertexts.append(current_ciphertext)
    possible_cipher_keys.append(current_key.bin)
    # Saves the current_sdes for use in the second DS-DES round.
    saved_sdes.append(current_sdes)

# Loops over all possible keys for the second S-DES (decryption).
for i in range(0b10000000000):
    current_key = BitArray(uint=i, length=10)
    current_sdes = saved_sdes[i]
    current_plaintext = ''
    # Applies the current_sdes decryption to all ciphertext blocks.
    for j in range(0, len(ciphertext), 2):
        current_plaintext += current_sdes.decrypt(ciphertext[j:j+2]).bin
    # Try to find a match of current_plaintext in possible_ciphertexts.
    try:
        found_index = possible_ciphertexts.index(current_plaintext)
        # First key is from the first S-DES.
        found_keys.append(possible_cipher_keys[found_index])
        # Second key is from the current (second) S-DES.
        found_keys.append(current_key.bin)
        break
    except ValueError:
        pass

end_time = time.time() - start_time

if len(found_keys) != 2:
    print('Unable to find the 20-bit key bundle.')
    exit()

print('Found key bundle:', found_keys)
hex_key = BitArray(bin=''.join(found_keys)).hex
print('20-bit combined key bundle as hex:', hex_key, '\n')

print('Testing the found key bundle with the given plaintext "' +
      ''.join([chr(int(plaintext[x:x+2], base=16)) for x in range(0, len(plaintext), 2)]) +
      '" (' + plaintext + '):')
print('Provided ciphertext:\n\t', ciphertext)

test_dsdes = DSDES(''.join(found_keys), 'b')
test_ciphertext = ''
for j in range(0, len(plaintext), 2):
    test_ciphertext += test_dsdes.encrypt(plaintext[j:j+2]).hex

print('Generated ciphertext with provided plaintext and found key bundle (' +
      hex_key + '):\n\t', test_ciphertext)
print('\nCompleted in', '%.2f' % end_time, 'seconds.')
