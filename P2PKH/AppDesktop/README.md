# Bitcoin P2PKH Address Generator

Un'applicazione desktop moderna e sicura per la generazione di indirizzi Bitcoin P2PKH (Pay-to-Public-Key-Hash) con interfaccia grafica intuitiva.

## Caratteristiche

- **Generazione sicura**: Utilizza crittografia ECDSA per generare chiavi private casuali
- **Multi-network**: Supporta mainnet, testnet e regtest
- **Interfaccia moderna**: GUI responsive con temi dinamici per ogni rete
- **Export facile**: Salvataggio delle chiavi in formato JSON
- **Thread sicuri**: Generazione asincrona per non bloccare l'interfaccia
- **Formati multipli**: Chiavi private in formato HEX e WIF

## Requisiti

- Python 3.8 o superiore
- PySide6
- Librerie crittografiche (ecdsa, base58)

## Installazione

### Installazione rapida

```bash
# Clona il repository
git clone <repository-url>
cd app_test

# Installa le dipendenze
pip install -r requirements.txt

# Avvia l'applicazione
python app.py
```

### Installazione in ambiente virtuale (consigliato)

```bash
# Crea ambiente virtuale
python -m venv bitcoin_generator

# Attiva l'ambiente (Windows)
bitcoin_generator\Scripts\activate

# Attiva l'ambiente (Linux/Mac)
source bitcoin_generator/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Avvia l'applicazione
python app.py
```

### Installazione su Linux

Per sistemi Linux, segui questi passaggi:

```bash
# Crea un ambiente virtuale
python3 -m venv venv

# Attiva l'ambiente virtuale
source venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt

# Esegui l'applicazione
python app.py
```

## Utilizzo

1. **Avvia l'applicazione**: Esegui `python app.py`
2. **Seleziona la rete**: Scegli tra mainnet, testnet o regtest
3. **Genera indirizzo**: Clicca su "Genera Indirizzo"
4. **Salva i dati**: Usa "Scarica Chiave" per esportare in JSON

### Esempio di output

```
Indirizzo: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
Chiave Privata (HEX): e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
Chiave Privata (WIF): 5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ
Chiave Pubblica: 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Network: mainnet
Tipo: P2PKH
```

## Architettura

```
app_test/
├── app.py              # Applicazione principale e entry point
├── controller.py       # Logica di business e gestione eventi
├── ui_components.py    # Componenti dell'interfaccia utente
├── utils.py           # Funzioni crittografiche Bitcoin
├── themes.py          # Gestione temi per diverse reti
├── requirements.txt   # Dipendenze Python
├── icon.ico          # Icona dell'applicazione
└── README.md         # Documentazione
```

### Componenti principali

- **BitcoinAddressGenerator**: Classe principale che coordina UI e logica
- **BitcoinController**: Gestisce la logica di business e gli eventi
- **BitcoinGeneratorUI**: Interfaccia utente con PySide6
- **ThemeManager**: Gestione temi dinamici per le reti
- **Utils**: Funzioni crittografiche per Bitcoin (ECDSA, Base58, etc.)

## Sicurezza

- Generazione di chiavi private con `os.urandom()` (crittograficamente sicuro)
- Implementazione standard ECDSA secp256k1
- Codifica Base58Check per indirizzi
- Supporto per chiavi pubbliche compresse
- **IMPORTANTE**: Questa è un'applicazione di sviluppo/test. Per uso in produzione, considera soluzioni hardware dedicate

## Reti supportate

| Rete | Descrizione | Prefisso Indirizzo | Prefisso WIF |
|------|-------------|-------------------|---------------|
| **Mainnet** | Rete Bitcoin principale | `1` | `5`, `K`, `L` |
| **Testnet** | Rete di test Bitcoin | `m`, `n` | `9`, `c` |
| **Regtest** | Rete locale per sviluppo | `m`, `n` | `9`, `c` |

## Temi

L'applicazione cambia automaticamente tema in base alla rete selezionata:
- **Mainnet**: Tema arancione
- **Testnet**: Tema verde
- **Regtest**: Tema blu

## Build e Distribuzione

### Per sviluppatori

```bash
# Build eseguibile con PyInstaller
pyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.ico;." app.py

# Build con file spec personalizzato
pyinstaller app.spec --clean
```

### Creazione installer

```bash
# Crea distribuzione
python setup.py sdist bdist_wheel

# Test locale
pip install dist/bitcoin-address-generator-*.whl
```

## Test

```bash
# Test funzionalità base
python -c "from utils import generate_address; print(generate_address('testnet'))"

# Test interfaccia
python app.py
```

## Licenza

Questo progetto è distribuito sotto licenza MIT.

## Disclaimer

Questo software è fornito "così com'è" senza garanzie di alcun tipo. L'autore non è responsabile per eventuali perdite o danni derivanti dall'uso di questo software. Utilizzare sempre pratiche di sicurezza appropriate quando si lavora con chiavi private Bitcoin.

## Risorse utili

- [Bitcoin Developer Guide](https://developer.bitcoin.org/)
- [BIP 32 - Hierarchical Deterministic Wallets](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki)
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [ECDSA Library](https://github.com/tlsfuzzer/python-ecdsa)

---

