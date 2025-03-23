# Generatore HD Wallet Bitcoin

Un generatore di wallet Bitcoin HD (Hierarchical Deterministic) compatibile con Electrum e altri wallet popolari, con interfaccia web locale e massima sicurezza.

## Funzionalità Principali

- Genera wallet compatibili con gli standard **BIP39, BIP44, BIP84**
- Supporta indirizzi **Legacy (P2PKH)** e **SegWit (P2WPKH)**
- Funziona sia su **Mainnet** che **Testnet**
- Genera fino a **20 indirizzi derivati** dallo stesso seed
- Supporta seed phrase da **12, 15, 18, 21, 24 parole**
- Esporta i dati del wallet in formato **JSON**

## Installazione

### Prerequisiti
- Python 3.8+
- pip

### Passaggi:
```bash
# Clona il repository
git clone https://github.com/davide3011/AddressGen.git
cd AddressGen

# Crea e attiva un ambiente virtuale (consigliato)
python -m venv venv
venv\Scripts\activate

# Installa le dipendenze
pip install -r requirements.txt

# Avvia l'applicazione
python app.py
```

Apri il browser all'indirizzo: http://localhost:5000

## Guida all'Uso

1. **Seleziona il tipo di indirizzo**:
   - Legacy (P2PKH) per massima compatibilità
   - SegWit (P2WPKH) per commissioni più basse

2. **Scegli la rete**:
   - Mainnet per Bitcoin reali
   - Testnet per Bitcoin di prova

3. **Imposta il numero di indirizzi** (da 1 a 20)

4. **Seleziona la lunghezza della seed phrase**

5. Clicca **"Genera"** per creare il wallet

6. **Salva** la seed phrase e le chiavi private in modo sicuro

## Compatibilità

Il wallet generato è compatibile con:

- **Electrum** (importazione via seed phrase)
- **Hardware Wallet**: Ledger, Trezor
- **Mobile Wallet**: BlueWallet, Trust Wallet, Exodus
- **Desktop Wallet**: Bitcoin Core, Electrum

## Sicurezza

- Tutte le operazioni avvengono **localmente** nel tuo browser
- **Nessun dato** viene inviato a server esterni
- Generazione di numeri casuali **crittograficamente sicuri**
- Supporto per ambienti **offline/air-gapped**

## 📂 Struttura del Progetto

```
AddressGen/
├── app.py              # Script principale
├── requirements.txt    # Dipendenze
├── static/             # Risorse statiche
│   ├── style.css
│   └── ...
├── templates/          # Template HTML
│   ├── index.html
│   └── guide.html
└── README.md           # Questo documento
```

## Come Contribuire

1. Fai un fork del repository
2. Crea un branch per la tua feature:
   ```bash
   git checkout -b feature/nuova-feature
   ```
3. Commit delle modifiche:
   ```bash
   git commit -m 'Aggiunta nuova feature'
   ```
4. Push sul branch:
   ```bash
   git push origin feature/nuova-feature
   ```
5. Crea una Pull Request

## Standard BIP Implementati

- **BIP39**: Mnemonic code for generating deterministic keys
- **BIP32**: Hierarchical Deterministic Wallets
- **BIP44**: Multi-Account Hierarchy for Deterministic Wallets
- **BIP84**: Derivation scheme for P2WPKH based accounts

## Licenza

Questo progetto è licenziato sotto la **MIT License**.