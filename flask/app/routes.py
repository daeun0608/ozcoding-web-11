from flask import Blueprint, request, jsonify, render_template, g
from flasgger.utils import swag_from

from .database import SessionLocal
from .models import Movie

bp = Blueprint("main", __name__)


@bp.before_app_request
def get_db():
    if "db" not in g:
        g.db = SessionLocal()


# 예외에도 실행, 마지막에 실행 반면 after_request response 객체 생성후 실행, 로깅 못함
@bp.teardown_app_request
def teardown_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/results")
def results():
    return render_template("results.html")


@bp.route("/admin")
def admin():
    db = g.db
    movies = db.query(Movie).all()
    return render_template("admin.html", movies=movies)


@bp.route("/admin/content", methods=["GET", "POST", "DELETE"])
def manage_movies():
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

    elif request.method == "DELETE":
        movie_id = request.args.get("id")
        if not movie_id:
            return jsonify({"error": "Missing movie id"}), 400

        movie = db.query(Movie).filter_by(id=movie_id).first()
        if not movie:
            return jsonify({"error": "Movie not found"}), 404

        db.delete(movie)
        db.commit()
        return jsonify({"message": "Movie deleted successfully"})


@bp.route("/recommend", methods=["POST"])
@swag_from(
    {
        "tags": ["Recommend"],
        "description": "장르 키워드를 기반으로 영화를 추천합니다.",
        "parameters": [
            {
                "name": "keyword",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {"keyword": {"type": "string", "example": "SF"}},
                    "required": ["keyword"],
                },
            }
        ],
        "responses": {
            200: {
                "description": "추천된 영화",
                "examples": {
                    "application/json": {
                        "title": "Interstellar",
                        "description": "A space exploration epic.",
                    }
                },
            },
            404: {"description": "추천 결과 없음"},
        },
    }
)
def recommend():
    keyword = request.json.get("keyword")
    db = g.db
    movies = db.query(Movie).filter(Movie.genre.ilike(f"%{keyword}%")).all()
    if movies:
        return jsonify(
            [
                {
                    "title": movie.title,
                    "description": movie.description,
                    "thumbnail_url": movie.thumbnail,
                }
                for movie in movies
            ]
        )
    else:
        return jsonify({"message": "No recommendation found"}), 404
