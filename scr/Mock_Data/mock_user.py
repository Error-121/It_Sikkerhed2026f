from dataclasses import dataclass
from scr.Flat_file.auth import get_cipher
from scr.Flat_file.user import User

@dataclass
class User:
    user_id: int
    first_name: str
    last_name: str
    address: str
    street_number: str
    password: str
    enabled: bool

# Initialize cipher for mock data
cipher = get_cipher()

# Mock user 1: Regular enabled user
mock_user_1_plaintext = {
    "user_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "address": "Main Street",
    "street_number": "123",
    "password": "Password123!",
    "enabled": True
}

mock_user_1 = User(
    user_id=1,
    first_name="John",
    last_name="Doe",
    address="Main Street",
    street_number="123",
    password="Password123!",
    enabled=True,
    encrypt=True,
    cipher=cipher
)

# Mock user 2: Disabled user
mock_user_2_plaintext = {
    "user_id": 2,
    "first_name": "Jane",
    "last_name": "Smith",
    "address": "Oak Avenue",
    "street_number": "456",
    "password": "SecurePass456@",
    "enabled": False
}

mock_user_2 = User(
    user_id=2,
    first_name="Jane",
    last_name="Smith",
    address="Oak Avenue",
    street_number="456",
    password="SecurePass456@",
    enabled=False,
    encrypt=True,
    cipher=cipher
)

# Mock user 3: User with special characters
mock_user_3_plaintext = {
    "user_id": 3,
    "first_name": "Bob",
    "last_name": "Johnson",
    "address": "Elm Road",
    "street_number": "789",
    "password": "MyP@ssw0rd",
    "enabled": True
}

mock_user_3 = User(
    user_id=3,
    first_name="Bob",
    last_name="Johnson",
    address="Elm Road",
    street_number="789",
    password="MyP@ssw0rd",
    enabled=True,
    encrypt=True,
    cipher=cipher
)

# Mock user 4: User for deletion/update tests
mock_user_4_plaintext = {
    "user_id": 4,
    "first_name": "Alice",
    "last_name": "Williams",
    "address": "Pine Boulevard",
    "street_number": "101",
    "password": "Test1234#",
    "enabled": True
}

mock_user_4 = User(
    user_id=4,
    first_name="Alice",
    last_name="Williams",
    address="Pine Boulevard",
    street_number="101",
    password="Test1234#",
    enabled=True,
    encrypt=True,
    cipher=cipher
)

# List of all mock users for easy iteration in tests
all_mock_users = [mock_user_1, mock_user_2, mock_user_3, mock_user_4]

# Plaintext versions for test assertions
all_mock_users_plaintext = [
    mock_user_1_plaintext,
    mock_user_2_plaintext,
    mock_user_3_plaintext,
    mock_user_4_plaintext
]