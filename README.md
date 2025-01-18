# Generatore di Indirizzi Bitcoin (P2PKH)

Questo programma consente di generare una chiave privata casuale, la relativa chiave pubblica e l'indirizzo P2PKH e salvare le informazioni in formato JSON. Include un'interfaccia grafica intuitiva per selezionare la rete (Mainnet o Testnet), il formato della chiave (compressa o non compressa), e un nome per il wallet.

## Funzionalità

- **Generazione di chiavi private:** Utilizzando una sorgente di numeri casuali sicura ad alta entropia.
- **Conversione WIF (Wallet Import Format):** Supporta sia chiavi compresse che non compresse (compatibilità con Electrum).
- **Generazione di chiavi pubbliche:** In formato compresso e non compresso.
- **Calcolo dell'indirizzo P2PKH:** Basato sulla rete scelta (Mainnet o Testnet).
- **Salvataggio dei dati:** Salva chiavi e indirizzi in un file JSON con un nome personalizzato.

## Requisiti

- Python 3.8 o superiore.
- Librerie Python:
  - `tkinter` (per l'interfaccia grafica, incluso nativamente in Python).
  - `ecdsa` (per le firme crittografiche).
  - `base58` (per l'encoding Base58).
- Sistema operativo: Linux.

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

### 4. Esegui il programma
Avvia il programma con il seguente comando:

```bash
python main.py
```

## Come usare il programma

1. Seleziona la rete:
   - Mainnet: Per creare indirizzi Bitcoin sulla rete principale.
   - Testnet: Per creare indirizzi sulla rete di test.

2. Scegli il formato della chiave pubblica:
   - Compressa: (Più breve, standard moderno).
   - Non compressa: (Legacy, più lunga).

3. Inserisci il nome del wallet:
   Il nome verrà usato come nome del file JSON per salvare le chiavi e l'indirizzo.

4. Genera le chiavi:
   Premi il pulsante "Genera Chiavi" per generare chiavi e indirizzi Bitcoin.

5. Salva i dati:
   Premi il pulsante "Salva i dati" per esportare le chiavi e l'indirizzo in un file JSON.

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

## Contributi
Se hai suggerimenti o vuoi contribuire al progetto, sentiti libero di aprire un'issue o una pull request su GitHub.

## Licenza
Questo progetto è distribuito sotto licenza MIT. Vedi il file LICENSE per maggiori dettagli.
