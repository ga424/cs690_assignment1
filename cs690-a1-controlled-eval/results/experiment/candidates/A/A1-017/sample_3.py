def is_palindrome_normalized(text):
    normalized = (char.lower() for char in text if char.isascii() and char.isalnum())
    sequence = ''.join(normalized)
    return sequence == sequence[::-1]
