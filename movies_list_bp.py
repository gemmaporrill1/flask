from flask import Blueprint, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from app import db, Movie

movies_list_bp = Blueprint("movies_list", __name__)


# Task 2: /movies-list -> Display the data on the page from Azure (MSSQL)
# Movie list dashboard
@movies_list_bp.route("/")  # HOF
def movie_list_page():
    movie_list = Movie.query.all()  # Select * from movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # list of dictionaries
    return render_template("movies.html", movies=data)


# Task 3: /movies-list/99 -> Display the data on the page from Azure (MSSQL)
# Movie list detail
@movies_list_bp.route("/<id>")  # HOF
def movie_detail_page(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie:
        data = filtered_movie.to_dict()
        return render_template("movie.html", movie=data)
    else:
        return "<h1>Movie not found</h1>"


@movies_list_bp.route("/add", methods=["GET"])  # HOF
def add_movie():
    return render_template("movie_form.html")


@movies_list_bp.route("/delete", methods=["POST"])  # HOF
def delete_movie_by_id():
    print(request.form.get("movie_id"))
    id = request.form.get("movie_id")
    filtered_movie = Movie.query.get(id)
    if not filtered_movie:
        return "<h1>Movie not found</h1>", 404

    try:
        data = filtered_movie.to_dict()
        db.session.delete(filtered_movie)
        db.session.commit()  # Making the change (update/delete/create) permanent
        return f"<h1>{data['name']} Movie deleted Successfully</h1>"
    except Exception as e:
        db.session.rollback()  # Undo the change
        return f"<h1>Error happened {str(e)}</h1>", 500


@movies_list_bp.route("/success", methods=["POST"])  # HOF
def create_movie():
    # Creating a dictionary
    data = {
        "name": request.form.get("name"),
        "poster": request.form.get("poster"),
        "rating": request.form.get("rating"),
        "summary": request.form.get("summary"),
        "trailer": request.form.get("trailer"),
    }

    new_movie = Movie(**data)
    try:
        db.session.add(new_movie)
        db.session.commit()
        # movies.append(new_movie)
        return f"<h1>{data['name']} Movie added Successfully</h1>"
    except Exception as e:
        db.session.rollback()  # Undo the change
        return f"<h1>Error happened {str(e)}</h1>", 500


@movies_list_bp.route("/update/<id>", methods=["POST"])
def update_movie_by_id_form(id):
    filtered_movie = Movie.query.get(id)
    if not filtered_movie:
        return "Movie could not be found"
    movie_data = filtered_movie.to_dict()
    try:
        for key, value in movie_data.items():
            if hasattr(filtered_movie, key):
                setattr(filtered_movie, key, value)

        db.session.commit()
        return "<h1>Updated Successfully</h1>"
    except Exception as e:
        return "Movie update error"
