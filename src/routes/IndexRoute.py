from flask import Blueprint


index_router=Blueprint("index_router",__name__)

@index_router.route("/")
def start():
    return "Hello World to my API"