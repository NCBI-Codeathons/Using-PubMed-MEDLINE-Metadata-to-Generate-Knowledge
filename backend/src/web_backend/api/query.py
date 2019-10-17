from flask import Blueprint, jsonify, request


api = Blueprint(
    'api',
    __name__,
)

@api.route("/query", methods=['POST'])
def query():
    param1 = request.json.get('param2')
    
    return jsonify({'param1': param1})
