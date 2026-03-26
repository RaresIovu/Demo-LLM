from flask import Flask, jsonify, request, Response
from service import get_knowledge, add_knowledge
from exceptions import DuplicateException

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
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    if not name or not price:
        return jsonify({"eroare": "Lipsesc date (nume sau pret)"}), 400
    try:
        item = add_knowledge(name, price)
        return jsonify({
            "message": "Produsul a fost adăugat",
            "data": item
        }), 201
    except DuplicateException as e:
        return jsonify({"eroare": str(e)}), 409

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

