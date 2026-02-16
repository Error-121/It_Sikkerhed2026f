import json, os
from dataclasses import asdict
from scr.Flat_file.user import User
from scr.Flat_file.auth import get_cipher

class Flat_file:
    def __init__(self, file_path="scr/Local_DB/users.json"):
        # Initialiser krypteringsobjektet
        self.cipher = get_cipher()
        # Sæt fil stien
        self.file_path = file_path

        # Tjek om filen eksisterer
        if os.path.exists(self.file_path):
            print(f"File {self.file_path} exists")
        else:
            # Opret mappe hvis den ikke eksisterer
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            # Opret fil med tom struktur
            with open(self.file_path, 'w') as file:
                json.dump({"users": [], "next_id": 1}, file, indent=4)
            print(f"File {self.file_path} created")

        # Indlæs JSON data i hukommelsen
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)
    
    def _load_db(self):
        """Læs JSON fil og returner parsede data"""
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    def _save_db(self, data):
        """Skriv data dictionary til JSON fil med korrekt formatering"""
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def _generate_user_id(self):
        """Returner next_id og øg den med 1"""
        user_id = self.data["next_id"]
        self.data["next_id"] += 1
        return user_id
    
    def create_user(self, first_name, last_name, address, street_number, password, enabled=True):
        """Opret en ny bruger og gem til databasen"""
        # Generer nyt bruger ID
        user_id = self._generate_user_id()
        
        # Opret User objekt med kryptering
        user = User(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            address=address,
            street_number=street_number,
            password=password,
            enabled=enabled,
            encrypt=True,
            cipher=self.cipher
        )
        
        # Konverter User til dictionary
        user_dict = asdict(user)
        
        # Tilføj til bruger listen
        self.data["users"].append(user_dict)
        
        # Gem til fil
        self._save_db(self.data)
        
        # Returner User objektet
        return user

    def decrypt_user(self, user_id):
        """Returner en bruger med dekrypteret PII data for visning/eksport"""
        for user in self.data["users"]:
            if user["user_id"] == user_id:
                # Opret en kopi for at undgå at ændre originalen
                decrypted_user = user.copy()
                
                # Dekrypter PII felter
                decrypted_user["first_name"] = User.decrypt_field(user["first_name"], self.cipher)
                decrypted_user["last_name"] = User.decrypt_field(user["last_name"], self.cipher)
                decrypted_user["address"] = User.decrypt_field(user["address"], self.cipher)
                decrypted_user["street_number"] = User.decrypt_field(user["street_number"], self.cipher)
                
                # user_id, enabled og password forbliver uændret
                return decrypted_user
        
        return None

    def get_user(self, user_id):
        """Hent en bruger baseret på user_id"""
        for user in self.data["users"]:
            if user["user_id"] == user_id:
                return User(**user, encrypt=False)
        return None
    
    def get_all_users(self):
        """Returner en liste af alle brugere som User objekter"""
        return [User(**user, encrypt=False) for user in self.data["users"]]
    
    def update_user(self, user_id, **kwargs):
        """Opdater specifikke felter for en bruger baseret på user_id"""
        # Indlæs frisk data fra fil
        self._load_db()
        
        # PII felter der skal krypteres
        pii_fields = ["first_name", "last_name", "address", "street_number"]
        
        # Find brugeren i listen
        for user in self.data["users"]:
            if user["user_id"] == user_id:
                # Behandl password særskilt (hash det)
                if "password" in kwargs:
                    kwargs["password"] = User.hash_password(kwargs["password"])
                
                # Krypter PII felter hvis de opdateres
                for field in pii_fields:
                    if field in kwargs:
                        kwargs[field] = User.encrypt_field(kwargs[field], self.cipher)
                
                # Opdater kun de felter der er angivet i kwargs
                user.update(kwargs)
                
                # Gem ændringerne til fil
                self._save_db(self.data)
                
                # Returner den opdaterede bruger som User objekt
                return User(**user, encrypt=False)
        
        # Returner None hvis brugeren ikke blev fundet
        return None
    
    def enable_user(self, user_id):
        """Aktiver en bruger ved at sætte enabled=True"""
        return self.update_user(user_id, enabled=True)
    
    def disable_user(self, user_id):
        """Deaktiver en bruger ved at sætte enabled=False"""
        return self.update_user(user_id, enabled=False)

    def delete_user(self, user_id):
        """Slet en bruger permanent fra databasen baseret på user_id"""
        # Indlæs frisk data fra fil
        self._load_db()
        
        # Find og fjern brugeren
        for user in self.data["users"]:
            if user["user_id"] == user_id:
                self.data["users"].remove(user)
                
                # Gem ændringerne til fil
                self._save_db(self.data)
                
                # Returner True for at indikere succesfuld sletning
                return True
        
        # Returner False hvis brugeren ikke blev fundet
        return False