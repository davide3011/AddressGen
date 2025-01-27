# Bitcoin HD Wallet Toolkit ???

Tool per la gestione di portafogli Bitcoin gerarchici deterministici (BIP32/39/44).

## Strumenti Disponibili ???
### 1. Generatore HD Wallet
```bash
python hd_wallet_generator.py
```
- Crea nuovi portafogli da zero

- Genera seed phrase BIP39 (12/18/24 parole)

- Deriva chiavi gerarchiche (BIP32/44)

## Analizzatore
```bash
python wallet_explorer.py
```
- Monitora portafogli esistenti

- Verifica saldi in tempo reale

- Analizza transazioni confermate/pending

## Funzionalit√† Comuni ?
? Supporto Mainnet/Testnet

?? Compatibilit‡ con standard BIP32/39/44

?? Gestione sicura delle chiavi private

?? Esportazione JSON strutturato

??? Validazione integrata degli input

## Installazione ??
```bash
pip install -r requirements.txt
```

## Funzionalit‡ ??
### Generatore HD
?? Generazione seed phrase con entropia configurabile

?? Supporto passphrase personalizzata

?? Derivazione path personalizzabile

?? Esportazione chiavi in formato WIF

### Analizzatore HD
?? Integrazione real-time con mempool.space

?? Dashboard saldi interattiva

?? Storico transazioni dettagliato

?? Allerta saldi pending

## Strutture Dati JSON ??
### Generatore HD
```bash
{
  "Network": "Mainnet",
  "Seed": "gravity example...24 words",
  "BIP32_Root_Key": "xprv9s21Zr...",
  "Addresses": [
    {
      "Address": "bc1q...",
      "Private_Key": {
        "WIF": "L3p6o9i..."
      }
    }
  ]
}
```
### Analizzatore HD
```bash
{
  "total_balances": {
    "confirmed": 0.54823145,
    "pending": 0.00120000
  },
  "addresses": [
    {
      "balance": {
        "confirmed": 0.21540000,
        "pending": 0.00050000
      }
    }
  ]
}
```

## Esempi d'Uso ??
### Generazione Wallet
```bash
=================== NUOVO WALLET ===================
Frase mnemonica (24 parole): 
burger voice rhythm prize switch empty drama wrap...

BIP32 Root Key: xprv9s21ZrQHp...
Indirizzo 1: bc1qj5pczk... - WIF: L3p6o9i...
```
### Analisi Wallet
```bash
=================== ANALISI SALDI ==================
  1. bc1qj5pczk... 
     Confermati: 0.21540000 ?
     In pending: 0.00050000 ?

Saldo totale: 0.54943145 ?
```

## Licenze ??
MIT License - Libero utilizzo con attribuzione.

## AVVERTENZA!
**I creatori non sono responsabili per perdite di fondi!**
