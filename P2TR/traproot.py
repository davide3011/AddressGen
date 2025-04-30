#!/usr/bin/env python3
"""
Generatore di indirizzi Bitcoin Taproot (P2TR)
Genera indirizzi Taproot per diverse reti (mainnet, testnet, regtest)
e salva il risultato in un file JSON.

Dipendenze:
    pip install coincurve
"""

import os
import json
import secrets
import hashlib
from typing import Dict, Tuple
import coincurve
import base58

# ----------------------------------------
# Bech32m encoding (BIP-350)
# ----------------------------------------
BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def bech32_polymod(values):
    generators = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        top = chk >> 25
        chk = ((chk & 0x1ffffff) << 5) ^ v
        for i in range(5):
            if (top >> i) & 1:
                chk ^= generators[i]
    return chk


def bech32_hrp_expand(hrp: str):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_create_checksum(hrp: str, data: bytes, spec: str = "bech32m") -> list:
    values = bech32_hrp_expand(hrp) + list(data) + [0, 0, 0, 0, 0, 0]
    if spec == "bech32m":
        const = 0x2bc830a3
    else:
        const = 1
    polymod = bech32_polymod(values) ^ const
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def bech32_encode(hrp: str, data: bytes, spec: str = "bech32m") -> str:
    combined = data + bytes(bech32_create_checksum(hrp, data, spec))
    return hrp + '1' + ''.join([BECH32_CHARSET[d] for d in combined])


def convertbits(data: bytes, from_bits: int, to_bits: int, pad: bool=True) -> list:
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << to_bits) - 1
    for b in data:
        acc = (acc << from_bits) | b
        bits += from_bits
        while bits >= to_bits:
            bits -= to_bits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (to_bits - bits)) & maxv)
    elif bits >= from_bits or ((acc << (to_bits - bits)) & maxv):
        raise ValueError("Invalid bits conversion")
    return ret

# ----------------------------------------
# Funzioni principali per Taproot
# ----------------------------------------

def generate_privkey() -> bytes:
    """Genera una chiave privata casuale di 32 byte"""
    return secrets.token_bytes(32)


def privkey_to_pubkey(privkey: bytes) -> bytes:
    """Deriva la chiave pubblica x-only (32 byte) da privata"""
    # coincurve restituisce pubkey compressa (33 byte)
    pub_compressed = coincurve.PrivateKey(privkey).public_key.format(compressed=True)
    # la parte x-only è pub_compressed[1:33]
    return pub_compressed[1:33]


def taproot_address(pubkey_xonly: bytes, network: str) -> str:
    """Costruisce un indirizzo Bech32m P2TR da chiave x-only"""
    # Witness version 1
    ver = 1
    program = pubkey_xonly
    # Convert to 5-bit array
    data = bytes([ver]) + bytes(convertbits(program, 8, 5))
    # HRP per le reti
    hrp_map = {'mainnet': 'bc', 'testnet': 'tb', 'regtest': 'bcrt'}
    hrp = hrp_map.get(network, 'bc')
    # Per witness version 1+, usare Bech32m
    return bech32_encode(hrp, data, spec="bech32m")


def privkey_to_wif(privkey: bytes, network: str) -> str:
    """Converte una chiave privata in formato WIF secondo la rete"""
    if network == 'mainnet':
        prefix = b'\x80'
    elif network == 'testnet' or network == 'regtest':
        prefix = b'\xef'
    else:
        prefix = b'\x80'
    extended = prefix + privkey
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    wif = base58.b58encode(extended + checksum)
    return wif.decode()


def generate_taproot_address_info(network: str) -> Dict[str, str]:
    """
    Genera chiave privata, chiave pubblica x-only e indirizzo P2TR per la rete indicata.
    """
    priv = generate_privkey()
    pub_xonly = privkey_to_pubkey(priv)
    addr = taproot_address(pub_xonly, network)
    wif = privkey_to_wif(priv, network)
    return {
        'private_key_hex': priv.hex(),
        'private_key_wif': wif,
        'public_key_xonly_hex': pub_xonly.hex(),
        'address': addr,
        'network': network
    }

# ----------------------------------------
# Funzioni I/O
# ----------------------------------------

def get_valid_network() -> str:
    """
    Chiede all'utente di selezionare una rete valida.
    """
    nets = list(taproot_address.__defaults__[1] if False else ['mainnet','testnet','regtest'])
    while True:
        choice = input(f"Seleziona la rete ({', '.join(nets)}): ").strip().lower()
        if choice in nets:
            return choice
        print(f"Rete non valida, scegli tra {', '.join(nets)}.")


def get_valid_filename(default: str = 'taproot_wallet') -> str:
    """
    Richiede un nome di file (senza estensione), restituisce nome con .json
    """
    name = input("Nome file output (senza estensione): ").strip()
    safe = ''.join(c for c in name if c.isalnum() or c in ('_','-')) or default
    return safe + '.json'


def save_to_json(data: Dict, filename: str) -> None:
    dirpath = os.path.dirname(filename)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filename,'w') as f:
        json.dump(data,f,indent=4)
    print(f"Dati salvati in {filename}")


def main():
    network = get_valid_network()
    info = generate_taproot_address_info(network)
    print("\n--- Risultato ---")
    print(f"Rete: {info['network']}")
    print(f"Chiave privata (hex): {info['private_key_hex']}")
    print(f"Chiave privata (WIF): {info['private_key_wif']}")
    print(f"Pubkey x-only (hex): {info['public_key_xonly_hex']}")
    print(f"Indirizzo P2TR: {info['address']}")
    fname = get_valid_filename()
    save_to_json(info, fname)

if __name__ == '__main__':
    main()