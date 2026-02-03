"""
Lab 4
- Alphabet: blank + 26 uppercase letters, validated before use.
- Generates random public/private keys with readable-sized primes.
- Encrypts user input block-by-block and immediately decrypts it again.
Designed for clarity in the console; numbers stay small for inspection.
"""

from __future__ import annotations

# Core modules used throughout the script.
import random
from typing import List

# Fixed alphabet required by the assignment: blank + A-Z.
ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# --------------------------- Validation helpers --------------------------- #


def validate_text(text: str) -> str:
    """Return uppercase text if it only uses characters from the alphabet."""
    text = text.upper()
    bad_chars = sorted({ch for ch in text if ch not in ALPHABET})
    if bad_chars:
        raise ValueError(
            "Only spaces and letters A-Z are allowed. "
            f"Problem characters: {', '.join(bad_chars)}"
        )
    return text


# ---------------------------- Number utilities ---------------------------- #


def is_prime(number: int) -> bool:
    """Quick trial-division check: fine for the small demo values we use."""
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2
    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def random_prime(low: int, high: int) -> int:
    """Pick a random prime from [low, high]."""
    while True:
        candidate = random.randint(low, high)
        if is_prime(candidate):
            return candidate


def gcd(a: int, b: int) -> int:
    # Classic Euclidean algorithm.
    while b:
        a, b = b, a % b
    return a


def mod_inverse(a: int, m: int) -> int:
    """
    Return the modular inverse of a modulo m.

    Uses the extended Euclidean algorithm so we can compute the private RSA
    exponent (d), which must satisfy (a * d) % m == 1 when a = e and m = phi.
    """
    t, new_t = 0, 1  # track Bézout coefficients for the inverse
    r, new_r = m, a  # start the remainder chain with (m, a)
    while new_r != 0:
        quotient = r // new_r  # integer division used by Euclid's algorithm
        t, new_t = new_t, t - quotient * new_t  # propagate coefficient updates
        r, new_r = new_r, r - quotient * new_r  # shrink remainders step by step
    if r != 1:
        raise ValueError("Inverse does not exist.")
    return t % m  # final coefficient is the modular inverse of a (mod m)


# ------------------------------ RSA primitives ---------------------------- #


def generate_keypair() -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Build a public/private key pair.

    The interval [200, 400] keeps numbers small enough to read easily.
    """
    # Choose two random primes in the readable interval.
    p = random_prime(200, 400)  # first random prime factor
    q = random_prime(200, 400)  # second random prime factor
    while q == p:
        q = random_prime(200, 400)  # regenerate until primes differ

    # Core RSA parameters.
    n = p * q  # modulus shared by both keys
    phi = (p - 1) * (q - 1)  # Euler totient: counts usable residues

    # Pick a small odd exponent that is coprime with phi.
    e = 3
    while gcd(e, phi) != 1:
        e += 2  # try the next odd exponent until coprime with phi

    # Compute private exponent via modular inverse.
    d = mod_inverse(e, phi)  # find d so that (e * d) % phi == 1
    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key


# -------------------------- Text/number conversion ------------------------ #


def text_to_numbers(text: str) -> List[int]:
    """Convert a validated string into alphabet indices (space=0, A=1, ...)."""
    return [ALPHABET.index(ch) for ch in text]


def numbers_to_text(numbers: List[int]) -> str:
    """Convert alphabet indices back into readable characters."""
    for value in numbers:
        if value < 0 or value >= len(ALPHABET):
            raise ValueError(f"Value {value} does not map to the alphabet.")
    return "".join(ALPHABET[value] for value in numbers)


def encrypt(plaintext: str, public_key: tuple[int, int]) -> List[int]:
    """
    Encrypt plaintext using the provided RSA public key (n, e).

    Validates the text, maps each character to its alphabet index, then applies
    modular exponentiation (value^e mod n) to produce readable ciphertext
    blocks for each character.
    """
    # RSA encryption on a character-by-character basis.
    plaintext = validate_text(plaintext)  # enforce alphabet rule
    n, e = public_key  # unpack modulus and exponent
    return [
        pow(value, e, n) for value in text_to_numbers(plaintext)
    ]  # modular exponentiation per character index


def decrypt(ciphertext: List[int], private_key: tuple[int, int]) -> str:
    """
    Decrypt ciphertext blocks using the RSA private key (n, d).

    Checks that every block is a valid integer within the modulus range, applies
    modular exponentiation (block^d mod n) to recover alphabet indices, and
    converts those indices back into the original plaintext.
    """
    # RSA decryption followed by conversion back to characters.
    n, d = private_key  # unpack modulus and private exponent
    if not ciphertext:
        raise ValueError("Ciphertext cannot be empty.")
    for block in ciphertext:
        if not isinstance(block, int) or block < 0 or block >= n:
            raise ValueError(f"Ciphertext block {block} is out of range.")
    numbers = [
        pow(block, d, n) for block in ciphertext
    ]  # modular exponentiation to recover alphabet indices
    return numbers_to_text(numbers)  # convert indices back to characters


def main() -> None:
    """Interactive console demo that showcases keygen, encrypt, and decrypt."""
    print("=" * 60)
    print(" RSA demo (alphabet: space + A-Z) ".center(60, "="))
    print("=" * 60)

    public_key, private_key = generate_keypair()
    print(f"Public key (n, e): {public_key}")
    print(f"Private key (n, d): {private_key}")
    print(f"Modulus n has {len(str(public_key[0]))} digits\n")

    # Ask the user for a sentence that follows the alphabet rule.
    plaintext = input("Enter plaintext: ")
    ciphertext = encrypt(plaintext, public_key)
    print("\nEncrypted blocks:")
    print(" ".join(str(block) for block in ciphertext))

    print("\nDecrypting with the private key ...")
    # Reverse the process using the private exponent.
    recovered = decrypt(ciphertext, private_key)
    print(f"Recovered plaintext: {recovered}")

    print("\nAll done! Run the script again to get a fresh random key pair.")


if __name__ == "__main__":
    main()

