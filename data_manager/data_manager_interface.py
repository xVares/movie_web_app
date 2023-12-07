from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """Interface for JSON storage module."""

    @staticmethod
    def is_fetch_successful(response):
        """
        Check if fetching was successful based on response value and return Boolean
        """
        if response == "True":
            return True
        return False

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def add_user(self, new_user_name):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def get_user_name_and_movies(self, user_id):
        pass

    @abstractmethod
    def add_movie(self, was_fetch_successful, fetched_res):
        pass

    @abstractmethod
    def update_user_movies(self, user_id, movie_id):
        pass

    @abstractmethod
    def delete_user_movie(self, user_id, movie_id):
        pass
