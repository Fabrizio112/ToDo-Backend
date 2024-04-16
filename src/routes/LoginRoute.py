from flask import Blueprint,request,jsonify
from ..models.User import User,user_schema
from ..utils.extensions import bcrypt,db
login_router=Blueprint('login_router',__name__)


@login_router.route('/signup', methods=["POST"])
def signup_user():
    name=request.json["name"]
    username=request.json["username"]
    email=request.json["email"]
    password=request.json["password"]

    email_exists= User.query.filter_by(email=email).first()


    if email_exists:
        return jsonify({"error":"Correo Electronico ya registrado"}),401


    hashed_password=bcrypt.generate_password_hash(password)
    new_user=User(name=name,username=username,email=email,password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@login_router.route("/login",methods=["POST"])
def login_user():
    email=request.json["email"]
    password=request.json["password"]

    user=User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error":"Correo electronico o contraseña incorrectas"}),401

    if not bcrypt.check_password_hash(user.password,password):
        return jsonify({"error":"Correo electronico o contraseña incorrectas"}),401

    return jsonify({
        "id":user.id,
        "email":email
    })
