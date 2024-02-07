from flask import Blueprint, jsonify, request
from config import data_manager

api = Blueprint("api", __name__)


# --- API Endpoints ---
@api.route('/users', methods=['GET'])
def get_users():
    users = data_manager.get_all_users()
    return jsonify(users)


@api.route('/users/<user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    try:
        username, movies = data_manager.get_username_and_movies(user_id)
        return jsonify({username: movies})
    except TypeError:
        return jsonify({"error": "User not found"}), 404


@api.route('/users/<user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    movie_data = request.json
    is_movie_added = data_manager.add_movie(user_id, movie_data)

    if is_movie_added:
        return jsonify({"success": True}), 201
    else:
        return (jsonify({
            "error": "Could not add movie. Probably already in user's favorite "
                     "list"
        }),
                400)
