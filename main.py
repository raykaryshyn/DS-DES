from sdes import DSDES

hex_str = '0x586519b031aaee9a235247601fb37baefbcd54d8c3763f8523d2a1315ed8bdcc'

dsdes = DSDES('0x0', '0x0')
print(dsdes.encrypt(hex_str))
