# Movie Web App

This is a simple Flask web application for managing movies and users. It utilizes Flask for the web framework and includes routes for viewing users, their movies, adding users, and managing movies.

## Setup

1. Install the required dependencies:
```bash
pip install Flask python-dotenv
```


2. Create a `.env` file in the project root directory and set your API key:
```bash
MY_API_KEY=your_api_key_here
```


3. Run the application:
```bash
python app.py
```


The app will be accessible at [http://localhost:5000/](http://localhost:5000/).

## Functionality

- **Home**: The default route displays the home page with dynamic content.

- **List Users**: Navigate to `/users` to view a list of users. The page dynamically updates the title and content.

- **List User Movies**: Access user-specific movies at `/users/<user_id>`. The page dynamically updates the title and content.

- **Add User**: Visit `/add_user` to render the form for adding a user. The page dynamically updates the title and content.

- **Add Movie**: Access `/users/<int:user_id>/add_movie` to render the form for adding a movie. The page dynamically updates the title and content.

- **Update Movie Details**: Navigate to `/users/<user_id>/update_movie/<movie_id>` to update movie details. The page dynamically updates the title and content.

- **Delete Movie**: Visit `/users/<user_id>/delete_movie/<movie_id>` to delete a movie. The page dynamically updates the title and content.


## Error Handling

The application includes error handlers for 404 and 500 errors, rendering appropriate error templates.