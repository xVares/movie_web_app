from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movie(db.Model):
    """Represents a movie in the database."""

    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(255), nullable=True)
    publication_year = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return (f"<Movie(movie_id={self.movie_id}, "
                f"title='{self.title}', "
                f"director='{self.director}', "
                f"publication_year={self.publication_year}, "
                f"rating={self.rating})>")

    def __str__(self):
        return (f"Movie ID: {self.movie_id}, "
                f"Title: '{self.title}', "
                f"Director: '{self.director}', "
                f"Year: {self.publication_year}, "
                f"Rating: {self.rating}")


class User(db.Model):
    """Represents a user in the database."""

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return (f"<User(user_id={self.user_id}, "
                f"user='{self.user}')>")

    def __str__(self):
        return (f"User ID: {self.user_id}, "
                f"User Name: '{self.user}'")


class UserMovies(db.Model):
    """Relationship table that links User and Movie entities together"""

    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), nullable=False)

    def __repr__(self):
        return (f"<UserMovies(entry_id={self.entry_id}, "
                f"user_id={self.user_id}, "
                f"movie_id={self.movie_id})>")

    def __str__(self):
        return (f"Entry ID: {self.entry_id}, "
                f"User ID: {self.user_id}, "
                f"Movie ID: {self.movie_id}")


class Review(db.Model):
    """Represents a movie review in the database."""

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), nullable=False)
    review_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return (f"<Review(review_id={self.review_id}, "
                f"movie_id={self.movie_id}, "
                f"review_text='{self.review_text[:50]}...')>")

    def __str__(self):
        return (f"Review ID: {self.review_id}, "
                f"Movie ID: {self.movie_id}, "
                f"Review: '{self.review_text}'")
