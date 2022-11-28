import hashlib

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


if __name__ == '__main__':
    app.run(debug=True)
