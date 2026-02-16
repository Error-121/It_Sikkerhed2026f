import pytest
import os, json
from scr.Flat_file.main import Flat_file
from scr.Flat_file.user import User
from scr.Mock_Data.mock_user import all_mock_users, all_mock_users_plaintext, mock_user_1_plaintext, mock_user_2_plaintext, mock_user_3_plaintext, mock_user_4_plaintext

# ==================== Test Setup ====================

TEST_DB_PATH = "scr/Flat_file/Local_DB/test_users.json"  # Sti til test database fil

# ==================== Helper Functions ====================

@pytest.fixture
def setup_test_db():
    """
    Opret en test database med mock brugere før hver test.
    Slet databasen efter testen er færdig.
    """
    # Given: Opret test database
    db = Flat_file(file_path=TEST_DB_PATH)
    
    # Tilføj alle mock brugere til databasen (de er allerede krypteret)
    for plaintext in all_mock_users_plaintext:
        db.create_user(
            first_name=plaintext["first_name"],
            last_name=plaintext["last_name"],
            address=plaintext["address"],
            street_number=plaintext["street_number"],
            password=plaintext["password"],
            enabled=plaintext["enabled"]
        )
    
    # Returner database objektet til testen
    yield db
    
    # Teardown: Slet test filen efter testen
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    # Slet også test mappen hvis den er tom
    test_dir = os.path.dirname(TEST_DB_PATH)
    if os.path.exists(test_dir) and not os.listdir(test_dir):
        os.rmdir(test_dir)


@pytest.fixture
def empty_test_db():
    """
    Opret en tom test database uden brugere.
    Bruges til tests der skal oprette brugere fra scratch.
    """
    # Given: Opret tom database
    db = Flat_file(file_path=TEST_DB_PATH)
    
    # Returner database objektet til testen
    yield db
    
    # Teardown: Slet test filen efter testen
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    # Slet også test mappen hvis den er tom
    test_dir = os.path.dirname(TEST_DB_PATH)
    if os.path.exists(test_dir) and not os.listdir(test_dir):
        os.rmdir(test_dir)


# ==================== CREATE Tests ====================

def test_create_user_success(empty_test_db):
    """Test oprettelse af en ny bruger"""
    # Given: En tom database
    db = empty_test_db
    
    # When: Vi opretter en ny bruger
    new_user = db.create_user(
        first_name="Test",
        last_name="User",
        address="Test Street",
        street_number="999",
        password="TestPass123!",
        enabled=True
    )
    
    # Then: Brugeren er oprettet med korrekte værdier (dekrypter for at verificere)
    assert new_user is not None
    assert new_user.user_id == 1
    assert new_user.enabled == True
    
    # Dekrypter PII data for at verificere
    decrypted = db.decrypt_user(new_user.user_id)
    assert decrypted["first_name"] == "Test"
    assert decrypted["last_name"] == "User"
    assert decrypted["address"] == "Test Street"
    assert decrypted["street_number"] == "999"
    
    # Verificer password hash
    assert User.verify_password(new_user.password, "TestPass123!")

# ==================== READ Tests ====================

def test_get_user_by_id_success(setup_test_db):
    """Test hentning af en bruger baseret på ID"""
    # Given: En database med mock brugere
    db = setup_test_db
    
    # When: Vi henter en bruger med ID 1
    user = db.get_user(1)
    
    # Then: Vi får den korrekte bruger tilbage (dekrypter for at verificere)
    assert user is not None
    assert user.user_id == 1
    
    decrypted = db.decrypt_user(user.user_id)
    assert decrypted["first_name"] == mock_user_1_plaintext["first_name"]
    assert decrypted["last_name"] == mock_user_1_plaintext["last_name"]


def test_get_user_by_id_not_found(setup_test_db):
    """Test hentning af en bruger der ikke eksisterer"""
    # Given: En database med mock brugere
    db = setup_test_db
    
    # When: Vi forsøger at hente en bruger med ugyldig ID
    user = db.get_user(999)
    
    # Then: Vi får None tilbage
    assert user is None


def test_get_all_users(setup_test_db):
    """Test hentning af alle brugere"""
    # Given: En database med 4 mock brugere
    db = setup_test_db
    
    # When: Vi henter alle brugere
    all_users = db.get_all_users()
    
    # Then: Vi får en liste med 4 brugere
    assert len(all_users) == 4
    assert all(hasattr(user, 'user_id') for user in all_users)


def test_get_all_users_empty_database(empty_test_db):
    """Test hentning af alle brugere fra tom database"""
    # Given: En tom database
    db = empty_test_db
    
    # When: Vi henter alle brugere
    all_users = db.get_all_users()
    
    # Then: Vi får en tom liste
    assert len(all_users) == 0
    assert all_users == []


# ==================== UPDATE Tests ====================

def test_update_user_first_name(setup_test_db):
    """Test opdatering af brugerens fornavn"""
    # Given: En database med mock brugere
    db = setup_test_db
    
    # When: Vi opdaterer fornavn for bruger 1
    updated_user = db.update_user(1, first_name="UpdatedName")
    
    # Then: Brugerens fornavn er opdateret (dekrypter for at verificere)
    assert updated_user is not None
    
    decrypted = db.decrypt_user(updated_user.user_id)
    assert decrypted["first_name"] == "UpdatedName"
    assert decrypted["last_name"] == mock_user_1_plaintext["last_name"]  # Andre felter er uændrede


def test_update_user_multiple_fields(setup_test_db):
    """Test opdatering af flere felter samtidig"""
    # Given: En database med mock brugere
    db = setup_test_db
    
    # When: Vi opdaterer flere felter for bruger 2
    updated_user = db.update_user(
        2,
        first_name="NewFirst",
        last_name="NewLast",
        address="New Address"
    )
    
    # Then: Alle angivne felter er opdateret (dekrypter for at verificere)
    decrypted = db.decrypt_user(updated_user.user_id)
    assert decrypted["first_name"] == "NewFirst"
    assert decrypted["last_name"] == "NewLast"
    assert decrypted["address"] == "New Address"
    assert decrypted["street_number"] == mock_user_2_plaintext["street_number"]  # Uændret


def test_update_user_password(setup_test_db):
    """Test opdatering af brugerens password"""
    # Given: En database med mock brugere
    db = setup_test_db
    
    # When: Vi opdaterer password for bruger 1
    new_password = "NewSecurePass123!"
    updated_user = db.update_user(1, password=new_password)
    
    # Then: Password er opdateret og hashet korrekt
    assert updated_user is not None
    assert User.verify_password(updated_user.password, new_password)
    # Gammelt password virker ikke længere
    assert not User.verify_password(updated_user.password, mock_user_1_plaintext["password"])


def test_update_user_not_found(setup_test_db):
    """Test opdatering af bruger der ikke eksisterer"""
    # Given: En database med mock brugere
    db = setup_test_db
    
    # When: Vi forsøger at opdatere en bruger med ugyldig ID
    updated_user = db.update_user(999, first_name="Test")
    
    # Then: Vi får None tilbage
    assert updated_user is None


def test_enable_user(setup_test_db):
    """Test aktivering af en disabled bruger"""
    # Given: En database hvor bruger 2 er disabled
    db = setup_test_db
    assert db.get_user(2).enabled == False
    
    # When: Vi aktiverer bruger 2
    enabled_user = db.enable_user(2)
    
    # Then: Brugeren er nu aktiveret
    assert enabled_user is not None
    assert enabled_user.enabled == True


def test_disable_user(setup_test_db):
    """Test deaktivering af en enabled bruger"""
    # Given: En database hvor bruger 1 er enabled
    db = setup_test_db
    assert db.get_user(1).enabled == True
    
    # When: Vi deaktiverer bruger 1
    disabled_user = db.disable_user(1)
    
    # Then: Brugeren er nu deaktiveret
    assert disabled_user is not None
    assert disabled_user.enabled == False


# ==================== DELETE Tests ====================

def test_delete_user_success(setup_test_db):
    """Test sletning af en eksisterende bruger"""
    # Given: En database med 4 brugere
    db = setup_test_db
    assert len(db.get_all_users()) == 4
    
    # When: Vi sletter bruger 3
    result = db.delete_user(3)
    
    # Then: Brugeren er slettet og vi har nu 3 brugere
    assert result == True
    assert len(db.get_all_users()) == 3
    assert db.get_user(3) is None


def test_delete_user_not_found(setup_test_db):
    """Test sletning af bruger der ikke eksisterer"""
    # Given: En database med mock brugere
    db = setup_test_db
    initial_count = len(db.get_all_users())
    
    # When: Vi forsøger at slette en bruger med ugyldig ID
    result = db.delete_user(999)
    
    # Then: Sletning fejler og antallet af brugere er uændret
    assert result == False
    assert len(db.get_all_users()) == initial_count


def test_delete_all_users(setup_test_db):
    """Test sletning af alle brugere én ad gangen"""
    # Given: En database med 4 brugere
    db = setup_test_db
    
    # When: Vi sletter alle brugere
    db.delete_user(1)
    db.delete_user(2)
    db.delete_user(3)
    db.delete_user(4)
    
    # Then: Databasen er tom
    assert len(db.get_all_users()) == 0
