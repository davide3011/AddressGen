# Generatore di indirizzi Bitcoin Taproot (P2TR)

Questo programma Python genera indirizzi Bitcoin Taproot (P2TR) per le reti reti mainnet, testnet e regtest e salva le chiavi e l'indirizzo risultante in un file JSON.

## Come si generano e come funzionano gli indirizzi Bitcoin Taproot (P2TR)

### 1. Introduzione
Gli indirizzi Taproot rappresentano l'evoluzione degli indirizzi Bitcoin, offrendo maggiore privacy, efficienza e flessibilità. Comprendere come vengono generati e come funzionano è fondamentale per chiunque voglia approfondire la tecnologia Bitcoin.

### 2. Generazione della chiave privata
La chiave privata è un numero casuale di 32 byte (256 bit), generato in modo sicuro tramite funzioni crittografiche (`secrets.token_bytes(32)`). Questa chiave è il segreto che permette di spendere i fondi associati all'indirizzo.

**Esempio:**
```
private_key = secrets.token_bytes(32)
```

### 3. Derivazione della chiave pubblica x-only (BIP-340)
La chiave pubblica viene calcolata dalla chiave privata tramite la curva ellittica secp256k1. Taproot utilizza la rappresentazione "x-only", cioè solo la coordinata X della chiave pubblica (32 byte), come richiesto da BIP-340 (Schnorr signatures).

**Esempio:**
```
pubkey_compressed = coincurve.PrivateKey(private_key).public_key.format(compressed=True)
pubkey_xonly = pubkey_compressed[1:33]
```

### 4. Il tweak Taproot e la costruzione della chiave finale (BIP-341)
Taproot permette di "tweakkare" la chiave pubblica, cioè modificarla matematicamente per includere condizioni di spesa aggiuntive (MAST). Nel caso più semplice (keypath spending), la chiave x-only viene usata direttamente come output key.

### 5. Costruzione dell'indirizzo P2TR
L'indirizzo Taproot è un SegWit v1 (witness version 1), codificato in formato Bech32m (BIP-350). La chiave pubblica x-only viene inserita come "witness program".

**Passaggi:**
- Si aggiunge il prefisso della rete (bc per mainnet, tb per testnet, bcrt per regtest)
- Si imposta la witness version a 1
- Si converte la chiave x-only in array di bit a 5 bit
- Si calcola la checksum Bech32m
- Si concatena tutto per ottenere l'indirizzo

**Esempio:**
```
address = bech32_encode(hrp, data, spec="bech32m")
```

### 6. Formato WIF della chiave privata
Il formato WIF (Wallet Import Format) permette di esportare/importare la chiave privata in modo compatibile con i wallet. Si aggiunge un prefisso di rete, si calcola il checksum e si codifica in base58.

### 7. Glossario dei termini principali
- **Chiave privata:** Numero segreto che controlla i fondi.
- **Chiave pubblica x-only:** Coordinata X della chiave pubblica, usata in Taproot.
- **Tweak:** Modifica matematica della chiave pubblica per aggiungere condizioni di spesa.
- **Witness version:** Versione del programma witness (1 per Taproot).
- **Bech32m:** Formato di encoding per indirizzi SegWit v1+.
- **WIF:** Formato standard per esportare la chiave privata.

### 8. Riferimenti e approfondimenti

- **[BIP-141 (SegWit v0)](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki):** Introduce il meccanismo di segregated witness e il calcolo del witness commitment nei blocchi.
- **[BIP-173 (Bech32)](https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki):** Definisce il formato Bech32 per gli indirizzi native SegWit v0.
- **[BIP-340 (Schnorr Signatures)](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki):** Specifica lo schema di firma Schnorr su secp256k1, usato da Taproot per il keypath spending.
- **[BIP-341 (Pay-to-Taproot)](https://en.bitcoin.it/wiki/BIP_0341):** Definisce il nuovo output type SegWit v1 (P2TR), le regole di spending, il tweak della chiave e il commitment MAST.
- **[BIP-342 (Tapscript)](https://trustmachines.co/blog/bitcoin-tapscript/):** Aggiorna il linguaggio di script per P2TR introducendo nuovi opcodes, versioning delle leaf script e validazione delle scriptpath.
- **[BIP-350 (Bech32m)](https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki):** Estende BIP-173 con una checksum "Bech32m" per gli indirizzi SegWit v1+ (compresi P2TR). 

## Come funziona il programma

Il programma genera una chiave privata casuale, deriva la chiave pubblica x-only secondo BIP-340, costruisce l'indirizzo Taproot (P2TR) in formato Bech32m (BIP-350) e salva tutte le informazioni in un file JSON. Supporta le reti mainnet, testnet e regtest.

### Dipendenze
- Python 3
- [coincurve](https://pypi.org/project/coincurve/)
- [base58](https://pypi.org/project/base58/)

Installa le dipendenze con:
```bash
pip install coincurve base58
```

### Utilizzo
1. Avvia lo script:
   ```bash
   python traproot.py
   ```
2. Scegli la rete desiderata tra mainnet, testnet o regtest.
3. Inserisci il nome del file di output (senza estensione).
4. Verrà generato un file JSON con le seguenti informazioni:
   - Chiave privata (hex)
   - Chiave privata (WIF)
   - Chiave pubblica x-only (hex)
   - Indirizzo Taproot (P2TR)
   - Rete selezionata

### Esempio di output JSON
```json
{
    "private_key_hex": "...",
    "private_key_wif": "...",
    "public_key_xonly_hex": "...",
    "address": "...",
    "network": "mainnet|testnet|regtest"
}
```

## Note
- Il programma non memorizza né trasmette le chiavi generate: assicurati di conservare in modo sicuro il file JSON prodotto.
- Per approfondimenti tecnici, consulta i BIP elencati sopra.

## LICENSE

Il programma è rilasciato sotto la licenza MIT.