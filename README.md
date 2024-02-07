# Movie Web App

This is a simple Flask web application for managing movies and users. It utilizes Flask for the web framework and
includes routes which utilize the SQLite framework SQLAlchemy for viewing users, their movies, adding users, and
managing movies.

### Features

- **User Management**: Users can be added to the system, and their details can be viewed along with the list of their
  favorite movies.

- **Movie Management**: Users can add movies to their favorites list, update movie details such as director, year, and
  rating, and delete movies from their favorites.

- **Review Management**: Users can add reviews for movies, and these reviews can be viewed on the movie details page.

## Setup

1. Install the required dependencies:

```bash  
pip install -r requirements.txt
```  

2. Create a `.env` file in the project root directory and set your API key. Copy paste follow line and
   replace `your_api_key` with your own OMDb API key:

```bash
API_KEY=your_api_key
```  

3. Run the application:

```bash  
python app.py
```  

The app will be accessible at [http://localhost:5000/](http://localhost:5000/).

## Functionality

- **Home**: The default route `/` and `/users` display a list of currently registered users.

- **List User Movies**: Access user-specific movies at `/users/<user_id>` by clicking on a username.

- **Add User**: Visit `/add_user` by clicking on the `Add User` button to render the form for adding a user.

- **Add Movie**: Access `/users/<int:user_id>/add_movie` by clicking on the `Add Movie` button next to a username to
  render the form for adding a movie.

- **Update Movie Details**: Navigate to `/users/<user_id>/update_movie/<movie_id>` by clicking on the `Update` button of
  a listed movie to update movie details.

- **Delete Movie**: Visit `/users/<user_id>/delete_movie/<movie_id>` by clicking on the `Delete` button of a listed
  movie to delete it.

- **Add Review**: Visit `/add_review/<user_id>/<movie_id>/<movie_title>` by clicking on the `Add Review` button of a
  listed movie to add a review.

- **Show Reviews**: Visit `/reviews/<movie_id>/<movie_title>` by clicking on the `Show Reviews` button of a listed movie
  to show all added reviews.

## API Endpoints

- The application also provides API endpoints for interacting with users and movies. These include:
    - `/api/users`: GET request to retrieve all users.
    - `/api/users/<user_id>/movies`:
        - GET request to retrieve all movies of a specific user.
        - POST request to add a movie to a user's favorites.

## Error Handling

The application includes error handlers for 404 and 400 errors, rendering appropriate error templates.

## Technologies used

- Python
- Flask
- SQLite
- SQLAlchemy
- pytest

## Planned Features

- Deleting / Updating Reviews
- Account Creation
- More API Endpoints
- Poster Images for Movies
- Improve UX & UI