"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String, 
                         nullable=False)
    
    last_name = db.Column(db.String, 
                          nullable=False)
    
    image_url = db.Column(db.String)

    def __repr__(self):
        user = self
        return f"<User id ={user.id} first_name={user.first_name} last_name={user.last_name}>"
