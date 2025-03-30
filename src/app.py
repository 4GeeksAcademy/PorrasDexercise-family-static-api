import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "id": 1,
    "first_name": "Jhon",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "id": 2,
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
jackson_family.add_member({
    "id": 3,
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    return jsonify(jackson_family.get_all_members()), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Miembro no encontrado"}), 404

@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()
    if not data or 'first_name' not in data or 'age' not in data or 'lucky_numbers' not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    if not isinstance(data['age'], int) or data['age'] <= 0:
        return jsonify({"error": "La edad debe ser un número mayor que 0"}), 400

    new_member = {
        'id': data.get('id', jackson_family.get_next_id()),
        'first_name': data['first_name'],
        'last_name': 'Jackson',
        'age': data['age'],
        'lucky_numbers': data['lucky_numbers']
    }
    jackson_family.add_member(new_member)
    return jsonify(new_member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    return jsonify({"error": "Miembro no encontrado"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)