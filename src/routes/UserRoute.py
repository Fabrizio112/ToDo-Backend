from flask import Blueprint,jsonify
from ..models.User import User,user_schema


user_router=Blueprint("user_router",__name__)

@user_router.route('/users/<email>',methods=["GET"])
def get_user(email):
    user=User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    user_json=user_schema.dump(user)
    return jsonify(user_json)