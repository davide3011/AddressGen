"""Vanity Address Generator - Genera indirizzi Bitcoin con pattern personalizzati"""

import secrets
import hashlib
import ecdsa
import base58
import json
import time
import sys

# Charset per Bech32
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
# Charset per Base58
BASE58_CHARS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def increment_private_key(private_key_hex):
    """Incrementa di 1 il valore della chiave privata"""
    private_key_int = int(private_key_hex, 16)
    private_key_int = (private_key_int + 1) % (2**256)
    return format(private_key_int, '064x')

def generate_p2pkh_address(compressed=True, private_key_hex=None):
    """Genera un indirizzo P2PKH da una chiave privata"""
    # Generazione o utilizzo della chiave privata
    if private_key_hex is None:
        private_key = secrets.token_bytes(32)
        private_key_hex = private_key.hex()
    else:
        private_key = bytes.fromhex(private_key_hex)

    # Calcolo della chiave pubblica
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    pubkey_bytes = vk.to_string()

    # Formattazione della chiave pubblica (compressa o non compressa)
    if compressed:
        x = pubkey_bytes[:32]
        y = pubkey_bytes[32:]
        prefix = b'\x02' if int.from_bytes(y, 'big') % 2 == 0 else b'\x03'
        public_key = prefix + x
    else:
        public_key = b'\x04' + pubkey_bytes

    public_key_hex = public_key.hex()

    # Calcolo dell'hash della chiave pubblica
    sha256_pubkey = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_pubkey)
    pubkey_hash = ripemd160.digest()

    # Creazione dell'indirizzo
    payload = b'\x00' + pubkey_hash
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    address = base58.b58encode(payload + checksum).decode()

    return private_key_hex, public_key_hex, address

# Funzioni Bech32 per P2WPKH
def bech32_polymod(values):
    chk = 1
    for v in values:
        b = chk >> 25
        chk = ((chk & 0x1ffffff) << 5) ^ v
        if b & 1: chk ^= 0x3b6a57b2
        if b & 2: chk ^= 0x26508e6d
        if b & 4: chk ^= 0x1ea119fa
        if b & 8: chk ^= 0x3d4233dd
        if b & 16: chk ^= 0x2a1462b3
    return chk

def bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]

def bech32_create_checksum(hrp, data):
    values = bech32_hrp_expand(hrp) + data
    polymod_val = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod_val >> 5 * (5 - i)) & 31 for i in range(6)]

def bech32_encode(hrp, data):
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + '1' + ''.join([CHARSET[d] for d in combined])

def convertbits(data, frombits, tobits, pad=True):
    """Converti una serie di valori da una base di bits a un'altra"""
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    for b in data:
        if b < 0 or b >> frombits:
            return None
        acc = (acc << frombits) | b
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad and bits:
        ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret

def generate_p2wpkh_address(private_key_hex=None):
    """Genera un indirizzo P2WPKH (Bech32) da una chiave privata"""
    # Generazione o utilizzo della chiave privata
    if private_key_hex is None:
        private_key = secrets.token_bytes(32)
        private_key_hex = private_key.hex()
    else:
        private_key = bytes.fromhex(private_key_hex)

    # Calcolo della chiave pubblica (sempre compressa per P2WPKH)
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    pubkey_bytes = vk.to_string()

    # Costruzione della chiave pubblica compressa
    x = pubkey_bytes[:32]
    y = pubkey_bytes[32:]
    prefix = b'\x02' if int.from_bytes(y, 'big') % 2 == 0 else b'\x03'
    public_key = prefix + x
    public_key_hex = public_key.hex()

    # Calcolo dell'hash della chiave pubblica
    sha256_pubkey = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_pubkey)
    pubkey_hash = ripemd160.digest()

    # Creazione dell'indirizzo Bech32
    hrp = "bc"
    converted = convertbits(list(pubkey_hash), 8, 5)
    if converted is None:
        raise ValueError("Errore nella conversione dei bits per Bech32")
    data = [0] + converted  # 0 = witness version
    address = bech32_encode(hrp, data)

    return private_key_hex, public_key_hex, address

def main():
    print("Generatore di Vanity Address")
    print("=============================\n")
    
    # Scelta del tipo di indirizzo
    while True:
        tipo = input("Seleziona il tipo di indirizzo (P2PKH o P2WPKH): ").strip().upper()
        if tipo in ["P2PKH", "P2WPKH"]:
            break
        print("Tipo di indirizzo non valido. Scegli tra P2PKH o P2WPKH.")
    
    # Per P2PKH, chiedi se usare chiavi compresse o non compresse
    compressed = True
    if tipo == "P2PKH":
        while True:
            compressed_input = input("Vuoi usare chiavi compresse? (s/n): ").strip().lower()
            if compressed_input in ["s", "si"]:
                break
            elif compressed_input in ["n", "no"]:
                compressed = False
                break
            print("Input non valido. Inserisci 's' per sì o 'n' per no.")

    # Input del pattern da cercare
    while True:
        pattern = input("Inserisci il pattern che l'indirizzo deve contenere: ").strip()
        if not pattern:
            print("Il pattern non può essere vuoto. Inserisci almeno un carattere.")
            continue
            
        # Controllo validità dei caratteri
        valid_chars = BASE58_CHARS if tipo == "P2PKH" else CHARSET
        invalid_chars = [c for c in pattern if c not in valid_chars]
        if invalid_chars:
            print(f"Caratteri non validi per indirizzo {tipo}: {''.join(invalid_chars)}")
            print(f"Caratteri validi: {valid_chars}")
            continue
        break

    # Posizione del pattern
    while True:
        posizione_input = input("Vuoi che il pattern sia all'inizio (digita 'inizio') o presente ovunque (digita 'ovunque')? ").strip().lower()
        if posizione_input in ["inizio", "ovunque"]:
            break
        print("Valore non valido per la posizione. Inserisci 'inizio' o 'ovunque'.")
        
    # Case sensitivity - solo per P2PKH, poiché P2WPKH usa solo minuscole
    case_sensitive = False  # Default per P2WPKH
    if tipo == "P2PKH":
        while True:
            case_sensitive_input = input("Vuoi che la ricerca rispetti maiuscole/minuscole come inserite? (s/n): ").strip().lower()
            if case_sensitive_input in ["s", "si", "sì"]:
                case_sensitive = True
                break
            elif case_sensitive_input in ["n", "no"]:
                case_sensitive = False
                break
            print("Input non valido. Inserisci 's' per sì o 'n' per no.")

    print("\nRicerca in corso... premi CTRL+C per interrompere")
    
    count = 0
    start_time = time.time()
    last_private_key = None
    try:
        while True:
            count += 1

            # Genera indirizzo
            if count == 1:
                # Prima generazione: chiave casuale
                if tipo == "P2PKH":
                    priv_hex, pub_hex, address = generate_p2pkh_address(compressed=compressed)
                else:
                    priv_hex, pub_hex, address = generate_p2wpkh_address()
                last_private_key = priv_hex
            else:
                # Generazioni successive: incrementa la chiave precedente
                last_private_key = increment_private_key(last_private_key)
                if tipo == "P2PKH":
                    priv_hex, pub_hex, address = generate_p2pkh_address(compressed=compressed, private_key_hex=last_private_key)
                else:
                    priv_hex, pub_hex, address = generate_p2wpkh_address(private_key_hex=last_private_key)

            # Prepara le stringhe per il confronto
            if not case_sensitive:
                address_to_check = address.lower()
                pattern_to_check = pattern.lower()
            else:
                address_to_check = address
                pattern_to_check = pattern
                
            # Verifica se l'indirizzo soddisfa il criterio
            match_found = (address_to_check.startswith(pattern_to_check) if posizione_input == "inizio" 
                          else pattern_to_check in address_to_check)

            # Aggiorna lo stato ogni 5k tentativi
            if count % 5000 == 0:
                sys.stdout.write(f"\rTentativi: {count}  -  Ultimo indirizzo generato: {address}")
                sys.stdout.flush()

            # Se l'indirizzo soddisfa il criterio, interrompi la ricerca
            if match_found:
                elapsed = time.time() - start_time
                print(f"\n\nTrovato dopo {count} tentativi in {elapsed:.2f} secondi!")
                print("Indirizzo:", address)
                print("Chiave privata (hex):", priv_hex)
                print("Chiave pubblica (hex):", pub_hex)
                break

    except KeyboardInterrupt:
        print("\nRicerca interrotta dall'utente.")
        return

    # Salvataggio risultati
    while True:
        file_name = input("\nInserisci il nome del file (senza estensione) in cui salvare i dati: ").strip()
        if file_name:
            break
        print("Il nome del file non può essere vuoto. Inserisci un nome valido.")
    
    if not file_name.endswith(".json"):
        file_name += ".json"

    # Costruisce il dizionario dei risultati
    result = {
        'type': tipo,
        'vanity_pattern': pattern,
        'position_requirement': posizione_input,
        'case_sensitive': case_sensitive,
        'attempts': count,
        'time_seconds': elapsed,
        'address': address,
        'private_key_hex': priv_hex,
        'public_key_hex': pub_hex
    }

    # Salvataggio dei risultati
    try:
        with open(file_name, 'w') as f:
            json.dump(result, f, indent=4)
        print(f"Dati salvati correttamente nel file: {file_name}")
    except Exception as e:
        print("Errore durante il salvataggio del file:", e)

if __name__ == '__main__':
    main()
