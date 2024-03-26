import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv

load_dotenv()

print(os.environ.get("AZURE_DATABASE_URL"))

app = Flask(__name__)

connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db = SQLAlchemy(app)

# try:
#     with app.app_context():
#         # Use text() to explicitly declare your SQL command
#         result = db.session.execute(text("SELECT 1")).fetchall()
#         print("Connection successful:", result)
# except Exception as e:
#     print("Error connecting to the database:", e)

# Model (SQLALchemy) = Schema


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))
    poster = db.Column(db.String(255))
    rating = db.Column(db.Float)
    summary = db.Column(db.String(500))
    trailer = db.Column(db.String(255))

    # JSON = keys
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "poster": self.poster,
            "rating": self.rating,
            "summary": self.summary,
            "trailer": self.trailer,
        }


# Task 2
@app.get("/movies")
def get_movies():
    movies = Movie.query.all()
    return render_template("movies.html", movies=movies)


# Task 3
@app.route("/movies/<id>")
def get_movie_by_id(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie:
        return render_template("movie.html", movie=filtered_movie)
    else:
        return "Movie not found", 404


# local
movies = [
    {
        "id": "99",
        "name": "Vikram",
        "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
        "rating": 8.4,
        "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
        "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
    },
    {
        "id": "100",
        "name": "RRR",
        "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
        "rating": 8.8,
        "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
        "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
    },
    {
        "id": "101",
        "name": "Iron man 2",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
        "rating": 7,
        "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
        "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
    },
    {
        "id": "102",
        "name": "No Country for Old Men",
        "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
        "rating": 8.1,
        "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
        "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
    },
    {
        "id": "103",
        "name": "Jai Bhim",
        "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
        "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
        "rating": 8.8,
        "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
    },
    {
        "id": "104",
        "name": "The Avengers",
        "rating": 8,
        "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
        "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
        "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
    },
    {
        "id": "105",
        "name": "Interstellar",
        "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
        "rating": 8.6,
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
        "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
    },
    {
        "id": "106",
        "name": "Baahubali",
        "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
        "rating": 8,
        "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
        "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
    },
    {
        "id": "107",
        "name": "Ratatouille",
        "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
        "rating": 8,
        "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
        "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
    },
    {
        "name": "PS2",
        "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
        "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
        "rating": 8,
        "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
        "id": "108",
    },
    {
        "name": "Thor: Ragnarok",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
        "rating": 8.8,
        "trailer": "https://youtu.be/NgsQ8mVkN8w",
        "id": "109",
    },
]


# jinja2 - templates

users = [
    {
        "name": "Gemma",
        "pic": "https://th.bing.com/th/id/R.72380963a35b3fba67398022db5ae99d?rik=ga0xsfijaETFdQ&riu=http%3a%2f%2f1.bp.blogspot.com%2f-NP0zmaopjRE%2fUhhnlfaNsrI%2fAAAAAAAAEuE%2fZ5HQX6Jhqik%2fs1600%2fa%2b(9).jpg&ehk=AGheMSErLhbTXsly541CsCFJA95DVaC6Hd3vxS6KKFU%3d&risl=&pid=ImgRaw&r=0",
        "pro": True,
    },
    {
        "name": "Tina",
        "pic": "https://www.ninjaonlinedating.com/blog/wp-content/uploads/2019/08/SmileModifiedKRAK.jpg",
        "pro": False,
    },
    {
        "name": "Alex",
        "pic": "https://writestylesonline.com/wp-content/uploads/2016/08/Follow-These-Steps-for-a-Flawless-Professional-Profile-Picture.jpg",
        "pro": True,
    },
]

name = "Gemma"
hobbies = ["Reading", "Yoga", "cooking"]


@app.route("/")
def hello_world():
    return "<p>Hellos!</p>"


@app.route("/about")
def about_page():
    return render_template("about.html", users=users)


@app.route("/profile")
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)


@app.route("/movies")
def dashboard_page():
    return render_template("movies.html", movies=movies)


# @app.route("/movies/<id>")
# def get_movie_by_id(id):
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
#     if filtered_movie:
#         return render_template("movie.html", movie=filtered_movie)
#     else:
#         return "Movie not found", 404


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("forms.html")


@app.route("/dashboard", methods=["POST"])
def dashboard_login_page():
    username = request.form.get("username")
    password = request.form.get("password")
    return f"Hi, {username}"


@app.route("/add_movie", methods=["GET"])
def add_movie_page():
    return render_template("movie_form.html")


@app.route("/movies", methods=["POST"])
def add_new_movie():

    name = request.form.get("name")
    poster = request.form.get("poster")
    rating = request.form.get("rating")
    summary = request.form.get("summary")
    trailer = request.form.get("trailer")
    form_data = {
        "name": name,
        "poster": poster,
        "rating": rating,
        "summary": summary,
        "trailer": trailer,
    }

    max_id = max([int(movie["id"]) for movie in movies])
    new_id = str(max_id + 1)
    form_data["id"] = new_id

    movies.append(form_data)

    return render_template("movies.html", movies=movies)


# @app.get("/movies")
# def get_movies():
#     return jsonify(movies)


# @app.post("/movies")
# def create_movie():
#     movie_data = request.json
#     movies.append(movie_data)
#     return jsonify(movies)


# 1 id higher than the max, send through
@app.post("/movies")
def create_new_movie():
    movie_data = request.json
    max_id = max([int(movie["id"]) for movie in movies])
    new_id = str(max_id + 1)
    movie_data["id"] = new_id
    movies.append(movie_data)
    return jsonify(movies)


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
@app.delete("/movies/<id>")
def delete_movie(id):
    # Permission to modify the lexical scope variable
    filtered_movie = next((movie for movie in movies if movie["id"] == id), None)

    if filtered_movie:
        movies.remove(filtered_movie)
        return jsonify({"message": "Deleted Successfully", "data": filtered_movie})
    else:
        return jsonify({"message": "Movie not found"}), 404


# unpacking operator or update
@app.put("/movies/<id>")
def update_movie(id):
    movie_data = request.json
    for movie in movies:
        if movie["id"] == id:
            movie.update(movie_data)  # same memory | mutable
            return jsonify({"message": "Movie updated successfully"})

    return jsonify({"error": "Movie not found"}), 404
