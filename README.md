# It_Sikkerhed2026f
Til IT Sikkerhed uddannelse 

## **It-Sikkerhed Readme**
Dette er et skole projekt på Zealand Næstved

### ** Test Strategier **
Emne der er udvalgt for opgaven er Passwords

de regler jeg bruger i opgaven er at længden på password skal være mellem 8–25. det skal inde holde mindst 1 stort bogstav, 1 lille bogstav, 1 ciffer, 1 symbol samt ingen mellemrum.

### *Ækvivalens*
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

### *Grænseværdi*
for længde reglen bliver der 7, 8 , 9 samt 24, 25, 26 testet hvor 8 og 25 er min og max på længden

| **Passwords** | resultat | hvorfor?             |
|---------------|----------|----------------------|
| Aa1!aaa       | fejler   | forkort              |
| Aa1!aaaa      | består   | er min               |
| Aa1!aaaaa     | består   | er inden for grænsen |
| Aa1! + a*20   | består   | er max               |
| Aa1! + a*20   | fejler   | er for lang          |

### *GRUD(L)*
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

### *Cycle-process-test*
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

### *Test Pyramiden*

unit test:(Grænseværdi og Ækvivalens høre til her)
her teste ting som reglerne for passwords som f.eks Grænseværdi og Ækvivalens. der her vi laver flest test da de er relativt hurtige at gennem føre

Integration Tests:(CRUD høre til her)
her tester man password inplmatering sammen med andre systemer som gemning, validereing og hasing, samt hvordan det fungere sammen med bruger navn i forskællige UI som login siden og bruger siden hvro man kan opdatere bruger info og password 

End to End Test:(Cycle-process-test høre til her)
her testets hele systemet og alle måde man kan bruge for at password på. men det tager længere tid og kræver flest recurser


### *Decision Table test*
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