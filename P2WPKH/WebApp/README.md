# Bitcoin SegWit Address Generator

**Bitcoin SegWit Address Generator** è un'app web che permette di generare indirizzi Bitcoin **P2WPKH** (SegWit) per le reti **Mainnet, Testnet e Regtest**.

L'app è pensata per **test in locale**, ma può essere facilmente integrata in un sito web.


## **Caratteristiche**
- Generazione di indirizzi **P2WPKH** (Bech32) per **Mainnet, Testnet e Regtest**  
- Mostra chiave privata in formato HEX e WIF  
- Scaricamento della chiave privata come file JSON  
- Interfaccia dinamica con colori in base alla rete selezionata  


## **Installazione e Avvio in Locale**
1. **Clona il repository**

2. **Crea un ambiente virtuale e installa le dipendenze:**

```sh
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\Activate
pip install -r requirements.txt
```

**3. Avvia il server Flask:**

```sh
python app.py
```

**4. Apri il browser e vai su:**

```
http://127.0.0.1:5000
```

## Deployment su un Sito Web

### 1. Installa Python e le dipendenze
Su un server Linux (Ubuntu/Debian), esegui:

```sh
sudo apt update && sudo apt install python3 python3-venv python3-pip
```
Poi, crea l'ambiente virtuale e installa le dipendenze:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Avvia l'app in produzione con Gunicorn

Esegui Gunicorn per un'istanza più stabile:

```sh
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
Ora l'app è accessibile all'indirizzo IP del server sulla porta 5000.

Poi configura Nginx per servire l'app come servizio web.

### 3. Configura Nginx per servire l'app
Se vuoi rendere l'app accessibile su internet con un dominio, puoi configurare Nginx come proxy inverso.

Installa Nginx:

```sh
sudo apt install nginx
```

Poi crea un file di configurazione per il sito:

```sh
sudo nano /etc/nginx/sites-available/address-generator
```
Inserisci questa configurazione:

```nginx
server {
    listen 80;
    server_name tuo-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Salva e chiudi (CTRL + X, Y, Invio), poi abilita la configurazione:

```sh
sudo ln -s /etc/nginx/sites-available/address-generator /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

Ora l'app è accessibile su tuo-dominio.com o all'IP del server.

## Licenza
Questo progetto è rilasciato sotto licenza MIT.
