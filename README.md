# (D)S-DES

Contains both the implementation, tests, and exploitation of (Double) Simplified Data Encryption Standard.

- **Implementation**
    - *sdes.py* (contains both S-DES and DS-DES)
- **Tests**
    - *kats.py* (S-DES known answer tests using ECB mode)
    - *cbc-decryption.py* (tests the exploitation results using CBC mode)
- **Exploitation**
    - *meet-in-the-middle.py*
    - *brute-force.py*

Requires the *bitstring* Python package which can be installed with `pip install bitstring`.
