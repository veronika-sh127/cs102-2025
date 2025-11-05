def decrypt_scytale(plaintext, n):
    """
    Расшифровка шифра Скитала
    """
    rows = len(plaintext) // n
    if len(plaintext) % n != 0:
        rows += 1

    ind = 0
    columns = []
    for i in range(n):
        col = []
        for j in range(rows):
            if ind < len(plaintext):
                col.append(plaintext[ind])
                ind += 1
        columns.append(col)

    ciphertext = ""
    for i in range(rows):
        for j in range(n):
            if i < len(columns[j]):
                ciphertext += columns[j][i]
    return ciphertext


print(decrypt_scytale("РНОАЫЙКЕСЕ_КТВА", 5))
