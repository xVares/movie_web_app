from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """Interface for JSON storage module."""

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def add_user(self):
        pass

    @abstractmethod
    def delete_user(self):
        pass

    @abstractmethod
    def get_user_and_movies(self, user_id):
        pass

    @abstractmethod
    def update_user_movies(self, user_id, movie_id):
        pass

    @abstractmethod
    def delete_user_movie(self, user_id, movie_id):
        pass
