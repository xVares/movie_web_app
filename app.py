import requests
from config import FETCH_MOVIE_URL, app, data_manager
from flask import request, render_template, abort
from api import api

app.register_blueprint(api, url_prefix="/api")


# --- Helper Functions ---
def render_index(title="Home - Movie App", content_type="home", **kwargs):
    """
    Render the index page with dynamic title, content type, main content and additional data.

    - Note: This is a helper function for rendering the index page.

    :param title: The title of the page. Defaults to "Home - Movie App".
    :type title: str

    :param content_type: The content type of the page. Defaults to "home".
    :type content_type: str

    :param **kwargs: Additional keyword arguments that will be passed to the template.

    :return: Rendered HTML content for the index page.
    :rtype: str
    """
    data_to_render = {
        "title": title,
        "content_type": content_type,
        **kwargs
    }
    return render_template("index.html", **data_to_render)


def fetch_data(url, movie_name):
    """
    Fetch movie data from an API using a given URL and movie name.

    - Note: This is a helper function for fetching movie data.

    :param url: The API endpoint URL.
    :type url: str

    :param movie_name: The name of the movie to search for.
    :type movie_name: dict

    :return: Tuple containing movie data and a boolean indicating success.
             If successful, the first element is the movie data, and the second element is True.
             If unsuccessful, both elements are None, and the second element is False.
    :rtype: tuple
    """
    res = requests.get(url, params=movie_name)
    movie_data = res.json()
    is_successful = movie_data["Response"]

    if is_successful == "True":
        return movie_data, True
    return None, False


# --- Routes ---
@app.route("/")
@app.route("/users")
def list_all_users():
    """Render the index page listing all users."""
    users = data_manager.get_all_users()
    return render_index(title="Users - Movie Web App", users=users)


@app.route("/users/<user_id>")
def list_user_movies(user_id):
    """Render the page listing movies of a specific user."""
    try:
        username, movies = data_manager.get_username_and_movies(user_id)

        # Is user in db? -> Render list movies page
        if username:
            return render_index(title=f"Movies of {username}  - Movie Web App",
                                content_type="list_movies",
                                user=username,
                                movies=movies,
                                user_id=user_id)
    except TypeError:
        abort(404, "User not in database.")


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    """Handle addition of a new user to the database."""
    if request.method == "GET":
        return render_index(title="Add User - Movie Web App", content_type="add_user")

    # If POST -> Add new user to db
    try:
        new_username = request.form["new_username"]

        # Check if the username is not empty
        if not new_username.strip():
            raise ValueError("Your username can't be empty")

        is_user_added = data_manager.add_user(new_username)

        if is_user_added:
            return render_index(title="Success", content_type="add_user_success")

        return abort(400, "There was an issue adding your username")

    except KeyError:
        abort(400, "Please provide a username")
    except ValueError as ve:
        abort(400, str(ve))


@app.route("/delete_user", methods=["POST"])
def delete_user():
    """Handle deletion of a user from the database."""
    try:
        user_id = int(request.form["user_id"])
        is_user_deleted = data_manager.delete_user(user_id)

        if is_user_deleted:
            return render_index(title="Success! - Movie Web App",
                                content_type="delete_user_success")
        raise TypeError

    except KeyError:
        abort(400, "We couldn't find you, please check your user ID")
    except TypeError:
        abort(400, "Please provide a valid user id")


@app.route("/users/<user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    """Handle addition of a movie to a user's favorites."""
    if request.method == "GET":
        return render_index(title="Add Movie - Movie Web App",
                            content_type="add_movie",
                            user_id=user_id)

    # If POST -> Fetch movie data from OMDb API endpoint
    movie_name = request.form.get("movie_name")
    movie_data, is_fetch_successful = fetch_data(FETCH_MOVIE_URL,
                                                 {"t": movie_name})

    # Is fetching successful? -> Try to add movie to users favorites
    if is_fetch_successful:
        is_movie_added = data_manager.add_movie(user_id, movie_data)

        # Is movie successfully added? -> Render success page
        if is_movie_added:
            return render_index(title="Success! - Movie Web App", content_type="add_movie_success")
        abort(400, description="Your movie is already in your favorites.")

    abort(400, "Sorry! We couldn't find your movie.")


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["GET", "POST"])
def update_movie_details(user_id, movie_id):
    """Handle updating details of a movie in a user's favorites."""
    if request.method == "GET":
        username, movies = data_manager.get_username_and_movies(user_id)
        movie = movies.get(movie_id)

        # Is movie in users favorites? -> Render update page
        if movie:
            return render_index(title="Update Movie - Movie Web App",
                                content_type="update_movie",
                                user_id=user_id,
                                movie_id=movie_id,
                                movie=movie)

        abort(400, description="An error occurred. Please ensure to let yourself be redirected")

    # If POST -> Get form data
    update_data = dict(request.form)

    # Validate data -> director = str | year = int | rating = int
    is_data_valid = all(((type(update_data["director"]) is str,
                          update_data["year"].isdigit(),
                          "." in update_data["rating"])))

    if not is_data_valid:
        abort(400, "Please ensure that your sent data has following types: Director = String, "
                   "Year = Integer, Rating = Integer or Float")

    # Change update data to desired type
    update_data["year"] = int(update_data.get("year"))
    update_data["rating"] = float(update_data.get("rating"))

    # Try update -> If successful render success page
    is_update_successful = data_manager.update_user_movies(user_id, movie_id, update_data)
    if is_update_successful:
        return render_index(title="Update Movie - Movie Web App",
                            content_type="update_movie_success")


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["POST"])
def delete_movie(user_id, movie_id):
    """Handle deletion of a movie from a user's favorites."""
    is_movie_deleted = data_manager.delete_user_movie(user_id, movie_id)

    if is_movie_deleted:
        return render_index(title="Success - Movie Web App",
                            content_type="delete_movie_success")

    # Raise error if deletion is not successful
    abort(404, "User is not in database or has no movies")


@app.route("/add_review/<user_id>/<movie_id>/<movie_title>", methods=["GET", "POST"])
def add_review(user_id, movie_id, movie_title):
    """Handle addition of a review for a movie by a user."""
    if request.method == "GET":
        return render_index(title="Add Review - Movie Web App",
                            content_type="add_review",
                            user_id=user_id,
                            movie_id=movie_id,
                            movie_title=movie_title)

    # If Post -> add review to db -> display success message
    review_text = request.form.get("review_text")
    is_review_added = data_manager.add_review(user_id, movie_id, review_text)

    if is_review_added:
        return render_index(title="Success - Movie Web App",
                            content_type="add_review_success",
                            movie_title=movie_title)

    # Display error message if review was not added
    abort(400, description="There was an error while adding your review")


@app.route("/reviews/<movie_id>/<movie_title>")
def list_reviews(movie_id, movie_title):
    """Render the page listing reviews for a specific movie."""
    reviews = data_manager.get_all_reviews(movie_id)

    return render_index(title="list Reviews - Movie Web App",
                        content_type="list_reviews",
                        movie_title=movie_title,
                        reviews=reviews)


# --- Error Handler ---
@app.errorhandler(400)
def bad_request(e):
    """Render a template for errors with the status code 400"""
    return render_template("error_templates/400.html", error=e), 400


@app.errorhandler(404)
def page_not_found(e):
    """Render a template for errors with the status code 404"""
    return render_template("error_templates/404.html", error=e), 404


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
