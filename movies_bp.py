from flask import Blueprint, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from app import db, Movie

movies_bp = Blueprint("movies", __name__)


@movies_bp.get("/")
def get_movies():
    movies = Movie.query.all()
    return render_template("movies.html", movies=movies)


@movies_bp.route("/<id>")
def get_movie_by_id(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie:
        return render_template("movie.html", movie=filtered_movie)
    else:
        return "Movie not found", 404


@movies_bp.delete("/<id>")
def delete_movie(id):
    filtered_movie = Movie.query.get(id)
    if not filtered_movie:
        return jsonify({"message": "Movie not found"}), 404

    try:
        data = filtered_movie.to_dict()
        db.session.delete(filtered_movie)
        db.session.commit()  # making the change (update/delete/create) permanent
        return jsonify({"message": "Deleted Successfully", "data": data})
    except Exception as e:
        db.session.rollback()  # undo the change
        return jsonify({"message": str(e)}), 500


@movies_bp.post("/")
def create_new_movie():
    movie_data = request.json
    new_movie = Movie(
        name=movie_data["name"],
        poster=movie_data["poster"],
        rating=movie_data["rating"],
        summary=movie_data["summary"],
        trailer=movie_data["trailer"],
    )
    try:
        db.session.add(new_movie)
        db.session.commit()
        result = {"message": "Added successfully", "data": new_movie.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()  # undo the change
        return jsonify({"message": str(e)}), 500


@movies_bp.put("/<id>")
def update_movie_by_id(id):
    filtered_movie = Movie.query.get(id)
    if not filtered_movie:
        return jsonify({"message": "Movie not found"}), 404

    movie_data = request.json
    try:
        for key, value in movie_data.items():
            if hasattr(filtered_movie, key):
                setattr(filtered_movie, key, value)

        db.session.commit()
        return jsonify(
            {"message": "Updated Successfully", "data": filtered_movie.to_dict()}
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 500
