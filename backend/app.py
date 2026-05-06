import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

nama_owner = os.environ.get('NAMA_PRAKTIKAN', 'Misterius')
nim_owner = os.environ.get('NIM_PRAKTIKAN', '00000000')

kantin_data = {
    "nama_kantin": "Kantin FPMIPA",
    "menu": ["Nasi Goreng", "Es Teh", "Gorengan"]
}

@app.route('/api/menu', methods=['GET']) # Sesuaikan dengan fetch di index.html
def get_info():
    response = {
        "nama_kantin": kantin_data["nama_kantin"],
        "menu": kantin_data["menu"],
        "pemilik": nama_owner, # Mengirim variabel dari os.environ
        "nim": nim_owner,      # Mengirim variabel dari os.environ
        "judul_katalog": "Katalog Kantin - Praktikum 2"
    }
    return jsonify(response)

@app.route('/api/menu/add-menu', methods=['POST']) # Sesuaikan dengan fetch tambahMenu
def add_menu():
    new_item = request.json.get('item')
    if new_item:
        kantin_data["menu"].append(new_item)
        return jsonify({"message": "Berhasil", "menu": kantin_data["menu"]}), 201
    return jsonify({"error": "Gagal"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)