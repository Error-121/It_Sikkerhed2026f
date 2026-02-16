import os
from cryptography.fernet import Fernet

KEY_PATH = "scr/Local_DB/secret.key"

def generate_key():
    """Generer en Fernet krypteringsnøgle og gem den i en fil"""
    return Fernet.generate_key()

def save_key(key):
    """Gem krypteringsnøglen i en fil"""
    # sørg for at mappen eksisterer
    os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)

    # Skriv nøglen til filen
    with open(KEY_PATH, 'wb') as key_file:
        key_file.write(key)
    print(f"Encryption key gemt til {KEY_PATH}")

def load_key():
    """Indlæs krypteringsnøglen fra filen"""
    if not os.path.exists(KEY_PATH):
        # Hvis nøglen ikke findes, generer en ny og gem den
        key = generate_key()
        save_key(key)
        return key

    # Læs nøglen fra filen
    with open(KEY_PATH, 'rb') as key_file:
        return key_file.read()

def get_cipher():
    """Returner en Fernet cipher objekt baseret på den indlæste nøgle"""
    key = load_key()
    return Fernet(key)