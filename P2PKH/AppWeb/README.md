# Bitcoin P2PKH Address Generator

**Bitcoin P2PKH Address Generator** è un'applicazione web che permette di generare indirizzi Bitcoin **P2PKH** (Legacy) per le reti **Mainnet, Testnet e Regtest**.

L'applicazione è sviluppata con Flask e può essere utilizzata sia in locale per scopi di test che integrata in un sito web.

## **Funzionalità**

- Generazione di indirizzi **P2PKH** (Legacy) per **Mainnet, Testnet e Regtest**
- Visualizzazione della chiave privata in formato HEX e WIF
- Esportazione della chiave privata come file JSON
- Interfaccia utente dinamica con colori differenti in base alla rete selezionata
- Interfaccia responsive adatta a dispositivi desktop e mobili

## **Come Funziona**

L'applicazione utilizza le seguenti librerie Python per generare indirizzi Bitcoin P2PKH:

- **ecdsa**: Per la generazione delle coppie di chiavi crittografiche
- **base58**: Per la codifica degli indirizzi P2PKH e delle chiavi private in formato WIF
- **hashlib**: Per le funzioni di hash SHA256 e RIPEMD160

Il processo di generazione degli indirizzi segue questi passaggi:

1. Generazione di una chiave privata casuale
2. Derivazione della chiave pubblica dalla chiave privata usando la curva ellittica SECP256k1
3. Compressione della chiave pubblica
4. Calcolo dell'hash SHA256 seguito da RIPEMD160 della chiave pubblica
5. Codifica dell'indirizzo in formato Base58Check con il prefisso appropriato per la rete selezionata

## **Installazione e Avvio in Locale**

1. **Clona il repository**

2. **Crea un ambiente virtuale e installa le dipendenze:**

```sh
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Avvia il server Flask:**

```sh
python app.py
```

4. **Apri il browser e vai su:**

```
http://127.0.0.1:5000
```

## **Deployment in Produzione**

### 1. Preparazione del Server

Su un server Linux (Ubuntu/Debian), esegui:

```sh
sudo apt update && sudo apt install python3 python3-venv python3-pip nginx
```

Clona il repository e configura l'ambiente Python:

```sh
git clone <url-repository>
cd <directory-repository>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurazione di Gunicorn

Gunicorn è un server WSGI HTTP per Python, più robusto di Flask per ambienti di produzione.

Installa Gunicorn (già incluso in requirements.txt):

```sh
pip install gunicorn
```

Per testare che Gunicorn funzioni correttamente:

```sh
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

Dove:
- `-w 4`: Avvia 4 worker processes
- `-b 127.0.0.1:5000`: Bind all'indirizzo locale sulla porta 5000
- `app:app`: Il primo "app" è il nome del file Python, il secondo è l'oggetto Flask

### 3. Configurazione di Nginx come Proxy Inverso

Nginx fungerà da proxy inverso, gestendo le connessioni client e inoltrando le richieste a Gunicorn.

Crea un file di configurazione per Nginx:

```sh
sudo nano /etc/nginx/sites-available/address-generator
```

Inserisci questa configurazione di base:

```nginx
server {
    listen 80;
    server_name tuo-dominio.com;  # Sostituisci con il tuo dominio o indirizzo IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/app/static;  # Sostituisci con il percorso assoluto alla cartella static
        expires 30d;
    }
}
```

Attiva la configurazione e riavvia Nginx:

```sh
sudo ln -s /etc/nginx/sites-available/address-generator /etc/nginx/sites-enabled/
sudo nginx -t  # Verifica la configurazione
sudo systemctl restart nginx
```

### 4. Configurazione di Gunicorn come Servizio Systemd

Per garantire che Gunicorn si avvii automaticamente all'avvio del server e si riavvii in caso di errori, crea un servizio systemd:

```sh
sudo nano /etc/systemd/system/address-generator.service
```

Inserisci questa configurazione:

```ini
[Unit]
Description=Gunicorn instance to serve Bitcoin P2PKH Address Generator
After=network.target

[Service]
User=<tuo-utente>  # Sostituisci con il tuo nome utente
Group=www-data
WorkingDirectory=/path/to/your/app  # Percorso assoluto alla directory dell'app
Environment="PATH=/path/to/your/app/venv/bin"  # Percorso all'ambiente virtuale
ExecStart=/path/to/your/app/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Attiva e avvia il servizio:

```sh
sudo systemctl enable address-generator
sudo systemctl start address-generator
sudo systemctl status address-generator  # Verifica lo stato
```

### 5. Configurazione HTTPS (Opzionale ma Raccomandata)

Per abilitare HTTPS con Let's Encrypt:

```sh
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tuo-dominio.com
```

Segui le istruzioni a schermo per completare la configurazione HTTPS.

## **Personalizzazione**

- Per disattivare il pulsante "Torna Indietro", modifica la variabile `SHOW_BACK_BUTTON` in `app.py` impostandola a `False`
- Per personalizzare l'aspetto dell'interfaccia, modifica i file CSS nella cartella `static`

## **Sicurezza**

Questa applicazione è pensata principalmente per scopi educativi e di test. Se utilizzata in produzione, considera che:

- Le chiavi private generate sono visualizzate nel browser
- Non c'è autenticazione o protezione degli endpoint
- È consigliabile implementare HTTPS per proteggere la comunicazione

## **Licenza**

Questo progetto è rilasciato sotto licenza MIT.
