from flask import Flask, jsonify, render_template
from data_manager.json_data_manager import JSONDataManager

JSON_DATA_PATH = "user_data/test_movie_name_inside.json"
data_manager = JSONDataManager(JSON_DATA_PATH)
app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to your Movie App"


@app.route("/users")
def list_users():
    users = data_manager.get_all_users()
    return render_template("users.html", users=users)


@app.route("/users/<int:user_id>")
def list_user_movies():
    pass


@app.route("/add_user")
def add_user():
    pass


@app.route("/users/<int:user_id>/add_movie")
def add_movie():
    pass


@app.route("/users/<user_id>/update_movie/<movie_id>")
def update_movie_details():
    pass


@app.route("/users/<user_id>/delete_movie/<movie_id>")
def delete_movie():
    pass


if __name__ == "__main__":
    app.run(debug=True)
