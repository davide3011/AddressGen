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

def private_key_to_p2wpkh_address(private_key_hex, network='mainnet'):
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    x = vk.pubkey.point.x()
    y = vk.pubkey.point.y()
    compressed_pubkey = bytes([0x02 + (y % 2)]) + x.to_bytes(32, 'big')

    sha256 = hashlib.sha256(compressed_pubkey).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256)
    hash160 = ripemd160.digest()

    hrp_map = {'mainnet': 'bc', 'testnet': 'tb', 'regtest': 'bcrt'}
    converted_bits = bech32.convertbits(hash160, 8, 5)
    address = bech32.bech32_encode(hrp_map[network], [0x00] + converted_bits)

    return address, compressed_pubkey.hex()

def generate_address(network):
    if network not in ['mainnet', 'testnet', 'regtest']:
        return {'error': 'Invalid network'}

    private_key_hex = generate_private_key()
    address, public_key = private_key_to_p2wpkh_address(private_key_hex, network)
    wif = private_key_to_wif(private_key_hex, network)

    return {
        'address': address,
        'private_key_hex': private_key_hex,
        'private_key_wif': wif,
        'public_key': public_key,
        'network': network,
        'type': 'P2WPKH'
    }
