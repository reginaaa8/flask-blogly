"""Models for Blogly."""

default_img = 'https://media.istockphoto.com/id/1337144146/vector/default-avatar-profile-icon-vector.jpg?s=612x612&w=0&k=20&c=BIbFwuv7FxTWvh5S3vB6bkT0Qv8Vn8N5Ffseq84ClGI='

from flask_sqlalchemy import SQLAlchemy

import datetime

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
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f"<User id ={u.id} first_name={u.first_name} last_name={u.last_name}>"
    
class Post(db.Model):
    """blog posts"""
    __tablename__ = 'posts'

    id =  db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True)
        
    title = db.Column(db.String, 
                          nullable=False)
        
    content = db.Column(db.String, 
                            nullable=False)
        
    created_at = db.Column(db.DateTime, 
                               nullable=False, 
                               default=datetime.datetime.now)
        
    user_id = db.Column(db.Integer, 
                            db.ForeignKey('users.id'), 
                            nullable=False)
        
    def __repr__(self):
            p = self
            return f"<id ={p.id} title={p.title} created_at={p.created_at} user_id={p.user_id}>"
    
class Tag(db.Model):
     """tags for posts"""
     __tablename__ = 'tags'

     id = db.Column(db.Integer, 
                    primary_key=True, 
                    autoincrement=True)
     
     tag_name = db.Column(db.String, 
                          unique=True,
                          nullable=False)
     
     posts = db.relationship(
          'Post', 
          secondary="posts_tags",
          backref="tags"
     )
    