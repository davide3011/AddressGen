from flask import Flask, jsonify, render_template, request
from utils import generate_address

app = Flask(__name__)

# Modifica questa variabile per attivare o meno il back-button
SHOW_BACK_BUTTON = False

@app.route('/')
def index():
    return render_template('index.html', show_back_button=SHOW_BACK_BUTTON)

@app.route('/generate')
def generate():
    network = request.args.get('network', 'mainnet')
    return jsonify(generate_address(network))

if __name__ == '__main__':
    app.run(debug=True)
