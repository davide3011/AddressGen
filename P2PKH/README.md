# Generatore di Indirizzi Bitcoin Legacy (P2PKH)

Questo programma genera indirizzi Bitcoin Legacy (Pay-to-Public-Key-Hash o P2PKH) per diverse reti Bitcoin (mainnet, testnet, regtest) e salva i dati generati in formato JSON. È uno strumento educativo che mostra il processo completo di generazione di un indirizzo Bitcoin, dalla creazione della chiave privata fino all'indirizzo finale.

## Indice

- [Requisiti](#requisiti)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Output](#output)
- [Teoria degli Indirizzi Bitcoin](#teoria-degli-indirizzi-bitcoin)
  - [1. Chiavi Private](#1-chiavi-private)
  - [2. Chiavi Pubbliche e Curve Ellittiche](#2-chiavi-pubbliche-e-curve-ellittiche)
  - [3. Funzioni di Hash](#3-funzioni-di-hash)
  - [4. Codifica Base58Check](#4-codifica-base58check)
  - [5. Formato WIF](#5-formato-wif)
  - [6. Processo Completo di Generazione](#6-processo-completo-di-generazione)

## Requisiti

Il programma richiede Python 3.6 o superiore e le seguenti librerie:

- `secrets`: Per la generazione di numeri casuali crittograficamente sicuri
- `hashlib`: Per le funzioni di hashing (SHA256, RIPEMD160)
- `json`: Per salvare i dati in formato JSON
- `ecdsa`: Per le operazioni con curve ellittiche
- `base58`: Per la codifica Base58Check

Puoi installare le dipendenze necessarie con pip:

```bash
pip install ecdsa base58
```

## Installazione

1. Clona o scarica questo repository
2. Assicurati di avere installato Python 3.6 o superiore
3. Installa le dipendenze come indicato sopra

## Utilizzo

Per eseguire il programma, naviga nella directory del progetto e lancia lo script:

```bash
python p2pkh.py
```

Il programma ti chiederà di:

1. Selezionare il tipo di rete Bitcoin (mainnet, testnet o regtest)
2. Scegliere se utilizzare chiavi pubbliche compresse o non compresse
3. Inserire un nome per il file JSON in cui salvare i dati generati

## Output

Il programma genera e visualizza:

- Chiave privata (in formato esadecimale)
- Chiave privata (in formato WIF - Wallet Import Format)
- Chiave pubblica (in formato esadecimale, compressa o non compressa)
- Indirizzo Bitcoin Legacy (P2PKH)

Tutti questi dati vengono anche salvati in un file JSON per riferimento futuro.

Esempio di output JSON:

```json
{
    "private_key_hex": "79b5742ff12ab5ed66162b6abddcd0de4127512967cea6e45605b4b04375245f",
    "wif": "L1JJAzuQHGTatSeU9jMvAEfUMMWiEp7dMYRcfYZHKBiMwWsSMhrN",
    "public_key_hex": "02c72e17480db0a7c946953e159de488d589acb1f23f0c10fd32bbc3045b62d7ba",
    "address": "1CGbKFQTaFBz4PPdTBMyc4vtQEsDNpJuyc",
    "network": "mainnet"
}
```

## Teoria degli Indirizzi Bitcoin

Questa sezione spiega in dettaglio il processo di generazione degli indirizzi Bitcoin Legacy (P2PKH) e i concetti crittografici alla base.

### 1. Chiavi Private

La chiave privata è il punto di partenza per la generazione di un indirizzo Bitcoin. È semplicemente un numero casuale di 256 bit (32 byte).

**Caratteristiche della chiave privata:**
- È un numero intero compreso tra 1 e 2^256 - 1
- Deve essere generata con un metodo crittograficamente sicuro
- Chi possiede la chiave privata ha il controllo completo dei bitcoin associati all'indirizzo
- Non deve mai essere condivisa

**Nel codice:**
```python
private_key = secrets.token_bytes(32)  # Genera 32 byte casuali (256 bit)
private_key_hex = private_key.hex()    # Converte in formato esadecimale
```

Il modulo `secrets` di Python è utilizzato invece di `random` perché fornisce numeri casuali crittograficamente sicuri, essenziali per la sicurezza delle chiavi private.

### 2. Chiavi Pubbliche e Curve Ellittiche

La chiave pubblica viene derivata dalla chiave privata utilizzando la crittografia a curve ellittiche (ECC), specificamente la curva secp256k1 usata da Bitcoin.

**Concetti fondamentali:**

- **Curva Ellittica**: Una curva matematica definita dall'equazione y² = x³ + ax + b. Bitcoin usa la curva secp256k1 dove a=0 e b=7, risultando in y² = x³ + 7.

- **Punto Generatore (G)**: Un punto predefinito sulla curva che serve come base per tutte le operazioni.

- **Moltiplicazione di Punto**: La chiave pubblica (K) è calcolata moltiplicando la chiave privata (k) per il punto generatore: K = k × G. Questa operazione è facile da calcolare in una direzione ma computazionalmente impossibile da invertire.

- **Formati di Chiave Pubblica**:
  - **Non compressa**: 65 byte (1 byte prefisso '04' + 32 byte coordinata X + 32 byte coordinata Y)
  - **Compressa**: 33 byte (1 byte prefisso '02' o '03' + 32 byte coordinata X). Il prefisso indica la parità della coordinata Y.

**Nel codice:**
```python
# Crea un oggetto SigningKey dalla libreria ecdsa usando la chiave privata
sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
# Ottiene la chiave di verifica (chiave pubblica)
vk = sk.get_verifying_key()
# Converte la chiave pubblica in bytes (coordinate x e y del punto sulla curva)
pubkey_bytes = vk.to_string()

# Compressione della chiave pubblica
if compressed:
    # Estrae le coordinate x e y (32 byte ciascuna)
    x, y = pubkey_bytes[:32], pubkey_bytes[32:]
    # Il prefisso dipende dalla parità di y: 02 se pari, 03 se dispari
    prefix = b'\x02' if int.from_bytes(y, 'big') % 2 == 0 else b'\x03'
    # La chiave compressa contiene solo il prefisso e la coordinata x
    pubkey = prefix + x
else:
    # La chiave non compressa ha il prefisso 04 seguito dalle coordinate x e y
    pubkey = b'\x04' + pubkey_bytes
```

### 3. Funzioni di Hash

Bitcoin utilizza diverse funzioni di hash crittografiche per aumentare la sicurezza e ridurre la dimensione degli indirizzi.

**Funzioni di hash utilizzate:**

- **SHA-256 (Secure Hash Algorithm 256-bit)**: Produce un digest di 32 byte (256 bit).

- **RIPEMD-160 (RACE Integrity Primitives Evaluation Message Digest 160-bit)**: Produce un digest di 20 byte (160 bit).

- **HASH160**: Una combinazione di SHA-256 seguito da RIPEMD-160. Usata per ridurre la dimensione della chiave pubblica da 33/65 byte a 20 byte.

- **Double SHA-256**: SHA-256 applicato due volte consecutivamente. Usato per calcolare i checksum.

**Nel codice:**
```python
def double_sha256(data: bytes) -> bytes:
    """Calcola il doppio hash SHA256 (SHA256(SHA256(data)))"""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def hash160(data: bytes) -> bytes:
    """Calcola l'hash HASH160 (RIPEMD160(SHA256(data)))"""
    return hashlib.new('ripemd160', hashlib.sha256(data).digest()).digest()

# Applicazione nel processo di generazione dell'indirizzo
pubkey_hash = hash160(pubkey)  # Applica HASH160 alla chiave pubblica
```

### 4. Codifica Base58Check

Base58Check è un formato di codifica usato in Bitcoin per rappresentare indirizzi e chiavi private in un formato leggibile e resistente agli errori.

**Caratteristiche di Base58Check:**

- Usa un alfabeto di 58 caratteri (Base58) che esclude caratteri facilmente confondibili: 0 (zero), O (lettera O), I (lettera i maiuscola), l (lettera L minuscola).

- Aggiunge un checksum di 4 byte alla fine dei dati per rilevare errori di trascrizione.

- Il checksum è calcolato come i primi 4 byte del double SHA-256 dei dati.

**Processo di codifica:**
1. Aggiungere un prefisso di rete ai dati (es. 0x00 per mainnet P2PKH)
2. Calcolare il checksum (primi 4 byte del double SHA-256 dei dati con prefisso)
3. Aggiungere il checksum alla fine dei dati con prefisso
4. Codificare il risultato in Base58

**Nel codice:**
```python
def encode_base58check(payload: bytes) -> str:
    """Codifica un payload in formato Base58Check"""
    return base58.b58encode(payload + double_sha256(payload)[:4]).decode()

# Applicazione per creare l'indirizzo
addr_payload = config['addr_prefix'] + pubkey_hash  # Aggiunge il prefisso di rete
address = encode_base58check(addr_payload)  # Codifica in Base58Check
```

### 5. Formato WIF

WIF (Wallet Import Format) è un formato standard per rappresentare le chiavi private Bitcoin in modo leggibile e facilmente importabile nei wallet.

**Struttura del formato WIF:**

1. **Prefisso di rete**: 1 byte che identifica la rete (0x80 per mainnet, 0xEF per testnet/regtest)
2. **Chiave privata**: 32 byte della chiave privata originale
3. **Flag di compressione** (opzionale): 1 byte (0x01) che indica se la chiave pubblica corrispondente è compressa
4. **Checksum**: 4 byte calcolati come i primi 4 byte del double SHA-256 dei dati precedenti

**Processo di codifica WIF:**
1. Aggiungere il prefisso di rete alla chiave privata
2. Se la chiave pubblica è compressa, aggiungere il byte 0x01
3. Calcolare il checksum e aggiungerlo alla fine
4. Codificare il risultato in Base58

**Nel codice:**
```python
# Crea il payload WIF aggiungendo il prefisso di rete e il suffisso di compressione se necessario
wif_payload = config['wif_prefix'] + private_key + (b'\x01' if compressed else b'')
# Codifica in Base58Check
wif = encode_base58check(wif_payload)
```

### 6. Processo Completo di Generazione

Ecco il processo completo di generazione di un indirizzo Bitcoin Legacy (P2PKH) passo per passo:

1. **Generazione della chiave privata**:
   - Generare 32 byte casuali crittograficamente sicuri
   - Verificare che il valore sia nell'intervallo valido (1 a 2^256-1)

2. **Derivazione della chiave pubblica**:
   - Applicare la moltiplicazione di punto sulla curva ellittica secp256k1: K = k × G
   - Formattare la chiave pubblica (compressa o non compressa)

3. **Calcolo dell'hash della chiave pubblica**:
   - Applicare SHA-256 alla chiave pubblica
   - Applicare RIPEMD-160 al risultato (HASH160)

4. **Creazione dell'indirizzo**:
   - Aggiungere il prefisso di rete all'hash della chiave pubblica (0x00 per mainnet)
   - Calcolare il checksum (primi 4 byte del double SHA-256)
   - Aggiungere il checksum alla fine
   - Codificare il risultato in Base58

5. **Creazione del formato WIF per la chiave privata**:
   - Aggiungere il prefisso di rete alla chiave privata (0x80 per mainnet)
   - Aggiungere il byte di compressione se necessario (0x01)
   - Calcolare il checksum e aggiungerlo
   - Codificare il risultato in Base58

**Nel codice:**
```python
def generate_legacy_address(network: str = 'mainnet', compressed: bool = True) -> Dict[str, str]:
    """Genera chiave privata, pubblica, WIF e indirizzo Bitcoin Legacy (P2PKH)"""
    # Ottiene i parametri di configurazione per la rete specificata
    config = get_network_config(network)
    
    # Generazione chiavi
    private_key = secrets.token_bytes(32)  # Chiave privata casuale
    private_key_hex = private_key.hex()
    pubkey, pubkey_hex = create_public_key(private_key, compressed)  # Chiave pubblica
    
    # Creazione indirizzo e WIF
    pubkey_hash = hash160(pubkey)  # Hash della chiave pubblica
    addr_payload = config['addr_prefix'] + pubkey_hash  # Payload indirizzo
    wif_payload = config['wif_prefix'] + private_key + (b'\x01' if compressed else b'')  # Payload WIF
    
    # Restituisce tutte le informazioni
    return {
        'private_key_hex': private_key_hex,
        'wif': encode_base58check(wif_payload),
        'public_key_hex': pubkey_hex,
        'address': encode_base58check(addr_payload),
        'network': network
    }
```

Questo processo garantisce che ogni indirizzo Bitcoin sia unico e sicuro, derivato matematicamente da una chiave privata che solo il proprietario conosce. La sicurezza del sistema si basa sulla difficoltà computazionale di invertire le funzioni di hash e le operazioni di curva ellittica utilizzate.

## Licenza

Questo progetto è rilasciato sotto licenza MIT.
