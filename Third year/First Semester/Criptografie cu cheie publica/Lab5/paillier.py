"""
Paillier cryptosystem demo with a 27-character alphabet (space + A-Z).
Run `python paillier.py`, enter a plaintext, and the script will:
1) Generate a fresh keypair
2) Encrypt your plaintext
3) Decrypt it back
All key components and intermediate values are printed for clarity.
"""

import math
import secrets
from dataclasses import dataclass
from typing import Tuple

ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # 27 symbols: leading space then A-Z
RADIX = len(ALPHABET)


# ---------- Number theory helpers ----------
def lcm(a: int, b: int) -> int:
    """Least common multiple, used for lambda."""
    return abs(a * b) // math.gcd(a, b)


def is_probable_prime(n: int, rounds: int = 12) -> bool:
    """Miller-Rabin primality check for odd n > 2."""
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # quick filters
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    # Write n-1 as 2^s * d with d odd
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2  # random base in [2, n-2]
        x = pow(a, d, n)  # a^d mod n
        if x == 1 or x == n - 1:  # strong probable prime for this base
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)  # square repeatedly
            if x == n - 1:  # passes this round
                break
        else:
            return False
    return True


def random_prime(bits: int) -> int:
    """Generate a probable prime of given bit length (retries until prime)."""
    if bits < 4:
        raise ValueError("Bit length too small for prime generation")
    while True:
        # Force top bit and oddness to get the right size and be odd (all primes are odd)
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(candidate):  # accept only if it passes Miller-Rabin
            return candidate


def modinv(a: int, m: int) -> int:
    """Modular inverse a^-1 mod m (raises if not invertible)."""
    try:
        return pow(a, -1, m) 
    except ValueError as exc:  # pragma: no cover - unlikely for valid keys
        raise ValueError("Inverse does not exist") from exc


def L(u: int, n: int) -> int:
    """L function from Paillier: L(u) = (u-1)//n."""
    return (u - 1) // n


# ---------- Encoding helpers ----------
def encode_text(text: str) -> int:
    """Encode text to integer using base-27 alphabet. Validates characters."""
    if not text:
        raise ValueError("Plaintext must not be empty")  # reject empty input
    text = text.upper()  # normalize to uppercase for alphabet lookup
    value = 0  # accumulator for base-27 digits
    for ch in text:
        idx = ALPHABET.find(ch)  # position of character in alphabet
        if idx == -1:
            raise ValueError(f"Invalid character: {ch!r}. Allowed: space and A-Z.")  
        # Treat the alphabet index as a base-27 digit: shift the accumulated
        # value left by one digit (multiply by 27) and append the new digit.
        # ex: AB -> encodes to 29
        # value = 0 * 27 + 1 = 1
        # value = 1 * 27 + 2 = 29
        value = value * RADIX + idx
    return value  


def decode_text(value: int) -> str:
    if value < 0:
        raise ValueError("Decoded value must be non-negative")
    if value == 0:
        return ALPHABET[0]  # space
    chars = []  # will collect digits (characters) in reverse
    while value:
        value, idx = divmod(value, RADIX)  # split off least-significant base-27 digit
        chars.append(ALPHABET[idx])  # map digit back to a character
    return "".join(reversed(chars))  # reverse to restore original order


# ---------- Key structures ----------
@dataclass(frozen=True)
class PublicKey:
    n: int
    g: int

    @property
    def n_sq(self) -> int:
        return self.n * self.n  # cache n^2 for repeated use

    def encrypt_int(self, m: int) -> int:
        """Encrypt integer m with random blinding r."""
        if not (0 <= m < self.n):
            raise ValueError("Plaintext integer must satisfy 0 <= m < n")
        # Choose random r in [1, n-1] coprime with n (blinding factor)
        while True:
            r = secrets.randbelow(self.n - 1) + 1
            if math.gcd(r, self.n) == 1:
                break
        c1 = pow(self.g, m, self.n_sq)      # g^m mod n^2
        c2 = pow(r, self.n, self.n_sq)      # r^n mod n^2 (randomizes encryption)
        return (c1 * c2) % self.n_sq        # ciphertext

    def encrypt_text(self, text: str) -> int:
        """Encode text then encrypt."""
        m = encode_text(text)
        return self.encrypt_int(m)


@dataclass(frozen=True)
class PrivateKey:
    lam: int
    mu: int
    n: int

    @property
    def n_sq(self) -> int:
        return self.n * self.n  # cache n^2 for repeated use

    def decrypt_int(self, c: int) -> int:
        """Decrypt integer ciphertext to integer plaintext."""
        if not (0 <= c < self.n_sq):
            raise ValueError("Ciphertext must satisfy 0 <= c < n^2")
        u = pow(c, self.lam, self.n_sq)   # c^lambda mod n^2
        l_val = L(u, self.n)              # apply L function
        return (l_val * self.mu) % self.n # multiply by mu mod n to get m

    def decrypt_text(self, c: int) -> str:
        """Decrypt integer ciphertext to plaintext string."""
        m = self.decrypt_int(c)
        return decode_text(m)


def generate_keypair(bits: int = 512) -> Tuple[PublicKey, PrivateKey]:
    """Generate Paillier keypair with ~bits modulus."""
    half = bits // 2
    p = random_prime(half)  # first large prime
    q = random_prime(half)  # second large prime
    while p == q:
        q = random_prime(half)

    # Build modulus and key parameters
    n = p * q                   # modulus n
    n_sq = n * n                # n^2 used throughout Paillier
    lam = lcm(p - 1, q - 1)     # lambda = lcm(p-1, q-1) (Carmichael function)

    # Choose g s.t. L(g^lambda mod n^2) is invertible mod n (so mu exists).
    # A common choice is g = n + 1; here we randomize until it works.
    while True:
        g = secrets.randbelow(n_sq - 1) + 1  # random g in [1, n^2)
        x = pow(g, lam, n_sq)                # g^lambda mod n^2
        l_val = L(x, n)                      # compute L(g^lambda mod n^2)
        if math.gcd(l_val, n) == 1:          # ensure mu exists
            break

    mu = modinv(l_val, n)  # mu = (L(g^lambda mod n^2))^{-1} mod n
    return PublicKey(n=n, g=g), PrivateKey(lam=lam, mu=mu, n=n)


# ---------- One-shot demo ----------
def run_demo() -> None:
    print("Paillier Cryptosystem (space + A-Z)")
    try:
        # 1) Ask user for plaintext, then encode to integer m
        message = input("Enter plaintext to encrypt: ")
        m_val = encode_text(message)  # validate + encode to integer

        # 2) Generate fresh keypair (public + private) per run
        pub, priv = generate_keypair(bits=512)

        # Display keys
        print("\nPublic key:")
        print(f"  n = {pub.n}")
        print(f"  g = {pub.g}")
        print("\nPrivate key:")
        print(f"  lambda = {priv.lam}")
        print(f"  mu = {priv.mu}")

        # 3) Size check: encoded message must satisfy m < n
        if m_val >= pub.n:
            raise ValueError("Encoded message too large for this modulus; use a shorter text.")

        print("\nPlaintext:")
        print(f"  text = {message.upper()}")
        print(f"  encoded integer = {m_val}")

        # 4) Encryption: pick random r coprime with n; compute c = g^m * r^n mod n^2
        c = pub.encrypt_int(m_val)
        print("\nCiphertext:")
        print(f"  c = {c}")

        # 5) Decryption: compute u = c^lambda mod n^2, then m = L(u)*mu mod n
        m_dec = priv.decrypt_int(c)
        text_dec = decode_text(m_dec)
        print("\nDecryption:")
        print(f"  decoded integer = {m_dec}")
        print(f"  decoded text    = {text_dec}")
    except Exception as exc:
        print(f"[error] {exc}")


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()

