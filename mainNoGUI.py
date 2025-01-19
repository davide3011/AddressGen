import os
import hashlib
import json
from ecdsa import SECP256k1, SigningKey
import base58

def generate_private_key():
    """
    Genera una chiave privata casuale di 256 bit.
    """
    return os.urandom(32)

def private_key_to_wif(private_key, compressed, network):
    """
    Converte una chiave privata in formato WIF.
    """
    # Aggiungi il prefisso di rete (0x80 per Mainnet, 0xef per Testnet)
    prefix = b'\x80' if network == "mainnet" else b'\xef'
    extended_key = prefix + private_key

    # Se la chiave è compressa, aggiungi il byte 0x01
    if compressed:
        extended_key += b'\x01'

    # Calcola il checksum (doppio SHA-256)
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]

    # Codifica in Base58Check
    wif = base58.b58encode(extended_key + checksum)
    return wif.decode()
    
def get_public_key(private_key, compressed):
    """
    Calcola la chiave pubblica dalla chiave privata utilizzando la curva secp256k1.
    Ritorna la chiave pubblica in formato compresso o non compresso.
    """
    sk = SigningKey.from_string(private_key, curve=SECP256k1)
    vk = sk.verifying_key
    public_key = vk.pubkey.point
    x, y = public_key.x(), public_key.y()

    if compressed:
        prefix = b'\x02' if y % 2 == 0 else b'\x03'
        public_key_compressed = prefix + x.to_bytes(32, byteorder='big')
        return public_key_compressed
    else:
        public_key_uncompressed = b'\x04' + x.to_bytes(32, byteorder='big') + y.to_bytes(32, byteorder='big')
        return public_key_uncompressed
        
def hash_public_key(public_key):
    """
    Applica SHA-256 seguito da RIPEMD-160 sulla chiave pubblica.
    """
    sha256 = hashlib.sha256(public_key).digest()
    print(f"Hash SHA-256 della chiave pubblica: {sha256.hex()}")

    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256)
    print(f"Hash RIPEMD-160 della chiave pubblica: {ripemd160.hexdigest()}")

    return ripemd160.digest()

def generate_address(public_key_hash, network):
    """
    Genera un indirizzo P2PKH utilizzando il public key hash e la rete scelta.
    """
    if network == "mainnet":
        prefix = b'\x00'
    elif network == "testnet":
        prefix = b'\x6f'
    else:
        raise ValueError("Rete non valida. Scegli 'mainnet' o 'testnet'.")

    payload = prefix + public_key_hash
    print(f"Payload (prefisso + public key hash): {payload.hex()}")

    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    print(f"Checksum: {checksum.hex()}")

    address = base58.b58encode(payload + checksum)
    return address.decode()

def save_to_json(private_key, wif_key, public_key, address, filename="keys&address.json"):
    """
    Salva i dettagli della chiave privata, chiave privata WIF, chiave pubblica e indirizzo in un file JSON.
    """
    data = {
        "private_key_hex": private_key.hex(),
        "private_key_wif": wif_key,
        "public_key_hex": public_key.hex(),
        "address": address
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Dati salvati in {filename}")

def main():
    # Scelta della rete
    network = input("\nSeleziona la rete (mainnet/testnet): ").strip().lower()

    # Scelta del formato (compresso o non compresso)
    compressed = input("\nUsare chiave pubblica compressa? (si/no): ").strip().lower() == "si"

    # Generazione della chiave privata
    private_key = generate_private_key()
    print(f"\nChiave privata generata (hex): {private_key.hex()}")

    # Calcolo della chiave privata in formato WIF
    if network not in ["mainnet", "testnet"]:
        print("Rete non valida. Usa 'mainnet' o 'testnet'.")
        return
    wif_key = private_key_to_wif(private_key, compressed, network)
    print(f"Chiave privata in formato WIF: {wif_key}")

    # Ricavo della chiave pubblica
    public_key = get_public_key(private_key, compressed)
    print(f"Chiave pubblica ({'compressa' if compressed else 'non compressa'}, hex): {public_key.hex()}")

    # Calcolo dell'indirizzo
    public_key_hash = hash_public_key(public_key)
    address = generate_address(public_key_hash, network)
    print(f"Indirizzo P2PKH ({network}): {address}\n")

    # Salvataggio dei dati in JSON
    save_to_json(private_key, wif_key, public_key, address)

if __name__ == "__main__":
    main()
