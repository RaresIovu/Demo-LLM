from flask import Flask, jsonify, request
from service import get_knowledge, get_allKnowledge, add_knowledge

app = Flask(__name__, template_folder="templates")

@app.route('/produse', methods=['GET']) 
def get_produse():
    try:
        content = get_allKnowledge() #Extragem continutul din baza de date
        if not content:
            return jsonify({"eroare": "Nu exista produse"})
        return jsonify(content)
    except Exception as e:
        return jsonify({"eroare": str(e)}), 500

@app.route('/produs/<int:produs_id>', methods=['GET'])
def get_produs(produs_id):
    try:
        content = get_knowledge(produs_id) #Extragem un produs din baza de date
        if not content:
            return jsonify({"eroare": "Produsul nu a fost gasit"})
        return jsonify(content)
    except Exception as e:
        return jsonify({"eroare": str(e)}), 200
    

@app.route('/add_produs/', methods=['POST'])
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
if __name__ == "__main__": #Toate fisierele python, cand sunt rulate, devin obiecte, care contin variabile(ex: __name__)
    app.run(debug=True, host="0.0.0.0", port=5000)

