from ..utils.extensions import db,ma

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    username=db.Column(db.String(100))
    email=db.Column(db.String(200))
    password=db.Column(db.String(100))
    todos=db.relationship('ToDo',backref='user')

class UserSchema(ma.Schema):
    class Meta:
        fields=('id','name','username','email','password','todos')
        exclude=('todos',)

user_schema=UserSchema()
users_schema=UserSchema(many=True)