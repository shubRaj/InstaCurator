from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    caption = db.Column(db.String(2083), nullable=False)
    hashed = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    def __repr__(self):
        return f'<Post {self.id}>'
