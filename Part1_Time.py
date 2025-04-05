# part1_time.py

import time
import hashlib

def encrypt_with_time(text: str) -> str:
    """
    Encrypt the given text using the current epoch time as a seed for hashing.
    Steps:
      1) Convert the epoch time to bytes
      2) Generate a SHA-256 hash (64 hex chars)
      3) XOR each character with pairs of hex digits from that hash
    """
    if not text:
        return ""

    # Get current epoch time and convert to bytes
    epoch_str = str(int(time.time())).encode('utf-8')
    # Create a SHA-256 hash
    time_hash = hashlib.sha256(epoch_str).hexdigest()  # 64 hex chars

    encrypted_chars = []
    for i, ch in enumerate(text):
        # Grab 2 hex digits from time_hash (wrapping with modulo if needed)
        h = int(time_hash[(2*i) % len(time_hash):(2*i+2) % len(time_hash)], 16)
        # XOR the ASCII code of the character
        enc_val = ord(ch) ^ h
        # Convert back to a character
        encrypted_chars.append(chr(enc_val))
    
    return "".join(encrypted_chars)
