from ..utils.extensions import db,ma
from datetime import datetime

class ToDo(db.Model):  
    id=db.Column(db.Integer, primary_key=True)   
    title=db.Column(db.String(200),nullable=False)
    fecha=db.Column(db.DateTime,default=datetime.now)
    description=db.Column(db.Text)
    id_user=db.Column(db.Integer,db.ForeignKey("user.id"))


class ToDoSchema(ma.Schema):
    class Meta:
        fields=('id','title','description','fecha','id_user')

todo_schema=ToDoSchema()
todos_schema=ToDoSchema(many=True)