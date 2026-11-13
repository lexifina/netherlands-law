# Inhoud
## § 1. Begripsbepalingen
## § 2. Registratie en aanlevering van taxivervoergegevens
## § 3. Techniek
## § 4. Overgangs- en slotbepalingen
## 1. Inleiding
### 1.1. Context
### 1.2. Doel
## 2. Processen
### 2.1. Aanmelden dienst (relateren chauffeur, ondernemer en voertuig)
### 2.2. Aanmelden rit en aanmelden pauze
### 2.3. Afmelden rit en afmelden pauze
### 2.4. Afmelden dienst
### 2.5. Aanmelden ICT-dienstverlener
### 2.6. Afmelden ICT-dienstverlener
### 2.7. Valideren van chauffeur
### 2.8. Opvragen van openstaande diensten en verrichtingen
### 2.9. Melden van gebeurtenissen van het registratiemiddel chauffeur
### 2.10. Opvragen chauffeursnummer
## 3. Berichten
### 3.1. Statusovergangen
### 3.2. Generieke berichtgegevens in headers
### 3.3. Functionele berichtgegevens
#### 3.3.1. Chauffeur
#### 3.3.2. Rijbewijs
#### 3.3.3. Authenticatie
#### 3.3.4. Ondernemer
#### 3.3.5. Voertuig
#### 3.3.6. Andere werkzaamheden
#### 3.3.7. Locatie
### 3.4. Aanmelden dienst (relateren chauffeur, ondernemer en voertuig)
### 3.5. Afmelden dienst
### 3.6. Aanmelden rit
### 3.7. Afmelden rit
### 3.8. Aanmelden pauze
### 3.9. Afmelden pauze
### 3.10. Aanmelden ICT-dienstverlener
### 3.11. Afmelden ICT-dienstverlener
### 3.12. Valideren chauffeur
### 3.13. Opvragen van openstaande diensten en verrichtingen
### 3.14. Melden van gebeurtenissen van het registratiemiddel chauffeur
### 3.15. Opvragen chauffeursnummer
### 3.16. Foutmeldingscodes
#### 3.16.1. Foutmeldingen wegens headers
#### 3.16.2. Foutmeldingen wegens fouten in het bericht zelf
#### 3.16.3. Foutmeldingen wegens verwerken inhoud
## 4. Technische eisen
### 4.1. Conventies
#### 4.1.1. JSON conventies
#### 4.1.2. Encoding
#### 4.1.3. Hoofdlettergevoeligheid
#### 4.1.4. Datum/tijd
#### 4.1.5. Berichtenverkeer
#### 4.1.6. Endpoints
### 4.2. Actualiteit van data
### 4.3. Beschikbaarheid en performance
#### 4.3.1. Beschikbaarheid
#### 4.3.2. Performance
## 5. Logging en monitoring verbinding
### 5.1. Logging
### 5.2. Connectie-monitoring
## 6. Foutafhandeling
### 6.1. Algemeen
### 6.2. Error in aanroep dienstgerelateerde endpoints
### 6.3. Error in aanroep /verbinding
### 6.4. Duplicaat detectie
## 7. Authenticatie en informatiebeveiliging
### 7.1. Authenticatie
#### 7.1.1. PKI Certificaten
#### 7.1.2. Authenticatie rijbewijs
#### 7.1.3. Authenticatie kentekenbewijs
### 7.2. Informatiebeveiliging
#### 7.2.1. Transport Layer Security (TLS)
#### 7.2.2. API-keys
### 7.3. Headers
