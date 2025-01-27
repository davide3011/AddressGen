# AddressGen - Generatore di Wallet Bitcoin Multiformato

**Tool modulare per generare wallet Bitcoin con backup strutturato e documentazione tecnica.**

## 🚀 Funzionalità Principali
- Generazione wallet per diversi standard:
  - `P2PKH`: Indirizzi legacy Pay-to-Public-Key-Hash
  - `HDwallet`: Wallet gerarchici deterministici (BIP32/BIP44)
- Supporto per mainnet e testnet4
- [Documentazione tecnica](documentation/) dettagliata per ogni standard
- Output in JSON con metadati completi

## 📁 Struttura del Repository
Ogni modulo ha una cartella dedicata con la propria documentazione e requisiti:

| Cartella       | Descrizione                                  | Stato       |
|----------------|----------------------------------------------|-------------|
| [/P2PK](P2PK/) | Generazione indirizzi legacy Pay-to-Public-Key | Pianificato    |
| [/P2PKH](P2PKH/)| Generazione indirizzi P2PKH con codifica Base58 | Completo    |
| [/HDwallet](HDwallet/)| Wallet gerarchici (BIP-32/44/39)           | In sviluppo |
|[/P2SH](P2SH/) | Generazione indirizzi legacy Pay-to-Script-Hash | Pianificato    |

**📚 Per istruzioni dettagliate su ogni modulo, consultare il README.md nella rispettiva cartella.**

## ⚙️ Installazione
1. Clona il repository:
   ```bash
   git clone https://github.com/davide3011/AddressGen && cd AddressGen
      ```
2. Per i moduli specifici installa i requisiti
   ```bash
    pip install -r P2PKH/requirements.txt  # Esempio per P2PKH
   ```

## 📄 Licenza
Distribuito sotto licenza MIT.
