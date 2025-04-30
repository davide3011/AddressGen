# AddressGen - Generatore di indirizzi


**GenAddress** è una raccolta di programmi per la generazione di indirizzi Bitcoin in diversi formati. 
Questo repository nasce con l'obiettivo di fornire strumenti funzionali per esplorare la logica alla base della generazione di indirizzi nella rete Bitcoin.


Per ulteriori approfondimenti consultare [Mastering Bitcoin – A. Antonopoulos](https://github.com/bitcoinbook/bitcoinbook)


**Nota**: Il progetto è in continua evoluzione.


## Struttura del Repository
Ogni modulo ha una cartella dedicata, contenente sia il codice che la documentazione specifica.


| Cartella                | Descrizione                                                    |
|-------------------------|----------------------------------------------------------------|
| [P2PK](P2PK/)           | Generazione indirizzi Pay-to-Public-Key                        |
| [P2PKH](P2PKH/)         | Generazione indirizzi P2PKH con codifica Base58                |
| [P2WPKH](P2WPKH/)       | Generazione indirizzi Native SegWit (P2WPKH)                   |
| [P2TR](P2TR/)           | Generazione indirizzi Native SegWit v1 (Taproot, P2TR)         |
| [HDwallet](HDwallet/)   | Wallet gerarchici deterministici (BIP32/BIP44/BIP39)           |
| [VanityAddress](VanityAddress)|Generazione di indirizzi personalizzati che contengono un prefisso |


**Nota**: Per istruzioni dettagliate su ogni modulo, consultare il README.md nella rispettiva cartella.


## Utilizzo


Ogni modulo fornisce script dedicati per la generazione degli indirizzi e la gestione dei wallet.


## Licenza
Distribuito sotto licenza MIT.

