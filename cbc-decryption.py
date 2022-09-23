from bitstring import BitArray
from sdes import DSDES

key = 'cfd53'
myDSDES = DSDES(key)

iv = BitArray(uint=0x9c, length=8)
cipher = '586519b031aaee9a235247601fb37baefbcd54d8c3763f8523d2a1315ed8bdcc'
cipher_bytes = bytearray.fromhex(cipher)

prev = iv
plain = ''
for i in range(len(cipher_bytes)):
    # Take next byte from cipher_bytes and transform into an 8-bit BitArray.
    encrypted_byte = BitArray(bytes=cipher_bytes[i:i+1])
    # Call the decrypt function on the byte.
    pre_decrypted_byte = myDSDES.decrypt(encrypted_byte.bin, 'b')
    # Finish the CBC decryption by XORing by the previous encrypted_byte (or IV).
    decrypted_byte = prev ^ pre_decrypted_byte
    # Append the ASCII character value of decrypted_byte to plain.
    plain += chr(int((decrypted_byte).hex, base=16))
    # Save the current encrypted_byte for decrypting the next byte in cipher_bytes.
    prev = encrypted_byte

print('CBC DS-DES Decryption')
print('---------------------\n')
print('20-bit Key:', key, '(' + BitArray(hex=key).bin + ')')
print('Ciphertext:', cipher)
print('Plaintext: ', plain)
