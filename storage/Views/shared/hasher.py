import hashlib

def getHash(input_string):
    hashed_value = hashlib.sha256(input_string.encode()).hexdigest()[:32]
    return hashed_value