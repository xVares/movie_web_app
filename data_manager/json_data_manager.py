import json
from .data_manager_interface import DataManagerInterface
from typing import Union


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename: str):
        self.filename = filename

    def get_all_users(self) -> Union[dict, None]:
        """Return all the users in a dict. If error occurs return None"""
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Default file in path {self.filename} not found.")
            return None

    def get_user_movies(self, user_id: dict):
        """Return all the movies for a given user"""
        if not isinstance(user_id, str):
            user_id = str(user_id)
        all_user = self.get_all_users()

        return all_user[user_id]["movies"]
