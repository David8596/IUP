import random
import string

def gen_pass(length, letters=True, digits=True, special=False):
    chars = ""
    if letters:
        chars += string.ascii_letters
    if digits:
        chars += string.digits
    if special:
        chars += "!@#$%^&*()"
    
    if not chars:
        chars = string.ascii_letters
    
    return ''.join(random.choice(chars) for _ in range(length))
