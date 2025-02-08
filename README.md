# AddressGen - Generatore di Wallet Bitcoin Multiformato

**Tool modulare per generare wallet Bitcoin con backup strutturato e documentazione tecnica.**

> **Nota:** Il progetto è in continua evoluzione. Nei prossimi aggiornamenti verranno aggiunti moduli per indirizzi P2PK, P2SH, bech32, P2TR e vanity address.

## 🚀 Funzionalità Principali
- **Generazione di wallet** per diversi standard:
  - **P2PK**: Indirizzi legacy Pay-to-Public-Key *(in sviluppo)*
  - **P2PKH**: Indirizzi legacy Pay-to-Public-Key-Hash (completo)
  - **P2WPKH**: Indirizzi Pay-to-Witness-Public-Key-Hash (completo)
  - **HDwallet**: Wallet gerarchici deterministici (BIP32/BIP44/BIP39) *(in sviluppo)*
- **Supporto per Mainnet e Testnet**  
  Utilizza il flag `--testnet` per generare indirizzi sulla rete di test.
- **Output in JSON** con metadati completi per ogni operazione.
- **Documentazione tecnica** dettagliata per ogni modulo disponibile in [documentation/](documentation/).

## 📁 Struttura del Repository
Ogni modulo ha una cartella dedicata, contenente sia il codice che la documentazione specifica:

| Cartella                | Descrizione                                                    | Stato         |
|-------------------------|----------------------------------------------------------------|---------------|
| [P2PK](P2PK/)           | Generazione indirizzi legacy Pay-to-Public-Key (P2PK)          | In Sviluppo   |
| [P2PKH](P2PKH/)         | Generazione indirizzi P2PKH con codifica Base58                | Completo      |
| [P2SH](P2SH/)           | Generazione indirizzi legacy Pay-to-Script-Hash                | Pianificato   |
| [P2WPKH](P2WPKH/)       | Generazione indirizzi Native SegWit (P2WPKH)                   | Completato    |
| [P2WSH](P2WSH/)         | Generazione indirizzi Native SegWit (P2WSH)                    | Pianificato   |
| [P2TR](P2TR/)           | Generazione indirizzi Pay-to-Taproot (P2TR)                    | Pianificato   |
| [HDwallet](HDwallet/)   | Wallet gerarchici deterministici (BIP32/BIP44/BIP39)           | In Sviluppo   |

**📚 Per istruzioni dettagliate su ogni modulo, consultare il README.md nella rispettiva cartella.**

## 🛠 Utilizzo

Ogni modulo fornisce script dedicati per la generazione degli indirizzi e la gestione dei wallet.

## 📄 Documentazione
La cartella [documentation](documentation/) contiene una guida completa e approfondita che illustra:
- Il funzionamento degli indirizzi Bitcoin (P2PK, P2PKH, P2SH, etc.)
- Le specifiche tecniche e gli algoritmi utilizzati nei vari moduli


## 📄 Licenza
Distribuito sotto licenza MIT.