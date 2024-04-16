from flask import Blueprint,jsonify,request
from ..models.Todo import ToDo,todo_schema,todos_schema
from ..models.User import User
from ..utils.extensions import db

todos_router=Blueprint("todos_router",__name__)


@todos_router.route("/todos/<id_user>",methods=["GET"])
def get_todos(id_user):
    all_todos=ToDo.query.filter_by(id_user=id_user).all()
    result=todos_schema.dump(all_todos)
    return jsonify(result)

@todos_router.route("/todos/<id>",methods=["GET"])
def get_todo(id):
    todo=ToDo.query.get(id)
    return todo_schema.jsonify(todo)

@todos_router.route("/todos",methods=["POST"])
def add_todo():
    title=request.json["title"]
    description=request.json["description"]
    id_user=request.json["id_user"]
    user=User.query.get(id_user)
    if not user:
        return jsonify({'error':'Usuario no encontrado'}),404
    new_todo=ToDo(title=title,description=description,user=user)

    db.session.add(new_todo)
    db.session.commit()

    todo_json=todo_schema.dump(new_todo)
    return jsonify(todo_json)

@todos_router.route('/todos/<id>',methods=["PUT"])
def update_todo(id):
    todo=ToDo.query.get(id)
    todo.title=request.json["title"]
    todo.description=request.json["description"]
    db.session.commit()
    return todo_schema.jsonify(todo)

@todos_router.route('/todos/<id>',methods=["DELETE"])
def delete_todo(id):
    todo=ToDo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return todo_schema.jsonify(todo)
