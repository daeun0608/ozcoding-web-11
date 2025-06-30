import json
from app.models import Movie


def test_index(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    content = response.data.decode("utf-8")
    assert "콘텐츠" in content


def test_add_movie(test_client):
    data = {
        "title": "Test Movie",
        "keywords": "Drama",
        "description": "A test movie description",
        "thumbnail_url": "thumbnail",
    }
    response = test_client.post(
        "/admin/content", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Movie added successfully"


def test_recommend_found(test_client, mock_session):
    # DB에 영화 직접 추가
    movie = Movie(
        title="Comedy Hit",
        genre="Comedy",
        description="Funny movie",
        thumbnail="thumbnail",
    )
    mock_session.add(movie)
    mock_session.commit()
    print(mock_session.query(Movie).all()[0].genre)

    response = test_client.post(
        "/recommend",
        data=json.dumps({"keyword": "Comedy"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data[0]["title"] == "Comedy Hit"


def test_recommend_not_found(test_client):
    response = test_client.post(
        "/recommend",
        data=json.dumps({"keyword": "Nonexistent"}),
        content_type="application/json",
    )
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "No recommendation found"
