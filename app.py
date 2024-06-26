import os
import uuid
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from extensions import db
from models.user import User
from flask_login import LoginManager

login_manager = LoginManager()

load_dotenv()

# print(os.environ.get("AZURE_DATABASE_URL"))

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")

# local database
# connection_string = os.environ.get("LOCAL_DATABASE_URL")

connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

db.init_app(app)

login_manager.init_app(app)


# Model (SQLALchemy) = Schema


@app.route("/add_movie", methods=["GET", "POST"])
def add_movie_page():
    return render_template("movie_form.html")


@app.route("/update_movie", methods=["GET", "POST"])
def update_movie_page():
    return render_template("update_form.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up_page():
    return render_template("sign_up.html")


from routes.movies_bp import movies_bp
from routes.movies_list_bp import movies_list_bp

app.register_blueprint(movies_bp, url_prefix="/movies")
app.register_blueprint(movies_list_bp, url_prefix="/movie-list")


# Task - User Model | id, username, password
# Sign Up page
# Login page


from routes.users_bp import users_bp

app.register_blueprint(users_bp)


from routes.main_bp import main_bp

app.register_blueprint(main_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        # db.drop_all()
        # db.create_all()  # creates all Models/tables!!!
        print("Creation done")
except Exception as e:
    print("Error connecting to the database:", e)


# Task 5
# @app.delete("/movies/<id>")
# def delete_movie_on_page(id):
#     filtered_movie = Movie.query.get(id)
#     if not filtered_movie:
#         return jsonify({"message": "Movie not found"}), 404

#     try:
#         data = filtered_movie.to_dict()
#         db.session.delete(filtered_movie)
#         db.session.commit()  # making the change (update/delete/create) permanent
#         return render_template("movies.html", movies=data)
#     except Exception as e:
#         db.session.rollback()  # undo the change
#         return jsonify({"message": str(e)}), 500


# POST


# shorter syntax -> if same variable/column name
# @app.post("/movies")
# def create_new_movie():
#     movie_data = request.json
#     new_movie = Movie(**movie_data)
#     try:
#         db.session.add(new_movie)
#         db.session.commit()
#         result = {"message": "Added successfully", "data": new_movie.to_dict()}
#         return jsonify(result), 201
#     except Exception as e:
#         db.session.rollback()  # undo the change
#         return jsonify({"message": str(e)}), 500


# @app.route("/movies", methods=["GET", "POST"])
# def add_new_movie():
#     try:
#         movie_data = request.json
#         new_movie = Movie(
#             name=movie_data["name"],
#             poster=movie_data["poster"],
#             rating=movie_data["rating"],
#             summary=movie_data["summary"],
#             trailer=movie_data["trailer"],
#         )

#         db.session.add(new_movie)
#         db.session.commit()
#         return render_template("movies.html", movies=new_movie)
#     except Exception as e:
#         db.session.rollback()  # undo the change
#         return jsonify({"message": str(e)}), 500


# Task 6 convert to DB call
# @app.put("/movies/<id>")
# def update_movie_by_id(id):
#     filtered_movie = Movie.query.get(id)
#     if not filtered_movie:
#         return jsonify({"message": "Movie not found"}), 404

#     movie_data = request.json
#     try:
#         filtered_movie.name = movie_data.get("name", filtered_movie.name)
#         filtered_movie.poster = movie_data.get("poster", filtered_movie.poster)
#         filtered_movie.rating = movie_data.get("rating", filtered_movie.rating)
#         filtered_movie.summary = movie_data.get("summary", filtered_movie.summary)
#         filtered_movie.trailer = movie_data.get("trailer", filtered_movie.trailer)

#         db.session.commit()
#         return jsonify(
#             {"message": "Updated Successfully", "data": filtered_movie.to_dict()}
#         )
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500


# better syntax


# Task 7 convert to db call using form


# @app.route("/update_movie", methods=["GET", "POST"])
# def update_movie_page():
#     return render_template("update_form.html")


# # better syntax


# local
# movies = [
#     {
#         "id": "99",
#         "name": "Vikram",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
#         "rating": 8.4,
#         "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
#         "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
#     },
#     {
#         "id": "100",
#         "name": "RRR",
#         "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
#         "rating": 8.8,
#         "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
#         "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
#     },
#     {
#         "id": "101",
#         "name": "Iron man 2",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
#         "rating": 7,
#         "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
#         "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
#     },
#     {
#         "id": "102",
#         "name": "No Country for Old Men",
#         "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
#         "rating": 8.1,
#         "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
#         "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
#     },
#     {
#         "id": "103",
#         "name": "Jai Bhim",
#         "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
#         "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
#         "rating": 8.8,
#         "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
#     },
#     {
#         "id": "104",
#         "name": "The Avengers",
#         "rating": 8,
#         "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
#         "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
#         "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
#     },
#     {
#         "id": "105",
#         "name": "Interstellar",
#         "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
#         "rating": 8.6,
#         "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
#         "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
#     },
#     {
#         "id": "106",
#         "name": "Baahubali",
#         "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
#         "rating": 8,
#         "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
#         "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
#     },
#     {
#         "id": "107",
#         "name": "Ratatouille",
#         "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
#         "rating": 8,
#         "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
#         "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
#     },
#     {
#         "name": "PS2",
#         "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
#         "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
#         "rating": 8,
#         "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
#         "id": "108",
#     },
#     {
#         "name": "Thor: Ragnarok",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
#         "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
#         "rating": 8.8,
#         "trailer": "https://youtu.be/NgsQ8mVkN8w",
#         "id": "109",
#     },
# ]


# jinja2 - templates


# name = "Gemma"
# hobbies = ["Reading", "Yoga", "cooking"]


# @app.route("/")
# def hello_world():
#     return "<p>Hellos!</p>"


# from about_bp import about_bp

# app.register_blueprint(about_bp, url_prefix="/about")


# @app.route("/profile")
# def profile_page():
#     return render_template("profile.html", name=name, hobbies=hobbies)


# @app.route("/movies")
# def dashboard_page():
#     return render_template("movies.html", movies=movies)


# @app.route("/movies/<id>")
# def get_movie_by_id(id):
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
#     if filtered_movie:
#         return render_template("movie.html", movie=filtered_movie)
#     else:
#         return "Movie not found", 404


# @app.route("/login", methods=["GET"])
# def login_page():
#     return render_template("forms.html")


# @app.route("/dashboard", methods=["POST"])
# def dashboard_login_page():
#     username = request.form.get("username")
#     password = request.form.get("password")
#     return f"Hi, {username}"


# @app.route("/movies/delete", methods=["POST"])
# def delete_movie_by_id():
#     movie_id = request.form.get("movie_id")
#     movie_to_delete = Movie.query.get(movie_id)

#     if movie_to_delete:
#         db.session.delete(movie_to_delete)
#         db.session.commit()
#         return "<h1>Movie Deleted</h1>"
#     else:
#         return "<h1>error deleting movie</h1>"


# @app.route("/movies", methods=["POST"])
# def add_new_movie():

#     name = request.form.get("name")
#     poster = request.form.get("poster")
#     rating = request.form.get("rating")
#     summary = request.form.get("summary")
#     trailer = request.form.get("trailer")
#     form_data = {
#         "name": name,
#         "poster": poster,
#         "rating": rating,
#         "summary": summary,
#         "trailer": trailer,
#     }

#     max_id = max([int(movie["id"]) for movie in movies])
#     new_id = str(max_id + 1)
#     form_data["id"] = new_id

#     movies.append(form_data)

#     return render_template("movies.html", movies=movies)


# @app.get("/movies")
# def get_movies():
#     return jsonify(movies)


# @app.post("/movies")
# def create_movie():
#     movie_data = request.json
#     movies.append(movie_data)
#     return jsonify(movies)


# 1 id higher than the max, send through
# @app.post("/movies")
# def create_new_movie():
#     movie_data = request.json
#     max_id = max([int(movie["id"]) for movie in movies])
#     new_id = str(max_id + 1)
#     movie_data["id"] = new_id
#     movies.append(movie_data)
#     return jsonify(movies)


# <variable name> | id -> keyword argument
# # match the movie with id
# task 1
# @app.get("/movies/<id>")
# def get_movie(id):
#     for movie in movies:
#         if movie["id"] == id:
#             return jsonify(movie)
#     return "completed"


# # task 1.1
# @app.get("/movies/<id>")
# def get_movie(id):
#     for movie in movies:
#         if movie["id"] == id:
#             return jsonify(movie)
#     return jsonify({"error": "Movie not found"}), 404


# # task 2
# @app.delete("/movies/<id>")
# def delete_movie(id):
#     for movie in movies:
#         if movie["id"] == id:
#             movies.remove(movie)
#             return jsonify(movie)
#     return jsonify({"error": "Movie not found"}), 404


# list comprehension
# @app.get("/movies/<id>")
# def get_movie(id):
#     filtered_movie = [movie for movie in movies in movies if movie["id"] == id]
#     return jsonify(filtered_movie[0])


# generator expression
# advantage | loop will stop as soon as a match is found
# @app.get("/movies/<id>")
# def get_movie(id):
#     filtered_movie = next(
#         (movie for movie in movies in movies if movie["id"] == id), None
#     )
#     return jsonify(filtered_movie)


# task 1.1 - generator expression
# @app.get("/movies/<id>")
# def get_movie(id):
#     filtered_movie = next(
#         (movie for movie in movies in movies if movie["id"] == id), None
#     )
#     if filtered_movie:
#         return jsonify(filtered_movie)
#     else:
#         return jsonify({"error": "Movie not found"}), 404


# task 2
# @app.delete("/movies/<id>")
# def delete_movie(id):
#     #permission to modify the lexical scope variable | reeassigning not allowed
#     global movies
#     filtered_movie = next(
#         (movie for movie in movies in movies if movie["id"] == id), None
#     )
#     movies.remove(filtered_movie)
#     return jsonify(filtered_movie)


# # task 2.1
# @app.delete("/movies/<id>")
# def delete_movie(id):
#     filtered_movie = next(
#         (movie for movie in movies in movies if movie["id"] == id), None
#     )
#     if filtered_movie:
#         movies.remove(filtered_movie)
#         return jsonify(filtered_movie)
#     else:
#         return jsonify({"error": "Movie not found"}), 404


# Ragav answer
# @app.delete("/movies/<id>")
# def delete_movie(id):
#     # Permission to modify the lexical scope variable
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)

#     if filtered_movie:
#         movies.remove(filtered_movie)
#         return jsonify({"message": "Deleted Successfully", "data": filtered_movie})
#     else:
#         return jsonify({"message": "Movie not found"}), 404


# unpacking operator or update
# @app.put("/movies/<id>")
# def update_movie(id):
#     movie_data = request.json
#     for movie in movies:
#         if movie["id"] == id:
#             movie.update(movie_data)  # same memory | mutable
#             return jsonify({"message": "Movie updated successfully"})

#     return jsonify({"error": "Movie not found"}), 404
