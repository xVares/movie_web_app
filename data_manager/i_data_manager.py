from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """Interface for JSON storage module."""
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass
