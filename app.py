from flask import Flask, jsonify, request, Response
from service import get_knowledge, add_knowledge

app = Flask(__name__, template_folder="templates")


produse = [
    {"id": 1, "nume": "Laptop", "pret": 3500},
    {"id": 2, "nume": "Mouse", "pret": 150}
]

@app.route('/produse', methods=['GET']) 
def get_produse():
    return jsonify({"date": produse})

@app.route('/produs/<int:produs_id>', methods=['GET'])
def get_produs(produs_id):
    content = get_knowledge(produs_id)
    if not content:
        return jsonify({"eroare": "Produsul nu a fost gasit"})
    return jsonify(content)
    

@app.route('/add_produs/', methods=['POST'])
def add_produs():
    name = request.json['name']
    price = request.json['price']
    code = add_knowledge(name, price)
    if code['Status'] == 'Duplicate':
        return jsonify({"eroare": "Produsul deja exista in lista"}), 409
    return jsonify("Produsul a fost adaugat cu succes"), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

