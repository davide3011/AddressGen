import os
import json
from ecdsa import SECP256k1

def generate_private_key():
    """Genera una chiave privata casuale di 256 bit."""
    return os.urandom(32)

def get_public_key(private_key):
    """Calcola la chiave pubblica in formato compresso e non compresso."""
    curve = SECP256k1
    generator = curve.generator

    private_key_int = int.from_bytes(private_key, byteorder='big')
    public_key_point = private_key_int * generator
    x, y = public_key_point.x(), public_key_point.y()

    # Formati della chiave pubblica
    public_key_uncompressed = b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')
    prefix = b'\x02' if y % 2 == 0 else b'\x03'
    public_key_compressed = prefix + x.to_bytes(32, 'big')

    return x, y, public_key_uncompressed, public_key_compressed

def create_key_data(private_key, private_key_int, x, y, pub_uncompressed, pub_compressed):
    """
    Crea il dizionario con i dati delle chiavi
    Restituisce:
        dict: struttura dati organizzata per il JSON
    """
    return {
        "private_key": {
            "hex": private_key.hex(),
            "decimal": str(private_key_int)
        },
        "public_key": {
            "uncompressed": pub_uncompressed.hex(),
            "compressed": pub_compressed.hex(),
            "x": x.to_bytes(32, 'big').hex(),
            "y": y.to_bytes(32, 'big').hex()
        }
    }

def save_to_json(data, filename):
    """
    Salva i dati in un file JSON
    Args:
        data (dict): dati da salvare
        filename (str): nome del file di output
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    # Generazione chiave privata
    private_key = generate_private_key()
    private_key_int = int.from_bytes(private_key, byteorder='big')
    
    # Recupero del punto generatore G
    curve = SECP256k1
    generator = curve.generator
    
    print("\nPunto Generatore (G):")
    print(f"x: {generator.x()}")
    print(f"y: {generator.y()}")

    # Stampa chiave privata
    print("\nChiave privata:")
    print(f"Formato esadecimale: {private_key.hex()}")
    print(f"Formato decimale: {private_key_int}")

    # Calcolo chiave pubblica
    x, y, pub_uncompressed, pub_compressed = get_public_key(private_key)

    print("\nCalcolo della chiave pubblica (P = k * G):")
    print(f"Coordinata x: {x}")
    print(f"Coordinata y: {y}")

    print("\nChiave pubblica (non compressa):", pub_uncompressed.hex())
    print("Chiave pubblica (compressa):", pub_compressed.hex())
    
    # Creazione e salvataggio JSON
    key_data = create_key_data(private_key, private_key_int, x, y, pub_uncompressed, pub_compressed)
    save_to_json(key_data, 'chiavi.json')
    
    print("\nFile chiavi.json creato con successo!")

if __name__ == "__main__":
    main()
