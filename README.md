# Generatore di Indirizzi Bitcoin (P2PKH)

Questo repository contiene due script Python che consentono di generare chiavi Bitcoin (privata e pubblica) e un indirizzo P2PKH. Lo script mainGUI.py hq un'interfaccia grafica (GUI), mentre l'altro (mainNoGUI.py) funziona interamente da riga di comando.

## Funzionalità
Entrambi gli script offrono:

- **Generazione di chiavi private:** Utilizzando una sorgente di numeri casuali sicura ad alta entropia.
- **Conversione WIF (Wallet Import Format):** Supporta sia chiavi compresse che non compresse (compatibilità con Electrum).
- **Generazione di chiavi pubbliche:** In formato compresso e non compresso.
- **Calcolo dell'indirizzo P2PKH:** Basato sulla rete scelta (Mainnet o Testnet).
- **Salvataggio dei dati:** Salva chiavi e indirizzi in un file JSON con un nome personalizzato.

## Requisiti

- **Python**: Versione 3.8 o superiore.
- **Librerie Python**:
  - `ecdsa`: Per le firme crittografiche.
  - `base58`: Per la codifica Base58.
  - `tkinter`: Necessario solo per la versione GUI.
- Sistema operativo: Linux.

## Struttura del progetto

- mainGUI.py: Script con interfaccia grafica (GUI).
- mainNoGUI.py: Script senza interfaccia grafica, eseguibile da riga di comando.
- requirements.txt: Dipendenze necessarie.
documentation/: Documentazione dettagliata sull'algoritmo e sul formato dei dati.

## Installazione

### 1. Clona il repository

Clona il progetto sul tuo computer:
```bash
git clone git@github.com:davide3011/AddressGen.git
cd AddressGen
```

### 2. Crea un ambiente virtuale (consigliato)
Crea e attiva un ambiente virtuale Python:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installa le dipendenze
Installa tutte le librerie necessarie:

```bash
pip install -r requirements.txt
```

Nota: Assicurati di avere tkinter installato. Su Linux/Debian, puoi installarlo con:

```bash
sudo apt install python3-tk
```

## Utilizzo
### Script con GUI

Avvia lo script:
```bash
python mainGUI.py
```

Interagisci con l'interfaccia:
- Seleziona la rete (Mainnet o Testnet).
- Scegli il formato della chiave pubblica (compressa o non compressa).
- Inserisci un nome per il wallet.
- Premi "Genera Chiavi" per creare chiavi e indirizzo.
- Premi "Salva i dati" per esportare le informazioni in un file JSON.

### Script senza GUI (CLI)
Avvia lo script:

```bash
python mainNoGUI.py
```

Segui le istruzioni fornite per:
- Selezionare la rete.
- Scegliere il formato della chiave pubblica.
- Generare e visualizzare chiavi e indirizzo.
- Salvare i risultati in un file JSON.

## Struttura del file JSON
Il file JSON generato conterrà i seguenti campi:

```bash
{
    "private_key_hex": "Hexadecimal format of the private key",
    "private_key_wif": "Private key in WIF format",
    "public_key_hex": "Hexadecimal format of the public key",
    "address": "Generated Bitcoin address (P2PKH)"
}
```

## Documentazione tecnica
Il repository include un file .tex e il corrispondente PDF che spiegano dettagliatamente:

   - Calcolo delle chiavi pubbliche:
   - Utilizzo dell'algoritmo ECDSA con curva SECP256k1.
   - Conversione in formato compresso e non compresso.
   - Generazione dell'indirizzo P2PKH:

File inclusi:
documentation/P2PKH.tex (file sorgente LaTeX).
documentation/P2PKH.pdf
Puoi leggere il file PDF nella cartella docs per comprendere meglio l'algoritmo utilizzato dal programma.

## Contributi
Se hai suggerimenti o vuoi contribuire al progetto, sentiti libero di aprire un'issue o una pull request su GitHub.

## Licenza
Questo progetto è distribuito sotto licenza MIT. Vedi il file LICENSE per maggiori dettagli.
