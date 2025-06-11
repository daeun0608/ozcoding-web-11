from flask import Blueprint, request, jsonify, render_template, g
from flasgger.utils import swag_from

from .database import SessionLocal
from .models import Movie

bp = Blueprint("main", __name__)


@bp.before_app_request
def get_db():
    if "db" not in g:
        g.db = SessionLocal()


@bp.teardown_app_request
def teardown_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@bp.route("/admin/content", methods=["GET", "POST"])
def manage_content():
    db = g.db

    if request.method == "POST":
        data = request.get_json()
        movie = Movie(
            title=data.get("title"),
            genre=data.get("keywords"),
            description=data.get("description"),
            thumbnail=data.get("thumbnail_url"),
        )
        db.add(movie)
        db.commit()
        return jsonify({"message": "Movie added successfully"})

    elif request.method == "GET":
        movies = db.query(Movie).all()
        movie_list = [
            {
                "id": m.id,
                "title": m.title,
                "genre": m.genre,
                "description": m.description,
            }
            for m in movies
        ]
        return jsonify(movie_list)
