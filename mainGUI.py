import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import hashlib
import json
from ecdsa import SECP256k1, SigningKey
import base58

# Funzioni esistenti
def generate_private_key():
    return os.urandom(32)

def private_key_to_wif(private_key, compressed, network):
    prefix = b'\x80' if network == "mainnet" else b'\xef'
    extended_key = prefix + private_key
    if compressed:
        extended_key += b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
    wif = base58.b58encode(extended_key + checksum)
    return wif.decode()

def get_public_key(private_key, compressed):
    sk = SigningKey.from_string(private_key, curve=SECP256k1)
    vk = sk.verifying_key
    public_key = vk.pubkey.point
    x, y = public_key.x(), public_key.y()
    if compressed:
        prefix = b'\x02' if y % 2 == 0 else b'\x03'
        return prefix + x.to_bytes(32, byteorder='big')
    else:
        return b'\x04' + x.to_bytes(32, byteorder='big') + y.to_bytes(32, byteorder='big')

def hash_public_key(public_key):
    sha256 = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256)
    return ripemd160.digest()

def generate_address(public_key_hash, network):
    prefix = b'\x00' if network == "mainnet" else b'\x6f'
    payload = prefix + public_key_hash
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    address = base58.b58encode(payload + checksum)
    return address.decode()

def save_to_json(private_key, wif_key, public_key, address, filename="keys&address.json"):
    data = {
        "private_key_hex": private_key.hex(),
        "private_key_wif": wif_key,
        "public_key_hex": public_key.hex(),
        "address": address
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Funzione principale per generare le chiavi
def generate_keys():
    network = network_var.get()
    compressed = compressed_var.get()

    if network not in ["mainnet", "testnet"]:
        messagebox.showerror("Errore", "Seleziona una rete valida!")
        return

    try:
        private_key = generate_private_key()
        wif_key = private_key_to_wif(private_key, compressed, network)
        public_key = get_public_key(private_key, compressed)
        public_key_hash = hash_public_key(public_key)
        address = generate_address(public_key_hash, network)

        # Abilita la text box temporaneamente per aggiornare il contenuto
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)  # Cancella il contenuto precedente
        result_text.insert(tk.END, f"Chiave Privata (hex): {private_key.hex()}\n")
        result_text.insert(tk.END, f"Chiave Privata (WIF): {wif_key}\n")
        result_text.insert(tk.END, f"Chiave Pubblica (hex): {public_key.hex()}\n")
        result_text.insert(tk.END, f"Indirizzo: {address}\n")

        # Disabilita nuovamente la text box per impedire modifiche
        result_text.config(state="disabled")

        # Salva i risultati globalmente per il salvataggio in JSON
        global result_data
        result_data = {
            "private_key": private_key,
            "wif_key": wif_key,
            "public_key": public_key,
            "address": address
        }

    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {e}")

# Funzione per salvare i dati in JSON
def save_results():
    try:
        # Recupero il nome wallet dal campo di testo
        wallet_name = wallet_name_var.get().strip()

        if not wallet_name:
            messagebox.showerror("Errore", "Inserisci un nome per il wallet prima di salvare!")
            return

        # Creiamo il nome del file in base al wallet_name
        # Potresti aggiungere controlli su caratteri speciali, se vuoi
        filename = f"{wallet_name}.json"

        save_to_json(
            result_data["private_key"],
            result_data["wif_key"],
            result_data["public_key"],
            result_data["address"],
            filename=filename
        )
        messagebox.showinfo("Successo", f"Dati salvati in {filename}")
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile salvare i dati: {e}")

# Crea la finestra principale
root = tk.Tk()
root.title("Generatore di Chiavi Bitcoin")
root.geometry("800x450")

# Variabili per i parametri
network_var = tk.StringVar(value="mainnet")
compressed_var = tk.BooleanVar(value=True)


# Variabile per il nome wallet
wallet_name_var = tk.StringVar(value="")

# Crea un frame per la sezione "Rete"
frame_network = tk.Frame(root, padx=10, pady=10)
frame_network.grid(row=0, column=0, sticky="nsew")

# Sezione "Rete"
tk.Label(frame_network, text="Seleziona la rete:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", pady=10)
tk.Radiobutton(frame_network, text="Mainnet", variable=network_var, value="mainnet", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
tk.Radiobutton(frame_network, text="Testnet", variable=network_var, value="testnet", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)

# Crea un frame per la sezione "Formato chiave"
frame_format = tk.Frame(root, padx=10, pady=10)
frame_format.grid(row=0, column=1, sticky="nsew")

# Sezione "Formato chiave"
tk.Label(frame_format, text="Formato della chiave pubblica:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", pady=10)
tk.Radiobutton(frame_format, text="Compressa", variable=compressed_var, value=True, font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
tk.Radiobutton(frame_format, text="Non compressa", variable=compressed_var, value=False, font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)

# Aggiungi un frame per il nome del wallet
frame_wallet_name = tk.Frame(root, padx=10, pady=10)
frame_wallet_name.grid(row=1, column=0, columnspan=2, sticky="nsew")

tk.Label(frame_wallet_name, text="Nome Wallet:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5)
wallet_name_entry = tk.Entry(frame_wallet_name, textvariable=wallet_name_var, font=("Arial", 12), width=30)
wallet_name_entry.grid(row=0, column=1, sticky="w", padx=5)

# Pulsante per generare le chiavi
tk.Button(root, text="Genera Chiavi", command=generate_keys, font=("Arial", 12), width=20).grid(row=2, column=0, columnspan=2, pady=10)

# Text box per mostrare i risultati
result_text = scrolledtext.ScrolledText(root, height=10, width=90)
result_text.grid(row=3, column=0, columnspan=2, pady=10)

# Pulsante per salvare i dati in JSON
tk.Button(root, text="Salva i dati", command=save_results, font=("Arial", 12), width=20).grid(row=4, column=0, columnspan=2, pady=10)

# Configura la griglia per adattarsi dinamicamente
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(3, weight=1)

# Avvia il loop dell'interfaccia
root.mainloop()

