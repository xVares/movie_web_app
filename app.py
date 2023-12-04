import logging
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, abort
from data_manager.json_data_manager import JSONDataManager

load_dotenv()

JSON_DATA_PATH = "user_data/movie_data.json"
API_KEY = os.environ.get("MY_API_KEY")

data_manager = JSONDataManager(JSON_DATA_PATH)
app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


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


@app.route("/")
@app.route("/users")
def list_all_users():
    users = data_manager.get_all_users()
    return render_index(title="Users - Movie Web App", content_type="list_users", users=users)


@app.route("/users/<user_id>")
def list_user_movies(user_id):
    try:
        user, movies = data_manager.get_user_and_movies(user_id)
        return render_index(title=f"Movies of {user}  - Movie Web App", content_type="list_movies",
                            user=user,
                            movies=movies)
    except KeyError as e:
        abort(404)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        # if GET -> render form to add user
        return render_template(title="Add User - Movie Web App", content_type="add_user")
    else:
        # if POST -> render form successful added
        return render_index(title="Add User - Movie Web App", content_type="add_user")


@app.route("/users/<user_id>/add_movie", methods=["POST"])
def add_movie(user_id):
    # if GET -> render form to add movie
    # if POST -> render success page
    return render_index(title="Success! - Movie Web App", content_type="add_movie")


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["PUT"])
def update_movie_details(user_id, movie_id):
    # if PUT -> render success form
    pass


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["DELETE"])
def delete_movie(user_id, movie_id):
    pass


@app.route("/form/<type>")
def render_form(type):
    if type == "which_user":
        render_index(title="Who are you? - Movie Web App", content_type="which_user")
    elif type == "add_movie":
        return render_index(title="Add Movie - Movie Web App", content_type="add_movie")
    elif type == "delete_movie":
        return render_index(title="Delete Movie - Movie Web App", content_type="delete_movie")
    elif type == "update_movie":
        return render_index(title="Update Movie - Movie Web App", content_type="update_movie")
    elif type == "add_user":
        pass
    elif type == "delete_user":
        pass
    else:
        abort(404)


# --- Error Handler ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_templates/404.html", error=e), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("error_templates/500.html", error=e), 500


if __name__ == "__main__":
    app.run(debug=True)
