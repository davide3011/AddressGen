# Bitcoin Key Generator (P2PK)

## ⚠️ Importante
Questo progetto è **puramente dimostrativo e accademico**.  
**Non utilizzare** per scopi reali o per gestire fondi crittografici.  
Gli indirizzi P2PK sono considerati **obsoleti** e **potenzialmente pericolosi**.

## 🚨 Perché P2PK è Obsoleto?
**Pay-to-Public-Key (P2PK)** è stato sostituito da standard più moderni per:

1. **Mancata protezione da errori**  
   - Nessun checksum per errori di battitura
   - Transazioni irreversibili in caso di errore

2. **Sicurezza ridotta**  
   - Esposizione diretta della chiave pubblica
   - Vulnerabilità potenziale ad attacchi quantistici
   - Rischio di cross-chain confusion

3. **Compatibilità limitata**  
   - Non supportato dai wallet moderni
   - Problemi con transazioni multisig
   - Difficoltà nell'implementazione di smart contract

## 🔒 Disclaimer
- Utilizzabile **esclusivamente per scopi educativi**
- I fondi inviati a indirizzi P2PK **possono essere persi definitivamente**
- Nessuna garanzia di sicurezza o corretto funzionamento

## 📋 Descrizione
Generatore didattico per comprendere i fondamenti delle chiavi crittografiche Bitcoin:
- Generazione chiavi ECDSA su curva secp256k1
- Calcolo coordinate del punto pubblico
- Conversione in formati compressi/non compressi
- Esportazione dati in formato JSON

## 🔧 Cosa Genera
- `private_key`: 
  - Formato esadecimale (64 caratteri)
  - Valore decimale (256 bit)
- `public_key`:
  - Versione non compressa (65 byte)
  - Versione compressa (33 byte)
  - Coordinate x/y sulla curva ellittica
- File JSON completo (`chiavi.json`)

## 🛠️ Come Funziona
1. **Generazione chiave privata**  
   Tramite `os.urandom` crittograficamente sicuro (256 bit)

2. **Calcolo chiave pubblica**  
   - Moltiplicazione ellittica: `P = k * G`
   - Utilizzo curva secp256k1 (stessa di Bitcoin)

3. **Formattazione**:
   - **Non compresso**: `0x04 + x + y` (65 byte)
   - **Compresso**: `0x02/0x03 + x` (33 byte)

4. **Output**:  
   Struttura JSON con tutti i parametri tecnici

## 🛠️ Come Usare
```bash
python3 key_generator.py
```
Output del programma:

```bash
Punto Generatore (G):
x: 55066263022277343669578718895168534326250603453777594175500187360389116729240
y: 32670510020758816978083085130507043184471273380659243275938904335757337482424

Chiave privata:
Formato esadecimale: a3c2b4... 
Formato decimale: 738957329...

Calcolo della chiave pubblica (P = k * G):
Coordinata x: 752625...
Coordinata y: 432987...

Chiave pubblica (non compressa): 04a3b2...
Chiave pubblica (compressa): 02a3b2...

File chiavi.json creato con successo!
```
## 📄 Esempio Output JSON (chiavi.json)
```bash
{
    "private_key": {
        "hex": "a3b2c1...",
        "decimal": "738957329..."
    },
    "public_key": {
        "uncompressed": "04a3b2...",
        "compressed": "02a3b2...",
        "x": "a3b2c1...",
        "y": "c1b2a3..."
    }
}
```
## 📦 Dipendenze

- Python 3.8+

- ecdsa (v0.18.0+)

## 📜 Licenza
MIT License
