# Generatore di Indirizzi Bitcoin SegWit (P2WPKH)

## Introduzione

Questo progetto implementa un generatore di indirizzi Bitcoin SegWit di tipo P2WPKH (Pay-to-Witness-Public-Key-Hash). Il programma genera una chiave privata casuale, deriva la corrispondente chiave pubblica, e crea un indirizzo SegWit utilizzando la codifica Bech32. Supporta diverse reti Bitcoin (mainnet, testnet, regtest) e permette di salvare i dati generati in formato JSON.

## Cos'è SegWit e P2WPKH

SegWit (Segregated Witness) è un aggiornamento del protocollo Bitcoin implementato nel 2017 che separa i dati della firma (witness) dal resto dei dati della transazione. Questa separazione ha portato diversi vantaggi:

1. **Riduzione delle commissioni**: Le transazioni SegWit sono più leggere in termini di peso computazionale.
2. **Aumento della capacità della rete**: Più transazioni possono essere incluse in un blocco.
3. **Eliminazione della malleabilità delle transazioni**: Risolve un problema che impediva alcune funzionalità avanzate come i Lightning Network.
4. **Retrocompatibilità**: Funziona anche con i wallet non aggiornati.

P2WPKH (Pay-to-Witness-Public-Key-Hash) è un tipo specifico di indirizzo SegWit che utilizza l'hash della chiave pubblica come destinatario del pagamento, simile al tradizionale P2PKH, ma con i vantaggi di SegWit.

## Algoritmo di Generazione degli Indirizzi P2WPKH

La generazione di un indirizzo P2WPKH segue questi passaggi fondamentali:

### 1. Generazione della Chiave Privata

Una chiave privata Bitcoin è semplicemente un numero casuale di 256 bit (32 byte). È fondamentale che questo numero sia generato in modo crittograficamente sicuro per garantire che non possa essere indovinato.

```python
private_key = secrets.token_bytes(32)  # Genera 32 byte casuali (256 bit)
private_key_hex = private_key.hex()    # Converte in formato esadecimale
```

Questa chiave privata deve essere mantenuta segreta, poiché chiunque la possieda può spendere i bitcoin associati all'indirizzo corrispondente.

### 2. Derivazione della Chiave Pubblica

La chiave pubblica viene derivata dalla chiave privata utilizzando la crittografia a curva ellittica, specificamente la curva SECP256k1 (la stessa usata da Bitcoin).

```python
sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
vk = sk.get_verifying_key()  # Ottiene la chiave di verifica (chiave pubblica)
pubkey_bytes = vk.to_string()  # 64 byte: [32 byte coordinata X | 32 byte coordinata Y]
```

La chiave pubblica può essere rappresentata in due formati:

- **Non compressa** (65 byte): Prefisso `04` seguito dalle coordinate X e Y complete.
- **Compressa** (33 byte): Prefisso `02` o `03` (a seconda della parità di Y) seguito dalla sola coordinata X.

```python
if compressed:
    # Formato compresso: prefisso (02 o 03) + coordinata X
    x = pubkey_bytes[:32]  # Primi 32 byte (coordinata X)
    y = pubkey_bytes[32:]  # Ultimi 32 byte (coordinata Y)
    prefix = b'\x02' if int.from_bytes(y, 'big') % 2 == 0 else b'\x03'  # Determina la parità di Y
    pubkey = prefix + x  # Chiave pubblica compressa (33 byte)
else:
    # Formato non compresso: prefisso (04) + coordinata X + coordinata Y
    pubkey = b'\x04' + pubkey_bytes  # Chiave pubblica non compressa (65 byte)
```

Il formato compresso è più efficiente e oggi è lo standard per Bitcoin.

### 3. Calcolo dell'Hash della Chiave Pubblica

Per creare un indirizzo P2WPKH, si calcola l'hash della chiave pubblica utilizzando prima SHA-256 e poi RIPEMD-160 (questa combinazione è nota come HASH160 in Bitcoin):

```python
sha256_pubkey = hashlib.sha256(pubkey).digest()  # Prima hash con SHA256
ripemd160 = hashlib.new('ripemd160', sha256_pubkey).digest()  # Poi hash con RIPEMD160
```

Questo processo riduce la dimensione della chiave pubblica da 33/65 byte a soli 20 byte, rendendo gli indirizzi più compatti.

### 4. Creazione del Witness Program

Per gli indirizzi P2WPKH, il witness program è composto da:
- Un byte di versione (0 per P2WPKH)
- L'hash RIPEMD-160 della chiave pubblica

```python
converted = convertbits(list(ripemd160), 8, 5)  # Converte da base 8 (byte) a base 5 (per Bech32)
data = [0] + converted  # Aggiunge il byte della witness version (0 per P2WPKH)
```

### 5. Codifica Bech32

Infine, il witness program viene codificato utilizzando Bech32, un formato di codifica sviluppato specificamente per gli indirizzi SegWit:

```python
address = bech32_encode(config['hrp'], data)  # Codifica in formato Bech32
```

Dove `hrp` (Human Readable Part) è il prefisso che indica la rete:
- `bc` per mainnet
- `tb` per testnet
- `bcrt` per regtest

Il risultato è un indirizzo che inizia con questi prefissi, seguito da "1" (separatore) e una stringa di caratteri che rappresenta il witness program codificato.

### 6. Formato WIF della Chiave Privata

Parallelamente, il programma genera anche il formato WIF (Wallet Import Format) della chiave privata, che è un modo standard per rappresentare le chiavi private Bitcoin in un formato più compatto e con controllo degli errori:

```python
if compressed:
    # Aggiunge il byte che indica che la chiave è compressa (0x01)
    extended_key = config['wif_prefix'] + private_key + b'\x01'
else:
    # Senza il byte di compressione per chiavi non compresse
    extended_key = config['wif_prefix'] + private_key

# Calcola il checksum (primi 4 byte del doppio hash SHA256)
checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
wif = base58.b58encode(extended_key + checksum).decode()  # Codifica in Base58
```

Il formato WIF include:
1. Un prefisso specifico della rete (0x80 per mainnet, 0xEF per testnet/regtest)
2. La chiave privata
3. Opzionalmente, un byte (0x01) che indica se la chiave pubblica corrispondente è compressa
4. Un checksum di 4 byte per il controllo degli errori

Il tutto viene poi codificato in Base58, un sistema di codifica simile al Base64 ma che evita caratteri ambigui.

## Dettagli Tecnici

### Crittografia a Curva Ellittica (ECDSA)

Bitcoin utilizza la curva ellittica SECP256k1 per la crittografia. Una curva ellittica è definita dall'equazione:

```
y² = x³ + ax + b
```

Dove per SECP256k1, a = 0 e b = 7, risultando in:

```
y² = x³ + 7
```

La sicurezza di questa crittografia si basa sul "problema del logaritmo discreto della curva ellittica" (ECDLP), che è computazionalmente difficile da risolvere: dato un punto G sulla curva e un altro punto P = kG, è estremamente difficile trovare k conoscendo solo P e G.

In Bitcoin:
- La chiave privata è il numero k
- La chiave pubblica è il punto P = kG, dove G è un punto generatore noto

### Codifica Bech32

Bech32 è un formato di codifica sviluppato per Bitcoin che offre diversi vantaggi:

1. **Resistenza agli errori**: Può rilevare fino a 4 errori di carattere e localizzare fino a 2 errori.
2. **Efficienza**: Utilizza 32 caratteri (a-z e 0-9, escludendo 1, b, i, o) che possono essere facilmente letti e digitati.
3. **Distinzione**: Gli indirizzi hanno un prefisso leggibile che indica la rete (bc1, tb1, bcrt1).

La codifica Bech32 converte i dati binari in gruppi di 5 bit (invece dei tradizionali 8 bit per byte), permettendo una rappresentazione più efficiente.

## Utilizzo del Programma

### Prerequisiti

Il programma richiede Python 3.6+ e le seguenti librerie:

```
base58==2.1.1
bech32==1.2.0
ecdsa==0.19.0
six==1.17.0
```

Puoi installarle con:

```bash
pip install -r requirements.txt
```

### Esecuzione

Per eseguire il programma:

```bash
python p2wpkh.py
```

Il programma chiederà di selezionare la rete (mainnet, testnet o regtest) e se utilizzare chiavi compresse o non compresse. Genererà quindi i dati e li mostrerà in output, permettendo di salvarli in un file JSON.

### Esempio di Output

```
Seleziona il tipo di rete (mainnet, testnet, regtest): mainnet
Utilizzare chiavi compresse? (s/n): s

--- Risultati ---
Chiave privata (hex): 1a2b3c4d5e6f...
Chiave privata (WIF): L2eG5...
Chiave pubblica (compressa, hex): 02abcd1234...
Indirizzo segwit bech32: bc1qxyz12345...

Inserisci il nome del file (senza estensione) per salvare i dati: my_address
Dati salvati correttamente nel file: my_address.json
```

## Sicurezza e Best Practices

Quando si lavora con chiavi private Bitcoin, è fondamentale seguire alcune best practices di sicurezza:

1. **Ambiente Sicuro**: Genera le chiavi su un sistema sicuro, preferibilmente offline.
2. **Backup**: Crea backup sicuri delle tue chiavi private.
3. **Non Riutilizzare**: Ogni indirizzo dovrebbe essere utilizzato una sola volta per massimizzare la privacy.
4. **Verifica**: Controlla sempre gli indirizzi generati prima di utilizzarli per transazioni reali.

## Conclusione

Questo generatore di indirizzi P2WPKH fornisce un modo semplice per creare indirizzi Bitcoin SegWit e comprendere il processo sottostante. È importante notare che per uso in produzione o con fondi reali, si dovrebbero utilizzare wallet più completi che implementano misure di sicurezza aggiuntive come la derivazione gerarchica deterministica (HD) e la crittografia delle chiavi private.

## Licenza

Questo progetto è rilasciato sotto licenza MIT.






