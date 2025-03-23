from flask import Flask, render_template, request, send_file, jsonify
from io import BytesIO
import json
import qrcode
from mnemonic import Mnemonic
from bip_utils import (
    Bip39SeedGenerator, Bip44, Bip84, Bip44Coins, Bip84Coins, Bip44Changes
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    addresses = []
    seed_phrase = ""
    wif = ""
    derivation_path = ""
    xprv = ""
    xpub = ""
    coin_type = None

    if request.method == "POST":
        addr_type = request.form["addr_type"]
        network = request.form["network"]
        count = int(request.form["count"])
        seed_length = int(request.form["seed_length"])

        # Mappa la lunghezza della seed phrase al valore di strength corrispondente
        # 12 parole = 128 bit, 15 parole = 160 bit, 18 parole = 192 bit, 21 parole = 224 bit, 24 parole = 256 bit
        strength_map = {
            12: 128,
            15: 160,
            18: 192,
            21: 224,
            24: 256
        }
        
        # Genera seed phrase con la lunghezza selezionata
        mnemo = Mnemonic("english")
        seed_phrase = mnemo.generate(strength=strength_map[seed_length])
        seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()

        # Seleziona coin e derivazione in base a rete e tipo
        if addr_type == "p2pkh":
            if network == "mainnet":
                wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
                derivation_path = "m/44'/0'/0'/0"
            else:
                wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN_TESTNET)
                derivation_path = "m/44'/1'/0'/0"
        elif addr_type == "p2wpkh":
            if network == "mainnet":
                wallet = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
                derivation_path = "m/84'/0'/0'/0"
            else:
                wallet = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN_TESTNET)
                derivation_path = "m/84'/1'/0'/0"
        
        # Estrai le chiavi estese (xprv/xpub, zprv/zpub, ecc.)
        account = wallet.Purpose().Coin().Account(0)
        bip32_obj = account.Bip32Object()
        xprv = bip32_obj.PrivateKey().ToExtended()
        xpub = bip32_obj.PublicKey().ToExtended()

        # Genera indirizzi
        for i in range(count):
            addr = wallet.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
            addresses.append({
                "index": i,
                "address": addr.PublicKey().ToAddress(),
                "wif": addr.PrivateKey().ToWif(),
                "path": f"{derivation_path}/{i}"
            })

        # Prendi WIF solo del primo
        wif = addresses[0]["wif"]

        # Prepara JSON da scaricare
        json_data = {
            "seed_phrase": seed_phrase,
            "extended_private_key": xprv,
            "extended_public_key": xpub,
            "addresses": addresses
        }

        with open("static/wallet_data.json", "w") as f:
            json.dump(json_data, f, indent=4)

    return render_template("index.html", addresses=addresses, seed=seed_phrase, wif=wif, path=derivation_path, xprv=xprv, xpub=xpub)

@app.route("/download")
def download():
    return send_file("static/wallet_data.json", as_attachment=True)

@app.route("/qrcode")
def generate_qrcode():
    address = request.args.get('address', '')
    if not address:
        return jsonify({"error": "Indirizzo non fornito"}), 400
    
    # Genera QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(address)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Salva l'immagine in un buffer di memoria
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

@app.route("/guida")
def guide():
    return render_template("guide.html")

if __name__ == "__main__":
    app.run(debug=True)
