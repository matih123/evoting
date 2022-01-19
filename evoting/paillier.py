from Crypto.Util import number
import random
from typing import Tuple

class PrivateKey:
    def __init__(self, p: int, q: int, n: int) -> None:
        self.l = (p - 1) * (q - 1)
        self.m = pow(self.l, -1, n)

class PublicKey:
    def __init__(self, n: int) -> None:
        self.n = n
        self.nsquare = n * n
        self.g = n + 1

def generate_keypair(bits: int):
    p = number.getPrime(bits // 2)
    q = number.getPrime(bits // 2)
    n = p * q
    return PrivateKey(p, q, n), PublicKey(n)

def encrypt(pubkey: PublicKey, message: int, r = None) -> Tuple[int, int]:
    if r is None:
         r = random.randint(1, pubkey.n - 1)
    
    x = pow(r, pubkey.n, pubkey.nsquare)

    c = (pow(pubkey.g, message, pubkey.nsquare) * x) % pubkey.nsquare

    return c, r

def decrypt(privkey: PrivateKey, pubkey: PublicKey, c: int) -> int:
    x = pow(c, privkey.l, pubkey.nsquare) - 1
    plaintext = ((x // pubkey.n) * privkey.m) % pubkey.n
    return plaintext

def add_encrypted(n1: int, n2: int, pubkey: PublicKey):
    return (n1 * n2) % pubkey.nsquare