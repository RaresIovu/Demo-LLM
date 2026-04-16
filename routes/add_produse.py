from flask import Blueprint, jsonify, request
from service import add_knowledge

add_bp = Blueprint('add_produse', __name__)

@add_bp.route('/add_produs', methods=['POST'])
def add_produs():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    if not name or not price:
        return jsonify({"eroare": "Lipsesc date (nume sau pret)"})
    try: #Exception handling, blocul de cod "asculta" exceptii(erori) si returneaza in functie de eroare
        item = add_knowledge(name, price)
        return jsonify({
            "message": "Produsul a fost adăugat",
            "data": item
        }), 201
    except Exception as e: #Nu se mai returneaza obiectul, ci doar eroarea
        return jsonify({"eroare": str(e)}), 409 #str "intreaba" obiectul daca are o metoda de string. foarte interesant
    #clasa Exception, pe care o mosteneste, contine astfel de metoda
