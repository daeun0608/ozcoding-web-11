from flask import Blueprint, request, jsonify, render_template, g
from flasgger.utils import swag_from

from .database import SessionLocal
from .models import Movie

bp = Blueprint("main", __name__)


@bp.before_request
def get_db():
    if "db" not in g:
        g.db = SessionLocal()


@bp.teardown_request
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
@swag_from({
    "tags":["Admin Content"],
    "description":"콘텐츠의 전체 목록을 조회 하는 API 입니다.",
    "responses":{
        200:{
            "description":"전체 콘텐츠 목록",
            "example":{
                "application/json":[{
                    "id":"영화 아이디",
                    "title":"영화 제목",
                    "genre":"영화 장르",
                    "description":"영화 설명",
                    "thumbnail":"영화 포스트 이미지",
                }]
            }
        }
    }
})
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
# @swag_from(
#     {
#         "tags": ["Recommend"],
#         "description": "장르 키워드를 기반으로 영화를 추천합니다.",
#         "parameters": [
#             {
#                 "name": "keyword",
#                 "in": "body",
#                 "schema": {
#                     "type": "object",
#                     "properties": {"keyword": {"type": "string", "example": "SF"}},
#                     "required": ["keyword"],
#                 },
#             }
#         ],
#         "responses": {
#             200: {
#                 "description": "추천된 영화",
#                 "examples": {
#                     "application/json": {
#                         "title": "Interstellar",
#                         "description": "A space exploration epic.",
#                     }
#                 },
#             },
#             404: {"description": "추천 결과 없음"},
#         },
#     }
# )
def recommend():
    """
    사용자가 입력한 키워드 기준 콘텐츠를 조회하고 반환합니다.
    ---
    tags:
      - Recommend
    consumes:
      - application/json
    parameters:
      - in: body
        name: keyword
        required: true
        schema:
          type: object
          required:
            - keyword
          properties:
            keyword:
              type: string
              example: SF
    responses:
      200:
        description: 입력한 키워드 기반 콘텐츠 목록
        examples:
          application/json:
            title: 조회된 영화 제목
            description: 조회된 영화 설명
            genre: 조회된 영화 장르
            thumbnail: 조회된 영화 포스터 이미지
      400:
        description: 입력한 키워드가 없는 경우
        examples:
          application/json:
            code: 9020
            message: Missing keyword
      404:
        description: 입력한 키워드 기반 매칭된 콘텐츠가 없는 경우
    """

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
