"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jhon ={
                "id": 1,
                "first_name": "Jhon",
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            }

jane =      {
                "id": 2,
                "first_name": "Jane",
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            }
jimmy =     {
                "id": 3,
                "first_name": "Jimmy",
                "age": 5,
                "lucky_numbers": [1]
            }

jackson_family.add_member(jhon)
jackson_family.add_member(jane)
jackson_family.add_member(jimmy)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404

    
@app.route('/member', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        if not data or 'first_name' not in data or 'age' not in data or 'lucky_numbers' not in data:
            return jsonify({"error": "Datos incompletos"}), 400

        new_member = {
            'first_name': data['first_name'],
            'last_name': 'Jackson',
            'age': data['age'],
            'lucky_numbers': data['lucky_numbers']
        }

        jackson_family.add_member(new_member)
        return jsonify(new_member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        if jackson_family.delete_member(member_id):
            return jsonify({"done": True}), 200
        else:
            return jsonify({"error": "Miembro no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
