import math
import hashlib
import requests
import secrets
import string
import time
import hashlib

def crack_hash(target_hash, dictionary_path, hash_type="sha1"):
    """Attempts to match a target hash by hashing a dictionary of passwords."""
    try:
        with open(dictionary_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                # Select the hashing algorithm
                if hash_type == "sha1":
                    guess = hashlib.sha1(word.encode()).hexdigest()
                elif hash_type == "md5":
                    guess = hashlib.md5(word.encode()).hexdigest()
                elif hash_type == "sha256":
                    guess = hashlib.sha256(word.encode()).hexdigest()
                else:
                    continue

                if guess == target_hash.lower():
                    return word
        return None
    except Exception as e:
        return f"Error: {str(e)}"


def get_pwned_count(password):
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200: return -1
        for line in response.text.splitlines():
            h, count = line.split(':')
            if h == suffix: return int(count)
        return 0
    except:
        return -1

def calculate_entropy(password):
    if not password: return 0, "N/A"
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(not c.isalnum() for c in password): pool += 32
    
    entropy = len(password) * math.log2(pool) if pool > 0 else 0
    
    if entropy < 40: rating = "Very Weak"
    elif entropy < 60: rating = "Weak"
    elif entropy < 80: rating = "Strong"
    else: rating = "Military Grade"
    
    return round(entropy, 2), rating

def generate_secure_password(length=16):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))
    