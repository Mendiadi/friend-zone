import hashlib
import json

import flask
import database

app = flask.Flask("fb_clone")

db = database.DataBase.get()


@app.route("/")
def index():
    return flask.jsonify({"connection": "ok"})


@app.route("/register", methods=["POST"])
def register():
    user_data = database.user(**flask.request.json)
    hash = hashlib.md5(user_data.password.encode()).hexdigest()
    user_data.password = hash
    if db.add_user(user_data):
        return flask.make_response(flask.jsonify(user_data.__dict__), 201)
    return flask.make_response(flask.jsonify({"error": "user already exists"}), 400)


@app.route("/login", methods=["POST"])
def login():
    user_data = database.user(**flask.request.json)
    hash = hashlib.md5(user_data.password.encode()).hexdigest()
    user_from_db = db.get_user(user_data.email)
    if not user_from_db:
        return flask.make_response(flask.jsonify({"error": "user not found"}), 404)
    if hash != user_from_db.password:
        return flask.make_response(flask.jsonify({"error": "user pass wrong"}), 400)
    return flask.make_response(flask.jsonify({"login": "ok"}), 200)


@app.route("/<user_>/post", methods=["POST"])
def create_post(user_):
    user_from_db = db.get_user(user_)
    if not user_from_db:
        return flask.make_response(flask.jsonify({"error": "user not found"}), 404)
    post_data = database.post(None, flask.request.json['text'], None)
    post_data.post_id = db.AUTO_INC()
    post_data.user_email = user_from_db.email
    if db.add_post(post_data):
        return flask.make_response(flask.jsonify(post_data.__dict__), 201)
    return flask.make_response(flask.jsonify({"error": "post error"}), 400)


@app.route("/<user_>/post", methods=["GET"])
def get_posts(user_):
    user_from_db = db.get_user(user_)
    if not user_from_db:
        return flask.make_response(flask.jsonify({"error": "user not found"}), 404)
    posts = db.get_posts_by_user(user_from_db.email)
    if not posts:
        posts = []
    else:
        posts = [post.__dict__ for post in posts]

    return flask.make_response(flask.jsonify({"posts": posts}), 200)


@app.route("/post/delete/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    if db.delete_post(post_id):
        return flask.make_response(flask.jsonify({"deleted": "ok"}), 200)
    return flask.make_response(flask.jsonify({"error": "post not found"}), 404)


if __name__ == '__main__':
    app.run(debug=True)
