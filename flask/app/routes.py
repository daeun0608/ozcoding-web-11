from flask import Blueprint, jsonify, render_template, g, request

from .database.database import SessionLocal
from .database.models import Movie

bp = Blueprint("main", __name__)


@bp.before_app_request
def get_db():
    if "db" not in g:
        g.db = SessionLocal()


@bp.after_request
def after_debug_log(response):
    # print("RUN After APP Request")
    return response


@bp.teardown_app_request
def teardown_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@bp.route("/admin")
def admin():
    # db = SessionLocal()
    db = g.db
    movies = db.query(Movie).all()

    return render_template("admin.html")


@bp.route("/admin/content", methods=["POST"])
def register_content():
    """
    콘텐츠 등록 API
    콘텐츠의 제목, 장르, 설명, 썸네일 이미지를 등록하는 API 입니다.

    Args:
        title: (str) : 콘텐츠 제목 입니다.
        genre: (str) : 콘텐츠 장르입니다. 서비스에서 검색에 사용될 값입니다.
        description: (str) : 콘텐츠 설명입니다.
        thumbnail_url: (str) : 콘텐츠 썸네일입니다.

    Returns:
        (json) : message 와 code 가지고 있습니다.
                 code 가 1000 일때 성공적으로 등록되었습니다.
    """

    db = g.db
    body_data = request.get_json()

    movie = Movie(
        title=body_data.get("title"),
        genre=body_data.get("genre"),
        description=body_data.get("description"),
        thumbnail=body_data.get("thumbnail_url"),
    )
    db.add(movie)  ##insert
    db.commit()
    return jsonify({"message": "success", "code": 1000})


@bp.route("/admin/content", methods=["GET"])
def get_content():
    """
    콘텐츠 조회 API
    콘텐츠의 전체 목록을 조회 하는 API 입니다.

    Args:


    Returns:
        (list) : 콘텐츠 목록이 반환됩니다.
    """

    db = g.db
    movies = db.query(Movie).all()
    movie_list = [
        {
            "id": movie.id,
            "title": movie.title,
            "genre": movie.genre,
            "description": movie.description,
            "thumbnail": movie.thumbnail,
        }
        for movie in movies
    ]
    return jsonify(movie_list)


@bp.route("/admin/content", methods=["DELETE"])
def delete_content():
    """
    콘텐츠 삭제 API
    콘텐츠 아이디를 전달하고 부합한 콘텐츠를 제거하는 API 입니다.

    Args:
        content_id: (str) : 삭제할 대상의 콘텐츠 ID 입니다.

    Returns:
        (json) : message 와 code 가지고 있습니다.
                 code 가 1000 일때 성공적으로 등록되었습니다.
    """

    db = g.db
    content_id = request.args.get("content_id")
    if not content_id:
        ## 9000 content id delete
        return jsonify({"error": "Missing content id", "code": 9000}), 400
    content = db.query(Movie).filter_by(id=content_id).first()
    if not content:
        return jsonify({"error": "Not found content", "code": 9010}), 404
    db.delete(content)
    db.commit()
    return jsonify({"message": "success", "code": 1000})


@bp.route("/recommend", methods=["POST"])
def recommend_content():
    """
    콘텐츠 추천 API
    사용자가 입력한 키워드 기준 콘텐츠를 조회하고 반환합니다.

    Args:
        keyword: (str): 사용자가 검색을 위해 입력하는 키워드 입니다.

    Returns:
        (list) : 사용자가 입력한 키워드 기반하여 조회된 콘텐츠 목록이 반환됩니다.
    """
    
    db = g.db
    keyword = request.json.get("keyword", None)
    if not keyword:
        return jsonify({"message": "Missing keyword", "code": 9020}), 400

    contents = db.query(Movie).filter(Movie.genre.ilike(f"%{keyword}%")).all()
    if contents:
        return jsonify([
            {
                "title":content.title,
                "description":content.description,
                "genre":content.genre,
                "thumbnail_url":content.thumbnail
            }
            for content in contents
        ])
    
    else:
        return jsonify({"message":"Not found content", "code":9030}), 404