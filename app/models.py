# Import necessary functions and modules from SQLAlchemy and the app package
from sqlalchemy.sql import func
from app import db

class Post(db.Model):
    """
    Post model representing a post in the database.
    
    Attributes:
        id (int): Primary key, unique identifier for the post.
        caption (str): Caption for the post, up to 2083 characters.
        hashed (str): Unique hash identifier for the post.
        created_at (datetime): Timestamp when the post was created.
    """
    __tablename__ = 'post'
    
    # Define columns for the Post model
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing primary key
    caption = db.Column(db.String(2083), nullable=False)  # Caption column with a maximum length of 2083 characters, cannot be null
    hashed = db.Column(db.String(64), nullable=False, unique=True, index=True)  # Unique hash identifier, indexed for faster queries, cannot be null
    created_at = db.Column(db.DateTime, server_default=func.now())  # Timestamp for creation, defaults to current time
    
    def __repr__(self):
        """
        Representation method for the Post model.
        
        Returns:
            str: A string representation of the Post object.
        """
        return f'<Post {self.id}>'

class User(db.Model):
    """
    User model representing a user in the database.
    
    Attributes:
        id (int): Primary key, unique identifier for the user.
        instagram_id (str): Unique Instagram ID for the user.
    """
    __tablename__ = "user"
    
    # Define columns for the User model
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing primary key
    instagram_id = db.Column(db.String(64), nullable=False, unique=True)  # Unique Instagram ID, cannot be null
