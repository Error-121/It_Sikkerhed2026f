# It_Sikkerhed2026f
Til IT Sikkerhed uddannelse 

## **It-Sikkerhed Readme**
Dette er et skole projekt på Zealand Næstved

### ** Test Strategier **
Emne der er udvalgt for opgaven er Passwords

de regler jeg bruger i opgaven er at længden på password skal være mellem 8–25. det skal inde holde mindst 1 stort bogstav, 1 lille bogstav, 1 ciffer, 1 symbol samt ingen mellemrum.

#### *Ækvivalens*
du opsætter regler for opsættelsen af et nyt password f.eks længde mellem 8 og 25 tegn, der skal være et antal specialtegn idet osv.

| **Passwords** | resultat | hvorfor?               |
|---------------|----------|------------------------|
| Abcdef1!      | består   | opfylder alle krav     |
| Abc1!         | fejler   | for kort               |
| A*24 + a1!    | fejler   | for lang               |
| abcdef1!      | fejler   | mangler stort bogstav  |
| ABCDEF1!      | fejler   | mangler lille bogstav  |
| Abcdefg!      | fejler   | mangler tal            |
| Abcdef12      | fejler   | mangler specialtegn    |
| Abc def1!     | fejler   | mangler har mellem rum |

#### *Grænseværdi*
for længde reglen bliver der 7, 8 , 9 samt 24, 25, 26 testet hvor 8 og 25 er min og max på længden

| **Passwords** | resultat | hvorfor?             |
|---------------|----------|----------------------|
| Aa1!aaa       | fejler   | forkort              |
| Aa1!aaaa      | består   | er min               |
| Aa1!aaaaa     | består   | er inden for grænsen |
| Aa1! + a*20   | består   | er max               |
| Aa1! + a*20   | fejler   | er for lang          |

#### *GRUD(L)*
med GRUD test ser vi på hvordan systement arbejder med password.

i test for __ tjekker vi
Create:
om passwords kan oprettes i systement og om de opfylder reglerne

Read:
Kan de læses fra hvor de gemt f.eks database, og samligning med gemte password når der logges ind. 

Update:
kan password ændres og gemmes i systemet

Delete:
kan man fjerne password fra systemet

List:
kan admin hente en liste af brugere og deres password

#### *Cycle-process-test*
her tester vi fulde livscyklusser af password 

Exemplar:

når en ny bruger oprettets og logger ind
    1. Opret konto med adgangskoden Abcdef1!
    2. Bekræft at adgangskoden er hashet og gemt
    3. Login med samme adgangskode → succes
    4. Login med forkert adgangskode → mislykkedes

Når en bruger ændre password
    1. Bruger logget ind med "Abcdef1!"
    2. Anmod om ændring af adgangskode
    3. Opdater til "NewPass2@"
    4. Den gamle adgangskode "Abcdef1!" virker ikke længere
    5. Den nye adgangskode "NewPass2@" virker

#### *Test Pyramiden*

unit test:(Grænseværdi og Ækvivalens høre til her)
her teste ting som reglerne for passwords som f.eks Grænseværdi og Ækvivalens. der her vi laver flest test da de er relativt hurtige at gennem føre

Integration Tests:(CRUD høre til her)
her tester man password inplmatering sammen med andre systemer som gemning, validereing og hasing, samt hvordan det fungere sammen med bruger navn i forskællige UI som login siden og bruger siden hvro man kan opdatere bruger info og password 

End to End Test:(Cycle-process-test høre til her)
her testets hele systemet og alle måde man kan bruge for at password på. men det tager længere tid og kræver flest recurser


#### *Decision Table test*
| Length 8–25 | Uppercase | Lowercase | Digit | Symbol | No Spaces | Result | Example |
|---|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS | Abcdef1! |
| ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | FAIL | Abc def1! |
| ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | FAIL | Abcdef12 |
| ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | FAIL | Abcdef1! |
| ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | FAIL | ABCDEF1! |
| ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | FAIL | abcdef1! |
| ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | FAIL | Abc1! |
| ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | FAIL | A*24 + a1! |
| ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | FAIL | weakpass |


### **Flat File**

#### *hvorfor er det smart at bruge en flat_file_db*
En flat file database muliggør hurtig prototyping og test af dataadgang uden afhængighed af en fuldt opsat databaseserver. Den reducerer kompleksitet i udviklingsfasen, eliminerer behovet for migrations og eksterne services, før der introduceres en egentlig database.

#### *Screenshot af mine unit test af flat_file_db*
![FLAT File Test](screenshot/Flat-File%201%202026-02-10_15-43.png)

##### *Risici:*
test_create_user_success - Hvis denne test fejler, kan systemet ikke oprette nye brugere, hvilket blokerer for registrering af nye konti.

test_get_user_by_id_success - Hvis denne test fejler, kan systemet ikke hente brugerdata, hvilket forhindrer login og visning af brugerprofiler.

test_get_user_by_id_not_found - Hvis denne test fejler, kan systemet returnere forkerte data eller crashe når der søges efter ikke-eksisterende brugere.

test_get_all_users - Hvis denne test fejler, kan administratorer ikke se en liste over alle brugere, hvilket begrænser brugeradministration.

test_get_all_users_empty_database - Hvis denne test fejler, kan systemet crashe når databasen er tom, hvilket forhindrer opstart af nye installationer.

test_update_user_first_name - Hvis denne test fejler, kan brugere ikke ændre deres fornavn, hvilket begrænser opdatering af brugeroplysninger.

test_update_user_multiple_fields - Hvis denne test fejler, kan brugere ikke opdatere flere felter samtidig, hvilket gør profilopdateringer ineffektive.

test_update_user_not_found - Hvis denne test fejler, kan systemet crashe eller overskrive forkerte data når der opdateres ikke-eksisterende brugere.

test_enable_user - Hvis denne test fejler, kan deaktiverede brugerkonti ikke genaktiveres, hvilket forhindrer gendannelse af adgang.

test_disable_user - Hvis denne test fejler, kan suspenderede eller problematiske brugere ikke deaktiveres, hvilket skaber sikkerhedsrisici.

test_delete_user_success - Hvis denne test fejler, kan brugere ikke slettes fra systemet, hvilket forhindrer overholdelse af GDPR og datahåndtering.

test_delete_user_not_found - Hvis denne test fejler, kan systemet crashe eller give fejl når der forsøges at slette ikke-eksisterende brugere.

test_delete_all_users - Hvis denne test fejler, kan databasen ikke ryddes, hvilket komplicerer test-miljøer og systemvedligeholdelse.

### **Flat File 2: Kryptering og Hasing**

#### *Valg af Algoritmer*

**Hashing (Password):**
- **Tilgængelige:** bcrypt, scrypt, PBKDF2, Argon2
- **Valgt:** Argon2id
- **Hvorfor:** Argon2id vandt Password Hashing Competition 2015 og er i dag den mest anbefalede standard. Den er mere modstandsdygtig over for GPU-baserede angreb end bcrypt og kombinerer beskyttelse mod både side-channel og timing attacks. Argon2id bruges af Microsoft, Google og anbefales af OWASP.

**Kryptering (PII-data):**
- **Tilgængelige:** AES-128, AES-256, ChaCha20, RSA
- **Valgt:** Fernet (AES-128 i CBC mode med HMAC)
- **Hvorfor:** Fernet er en symmetrisk kryptering der automatisk håndterer IV-generering, message authentication og padding. Dette reducerer risikoen for implementeringsfejl. For et flat-file system er symmetrisk kryptering mere praktisk end asymmetrisk (RSA), da vi både skal kryptere og dekryptere data fra samme application.

#### *Hvornår Krypteres Data*

Data krypteres **ved oprettelse og opdatering** af brugere:
- **Personlige oplysninger (PII):** `first_name`, `last_name`, `address`, `street_number` krypteres med Fernet før de gemmes i JSON-filen
- **Password:** Hashes med Argon2 (envejskryptering) ved oprettelse og når bruger ændrer password

**Hvorfor:** GDPR kræver "passende tekniske foranstaltninger" til beskyttelse af persondata (Artikel 32). Kryptering sikrer at data er ulæselig hvis JSON-filen kompromitteres. Password hashing betyder at selv systemadministratorer ikke kan se brugerens plaintext password.

#### *Hvornår Dekrypteres Data*

Data dekrypteres kun **on-demand** når det er nødvendigt:
- **Visning af brugerprofil:** Når en bruger ser deres egen profil dekrypteres PII-felterne
- **Admin-funktioner:** Når admin skal se brugeroplysninger
- **Export:** Ved GDPR-anmodninger om dataudtræk (right to data portability)

**Hvorfor:** Princippet om "data minimization" - vi holder data krypteret så længe som muligt og dekrypterer kun når der er et legitimt behov. Password dekrypteres **aldrig** fordi det er hashed (envejskryptering).

#### *Hvornår Fjernes Dekrypteret Data*

Dekrypteret data fjernes fra hukommelsen **umiddelbart efter brug**:
- **Efter visning:** Når `decrypt_user()` funktionen returnerer data til UI, slettes den dekrypterede kopi når funktionen afsluttes (Python garbage collection)
- **Efter opdatering:** Når PII-felter opdateres, krypteres de nye værdier med det samme og plaintext slettes
- **Mellem requests:** I en web-applikation ville dekrypteret data kun eksistere i varigheden af et HTTP-request

**Hvorfor:** Jo kortere tid dekrypteret data eksisterer i hukommelsen, jo mindre er risikoen for at det bliver eksponeret ved memory dumps, debugging eller andre angreb. Dette følger "defense in depth" princippet.

#### *Andre Sikkerhedshensyn*

**Nøglehåndtering:**
- Krypteringsnøglen gemmes i separat fil (`secret.key`) og skal beskyttes med filsystem-rettigheder
- I produktion bør nøglen gemmes i en dedikeret key management service (Azure Key Vault, AWS KMS)
- Nøglen må **aldrig** committes til source control (.gitignore)

**Compliance:**
- **GDPR Artikel 17:** `delete_user()` funktionen sikrer "right to erasure" - sletter både krypteret og hashet data permanent
- **GDPR Artikel 32:** Brug af state-of-the-art kryptering (Argon2, Fernet) opfylder kravet om "appropriate technical measures"
- **GDPR Artikel 25:** "Privacy by design" - data er krypteret by default, ikke som opt-in

**Begrænsninger i Flat File:**
- Hele JSON-filen skal læses for at finde én bruger (ikke optimal for store datasets)
- Ingen audit log - vi ved ikke hvem der har dekrypteret data hvornår
- Single encryption key for alle brugere (produktion bør bruge per-user keys eller envelope encryption)
- Mangler key rotation mekanisme

