import secrets
import hashlib
import json
import ecdsa
import base58

def generate_p2pkh_address(network: str = 'mainnet') -> dict:
    """
    Genera:
      - chiave privata in formato hex,
      - chiave privata in formato WIF,
      - chiave pubblica compressa in formato hex,
      - indirizzo P2PKH in Base58Check.

    Parametro network: 'mainnet' o 'testnet'
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

    # Crea l'indirizzo P2PKH in Base58Check
    prefix = b'\x00' if network == 'mainnet' else b'\x6F'  # 0x00 per Mainnet, 0x6F per Testnet
    payload = prefix + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    address = base58.b58encode(payload + checksum).decode('utf-8')

    # Crea la rappresentazione WIF della chiave privata
    wif_prefix = b'\x80' if network == 'mainnet' else b'\xEF'
    extended_key = wif_prefix + private_key + b'\x01'  # Aggiungi il byte 0x01 per indicare chiave compressa
    checksum_wif = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
    wif = base58.b58encode(extended_key + checksum_wif).decode('utf-8')

    return {
        'private_key_hex': private_key_hex,
        'wif': wif,
        'public_key_hex': pubkey_hex,
        'address': address,
        'network': network
    }
    
if __name__ == '__main__':
    network = input("Seleziona il tipo di rete (mainnet, testnet): ").strip().lower()
    if network not in ['mainnet', 'testnet']:
        print("Errore: Devi scegliere tra 'mainnet' e 'testnet'.")
        exit(1)

    try:
        result = generate_p2pkh_address(network)
        print("\n--- Risultati ---")
        print("Chiave privata (hex):", result['private_key_hex'])
        print("Chiave privata (WIF):", result['wif'])
        print("Chiave pubblica (compressa, hex):", result['public_key_hex'])
        print("Indirizzo P2PKH:", result['address'])

        # Salvataggio automatico in un file JSON
        nome_file = input("\nInserisci il nome del file (senza estensione) per salvare i dati: ").strip()
        if not nome_file:
            nome_file = "dati"
            print("Nome del file non valido. Verrà utilizzato il nome di default: dati.json")
        if not nome_file.endswith('.json'):
            nome_file += '.json'
        with open(nome_file, 'w') as f:
            json.dump(result, f, indent=4)
        print(f"Dati salvati correttamente nel file: {nome_file}")
    except Exception as e:
        print("Errore:", e)    
