# HD WALLET

# generazione seed phrase BIP39
# possibilità di scelta entropia seed (12 - 18 - 24 parole)
# scelta o no di aggiugere passphrase
# scelta rete (mainnet - testnet)
# chiavi privata master, pubblica master e chain code BIP32 (root Key BIP32)
# derivation path BIP32
# extended private key, extended public key BIP44
# generazione di n indirizzi a scelta (con chiavi)

# da aggiungere:
# implementazione per electrum (m/84'/0'0')
# scrivere il codice con meno librerie (vederle su GitHub)

import hashlib
import base58
import json
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip32Slip10Secp256k1, Bip44, Bip44Coins, Bip44Changes

def private_key_to_wif(private_key: str, network: str = "mainnet", compressed: bool = True) -> str:
    """
    Converte una chiave privata raw in formato WIF.

    Args:
        private_key (str): Chiave privata in formato esadecimale.
        network (str): Rete ("mainnet" o "testnet").
        compressed (bool): Se la chiave pubblica associata è compressa.

    Returns:
        str: Chiave privata in formato WIF.
    """
    # Aggiungi il prefisso in base alla rete
    if network == "mainnet":
        prefix = b'\x80'  # Mainnet
    elif network == "testnet":
        prefix = b'\xef'  # Testnet
    else:
        raise ValueError("Rete non valida. Usa 'mainnet' o 'testnet'.")

    # Concatena prefisso e chiave privata
    private_key_bytes = bytes.fromhex(private_key)
    if compressed:
        extended_key = prefix + private_key_bytes + b'\x01'
    else:
        extended_key = prefix + private_key_bytes

    # Calcola il checksum
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]

    # Concatena e codifica in Base58
    wif = base58.b58encode(extended_key + checksum).decode()
    return wif
    
def generate_hd_wallet():
    # Scegli la lunghezza della frase mnemonica
    print("Scegli la lunghezza della frase mnemonica:")
    print("1. 12 parole (128 bit)")
    print("2. 18 parole (192 bit)")
    print("3. 24 parole (256 bit)")
    choice = input("Inserisci il numero corrispondente alla scelta (1/2/3): ").strip()
    
    words_number = {"1": 12, "2": 18, "3": 24}.get(choice, 12)  # Default a 12 parole
    mnemonic_obj = Bip39MnemonicGenerator().FromWordsNumber(words_number)
    mnemonic = mnemonic_obj.ToStr()  # Converte l'oggetto in stringa
    print(f"\nFrase mnemonica generata ({words_number} parole): {mnemonic}\n")

    # Inserisci una passphrase opzionale
    passphrase = input("Inserisci una passphrase (premi Invio per lasciare vuoto): ").strip()
     
    # Genera il seed BIP39 dalla frase mnemonica
    seed_generator = Bip39SeedGenerator(mnemonic)
    bip39_seed = seed_generator.Generate(passphrase)
    print(f"\nBIP39 Seed: {bip39_seed.hex()}\n")
    
    # Scegli la rete (mainnet o testnet)
    print("Scegli la rete per gli indirizzi:")
    print("1. Mainnet (Bitcoin)")
    print("2. Testnet (Bitcoin Test Network)")
    network_choice = input("Inserisci il numero corrispondente alla rete (1/2): ").strip()
    network = Bip44Coins.BITCOIN if network_choice == "1" else Bip44Coins.BITCOIN_TESTNET
    network_name = "Mainnet" if network_choice == "1" else "Testnet"
    print(f"\nHai scelto la rete: {network_name}\n")

    # Genera la chiave root BIP32
    bip32_ctx = Bip32Slip10Secp256k1.FromSeed(bip39_seed)
    bip32_root_key = bip32_ctx.PrivateKey().ToExtended()
    print(f"BIP32 Root Key: {bip32_root_key}\n")

    # Deriva le chiavi usando il percorso BIP44: m/44'/0'/0'
    bip44_ctx = Bip44.FromSeed(bip39_seed, network)
    bip44_account = bip44_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
    derivation_path = "m/44'/0'/0'/0" if network_choice == "1" else "m/44'/1'/0'/0"
    print(f"BIP32 Derivation Path: {derivation_path}\n")
    
    # Genera gli indirizzi con relative chiavi
    num_addresses = int(input("Quanti indirizzi vuoi generare? (Default: 10): ").strip() or 10)
    addresses = []

    print("\nIndirizzi generati:\n")
    for i in range(num_addresses):
        address_ctx = bip44_account.AddressIndex(i)
        private_key_raw = address_ctx.PrivateKey().Raw().ToHex()
        private_key_wif = private_key_to_wif(private_key_raw, network_name.lower(), compressed=True)

        address_data = {
            "Index": i + 1,
            "Address": address_ctx.PublicKey().ToAddress(),
            "Private Key (Hex)": private_key_raw,
            "Private Key (WIF)": private_key_wif,
            "Public Key": address_ctx.PublicKey().RawCompressed().ToHex()
        }
        addresses.append(address_data)
        print(f"Indirizzo {i + 1}:")
        print(f"  Address: {address_data['Address']}")
        print(f"  Private Key (Hex): {address_data['Private Key (Hex)']}")
        print(f"  Private Key (WIF): {address_data['Private Key (WIF)']}")
        print(f"  Public Key: {address_data['Public Key']}\n")

    # Chiedi il nome del file JSON
    wallet_name = input("Inserisci il nome del wallet (esempio: mio_wallet): ").strip()
    if not wallet_name.endswith(".json"):
        wallet_name += ".json"

    # Struttura i dati per il salvataggio
    wallet_data = {
        "Network": network_name,
        "Seed": mnemonic,
        "Passphrase": passphrase if passphrase else "None",
        "BIP39_Seed": bip39_seed.hex(),
        "BIP32_Root_Key": bip32_root_key,
        "BIP32_Derivation_Path": derivation_path,
        "Addresses": addresses
    }

    # Salva i dati in un file JSON
    save_to_json(wallet_data, wallet_name)
    
def save_to_json(data, filename):
    """Salva i dati in un file JSON."""
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"\nDati salvati in '{filename}'")

# Esegui il programma
if __name__ == "__main__":
    generate_hd_wallet()
