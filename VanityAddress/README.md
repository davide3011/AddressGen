# Generatore di Vanity Address Bitcoin

## Introduzione

Questo progetto nasce con l'obiettivo di dimostrare concretamente il valore dell'intelligenza artificiale come strumento assistivo nello sviluppo software. I vanity address Bitcoin sono indirizzi personalizzabili che consentono di includere una sequenza di caratteri significativa, migliorando memorabilità e verificabilità. 
Maggiori informazioni su cosa sono i vanity address sono disponibili nel [documento ufficiale di Bit2Me Academy](https://academy.bit2me.com/it/que-es-una-vanity-address/).

Ho iniziato lo sviluppo creando il prototipo iniziale vanity.py utilizzando Python, un linguaggio ideale per questa fase grazie alla sua semplicità, immediatezza e rapidità di prototipazione. Ciò mi ha permesso di validare velocemente il concetto e arrivare rapidamente a un Minimum Viable Product (MVP) funzionante.

Nella fase successiva, ho sfruttato le potenzialità dell'intelligenza artificiale per tradurre il codice Python in un'implementazione più efficiente e performante in C++. Questo processo di traduzione è stato seguito da un ciclo iterativo di ottimizzazioni, sempre supportato dall'IA, che ha permesso di migliorare sensibilmente il codice in termini di prestazioni, sicurezza e qualità.

## Obiettivi del Progetto

Mostrare come l'intelligenza artificiale può essere utilizzata efficacemente come assistente nello sviluppo software, semplificando operazioni complesse come traduzioni e ottimizzazioni.

Evidenziare il valore aggiunto derivante dalla collaborazione tra sviluppatore e IA in tutte le fasi di sviluppo, dalla prototipazione iniziale alla realizzazione di software performanti in linguaggi più complessi come il C++.

## Istruzioni Docker

### Prerequisiti

- Docker installato sul tuo sistema
- I file sorgente del progetto (già presenti nella cartella)

### 1. Costruzione dell'Immagine Docker

Per costruire l'immagine Docker, esegui il seguente comando dalla directory principale del progetto (dove si trova il Dockerfile):

```bash
docker build -t vanity-generator .
```

Questo comando creerà un'immagine Docker chiamata `vanity-generator` contenente tutte le dipendenze necessarie e compilerà automaticamente il programma.

### 2. Esecuzione del Container

Per avviare il container e il generatore di vanity address:

```bash
docker run -it --rm vanity-generator
```

### 3. Utilizzo del Programma

Una volta avviato, il programma:
1. Mostrerà il numero di core CPU disponibili
2. Chiederà quanti core utilizzare (0 per usarli tutti)
3. Chiederà di inserire il prefisso desiderato per l'indirizzo Bitcoin

Inserisci i valori richiesti e premi Invio per avviare la ricerca.

### 4. Comandi Docker Utili

- Per visualizzare le immagini Docker disponibili: `docker images`
- Per visualizzare i container in esecuzione: `docker ps`
- Per fermare un container in esecuzione: `docker stop [CONTAINER_ID]`
- Per rimuovere l'immagine Docker: `docker rmi vanity-generator`
- Pulizia completa: `docker system prune -a`

## Funzionamento del programma

### Architettura del Software
1. **Generazione chiavi crittografiche**: Utilizzo della curva ellittica secp256k1 per generare coppie di chiavi ECDSA
2. **Derivazione indirizzi**: Conversione della chiave pubblica in formato Bitcoin (SHA-256 + RIPEMD-160 + Base58Check)
3. **Motore di ricerca parallelo**: Implementazione multithreading per sfruttare tutti i core CPU disponibili
4. **Gestione degli errori**: Controlli su input utente e gestione delle eccezioni

### Algoritmo Principale
1. Genera una chiave privata casuale (32 byte)
2. Calcola la chiave pubblica corrispondente
3. Deriva l'indirizzo Bitcoin (formato P2PKH)
4. Verifica se l'indirizzo contiene il prefisso richiesto
5. Ripete il processo in parallelo su tutti i core selezionati


### Ottimizzazioni C++
- **Parallelismo avanzato**: Utilizzo di std::async per task asincroni
- **Gestione memoria**: Utilizzo di smart pointer e allocazione stack
- **Crittografia efficiente**: Libreria OpenSSL ottimizzata per operazioni ECDSA
- **Contatori atomici**: Variabili atomiche per statistiche in tempo reale
- **Compilazione**: Ottimizzazioni -O3 e link-time optimization

## Licenza

Questo progetto è rilasciato sotto licenza MIT.