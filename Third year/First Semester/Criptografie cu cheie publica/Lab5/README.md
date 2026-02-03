## Paillier Cryptosystem 

Minimal Paillier demo using a 27-character alphabet (`space + A-Z`).

### How to run

1) Open a terminal in this folder.
2) Run: `python paillier.py`
3) When asked, type the plaintext you want to encrypt. The script will:
   - Generate a fresh keypair (512-bit modulus).
   - Show the public and private key values.
   - Encode your plaintext, encrypt it, show the ciphertext.
   - Decrypt it back and show the decoded text and integer.

### Notes

- Alphabet: `" ABCDEFGHIJKLMNOPQRSTUVWXYZ"`.
- Messages are uppercased and packed as base-27 integers; decryption reverses this.
- If the encoded message is too large for the modulus, shorten the text or use a bigger key (would require a small code change).
