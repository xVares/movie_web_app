import logging
import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, render_template, abort
from data_manager.json_data_manager import JSONDataManager

load_dotenv()

JSON_DATA_PATH = "user_data/movie_data.json"
API_KEY = os.environ.get("MY_API_KEY")
FETCH_MOVIE_URL = f"http://www.omdbapi.com/?apikey={API_KEY}&"

data_manager = JSONDataManager(JSON_DATA_PATH)
app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# --- Helper Functions ---
def render_index(title="Home - Movie App", content_type="home", **kwargs):
    """
    Render template for the index page with dynamic title and content type.

    Parameters:
    - title (str): The title of the page. Defaults to "Home - Movie App".
    - content_type (str): The content type of the page. Defaults to "home".
    - **kwargs: Additional keyword arguments that will be passed to the template.

    Returns:
    str: Rendered HTML content for the index page.
    """
    data_to_render = {
        "title": title,
        "content_type": content_type,
        **kwargs
    }
    return render_template("index.html", **data_to_render)


def fetch_data(url, movie_name):
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
    return render_index(title="Users - Movie Web App", content_type="home", users=users)


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
        # if GET -> render form to add user
        return render_index(title="Add User - Movie Web App", content_type="add_user")

    # if POST -> render form successful added
    return render_index(title="Success", content_type="add_user_success")


@app.route("/delete_user/<user_id>", methods=["GET", "DELETE"])
def delete_user(user_id):
    if request.method == "DELETE":
        # if DELETE -> delete user
        return render_index(title="Add User - Movie Web App", content_type="delete_user")

    # if GET -> render form to delete user
    return render_index(title="Add User - Movie Web App", content_type="delete_user_success")


@app.route("/users/<user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    if request.method == "POST":
        # if POST -> fetch movie data and render success page
        print("req.form: ", request.form)
        movie_name = request.form["movie_name"]  # get name -> from form
        movie_data, is_fetch_successful, error_message = fetch_data(FETCH_MOVIE_URL,
                                                                    {"t": movie_name})

        if is_fetch_successful:
            data_manager.add_movie(is_fetch_successful, movie_data)
            return render_index(title="Success! - Movie Web App", content_type="add_movie_success")

        abort(400, description=error_message)

    # if GET -> render form to add movie
    return render_index(title="Add Movie - Movie Web App", content_type="add_movie",
                        user_id=user_id)


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["GET", "PUT"])
def update_movie_details(user_id, movie_id):
    if request.method == "PUT":
        # if PUT -> Update movie & render success
        return render_index(title="Update Movie - Movie Web App",
                            content_type="update_movie_success")
    # if GET -> render form to update movie
    return render_index(title="Update Movie - Movie Web App", content_type="update_movie")


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["GET", "DELETE"])
def delete_movie(user_id, movie_id):
    # if DELETE -> render success page & delete movie
    if request.method == "DELETE":
        return render_index(title="Update Movie - Movie Web App",
                            content_type="delete_movie_success")

    # if GET -> render form to delete movie
    return render_index(title="Update Movie - Movie Web App", content_type="delete_movie")


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
