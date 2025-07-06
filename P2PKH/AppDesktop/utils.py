import os
import hashlib
import base58
import ecdsa
# bech32 non utilizzato, rimosso per semplificare

# Genera una chiave privata casuale di 32 byte
def generate_private_key():
    return os.urandom(32).hex()

# Converte chiave privata in formato WIF (Wallet Import Format)
def private_key_to_wif(private_key_hex, network='mainnet'):
    private_key_bytes = bytes.fromhex(private_key_hex)
    # Prefissi di rete per WIF
    version = {'mainnet': b'\x80', 'testnet': b'\xef', 'regtest': b'\xef'}[network]
    extended = version + private_key_bytes + b'\x01'  # Flag di compressione
    # Doppio SHA256 per il checksum
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return base58.b58encode(extended + checksum).decode('utf-8')

# Genera indirizzo P2PKH da chiave privata
def private_key_to_p2pkh_address(private_key_hex, network='mainnet'):
    # Crea chiave di firma ECDSA
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    
    # Genera chiave pubblica compressa
    x, y = vk.pubkey.point.x(), vk.pubkey.point.y()
    compressed_pubkey = bytes([0x02 + (y % 2)]) + x.to_bytes(32, 'big')

    # Hash160: SHA256 seguito da RIPEMD160
    hash160 = hashlib.new('ripemd160', hashlib.sha256(compressed_pubkey).digest()).digest()

    # Prefissi di rete per indirizzi P2PKH
    prefix = {'mainnet': b'\x00', 'testnet': b'\x6f', 'regtest': b'\x6f'}[network]
    extended_hash = prefix + hash160
    
    # Checksum: primi 4 byte del doppio SHA256
    checksum = hashlib.sha256(hashlib.sha256(extended_hash).digest()).digest()[:4]
    
    # Codifica finale in Base58Check
    address = base58.b58encode(extended_hash + checksum).decode('utf-8')
    return address, compressed_pubkey.hex()

# Funzione principale: genera un indirizzo Bitcoin completo
def generate_address(network):
    # Validazione della rete
    if network not in ['mainnet', 'testnet', 'regtest']:
        return {'error': 'Invalid network'}

    # Genera tutti i componenti dell'indirizzo
    private_key_hex = generate_private_key()
    address, public_key = private_key_to_p2pkh_address(private_key_hex, network)
    wif = private_key_to_wif(private_key_hex, network)

    # Restituisce tutti i dati in un dizionario
    return {
        'address': address,
        'private_key_hex': private_key_hex,
        'private_key_wif': wif,
        'public_key': public_key,
        'network': network,
        'type': 'P2PKH'
    }
