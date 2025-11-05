def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    alf = 26
    for index, char in enumerate(plaintext):
        if char.isalpha():
            if char.isupper():
                base = ord("A")
            else:
                base = ord("a")
            shift = ord(keyword[index % len(keyword)]) - base
            ciphertext += chr((ord(char) - base + shift) % alf + base)
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for index, char in enumerate(ciphertext):
        if char.isalpha():
            if char.isupper():
                base = ord("A")
            else:
                base = ord("a")
            shift = ord(keyword[index % len(keyword)]) - base
            plaintext += chr((ord(char) - base - shift) % 26 + base)
        else:
            plaintext += char
    return plaintext


if __name__ == "__main__":
    print(encrypt_vigenere("introduction to python", "lsci"))
    print(decrypt_vigenere("tfvzzvwkeaqv lq aqvpzf", "lsci"))
