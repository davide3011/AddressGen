# Indirizzi P2PK (Pay-to-Public-Key) in Bitcoin

## Introduzione

Questo repository contiene un'implementazione didattica degli indirizzi P2PK (Pay-to-Public-Key) di Bitcoin. Il codice è stato sviluppato esclusivamente a scopo educativo per comprendere i meccanismi crittografici alla base dei primi indirizzi Bitcoin.

## Contesto Storico

Gli indirizzi P2PK rappresentano uno dei primi metodi utilizzati in Bitcoin per inviare fondi a un destinatario. Furono introdotti da Satoshi Nakamoto nelle prime versioni del protocollo Bitcoin e utilizzati estensivamente nei primi blocchi della blockchain.

Il primo blocco della blockchain Bitcoin (il "blocco genesi") utilizzava proprio uno script P2PK per assegnare la ricompensa di 50 BTC. Anche le prime transazioni effettuate da Satoshi Nakamoto utilizzavano questo formato.

## Perché P2PK è stato abbandonato

Nonostante la loro importanza storica, gli indirizzi P2PK sono stati gradualmente abbandonati a favore di formati più avanzati come P2PKH (Pay-to-Public-Key-Hash) e, successivamente, P2SH (Pay-to-Script-Hash) e SegWit per diverse ragioni:

1. **Sicurezza**: Gli indirizzi P2PK espongono direttamente la chiave pubblica nella blockchain. Sebbene attualmente non sia possibile derivare una chiave privata da una chiave pubblica con la tecnologia disponibile, si teme che i computer quantistici potrebbero un giorno rendere questo possibile. Con P2PKH, la chiave pubblica viene esposta solo quando si spende, riducendo questa vulnerabilità.

2. **Dimensione**: Gli script P2PK sono più grandi degli script P2PKH, specialmente quando utilizzano chiavi pubbliche non compresse (65 byte contro 20 byte di hash).

3. **Usabilità**: Gli indirizzi P2PKH hanno un formato più corto e includono un checksum per prevenire errori di digitazione, rendendoli più pratici per l'uso quotidiano.

4. **Mancanza di indirizzi leggibili**: P2PK non aveva un formato di indirizzo leggibile dall'uomo come quello introdotto successivamente con P2PKH (gli indirizzi Bitcoin che iniziano con "1").

## Teoria Crittografica

### Crittografia a Curva Ellittica

Bitcoin utilizza la crittografia a curva ellittica (ECC), specificamente la curva secp256k1, per generare coppie di chiavi. Questa curva è definita dall'equazione:

```
y² = x³ + 7 (mod p)
```

dove p è un numero primo molto grande (2²⁵⁶ - 2³² - 2⁹ - 2⁸ - 2⁷ - 2⁶ - 2⁴ - 1).

La sicurezza di ECC si basa sul "problema del logaritmo discreto su curve ellittiche" (ECDLP), che rende computazionalmente impossibile derivare la chiave privata dalla chiave pubblica.

### Chiavi Private e Pubbliche

1. **Chiave Privata**: Un numero casuale di 256 bit (32 byte). Deve essere mantenuto segreto e rappresenta il "diritto di proprietà" sui bitcoin.

2. **Chiave Pubblica**: Un punto sulla curva ellittica derivato dalla chiave privata. Può essere condiviso pubblicamente e viene utilizzato per verificare le firme.
   - **Non compressa**: 65 byte (1 byte di prefisso 0x04 + 32 byte per la coordinata X + 32 byte per la coordinata Y)
   - **Compressa**: 33 byte (1 byte di prefisso 0x02/0x03 + 32 byte per la coordinata X)

## Script P2PK

Uno script P2PK ha una struttura molto semplice:

```
<lunghezza della chiave pubblica> <chiave pubblica> OP_CHECKSIG
```

In esadecimale, per una chiave pubblica non compressa, appare come:

```
41 <65 byte della chiave pubblica> AC
```

Dove:
- `41` è l'opcode che indica di inserire i prossimi 65 byte nello stack
- `<chiave pubblica>` sono i 65 byte della chiave pubblica non compressa
- `AC` è l'opcode per OP_CHECKSIG, che verifica la firma

Per spendere i bitcoin inviati a uno script P2PK, il proprietario deve fornire una firma valida creata con la chiave privata corrispondente alla chiave pubblica nello script.

## Formato WIF (Wallet Import Format)

Il formato WIF è un modo standard per rappresentare le chiavi private Bitcoin in un formato più leggibile e sicuro. Il processo di codifica WIF include:

1. Prendere la chiave privata (32 byte)
2. Aggiungere un byte di prefisso (0x80 per mainnet, 0xEF per testnet)
3. Se la chiave è per una pubkey compressa, aggiungere un byte 0x01 alla fine
4. Calcolare un checksum (primi 4 byte del doppio SHA-256 dei dati precedenti)
5. Concatenare i dati con il checksum
6. Codificare il risultato in Base58

Questo formato facilita l'importazione e l'esportazione di chiavi private tra diversi wallet Bitcoin.

## Funzionamento del Programma

Il programma `p2pk.py` implementa la generazione di indirizzi P2PK seguendo questi passaggi:

### 1. Generazione della Chiave Privata

Utilizza `secrets.token_bytes(32)` per generare 32 byte casuali crittograficamente sicuri che costituiscono la chiave privata.

### 2. Derivazione della Chiave Pubblica

Utilizza la libreria `ecdsa` con la curva SECP256k1 per derivare la chiave pubblica dalla chiave privata. Il programma supporta sia chiavi pubbliche compresse (33 byte) che non compresse (65 byte).

### 3. Costruzione dello Script P2PK

Crea lo script P2PK combinando:
- Un opcode di push che indica la lunghezza della chiave pubblica
- La chiave pubblica stessa
- L'operazione OP_CHECKSIG (opcode: 0xAC)

### 4. Creazione del Formato WIF

Converte la chiave privata nel formato WIF (Wallet Import Format) seguendo il processo descritto sopra, includendo il prefisso di rete appropriato e, se necessario, il flag di compressione.

### 5. Output e Salvataggio

Il programma visualizza i risultati a schermo e salva i dati generati in un file JSON per riferimento futuro.

## Utilizzo del Programma

Per utilizzare il programma:

1. Assicurarsi di avere Python installato con le dipendenze necessarie (`ecdsa`, `base58`)
2. Eseguire `python p2pk.py`
3. Seguire le istruzioni a schermo per selezionare il tipo di rete e se utilizzare chiavi compresse
4. I risultati verranno visualizzati e salvati in un file JSON

## Nota Importante

Questo codice è fornito **esclusivamente a scopo didattico**. Gli indirizzi P2PK non sono più utilizzati nelle transazioni Bitcoin moderne e non dovrebbero essere utilizzati per conservare fondi reali. Per applicazioni reali, si consiglia di utilizzare wallet Bitcoin moderni che implementano le più recenti pratiche di sicurezza.

## Conclusione

Lo studio degli indirizzi P2PK offre una finestra sull'evoluzione di Bitcoin e sui principi crittografici fondamentali che ne sono alla base. Comprendere questi concetti è essenziale per chiunque voglia approfondire il funzionamento interno di Bitcoin e delle criptovalute in generale.

## Licenza

Questo progetto è rilasciato sotto licenza MIT.