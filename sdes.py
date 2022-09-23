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
        """Generates the round keys to be used for their respective rounds.
        Populates the list self.round_keys, each 8 bits long.

        The first element used in self.round_keys is to be used in the first round of
        encryption/decryption. The second element for the second round. And so on.
        """
        C, D = self._pc1(self.key)
        # Represents the left shift table for each of the four rounds.
        left_shifts = (1, 2, 2, 2)
        # Either initializes or resets self.round_keys.
        self.round_keys = []

        for round in range(4):
            # Applies the left shift(s) to C and D for each current round.
            C.rol(left_shifts[round])
            D.rol(left_shifts[round])
            # Join and permute (PC2) C and D before adding it to the round key list.
            self.round_keys.append(self._pc2(C + D))

    def _permute(self, input, pos_list):
        """A utility method to permute an input based on a position list.

        Keyword arguments:
        input -- The BitArray to be permuted.
        pos_list -- A list of positions that is the same length as the permuted BitArray
            with indicies of the permuted order.

        Returns:
        A BitArray of the permuted input.
        """
        out = BitArray(len(pos_list))

        i = 0
        for pos in pos_list:
            out.set(input[pos - 1], i)
            i += 1

        return out

    def _pc1(self, k):
        """Permuted Choice 1 is the first permutation to be ran on the provided key before
        round key generation.

        Splits into two lists, C and D, each 5 bits long.

        Keyword arguments:
        k -- The original provided key (BitArray).

        Returns:
        The 5-bit long BitArray variables C and D.
        """
        PC1_C = (3, 5, 2, 7, 4)
        PC1_D = (10, 1, 9, 8, 6)
        return self._permute(k, PC1_C), self._permute(k, PC1_D)

    def _pc2(self, cd):
        """Permuted Choice 2 is the final permutation to be ran on the combination of C and D
        before resulting in a specific (1...4) round key.

        Keyword arguments:
        cd -- The combination of the C and D BitArray variables (10 bits long).

        Returns:
        The 8-bit final key for a specific round (BitArray).
        """
        PC2_pos = (6, 3, 7, 4, 8, 5, 10, 9)
        return self._permute(cd, PC2_pos)

    def _ip(self, input):
        """The Initial Permutation ran on an 8-bit block of input.

        Keyword arguments:
        input -- The initial input block (8 bits long, BitArray).

        Returns:
        The permuted input (8 bits long, BitArray).
        """
        IP_pos = (2, 6, 3, 1, 4, 8, 5, 7)
        return self._permute(input, IP_pos)

    def _ipi(self, preout):
        """The Inverse Initial Permutation ran on the preoutput before resulting in
        the final output.

        Keyword arguments:
        preout -- The preoutput (8 bits long, BitArray).

        Returns:
        The final output (8 bits long, BitArray).
        """
        IPi_pos = (4, 1, 3, 5, 7, 2, 8, 6)
        return self._permute(preout, IPi_pos)

    def _e(self, r):
        """The Expansion Function, E, expands a 4-bit input to 8 bits using
        the E bit-selection table.

        Keyword arguments:
        r -- Input to be expanded (4 bits long, BitArray).

        Returns:
        The expanded input (8 bits long, BitArray).
        """
        E_pos = (4, 1, 2, 3, 2, 3, 4, 1)
        return self._permute(r, E_pos)

    def _s(self, input, s_box):
        """A utility for Selection Functions uses the outer bits of the 4-bit input to select
        the row of the S box and the middle two bits to select the column.

        Keyword arguments:
        input -- Input to be used for selection (4 bits long, BitArray).
        s_box -- 4x4 tuple representing the S box table.

        Returns:
        The 2-bit representation of the selected value (BitArray).
        """
        # Selection of the row using the two outermost bits.
        row = BitArray(2)
        row.set(input[0], 0)
        row.set(input[3], 1)
        # Selection of the column using the two innermost bits.
        column = BitArray(2)
        column.set(input[1], 0)
        column.set(input[2], 1)
        # The 2-bit binary representation of the selected row/column value in s_box.
        return BitArray(uint=s_box[row.uint][column.uint], length=2)

    def _s1(self, b):
        """The S1 Selection Function uses the input to select a value from the S1 S-box.

        Keyword arguments:
        b -- Input to be used for selection (4 bits long, BitArray).

        Returns:
        The 2-bit representation of the selected value (BitArray).
        """
        S1_box = (
            (1, 0, 3, 2),
            (3, 2, 1, 0),
            (0, 2, 1, 3),
            (3, 1, 3, 2)
        )
        return self._s(b, S1_box)

    def _s2(self, b):
        """The S2 Selection Function uses the input to select a value from the S1 S-box.

        Keyword arguments:
        input -- Input to be used for selection (4 bits long, BitArray).

        Returns:
        The 2-bit representation of the selected value (BitArray).
        """
        S2_box = (
            (0, 1, 2, 3),
            (2, 0, 1, 3),
            (3, 0, 1, 0),
            (2, 1, 0, 3)
        )
        return self._s(b, S2_box)

    def _p(self, s):
        """The Permute Function, P, permutes a 4-bit input using the P bit-selection table.

        Keyword arguments:
        s -- Input to be permuted (4 bits long, BitArray).

        Returns:
        The permuted result (4 bits long, BitArray).
        """
        P_pos = (2, 4, 3, 1)
        return self._permute(s, P_pos)

    def _f(self, R, round):
        """The Cipher Function, F, uses R and the current round key, K, to produce F(R, K).

        Keyword arguments:
        R -- Input to be used with the round key (4 bits long, BitArray).
        round -- Current round index (int).

        Returns:
        Result of the Cipher Function (4 bits long, BitArray).
        """
        # XOR of the current round key and the expansion of R.
        B = self.round_keys[round] ^ self._e(R)
        # Splits B (8 bits) into the first 4 bits (B1) and last 4 bits (B2).
        B1, B2 = self._s1(B[:4]), self._s2(B[4:])
        return self._p(B1 + B2)

    def _handleInput(self, msg, type=None):
        """Handles an input message by formatting a binary or hexadecimal
        string representation into a BitArray.

        Keyword arguments:
        msg -- A string representation of one of the supported types.
        type -- Supported types are 'h' (hexadecimal, DEFAULT) and 'b' (binary).

        Returns:
        The resulting BitArray variable from the input message.
        """
        if type == 'b':
            return BitArray(bin=msg)
        else:
            return BitArray(hex=msg)

    def encrypt(self, msg, type=None):
        msg = self._handleInput(msg, type)

        perm = self._ip(msg)
        L, R = perm[:4], perm[4:]

        for round in range(4):
            L, R = R, L ^ self._f(R, round)

        return self._ipi(R + L)

    def decrypt(self, cipher, type=None):
        cipher = self._handleInput(cipher, type)

        perm = self._ip(cipher)
        L, R = perm[:4], perm[4:]

        for round in range(3, -1, -1):
            L, R = R, L ^ self._f(R, round)

        return self._ipi(R + L)


class DSDES:
    """A class to represent the double S-DES (DS-DES) algorithm.
    Uses a specified 20-bit key to encrypt any 8-bit block.
    Accepts hexidecimal and binary string formats for both the key and block.
    Any returns after encryption/decryption are instances of bitstring.BitArray.
    """

    def __init__(self, key, type=None):
        """Sets up two instances of SDES with a specified 20-bit hexadecimal or binary key.
        The most significant 10 bits are used for the first SDES and
        the least significant 10 bits for the second SDES.

        Keyword arguments:
        key --  A string representing the key to be used for encryption/decryption.
            Not required to include the base prefix ('0x' or '0b').
            Binary keys must explicitly define 20 bits.
        type -- The base of the provided key: 
            hexadecimal (default, no arg required) or binary ('b').
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
