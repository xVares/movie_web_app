import json
from .data_manager_interface import DataManagerInterface
from typing import Union


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename: str):
        self.filename = filename

    @staticmethod
    def parse_json(filename) -> dict:
        with open(filename, "r") as file:
            return json.load(file)

    @staticmethod
    def write_json(filename, content):
        with open(filename, "w") as file:
            json.dump(content, file, indent=4)

    def get_all_users(self) -> Union[dict, None]:
        """Return all the users in a dict. If error occurs return None"""
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except OSError as e:
            print(f"Default file in path {self.filename} not found.\\n"
                  f"Error: {e}")
            return None

    def add_user(self):
        pass

    def delete_user(self):
        pass

    def get_user_and_movies(self, user_id) -> tuple:
        """Return all the movies for a given user"""
        if not isinstance(user_id, str):
            user_id = str(user_id)

        all_users = self.get_all_users()
        user = all_users[user_id]

        return user.get("name"), user.get("movies")

    def update_user_movies(self, user_id, movie_id):
        """Update all the movies for a given user"""
        all_users = self.parse_json(self.filename)

    def delete_user_movie(self, user_id, movie_id):
        """Delete the specified movie of a user"""
