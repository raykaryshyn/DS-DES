from sdes import SDES

# 0000000000
# 1111111111
# 0111101000
# 1000010111

sdes = SDES('1000010111', 'b')
print(sdes.encrypt(sdes.encrypt('10101010', 'b').bin, 'b').bin)
