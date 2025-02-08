import secrets
import hashlib
import json
import ecdsa
import base58
from bech32 import bech32_encode, convertbits
import tkinter as tk
from tkinter import messagebox

def generate_segwit_address(network: str = 'mainnet') -> dict:
    """
    Genera:
      - chiave privata in formato hex,
      - chiave privata in formato WIF,
      - chiave pubblica compressa in formato hex,
      - indirizzo segwit bech32.
      
    Parametro network: 'mainnet', 'testnet' o 'regtest'
    """
    # Genera la chiave privata (32 byte)
    private_key = secrets.token_bytes(32)
    private_key_hex = private_key.hex()

    # Genera la chiave pubblica compressa utilizzando ECDSA e la curva SECP256k1
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    pubkey_bytes = vk.to_string()  # 64 byte (non compresso)
    x = pubkey_bytes[:32]
    y = pubkey_bytes[32:]
    prefix = b'\x02' if int.from_bytes(y, 'big') % 2 == 0 else b'\x03'
    pubkey_compressed = prefix + x
    pubkey_hex = pubkey_compressed.hex()

    # Calcola HASH160 della chiave pubblica compressa (SHA256 -> RIPEMD160)
    sha256_pubkey = hashlib.sha256(pubkey_compressed).digest()
    ripemd160 = hashlib.new('ripemd160', sha256_pubkey).digest()

    # Crea l'indirizzo segwit bech32 (P2WPKH)
    converted = convertbits(list(ripemd160), 8, 5)
    if converted is None:
        raise ValueError("Errore nella conversione dei bit per la codifica Bech32")
    data = [0] + converted  # witness version = 0
    hrp = {'mainnet': 'bc', 'testnet': 'tb', 'regtest': 'bcrt'}.get(network)
    if hrp is None:
        raise ValueError("Network non supportato. Scegli tra 'mainnet', 'testnet' o 'regtest'.")
    address = bech32_encode(hrp, data)

    # Crea la rappresentazione WIF della chiave privata
    wif_prefix = b'\x80' if network == 'mainnet' else b'\xEF'
    extended_key = wif_prefix + private_key + b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
    wif = base58.b58encode(extended_key + checksum).decode('utf-8')

    return {
        'private_key_hex': private_key_hex,
        'wif': wif,
        'public_key_hex': pubkey_hex,
        'address': address,
        'network': network
    }
    
# --- Definizione dell'interfaccia grafica con tkinter ---
class SegwitGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generatore Indirizzi SegWit")
        self.resizable(False, False)
        
        # Variabile per memorizzare i dati generati
        self.generated_data = None

        # --- Sezione Network ---
        tk.Label(self, text="Seleziona il tipo di rete:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.network_var = tk.StringVar(value="mainnet")
        # Radiobutton in colonna
        tk.Radiobutton(self, text="Mainnet", variable=self.network_var, value="mainnet") \
            .grid(row=1, column=0, padx=5, pady=2, sticky="w")
        tk.Radiobutton(self, text="Testnet", variable=self.network_var, value="testnet") \
            .grid(row=2, column=0, padx=5, pady=2, sticky="w")
        tk.Radiobutton(self, text="Regtest", variable=self.network_var, value="regtest") \
            .grid(row=3, column=0, padx=5, pady=2, sticky="w")
        
        # --- Sezione Nome file ---
        tk.Label(self, text="Nome file JSON (senza estensione):") \
            .grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.file_entry = tk.Entry(self, width=30)
        self.file_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")
        self.file_entry.insert(0, "")
        
        # --- Pulsanti ---
        self.gen_button = tk.Button(self, text="Genera Indirizzo", command=self.generate_address)
        self.gen_button.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.save_button = tk.Button(self, text="Salva in JSON", command=self.save_json)
        self.save_button.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        
        # --- Area di testo per i risultati ---
        self.result_text = tk.Text(self, height=10, width=80)
        self.result_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
    
    def generate_address(self):
        network = self.network_var.get()
        try:
            result = generate_segwit_address(network)
            self.generated_data = result  # Salva i dati generati per l'eventuale salvataggio
            text = (
                f"Network: {result['network']}\n"
                f"Chiave privata (hex): {result['private_key_hex']}\n"
                f"Chiave privata (WIF): {result['wif']}\n"
                f"Chiave pubblica (compressa, hex): {result['public_key_hex']}\n"
                f"Indirizzo segwit bech32: {result['address']}\n"
            )
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella generazione: {e}")
    
    def save_json(self):
        if self.generated_data is None:
            messagebox.showerror("Errore", "Non ci sono dati generati da salvare. Genera prima un indirizzo.")
            return
        filename = self.file_entry.get().strip()
        if not filename:
            filename = ""
        if not filename.endswith(".json"):
            filename += ".json"
        try:
            with open(filename, 'w') as f:
                json.dump(self.generated_data, f, indent=4)
            messagebox.showinfo("Salvataggio", f"Dati salvati nel file: {filename}")
        except Exception as e:
            messagebox.showerror("Errore di Salvataggio", f"Errore nel salvataggio: {e}")

if __name__ == "__main__":
    app = SegwitGUI()
    app.mainloop()
