import os
import hashlib
import base58
import ecdsa
import bech32

def generate_private_key():
    return os.urandom(32).hex()

def private_key_to_wif(private_key_hex, network='mainnet'):
    private_key_bytes = bytes.fromhex(private_key_hex)
    version = {'mainnet': b'\x80', 'testnet': b'\xef', 'regtest': b'\xef'}[network]
    extended = version + private_key_bytes + b'\x01'  # Compression flag
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return base58.b58encode(extended + checksum).decode('utf-8')

def private_key_to_p2pkh_address(private_key_hex, network='mainnet'):
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    x = vk.pubkey.point.x()
    y = vk.pubkey.point.y()
    compressed_pubkey = bytes([0x02 + (y % 2)]) + x.to_bytes(32, 'big')

    sha256 = hashlib.sha256(compressed_pubkey).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256)
    hash160 = ripemd160.digest()

    # Prefissi per indirizzi P2PKH
    prefix_map = {'mainnet': b'\x00', 'testnet': b'\x6f', 'regtest': b'\x6f'}
    prefix = prefix_map[network]
    
    # Aggiungi il prefisso all'hash160
    extended_hash = prefix + hash160
    
    # Calcola il checksum
    checksum = hashlib.sha256(hashlib.sha256(extended_hash).digest()).digest()[:4]
    
    # Codifica in Base58Check
    address = base58.b58encode(extended_hash + checksum).decode('utf-8')

    return address, compressed_pubkey.hex()

def generate_address(network):
    if network not in ['mainnet', 'testnet', 'regtest']:
        return {'error': 'Invalid network'}

    private_key_hex = generate_private_key()
    address, public_key = private_key_to_p2pkh_address(private_key_hex, network)
    wif = private_key_to_wif(private_key_hex, network)

    return {
        'address': address,
        'private_key_hex': private_key_hex,
        'private_key_wif': wif,
        'public_key': public_key,
        'network': network,
        'type': 'P2PKH'
    }
