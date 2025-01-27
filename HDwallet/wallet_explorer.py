import hashlib
import base58
import json
import requests
from bip_utils import (
    Bip39MnemonicValidator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
    Bip32Slip10Secp256k1
)

def private_key_to_wif(private_key: str, network: str = "mainnet", compressed: bool = True) -> str:
    prefix = b'\x80' if network == "mainnet" else b'\xef'
    private_key_bytes = bytes.fromhex(private_key)
    extended_key = prefix + private_key_bytes + (b'\x01' if compressed else b'')
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
    return base58.b58encode(extended_key + checksum).decode()

def fetch_address_info(address: str, network: str) -> dict:
    # Fix: Usa il percorso corretto per mainnet/testnet4
    if network == "testnet4":
        base_url = "https://mempool.space/testnet4"
    else:
        base_url = "https://mempool.space" if network == "mainnet" else "https://mempool.space"
    
    try:
        response = requests.get(f"{base_url}/api/address/{address}", timeout=15)
        return response.json() if response.status_code == 200 else {}
    except requests.RequestException:
        return {}

def input_seed_phrase():
    while True:
        seed_phrase = input("Inserisci la tua seed phrase (12, 18 o 24 parole): ").strip()
        try:
            Bip39MnemonicValidator().Validate(seed_phrase)
            return seed_phrase
        except ValueError as e:
            print(f"Errore: {e}. Riprova.")

def generate_hd_wallet_from_seed(seed_phrase: str):
    passphrase = input("Passphrase (premi Invio per vuoto): ").strip()
    bip39_seed = Bip39SeedGenerator(seed_phrase).Generate(passphrase)
    
    # Scelta rete con controllo input
    while True:
        network_choice = input("\n1. Mainnet\n2. Testnet\nScelta (1/2): ").strip()
        if network_choice in ("1", "2"):
            break
        print("Scelta non valida. Inserire 1 o 2")
    
    network_name = "mainnet" if network_choice == "1" else "testnet4"
    coin_type = Bip44Coins.BITCOIN if network_choice == "1" else Bip44Coins.BITCOIN_TESTNET
    
    # Genera indirizzi
    bip44_ctx = Bip44.FromSeed(bip39_seed, coin_type)
    bip44_address_ctx = bip44_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
    
    num_addr = int(input("\nQuanti indirizzi generare? (Default: 10): ").strip() or 10)
    
    total_confirmed = 0
    total_pending = 0
    addresses = []

    print(f"\n{' INDIRIZZI ':=^70}")
    for i in range(num_addr):
        address_ctx = bip44_address_ctx.AddressIndex(i)
        address = address_ctx.PublicKey().ToAddress()
        info = fetch_address_info(address, network_name)
        
        # Calcolo saldi con gestione errori
        try:
            confirmed = info.get('chain_stats', {})
            pending = info.get('mempool_stats', {})
            
            confirmed_satoshi = confirmed.get('funded_txo_sum', 0) - confirmed.get('spent_txo_sum', 0)
            pending_satoshi = pending.get('funded_txo_sum', 0) - pending.get('spent_txo_sum', 0)
        except Exception as e:
            print(f"Errore nel calcolo saldo per {address}: {str(e)}")
            confirmed_satoshi = pending_satoshi = 0

        total_satoshi = confirmed_satoshi + pending_satoshi
        
        # Converti in BTC
        confirmed_btc = confirmed_satoshi / 10**8
        pending_btc = pending_satoshi / 10**8
        total_btc = total_satoshi / 10**8
        
        # Aggiorna totali
        total_confirmed += confirmed_satoshi
        total_pending += pending_satoshi
        
        # Aggiungi indirizzo
        addresses.append({
            "Index": i + 1,
            "Address": address,
            "Private_Key": {
                "Hex": address_ctx.PrivateKey().Raw().ToHex(),
                "WIF": private_key_to_wif(address_ctx.PrivateKey().Raw().ToHex(), network_name)
            },
            "Public_Key": address_ctx.PublicKey().RawCompressed().ToHex(),
            "Balance": {
                "confirmed": confirmed_btc,
                "pending": pending_btc,
                "total": total_btc
            },
            "Balance_satoshi": {
                "confirmed": confirmed_satoshi,
                "pending": pending_satoshi,
                "total": total_satoshi
            }
        })

        # Stampa formattata
        print(f"{i+1:>3}. {address}")
        print(f"   Confermati: {confirmed_btc:.8f} ₿")
        print(f"   In pending: {pending_btc:.8f} ₿")
        print(f"   Totale:     {total_btc:.8f} ₿\n")

    # Calcola totali finali
    total_confirmed_btc = total_confirmed / 10**8
    total_pending_btc = total_pending / 10**8
    total_total_btc = (total_confirmed + total_pending) / 10**8

    print(f"\n{' RIEPILOGO ':=^70}")
    print(f"{'Rete:':<15} {network_name.upper()}")
    print(f"{'Saldo confermato:':<15} {total_confirmed_btc:.8f} ₿")
    print(f"{'Saldo in pending:':<15} {total_pending_btc:.8f} ₿")
    print(f"{'Saldo totale:':<15} {total_total_btc:.8f} ₿")

    # Salva in JSON
    wallet_name = input("\nNome file per salvare (senza estensione): ").strip() + ".json"
    with open(wallet_name, "w") as f:
        json.dump({
            "network": network_name,
            "seed": seed_phrase,
            "passphrase": passphrase or None,
            "derivation_path": f"m/44'/{(0 if network_choice == '1' else 1)}'/0'/0",
            "total_balances": {
                "confirmed": total_confirmed_btc,
                "pending": total_pending_btc,
                "total": total_total_btc
            },
            "addresses": addresses
        }, f, indent=4, default=lambda o: str(o) if not isinstance(o, (int, float, str, bool, type(None))) else o)
    
    print(f"\nDati salvati in {wallet_name}")

if __name__ == "__main__":
    print("\n=== Generatore HD Wallet da Seed Phrase ===")
    generate_hd_wallet_from_seed(input_seed_phrase())
