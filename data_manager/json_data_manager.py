import json
from requests import HTTPError
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

    def get_user_name_and_movies(self, user_id) -> tuple:
        """Return all the movies for a given user"""
        if not isinstance(user_id, str):
            user_id = str(user_id)

        all_users = self.get_all_users()
        user = all_users[user_id]

        return user.get("name"), user.get("movies")

    def add_movie(self, is_fetch_successful, fetched_movie_data):
        """
       Add a new movie with its name, rating, and other details to the database.
       Modify the JSON by adding the new movie to the database.
       """
        # fetch data and parse it from database
        try:
            if not is_fetch_successful:
                raise HTTPError("We couldn't find the movie you were searching for.")

            fetched_movie_title = fetched_movie_data["Title"]
            fetched_movie_rating = fetched_movie_data["imdbRating"]
            fetched_movie_year = fetched_movie_data["Year"]

            stored_movie_data = self.parse_json(self.filename)

            # check if movie is in database --> flag = True
            movie_in_database = False
            if fetched_movie_title in stored_movie_data:
                movie_in_database = True

            # add movie to database if it doesn't exist and response is true
            if movie_in_database:
                pass
                # TODO: Raise error if movie in database, return error code -> abort in app
                print(f"{fetched_movie_title} is already on the list")
            else:
                new_movie = {
                    "rating": fetched_movie_rating,
                    "year": fetched_movie_year
                }
                #  Add fetched movie to database
                stored_movie_data[fetched_movie_title] = new_movie
                self.write_json(self.filename, stored_movie_data)
                print(f"{fetched_movie_title} was successfully added to the list")
        # TODO: implement Error handling
        except HTTPError as e:
            return None, 400, e

    def update_user_movies(self, user_id, movie_id):
        """Update all the movies for a given user"""
        all_users = self.parse_json(self.filename)

    def delete_user_movie(self, user_id, movie_id):
        """Delete the specified movie of a user"""
