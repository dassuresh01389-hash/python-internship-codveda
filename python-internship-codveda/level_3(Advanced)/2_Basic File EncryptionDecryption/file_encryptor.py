#!/usr/bin/env python3
"""
File Encryption/Decryption – Internship Submission
Author: Suresh Das
Date: 2026-08-28

Description:
    Encrypts or decrypts a text file using Fernet symmetric encryption.
    A password is used to derive a secure key via PBKDF2.

Usage:
    # Encrypt a file
    python file_encryptor.py --mode encrypt --input secret.txt --output secret.enc --password mypassword

    # Decrypt a file
    python file_encryptor.py --mode decrypt --input secret.enc --output secret_decrypted.txt --password mypassword

Dependencies:
    cryptography (install with: pip install cryptography)
"""

import os
import sys
import argparse
import base64
from pathlib import Path
from typing import Optional

# We use cryptography for secure encryption.
# If not installed, we fall back to a simple Caesar cipher (not secure, for demo only).
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️  cryptography library not installed. Falling back to Caesar cipher (insecure).")
    print("   For production, install: pip install cryptography")


# ---------- Fernet Encryption (Secure) ----------
class FernetEncryptor:
    """Encrypt/decrypt using Fernet symmetric encryption."""

    def __init__(self, password: str, salt: bytes = b'salt_1234'):
        self.password = password.encode()
        self.salt = salt

    def _derive_key(self) -> bytes:
        """Derive a Fernet key from password and salt."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key

    def encrypt(self, plaintext: bytes) -> bytes:
        """Encrypt bytes and return ciphertext."""
        key = self._derive_key()
        f = Fernet(key)
        return f.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """Decrypt bytes and return plaintext."""
        key = self._derive_key()
        f = Fernet(key)
        try:
            return f.decrypt(ciphertext)
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")


# ---------- Caesar Cipher (Fallback, Insecure) ----------
class CaesarCipher:
    """
    Simple Caesar cipher for demo when cryptography is not available.
    NOT SECURE – only for educational purposes.
    """

    def __init__(self, password: str):
        # Use password to determine shift (0-25)
        self.shift = sum(ord(c) for c in password) % 26

    def encrypt(self, plaintext: bytes) -> bytes:
        shift = self.shift
        result = []
        for byte in plaintext:
            # Only shift printable ASCII characters (32-126)
            if 32 <= byte <= 126:
                shifted = (byte - 32 + shift) % 95 + 32
                result.append(shifted)
            else:
                result.append(byte)
        return bytes(result)

    def decrypt(self, ciphertext: bytes) -> bytes:
        shift = self.shift
        result = []
        for byte in ciphertext:
            if 32 <= byte <= 126:
                shifted = (byte - 32 - shift) % 95 + 32
                result.append(shifted)
            else:
                result.append(byte)
        return bytes(result)


# ---------- Main File Processing ----------
def process_file(
    mode: str,
    input_file: str,
    output_file: str,
    password: str,
    use_fernet: bool = True
) -> None:
    """
    Read input file, encrypt/decrypt content, write to output file.
    """
    # Check if input file exists
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Read input file (binary mode to handle any content)
    with open(input_file, "rb") as f:
        data = f.read()

    # Choose encryptor
    if use_fernet and CRYPTO_AVAILABLE:
        encryptor = FernetEncryptor(password)
    else:
        encryptor = CaesarCipher(password)
        if use_fernet:
            print("⚠️  cryptography not available, using Caesar cipher instead.")

    # Perform operation
    if mode == "encrypt":
        result = encryptor.encrypt(data)
        print(f"✅ File encrypted successfully.")
    elif mode == "decrypt":
        result = encryptor.decrypt(data)
        print(f"✅ File decrypted successfully.")
    else:
        raise ValueError(f"Invalid mode: {mode}")

    # Write output file
    with open(output_file, "wb") as f:
        f.write(result)
    print(f"💾 Output written to: {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt a file using a password."
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["encrypt", "decrypt"],
        help="Mode: encrypt or decrypt"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input file"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to output file"
    )
    parser.add_argument(
        "--password",
        required=True,
        help="Password for encryption/decryption"
    )
    parser.add_argument(
        "--fernet",
        action="store_true",
        default=True,
        help="Use Fernet encryption (secure, requires cryptography package) [default]"
    )
    parser.add_argument(
        "--caesar",
        action="store_true",
        help="Use Caesar cipher (insecure, for demo only)"
    )
    args = parser.parse_args()

    # Determine encryption method
    use_fernet = args.fernet and not args.caesar

    try:
        process_file(
            mode=args.mode,
            input_file=args.input,
            output_file=args.output,
            password=args.password,
            use_fernet=use_fernet
        )
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"❌ Permission error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # If no arguments, show help
    if len(sys.argv) == 1:
        print(__doc__)
        sys.exit(0)
    main()