# Import the database object and models from the app package
from app import db
from app.models import Post, User

def create_post(caption, hashed):
    """
    Create a new post and add it to the database.
    
    Args:
        caption (str): The caption for the post.
        hashed (str): A unique hash identifier for the post.
    
    Returns:
        Post: The newly created Post object.
    """
    new_post = Post(caption=caption, hashed=hashed)  # Create a new Post object
    db.session.add(new_post)  # Add the new post to the session
    db.session.commit()  # Commit the session to save the post to the database
    return new_post  # Return the newly created post

def get_post_by_hashed(hashed):
    """
    Retrieve a post from the database by its hash.
    
    Args:
        hashed (str): The hash identifier of the post.
    
    Returns:
        Post: The Post object matching the given hash, or None if no match is found.
    """
    return Post.query.filter_by(hashed=hashed).first()  # Query the database for the post with the given hash

def create_user(instagram_id):
    """
    Create a new user and add it to the database.
    
    Args:
        instagram_id (str): The Instagram ID of the user.
    
    Returns:
        User: The newly created User object.
    """
    new_user = User(instagram_id=instagram_id)  # Create a new User object
    db.session.add(new_user)  # Add the new user to the session
    db.session.commit()  # Commit the session to save the user to the database
    return new_user  # Return the newly created user

def get_user_by_instagram_id(instagram_id):
    """
    Retrieve a user from the database by their Instagram ID.
    
    Args:
        instagram_id (str): The Instagram ID of the user.
    
    Returns:
        User: The User object matching the given Instagram ID, or None if no match is found.
    """
    return User.query.filter_by(instagram_id=instagram_id).first()  # Query the database for the user with the given Instagram ID
