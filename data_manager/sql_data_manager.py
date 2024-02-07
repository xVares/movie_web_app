from .data_manager_interface import DataManagerInterface
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .sql_data_models import db, User, Movie, UserMovies, Review


class SQLiteDataManager(DataManagerInterface):
    """Data manager for handling SQLite data bases"""

    def __init__(self, app, db_uri):
        """
        Initializes the application with necessary configurations and binds the SQLAlchemy
        service to the provided Flask app.

        :param app: The Flask application instance to configure.
        :type app: Flask
        :param db_uri: Database URI for the SQLAlchemy database connection.
        :type db_uri: str
        """
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

    def get_all_users(self) -> dict:
        """
        Retrieves all users from the database and returns them in a dictionary.

        Each key in the dictionary is a user ID, and the corresponding value is another dictionary
        with information about the user, such as their name. This structure allows for
        easy access to each user's details in templates and other parts of the application like
        the jinja2 templates.

        :return: A dictionary where each key is a user ID and each value is a dictionary with the
                 user's details. Currently, the user's details include only their name under the
                 key 'name'.
        :rtype: dict
        """
        try:
            db.create_all()
            # Get ID and name of all users
            all_users = User.query.with_entities(User.user_id, User.user).all()

            # Create a dictionary where user ID is the key and username is the value
            users_dict = {user_id: {"name": user_name} for user_id, user_name in all_users}
            return users_dict

        except Exception as e:
            # Catch-all for any exception
            print(f"Error retrieving users: {e}")
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
            return True

        except IntegrityError as e:
            # Handle specific integrity errors, such as duplicate username
            print(f"Integrity error while adding new user: {e}")
            db.session.rollback()
            return False

        except SQLAlchemyError as e:
            # Handle general SQLAlchemy errors
            print(f"Database error while adding new user: {e}")
            db.session.rollback()
            return False

        except Exception as e:
            # Catch-all for any other exceptions
            print(f"Unexpected error while adding new user: {e}")
            db.session.rollback()
            return False

    def delete_user(self, user_id) -> bool:
        """
        Deletes a user and all their associated movies from the database based on the provided
        user ID.

        :param user_id: The ID of the user to be deleted.
        :type user_id: int

        :return: A boolean value indicating whether the deletion was successful.
        """
        user_to_delete = User.query.filter_by(user_id=user_id).first()

        if user_to_delete:
            UserMovies.query.filter_by(user_id=user_id).delete()
            db.session.delete(user_to_delete)
            db.session.commit()
            return True

        return False

    def get_username_and_movies(self, user_id) -> tuple:
        """
        Retrieves the specified user's username and their associated movies as a dictionary.

        :param user_id: The ID of the user whose username and movies are to be retrieved.
        :type user_id: int

        :return: A tuple containing the user's username and a dictionary of their movies,
        where the dictionary key is the movie ID and its value is another dictionary containing
        the movie's title, director, year of publication, and rating.
        """
        user = User.query.filter_by(user_id=user_id).first()
        username = user.user

        # Get user movies by joining Movie table with user ID and movie ID from UserMovies table
        user_movies = db.session.query(Movie).join(
            UserMovies, UserMovies.movie_id == Movie.movie_id).filter(
            UserMovies.user_id == user_id).all()

        # Return username & empty dict if user has no movies
        if not user_movies:
            return username, {}

        # Create dict of user movies with their respective movie ID as key
        movies_dict = {}
        for movie in user_movies:
            movie_dict = {
                "title": movie.title,
                "director": movie.director,
                "year": movie.publication_year,
                "rating": movie.rating

            }
            movies_dict[str(movie.movie_id)] = movie_dict

        return username, movies_dict

    def add_movie(self, user_id, fetched_movie_data) -> bool:
        """
         Adds a movie to the database if it's not already in the user's list of favorites.

         :param user_id: ID of the user.
         :type user_id: int

         :param fetched_movie_data: Dictionary containing movie data.
         :type fetched_movie_data: dict

         :return: Boolean indicating if the addition was successful.
         """
        fetched_movie_title = fetched_movie_data["Title"]
        fetched_movie_director = fetched_movie_data["Director"]
        fetched_movie_year = int(fetched_movie_data["Year"])
        fetched_movie_rating = float(fetched_movie_data["imdbRating"])

        # Check if movie is already in users list
        movie = Movie.query.filter_by(title=fetched_movie_title).first()
        if movie:
            is_in_favorite = UserMovies.query.filter_by(user_id=user_id,
                                                        movie_id=movie.movie_id).first()
            if is_in_favorite:
                return False

            # Add movie to users list
            new_favorite_movie = UserMovies(user_id=user_id, movie_id=movie.movie_id)
            db.session.add(new_favorite_movie)
            db.session.commit()
            return True

        # If movie is not already in Movie table -> Add to Movie table & users list
        if not movie:
            new_movie = Movie(title=fetched_movie_title,
                              director=fetched_movie_director,
                              publication_year=fetched_movie_year,
                              rating=fetched_movie_rating)
            # Commit addition to generate movie ID
            db.session.add(new_movie)
            db.session.commit()

            # Add movie to users list
            new_favorite_movie = UserMovies(user_id=user_id, movie_id=new_movie.movie_id)
            db.session.add(new_favorite_movie)
            db.session.commit()
            return True

        return False

    def update_user_movies(self, user_id, movie_id, update_data):
        """
        Updates a movie record for a given user and movie.

        :param user_id: ID of the user associated with the movie.
        :type user_id: int

        :param movie_id: ID of the movie to update.
        :type movie_id: int

        :param update_data: Dictionary containing movie details to update.
        :type update_data: dict

        :return: Boolean indicating if the update was successful.

        Note: Even though the user_id is not used, it is implemented for a planned many-to-many
        relationship
        """
        movie_to_update = Movie.query.filter_by(movie_id=movie_id).first()

        if not movie_to_update:
            return False

        # Update movie in database with new data
        for key, value in update_data.items():
            setattr(movie_to_update, key, value)

        # Commit the changes to database
        try:
            db.session.commit()
            return True
        except Exception as e:
            print(f"An error occurred {e}")
            db.session.rollback()
            return False

    def delete_user_movie(self, user_id, movie_id):
        """
        Deletes a specific movie associated with a user from the UserMovies table.

        :param user_id: The ID of the user whose movie entry is to be deleted.
        :type user_id: int

        :param movie_id: The ID of the movie to be deleted from the user's list.
        :type movie_id: int

        :return: True if the movie was successfully deleted, False otherwise.
        :rtype: bool
        """
        movie_to_delete = UserMovies.query.filter_by(user_id=user_id, movie_id=movie_id).first()

        if movie_to_delete:
            db.session.delete(movie_to_delete)
            db.session.commit()
            return True

        return False

    def add_review(self, user_id, movie_id, review_text) -> bool:
        """
        Adds a new review to the database for a specific movie by a specific user.

        :param user_id: The ID of the user who is adding the review.
        :type user_id: int

        :param movie_id: The ID of the movie for which the review is added.
        :type movie_id: int

        :param review_text: The content of the review being added.
        :type review_text: str

        :return: True if the review was successfully added to the database, False otherwise.
        :rtype: bool
        """
        try:
            new_review = Review(user_id=user_id, movie_id=movie_id, review_text=review_text)

            db.session.add(new_review)
            db.session.commit()
            return True

        except Exception as e:
            print(f"An error occurred {e}")
            db.session.rollback()
            return False

    def get_all_reviews(self, movie_id):
        """
        Retrieves all reviews for a given movie from the database and formats them into a dictionary.

        This function performs a database query to fetch all reviews associated with the
        specified movie ID.
        It joins the Review and User tables to include user details in the result. The function
        then constructs a dictionary where each key is a review ID, and the value is another
        dictionary containing details of the review, including movie ID, user ID, username,
        and review text.

        :param movie_id: The ID of the movie for which reviews are being retrieved.
        :type movie_id: int
        :return: A dictionary of review details keyed by review ID.
        :rtype: dict
        """
        # Get all reviews of a given movie
        user_reviews = db.session.query(Review).join(
            User, User.user_id == Review.user_id).filter(
            Review.movie_id == movie_id).all()

        # Create dict so jinja2 template can iterate over it
        user_reviews_dict = {
            review.review_id: {
                "movie_id": review.movie_id,
                "user_id": review.user_id,
                "user_name": review.user.user,
                "review_text": review.review_text
            }
            for review in user_reviews
        }

        return user_reviews_dict
