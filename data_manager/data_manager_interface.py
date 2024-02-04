from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """Interface for JSON storage module."""

    @staticmethod
    def is_fetch_successful(response):
        """Check if fetching was successful based on response value and return Boolean."""
        if response == "True":
            return True
        return False

    @abstractmethod
    def get_all_users(self):
        """Get all users from the storage."""
        pass

    @abstractmethod
    def add_user(self, new_username):
        """Add a new user to the storage."""
        pass

    @abstractmethod
    def delete_user(self, user_id):
        """Delete a user from the storage."""
        pass

    @abstractmethod
    def get_username_and_movies(self, user_id):
        """Get the name and movies of a user from the storage."""
        pass

    @abstractmethod
    def add_movie(self, user_id, fetched_res):
        """Add a new movie to the user's collection."""
        pass

    @abstractmethod
    def update_user_movies(self, user_id, movie_id, update_data):
        """Update the specified movie data for a given user."""
        pass

    @abstractmethod
    def delete_user_movie(self, user_id, movie_id):
        """Delete the specified movie of a user."""
        pass
