from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from datetime import datetime
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

bcrypt=Bcrypt(app)

# configuro la base de datos, con el nombre el usuario y la clave
app.config["SECRET_KEY"]='12345678F'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:1234@localhost/todos'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino las tablas
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    username=db.Column(db.String(100))
    email=db.Column(db.String(200))
    password=db.Column(db.String(100))
    todos=db.relationship("ToDo",backref="user")


class ToDo(db.Model):   # la clase Producto hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    title=db.Column(db.String(200),nullable=False)
    fecha=db.Column(db.DateTime,default=datetime.now)
    description=db.Column(db.Text)
    id_user=db.Column(db.Integer,db.ForeignKey("user.id"))
    #  si hay que crear mas tablas , se hace aqui

with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class ToDoSchema(ma.Schema):
    class Meta:
        fields=('id','title','description','fecha','id_user')

class UserSchema(ma.Schema):
    class Meta:
        fields=('id','name','username','email','password','todos')



todo_schema=ToDoSchema()            
todos_schema=ToDoSchema(many=True)  
user_schema=UserSchema()

@app.route("/")
def start():
    return "Hello World to my API"

@app.route('/signup', methods=["POST"])
def signup_user():
    name=request.json["name"]
    username=request.json["username"]
    email=request.json["email"]
    password=request.json["password"]

    username_exists=User.query.filter_by(username=username).first()
    email_exists= User.query.filter_by(email=email).first()

    if username_exists:
        return jsonify({"error":"Username Already Exist"})
    if email_exists:
        return jsonify({"error":"Email Already Exist"})


    hashed_password=bcrypt.generate_password_hash(password)
    new_user=User(name=name,username=username,email=email,password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route("/login",methods=["POST"])
def login_user():
    email=request.json["email"]
    password=request.json["password"]

    user=User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error":"Unauthorized Access"}),401
    
    if not bcrypt.check_password_hash(user.password,password):
        return jsonify({"error":"Unauthorized"}),401

    return jsonify({
        "id":user.id,
        "email":email
    })

@app.route("/todos/<id_user>",methods=["GET"])
def get_todos(id_user):
    all_todos=ToDo.query.filter_by(id_user=id_user).all()
    result=todos_schema.dump(all_todos)
    return jsonify(result)

@app.route("/todos/<id>",methods=["GET"])
def get_todo(id):
    todo=ToDo.query.get(id)
    return todo_schema.jsonify(todo)

@app.route("/todos",methods=["POST"])
def add_todo():
    title=request.json["title"]
    description=request.json["description"]
    id_user=request.json["id_user"]
    new_todo=ToDo(title=title,description=description,id_user=id_user)
    db.session.add(new_todo)
    db.session.commit()
    return todo_schema.jsonify(new_todo)

@app.route('/todos/<id>',methods=["PUT"])
def update_todo(id):
    todo=ToDo.query.get(id)
    todo.title=request.json["title"]
    todo.description=request.json["description"]
    db.session.commit()
    return todo_schema.jsonify(todo)

@app.route('/todos/<id>',methods=["DELETE"])
def delete_todo(id):
    todo=ToDo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return todo_schema.jsonify(todo)

# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000