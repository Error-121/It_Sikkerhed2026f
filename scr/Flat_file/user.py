from dataclasses import dataclass
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

@dataclass
class User:
    user_id: int
    first_name: str
    last_name: str
    address: str
    street_number: str
    password: str
    enabled: bool = True

    def __init__(self, user_id, first_name, last_name, address, street_number, password, enabled=True, encrypt=False, cipher=None):
        '''Initialiser bruger med valgfri kryptering af PII-felter'''
        self.user_id = user_id
        self.enabled = enabled

        if encrypt and cipher:
            # Krypter PII-felterne før lagring
            self.first_name = self.encrypt_field(first_name, cipher)
            self.last_name = self.encrypt_field(last_name, cipher)
            self.address = self.encrypt_field(address, cipher)
            self.street_number = self.encrypt_field(street_number, cipher)
            # Hash passwordet før lagring
            self.password = self.hash_password(password)
        else:
            # Gem PII-felterne som de er, uden kryptering
            self.first_name = first_name
            self.last_name = last_name
            self.address = address
            self.street_number = street_number
            self.password = password

    @staticmethod
    def hash_password(password):
        """Hash passwordet ved hjælp af Argon2"""
        ph = PasswordHasher()
        return ph.hash(password)

    @staticmethod
    def verify_password(hashed_password, plaintext_password):
        """Verificer et plaintext password mod det Argon2 hash"""
        ph = PasswordHasher()
        try:
            ph.verify(hashed_password, plaintext_password)
            return True
        except VerifyMismatchError:
            return False

    @staticmethod
    def encrypt_field(plaintext, cipher):
        """Krypter et plaintext felt ved hjælp af Fernet cipher"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        return cipher.encrypt(plaintext).decode()

    @staticmethod
    def decrypt_field(encrypted_text, cipher):
        """Dekrypter et krypteret felt ved hjælp af Fernet cipher"""
        if isinstance(encrypted_text, str):
            encrypted_text = encrypted_text.encode()
        return cipher.decrypt(encrypted_text).decode()