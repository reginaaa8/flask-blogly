"""Models for Blogly."""

default_img = 'https://media.istockphoto.com/id/1337144146/vector/default-avatar-profile-icon-vector.jpg?s=612x612&w=0&k=20&c=BIbFwuv7FxTWvh5S3vB6bkT0Qv8Vn8N5Ffseq84ClGI='

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """blogly user"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String, 
                         nullable=False)
    
    last_name = db.Column(db.String, 
                          nullable=False)
    
    image_url = db.Column(db.String, 
                          nullable=True, 
                          default=default_img)

    def __repr__(self):
        u = self
        return f"<User id ={u.id} first_name={u.first_name} last_name={u.last_name}>"
    
