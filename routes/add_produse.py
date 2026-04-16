from flask import Blueprint, jsonify, request
from service import add_knowledge

add_bp = Blueprint('add_produse', __name__)

@add_bp.route('/add_produs', methods=['POST'])
def add_produs():
    data = request.get_json()
    if not data:
        return jsonify({"eroare": "Body-ul cererii trebuie sa fie JSON"}), 400

    name = data.get('name')
    price = data.get('price')

    # Validare name: trebuie sa fie string nevid
    if not name or not isinstance(name, str) or not name.strip():
        return jsonify({"eroare": "Campul 'name' este obligatoriu si nu poate fi gol"}), 400

    # Validare price: trebuie sa fie numar (int sau float) si pozitiv
    if price is None:
        return jsonify({"eroare": "Campul 'price' este obligatoriu"}), 400
    if not isinstance(price, (int, float)) or isinstance(price, bool):
        return jsonify({"eroare": "Campul 'price' trebuie sa fie un numar"}), 400
    if price <= 0:
        return jsonify({"eroare": "Campul 'price' trebuie sa fie un numar pozitiv"}), 400

    name = name.strip()
    try: #Exception handling, blocul de cod "asculta" exceptii(erori) si returneaza in functie de eroare
        item = add_knowledge(name, price)
        return jsonify({
            "message": "Produsul a fost adăugat",
            "data": item
        }), 201
    except Exception as e: #Nu se mai returneaza obiectul, ci doar eroarea
        return jsonify({"eroare": str(e)}), 409 #str "intreaba" obiectul daca are o metoda de string. foarte interesant
    #clasa Exception, pe care o mosteneste, contine astfel de metoda
