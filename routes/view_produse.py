from flask import Blueprint, jsonify, request
from service import get_allKnowledge, get_knowledge

view_bp = Blueprint('view_produse', __name__)

@view_bp.route('/produse', methods=['GET']) 
def get_produse():
    try:
        content = get_allKnowledge() #Extragem continutul din baza de date
        if not content:
            return jsonify({"eroare": "Nu exista produse"})
        return jsonify(content)
    except Exception as e:
        return jsonify({"eroare": str(e)}), 500

@view_bp.route('/produs/<int:produs_id>', methods=['GET'])
def get_produs(produs_id):
    try:
        content = get_knowledge(produs_id) #Extragem un produs din baza de date
        if not content:
            return jsonify({"eroare": "Produsul nu a fost gasit"})
        return jsonify(content)
    except Exception as e:
        return jsonify({"eroare": str(e)}), 200