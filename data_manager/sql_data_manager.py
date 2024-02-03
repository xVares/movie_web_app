from .data_manager_interface import DataManagerInterface
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .sql_data_models import db, User, Movie, UserMovies


class SQLiteDataManager(DataManagerInterface):
    """Data manager for handling SQLite data bases"""

    def __init__(self, app, db_uri):
        self.app = app
        db.init_app(app)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

    def get_all_users(self) -> dict:
        """
        Retrieves all users from the database and returns them in a dictionary.

        Each key in the dictionary is a user ID, and the corresponding value is another dictionary
        with information about the user, such as their name. This structure allows for
        easy access to each user's details in templates and other parts of the application.

        :return: A dictionary where each key is a user ID and each value is a dictionary with the
                 user's details. Currently, the user's details include only their name under the
                 key 'name'.
        :rtype: dict
        """
        try:
            # Get ID and name of all users
            db.create_all()
            users_query = User.query.with_entities(User.user_id, User.user).all()
            # Create a dictionary where user ID is the key and username is the value
            users_dict = {user_id: {"name": user_name} for user_id, user_name in users_query}
            return users_dict
        except Exception as e:
            # Log the exception or print it. Consider using a logging framework for production
            print(f"Error retrieving users: {e}")
            # Return an empty dict or a meaningful error message
            return {}

    def add_user(self, new_username):
        """
        Adds a new user to the database using the provided username.

        :param new_username: The username of the new user to be added.
        :type new_username: str
        :return: None
        """
        try:
            new_user = User(user=new_username)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            # Handle specific integrity errors, such as duplicate username
            print(f"Integrity error while adding new user: {e}")
            db.session.rollback()
        except SQLAlchemyError as e:
            # Handle general SQLAlchemy errors
            print(f"Database error while adding new user: {e}")
            db.session.rollback()
        except Exception as e:
            # Catch-all for any other exceptions
            print(f"Unexpected error while adding new user: {e}")
            db.session.rollback()

    def delete_user(self, user_id):
        """
        Deletes a user from the database based on the provided user ID.
        If the user is successfully deleted, it returns True otherwise it returns False.

        :param user_id: The ID of the user to be deleted.
        :type user_id: int
        :return: A boolean value indicating whether the deletion was successful.
        :rtype: bool
        """
        user_to_delete = User.query.filter_by(user_id=user_id).first()
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            return True
        return False

    def get_username_and_movies(self, user_id):
        pass

    def add_movie(self, user_id, is_fetch_successful, fetched_movie_data) -> bool:
        pass

    def update_user_movies(self, user_id, movie_id, update_data):
        pass

    def delete_user_movie(self, user_id, movie_id):
        pass
