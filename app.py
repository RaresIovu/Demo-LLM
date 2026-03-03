from flask import Flask, jsonify, request, Response

app = Flask(__name__, template_folder="templates")

produse = [
    {"id": 1, "nume": "Laptop", "pret": 3500},
    {"id": 2, "nume": "Mouse", "pret": 150}
]

@app.route('/produse', methods=['GET']) 
def get_produse():
    return jsonify({"date": produse, "frate": produse})

@app.route('/produs/<int:produs_id>', methods=['GET'])
def get_produs(produs_id):
    rezultat = [p for p in produse if p['id'] == produs_id]
    if len(rezultat) == 0:
        return jsonify({"eroare": "Produsul nu a fost găsit"}), 404
    return jsonify(rezultat[0])

@app.route('/add_produs/', methods=['POST'])
def add_produs():
    nou_produs = {
        "id": len(produse) + 1,
        "nume": request.json['nume'],
        "pret": request.json['pret']
    }
    produse.append(nou_produs)
    return jsonify(nou_produs), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

