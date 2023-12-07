import json
from abc import ABC
from uuid import uuid4
from .data_manager_interface import DataManagerInterface
from typing import Union


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename: str):
        self.filename = filename

    @staticmethod
    def parse_json(filename) -> dict:
        """
        Parse JSON data from a file.

        :param filename: The path to the JSON file.
        :type filename: str
        :return: A dictionary containing the parsed JSON data.
        :rtype: dict
        """
        with open(filename, "r") as file:
            return json.load(file)

    @staticmethod
    def write_json(filename, content):
        """
        Write JSON content to a file.

        :param filename: The path to the JSON file.
        :type filename: str
        :param content: The data to be written to the file.
        :type content: Any valid JSON-serializable object
        """
        with open(filename, "w") as file:
            json.dump(content, file, indent=4)

    def get_all_users(self) -> Union[dict, None]:
        """
        Return all the users from a JSON file as a dictionary.

        :return: A dictionary containing user data if successful, or None if an error occurs.
        :rtype: Union[dict, None]
        """
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except OSError:
            return None

    def add_user(self, new_user_name):
        """
        Adds a new user to the database.

        :param new_user_name: The name of the new user.
        :return: True if the user was successfully added, False if the user already exists
                 in the database.
        """
        all_user = self.parse_json(self.filename)

        # Generate a new user ID and add the user to the database
        new_user_id = str(uuid4())
        all_user[new_user_id] = {
            "name": new_user_name,
            "movies": {}
        }

        # Update the JSON file with the new user
        self.write_json(self.filename, all_user)

        return True

    def delete_user(self, user_id):
        """
        Delete a user from the database.

        :param user_id: The unique identifier of the user to be deleted.
        :type user_id: str
        :return: True if the user was successfully deleted, False if the user does not exist.
        :rtype: bool
        """
        all_user = self.parse_json(self.filename)

        if user_id in all_user:
            del all_user[user_id]
            self.write_json(self.filename, all_user)
            return True

        return False

    def get_user_name_and_movies(self, user_id) -> Union[tuple, False]:
        """
        Get the name and movies of a user from the database.

        :param user_id: The unique identifier of the user.
        :type user_id: str
        :return: A tuple containing the user's name and movie collection if the user exists,
                 otherwise False.
        :rtype: Union[tuple, False]
        """
        all_users = self.get_all_users()
        user = all_users.get(user_id)

        if not user:
            return False

        user_name = user.get("name")
        user_movies = user.get("movies")

        if not user_movies:
            user_movies = None

        return user_name, user_movies

    def add_movie(self, is_fetch_successful, fetched_movie_data) -> bool:
        """
        Add a new movie to the user's collection.

        :param is_fetch_successful: A boolean indicating whether the movie data was successfully fetched.
        :type is_fetch_successful: bool
        :param fetched_movie_data: The data of the fetched movie.
        :type fetched_movie_data: dict
        :return: True if the movie was successfully added, False if the movie already exists in the collection.
        :rtype: bool
        """
        fetched_movie_title = fetched_movie_data["Title"]
        fetched_movie_director = fetched_movie_data["Director"]
        fetched_movie_year = fetched_movie_data["Year"]
        fetched_movie_rating = fetched_movie_data["imdbRating"]

        stored_movie_data = self.parse_json(self.filename)

        if fetched_movie_title in stored_movie_data:
            return False

        unique_id = str(uuid4())
        new_movie = {
            "name": fetched_movie_title,
            "director": fetched_movie_director,
            "rating": fetched_movie_rating,
            "year": fetched_movie_year
        }
        #  Add fetched movie to database
        stored_movie_data["movies"][unique_id] = new_movie
        self.write_json(self.filename, stored_movie_data)

        return True

    def update_user_movies(self, user_id, movie_id):
        """Update all the movies for a given user"""
        pass

    def delete_user_movie(self, user_id, movie_id):
        """Delete the specified movie of a user"""
        pass
