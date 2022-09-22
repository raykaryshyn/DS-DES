from bitstring import BitArray


class SDES:
    """A class to represent the simple-DES (S-DES) algorithm.
    Uses a specified 10-bit key to encrypt any 8-bit block.
    Accepts hexidecimal and binary string formats for both the key and block.
    Internally uses the bitstring package and its BitArray class for easier bit manipulation.
    Any returns after encryption/decryption are instances of BitArray.
    """

    def __init__(self, key, type=None):
        """Sets up an instance of SDES with a specified 10-bit hexadecimal or binary key.

        Keyword arguments:
        key -- A string representing the key to be used for encryption/decryption.
            Not required to include the base prefix ('0x' or '0b').
            Binary keys must explicitly define 10 bits.
        type -- The base of the provided key: 
            hexadecimal (default, no arg required) or binary ('b').
        """
        if type == 'b':
            self.key = BitArray(bin=key)
        else:
            # First converts hex string representation to binary
            # and pads the MSBs with 0s for the whole being 10 bits long.
            self.key = BitArray(bin=(bin(int(key, 16))[2:]).zfill(10))
        # Populates the list self.round_keys.
        self._genRoundKeys()

    def _genRoundKeys(self):
        C, D = self._pc1(self.key)
        left_shifts = (1, 2, 2, 2)
        self.round_keys = []

        for round in range(4):
            C.rol(left_shifts[round])
            D.rol(left_shifts[round])
            CD = C.copy()
            CD.append(D)
            self.round_keys.append(self._pc2(CD))

    def _permute(self, input, pos_list, length):
        out = BitArray(length)

        i = 0
        for pos in pos_list:
            out.set(input[pos - 1], i)
            i += 1

        return out

    def _pc1(self, k):
        PC1_C = (3, 5, 2, 7, 4)
        PC1_D = (10, 1, 9, 8, 6)
        return self._permute(k, PC1_C, 5), self._permute(k, PC1_D, 5)

    def _pc2(self, cd):
        PC2_pos = (6, 3, 7, 4, 8, 5, 10, 9)
        return self._permute(cd, PC2_pos, 8)

    def _ip(self, input):
        IP_pos = (2, 6, 3, 1, 4, 8, 5, 7)
        return self._permute(input, IP_pos, 8)

    def _ipi(self, a):
        IPi_pos = (4, 1, 3, 5, 7, 2, 8, 6)
        return self._permute(a, IPi_pos, 8)

    def _split_perm(self, perm):
        return (perm[:4], perm[4:])

    def _e(self, a):
        E_pos = (4, 1, 2, 3, 2, 3, 4, 1)
        return self._permute(a, E_pos, 8)

    def _p(self, a):
        P_pos = (2, 4, 3, 1)
        return self._permute(a, P_pos, 4)

    def _s1(self, a):
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

        return BitArray(uint=S1_box[row.uint][column.uint], length=2)

    def _s2(self, a):
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

        return BitArray(uint=S2_box[row.uint][column.uint], length=2)

    def _f(self, R, round):
        B = self.round_keys[round] ^ self._e(R)
        B1, B2 = self._s1(B[:4]), self._s2(B[4:])
        B1.append(B2)

        return self._p(B1)

    def _handleInput(self, msg, type=None):
        if type == 'b':
            msg = BitArray(bin=msg)
        else:
            msg = BitArray(hex=msg)

        return msg

    def encrypt(self, msg, type=None):
        msg = self._handleInput(msg, type)

        perm = self._ip(msg)
        L, R = self._split_perm(perm)

        for round in range(4):
            L, R = R, L ^ self._f(R, round)

        L, R = R, L
        L.append(R)

        return self._ipi(L)

    def decrypt(self, cipher, type=None):
        cipher = self._handleInput(cipher, type)

        perm = self._ip(cipher)
        L, R = self._split_perm(perm)

        for round in range(3, -1, -1):
            L, R = R, L ^ self._f(R, round)

        L, R = R, L
        L.append(R)

        return self._ipi(L)


class DSDES:
    """A class to represent the double S-DES (DS-DES) algorithm.
    Uses a specified 20-bit key to encrypt any 8-bit block.
    Accepts hexidecimal and binary string formats for both the key and block.
    Any returns after encryption/decryption are instances of bitstring.BitArray.
    """

    def __init__(self, key, type=None):
        """Sets up two instances of SDES with a specified 20-bit hexadecimal or binary key.
        See SDES documentation for key and type restrictions.

        Keyword arguments:
        key -- Key.
        type -- Key type (not required, default same as SDES).
        """
        if type == 'b':
            key = BitArray(bin=key)
        else:
            # First converts hex string representation to binary
            # and pads the MSBs with 0s for the whole being 20 bits long.
            key = BitArray(bin=(bin(int(key, 16))[2:]).zfill(20))

        self.sdes1 = SDES(key[:10].bin, 'b')
        self.sdes2 = SDES(key[10:].bin, 'b')

    def encrypt(self, msg, type=None):
        return self.sdes2.encrypt(self.sdes1.encrypt(msg, type).bin, type)

    def decrypt(self, cipher, type=None):
        return self.sdes1.decrypt(self.sdes2.decrypt(cipher, type).bin, type)
