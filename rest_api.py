import hashlib
import socket

import flask
# my imports
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


@app.route("/posts")
def get_all_posts():
    posts = db.get_all_posts()
    posts = [post.__dict__ for post in posts]
    return flask.make_response(flask.jsonify({"posts": posts}), 200)


@app.route("/search/<query>")
def search(query):
    users = db.get_users()
    res = []
    for user in users:
        if query in user.email:
            res.append(user.__dict__)

    return flask.make_response(flask.jsonify({"users": res}), 200)


@app.route("/post/edit/<post_id>", methods=["PUT"])
def update_post(post_id):
    data = database.post(**flask.request.json)

    if int(post_id) != int(data.post_id):
        return flask.make_response(flask.jsonify({"error": "post id modified"}), 400)
    if not db.update_post(data, data.post_id):
        return flask.make_response(flask.jsonify({"error": "something went wrong"}), 400)
    return flask.make_response(flask.jsonify({"post": data.__dict__}), 201)


@app.route("/post/like/<post_id>", methods=["POST"])
def like_post(post_id):
    if db.get_post_by_id(post_id):
        data = database.likes(**flask.request.json)
        if int(post_id) != int(data.post_id):
            return flask.make_response(flask.jsonify({"error": "post id modified"}), 400)
        likes_user = db.get_user_likes(user_email=data.user_email)
        if likes_user:
            for like in likes_user:
                if int(like.post_id) == int(post_id):
                    db.delete_like(like)
                    return flask.make_response(flask.jsonify({"dislike": like.__dict__}), 200)
        db.add_like(data)
        return flask.make_response(flask.jsonify({"like": data.__dict__}), 201)
    return flask.make_response(flask.jsonify({"error": "post not found"}), 404)

#
# @app.route("/post/like/<post_id>/<user_email>", methods=["DELETE"])
# def dislike_post(post_id, user_email):
#     if db.get_post_by_id(post_id):
#         data = database.likes(user_email, post_id)
#         print(data.__dict__)
#         if int(post_id) != int(data.post_id):
#             return flask.make_response(flask.jsonify({"error": "post id modified"}), 400)
#         likes_user = db.get_user_likes(user_email=data.user_email)
#         if not likes_user:
#             for like in likes_user:
#                 if int(like.post_id) == int(post_id):
#                     return flask.make_response(flask.jsonify({"error": "like not found"}), 404)
#         db.delete_like(data)
#         return flask.make_response(flask.jsonify({"like_deleted": data.__dict__}), 201)
#     return flask.make_response(flask.jsonify({"error": "post not found"}), 404)
@app.route("/post/<post_id>")
def get_post_by_id(post_id):
    post=db.get_post_by_id(post_id)
    if post:
        return flask.make_response(flask.jsonify({"post":post.__dict__}), 200)
    return flask.make_response(flask.jsonify({"error": "post not found"}), 404)

@app.route("/post/like/<post_id>", methods=["GET"])
def get_like_by_post(post_id):
    if not db.get_post_by_id(post_id):
        return flask.make_response(flask.jsonify({"error": "post not found"}), 404)
    like_ = db.get_post_likes(post_id)
    if like_:
        return flask.make_response(flask.jsonify({"likes": [like__.__dict__
                                                            for like__ in like_], "count": len(like_)}), 201)
    return flask.make_response(flask.jsonify({"likes": [], "count": 0}), 201)


@app.route("/like/<user_email>")
def get_like_by_email(user_email):
    likes = db.get_user_likes(user_email)
    if likes:

        return flask.make_response(flask.jsonify({"likes": [like.__dict__ for like in likes]}), 200)
    return flask.make_response(flask.jsonify({"likes": []}), 200)

if __name__ == '__main__':

    app.run(debug=True,host=socket.gethostbyname(socket.gethostname()))
