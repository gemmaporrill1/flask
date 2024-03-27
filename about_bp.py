from flask import Blueprint, render_template

users = [
    {
        "id": "1",
        "name": "Gemma",
        "pic": "https://th.bing.com/th/id/R.72380963a35b3fba67398022db5ae99d?rik=ga0xsfijaETFdQ&riu=http%3a%2f%2f1.bp.blogspot.com%2f-NP0zmaopjRE%2fUhhnlfaNsrI%2fAAAAAAAAEuE%2fZ5HQX6Jhqik%2fs1600%2fa%2b(9).jpg&ehk=AGheMSErLhbTXsly541CsCFJA95DVaC6Hd3vxS6KKFU%3d&risl=&pid=ImgRaw&r=0",
        "pro": True,
    },
    {
        "id": "2",
        "name": "Tina",
        "pic": "https://www.ninjaonlinedating.com/blog/wp-content/uploads/2019/08/SmileModifiedKRAK.jpg",
        "pro": False,
    },
    {
        "id": "3",
        "name": "Alex",
        "pic": "https://writestylesonline.com/wp-content/uploads/2016/08/Follow-These-Steps-for-a-Flawless-Professional-Profile-Picture.jpg",
        "pro": True,
    },
]

about_bp = Blueprint("about", __name__)


# url prefix
@about_bp.route("/")
def about_page():
    return render_template("about.html", users=users)


@about_bp.route("/<id>")
def about_page_by_id(id):
    filtered_users = [user for user in users if user["id"] == id]
    print(filtered_users)
    return render_template("about.html", users=filtered_users)
