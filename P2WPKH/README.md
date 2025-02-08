# Generatore di Indirizzi Bitcoin SegWit (P2WPKH)

Questo progetto fornisce due strumenti per generare indirizzi Bitcoin **SegWit (P2WPKH)**:
- **cli.py**: versione da riga di comando (CLI).
- **gui.py**: versione con interfaccia grafica (GUI) realizzata con `tkinter`.

## **Cos'è un indirizzo P2WPKH**
Un **P2WPKH (Pay-to-Witness-Public-Key-Hash)** è un indirizzo Bitcoin basato su **SegWit (Segregated Witness)**, introdotto per migliorare la scalabilità e ridurre le commissioni di transazione.

### Vantaggi di P2WPKH (SegWit)
1. **Fee più basse**: Le transazioni pesano meno e quindi costano meno.
2. **Migliore scalabilità**: Aumento del numero di transazioni che possono essere incluse in un blocco.
3. **Eliminazione della transaction malleability**: Protegge le transazioni da modifiche indesiderate dell'hash.
4. **Retrocompatibilità**: Supportato da wallet e software aggiornati, pur mantenendo compatibilità tramite P2SH.

## **Installazione**
### 1. Clona il repository


### 2. Crea un ambiente virtuale Python
python3 -m venv venv
source venv/bin/activate  # Su Linux/macOS
venv\Scripts\activate      # Su Windows

### 3. Installa le dipendenze
```bash
pip install -r requirements.txt
```

## Eseguire il programma

Il programma chiederà di selezionare la rete (mainnet, testnet o regtest), genererà i dati e li mostrerà in output.

### Output
Il programma stampa e salva automaticamente i seguenti dati in un file JSON:

```
Chiave privata (HEX)
Chiave privata in formato WIF
Chiave pubblica compressa (HEX)
Indirizzo Bitcoin P2WPKH (bech32)
```

## Esempio di output
```
Seleziona il tipo di rete (mainnet, testnet, regtest): mainnet

--- Risultati ---
Chiave privata (hex): 1a2b3c4d5e6f...
Chiave privata (WIF): L2eG5...
Chiave pubblica (compressa, hex): 02abcd1234...
Indirizzo segwit bech32: bc1qxyz12345...

Inserisci il nome del file (senza estensione) per salvare i dati: my_address
Dati salvati correttamente nel file: my_address.json
```

## Utilizzo della versione GUI
La versione GUI offre un'interfaccia grafica per generare e salvare indirizzi P2WPKH.

### Eseguire il programma

1. Selezione del network (Mainnet, Testnet, Regtest).

2. Campo di testo per inserire il nome del file JSON.

3. Pulsante "Genera Indirizzo" per generare un nuovo indirizzo e mostrarlo nell'area di testo.

4. Pulsante "Salva in JSON" per salvare i dati generati in un file.

Il programma mostra i dati generati in una finestra e permette di salvarli in un file JSON.

## Licenza
Questo progetto è rilasciato sotto licenza MIT.







