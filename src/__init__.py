from flask import Flask
from flask_cors import CORS     
from .utils.extensions import ma,db
from .routes.LoginRoute import login_router
from .routes.TodosRoute import todos_router
from .routes.IndexRoute import index_router
from .routes.UserRoute import user_router

def create_application():
    app=Flask(__name__)
    CORS(app)

    app.config["SECRET_KEY"]='12345678F'
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:1234@localhost/todos'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

    db.init_app(app)
    ma.init_app(app)

    @app.route("/")
    def start():
        return "Hello World to my API"
    app.register_blueprint(login_router)
    app.register_blueprint(todos_router)
    app.register_blueprint(user_router)
    app.register_blueprint(index_router)

    with app.app_context():
        db.create_all()

    return app
