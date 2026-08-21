import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import caesar_cipher, atbash_cipher, rot13_cipher, vigenere_cipher, sha256

def test_caesar_encrypt():
    assert caesar_cipher("HELLO", 3) == "KHOOR"

def test_caesar_decrypt():
    assert caesar_cipher("KHOOR", 3, decrypt=True) == "HELLO"

def test_atbash():
    assert atbash_cipher("ABC XYZ") == "ZYX CBA"

def test_rot13():
    assert rot13_cipher("HELLO") == "URYYB"

def test_vigenere():
    assert vigenere_cipher("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
    assert vigenere_cipher("LXFOPVEFRNHR", "LEMON", decrypt=True) == "ATTACKATDAWN"

def test_sha256():
    assert sha256("hello") == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

def test_preserves_symbols():
    assert caesar_cipher("Hello, World! 123", 3) == "Khoor, Zruog! 123"
