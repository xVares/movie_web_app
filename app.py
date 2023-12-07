import logging
import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, render_template, abort
from data_manager.json_data_manager import JSONDataManager

load_dotenv()

# TODO: del test db, outcomment real db
# JSON_DATA_PATH = "user_data/movie_data.json"
TEST_JSON_DATA_PATH = "tests/test.json"
API_KEY = os.environ.get("MY_API_KEY")
FETCH_MOVIE_URL = f"http://www.omdbapi.com/?apikey={API_KEY}&"

data_manager = JSONDataManager(TEST_JSON_DATA_PATH)
app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


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
    :return: A tuple containing movie data and a boolean indicating success.
             If successful, the first element is the movie data, and the second element is True.
             If unsuccessful, both elements are None, and the second element is False.
    :rtype: tuple
    """
    res = requests.get(url, {"t": movie_name})
    movie_data = res.json()
    is_successful = movie_data["Response"]

    if is_successful == "True":
        return movie_data, True
    return None, False


@app.route("/")
@app.route("/users")
def list_all_users():
    users = data_manager.get_all_users()
    return render_index(title="Users - Movie Web App", users=users)


@app.route("/users/<user_id>")
def list_user_movies(user_id):
    try:
        user_name, movies = data_manager.get_user_name_and_movies(user_id)

        return render_index(title=f"Movies of {user_name}  - Movie Web App",
                            content_type="list_movies",
                            user=user_name,
                            movies=movies,
                            user_id=user_id)
    except KeyError as e:
        print(f"Error:{e}")
        abort(404)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_index(title="Add User - Movie Web App", content_type="add_user")

    new_user_name = request.form.get("new_user_name")
    is_adding_successful = data_manager.add_user(new_user_name)

    if is_adding_successful:
        return render_index(title="Success", content_type="add_user_success")

    abort()


@app.route("/delete_user", methods=["POST"])
def delete_user():
    user_id = request.form.get("user_id")
    is_deletion_successful = data_manager.delete_user(user_id)

    if is_deletion_successful:
        return render_index(title="Success! - Movie Web App", content_type="delete_user_success")

    abort(400, description="")


@app.route("/users/<user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    if request.method == "GET":
        return render_index(title="Add Movie - Movie Web App", content_type="add_movie",
                            user_id=user_id)

    # if POST -> fetch movie data and render success page
    movie_name = request.form.get("movie_name", "")  # get name -> from form
    movie_data, is_fetch_successful = fetch_data(FETCH_MOVIE_URL,
                                                 {"t": movie_name})

    if is_fetch_successful:
        data_manager.add_movie(is_fetch_successful, movie_data)
        return render_index(title="Success! - Movie Web App", content_type="add_movie_success")

    abort(400, description="Sorry! We couldn't find your movie.")


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["GET", "POST"])
def update_movie_details(user_id, movie_id):
    if request.method == "GET":
        user_name, movies = data_manager.get_user_name_and_movies(user_id)
        movie = movies.get(movie_id)
        return render_index(title="Update Movie - Movie Web App", content_type="update_movie",
                            user_id=user_id,
                            movie_id=movie_id,
                            movie=movie)
    # if POST -> update movie
    data_manager.update_user_movies(user_id, movie_id)
    return render_index(title="Update Movie - Movie Web App",
                        content_type="update_movie_success")


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["POST"])
def delete_movie(user_id, movie_id):
    is_deletion_successful = data_manager.delete_user_movie(user_id, movie_id)

    if is_deletion_successful:
        return render_index(title="Success - Movie Web App",
                            content_type="delete_movie_success")

    abort(400, description="Your movie is already in the database.")


# --- Error Handler ---
@app.errorhandler(400)
def bad_request(e, description="You might have a typo in your request"):
    return render_template("error_templates/400.html", error=e,
                           error_reason=f"{description} Please check your input"), 400


def page_not_found(e):
    return render_template("error_templates/404.html", error=e), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("error_templates/500.html", error=e), 500


if __name__ == "__main__":
    app.run(debug=True)
