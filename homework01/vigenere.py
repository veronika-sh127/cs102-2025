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
    index = 0
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                base = ord("A")
                shift = ord(keyword[index % len(keyword)]) - base
            else:
                base = ord("a")
                shift = ord(keyword[index % len(keyword)]) - base
            ciphertext += chr((ord(char) - base + shift) % 26 + base)
            index +=1
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
    index = 0
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                base = ord("A")
                shift = ord(keyword[index % len(keyword)]) - base
            else:
                base = ord("a")
                shift = ord(keyword[index % len(keyword)]) - base
            plaintext += chr((ord(char) - base - shift) % 26 + base)
            index += 1
        else:
            plaintext += char
    return plaintext

print(decrypt_vigenere('LXFOPVEFRNHR', "LEMON"))