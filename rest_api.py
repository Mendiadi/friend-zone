import functools
import hashlib
import flask, flask_login

# my imports
import configure
import database

if not configure.app_config:
    print("cant run")
    exit(-1)
app = flask.Flask(configure.app_config.name)
app.secret_key = "secret"


login_manager = flask_login.LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

db = database.DataBase.get(configure.app_config)


@login_manager.user_loader
def load_user(user_id):
    return db.get_user_by_id(user_id)


@app.route("/")
def index():
    return flask.jsonify({"connection": "ok"})


@app.route("/api/user/<string:email>")
def get_user_by_email(email):
    u = db.get_user(email)
    if u:
        return flask.make_response(flask.jsonify(u.__dict__), 200)
    return flask.make_response(flask.jsonify({"error": "user not found"}), 404)


@app.route("/api/user/<int:user_id>")
def get_user_by_id(user_id):
    u = db.get_user_by_id(user_id)
    if u:
        return flask.make_response(flask.jsonify(u.__dict__), 200)
    return flask.make_response(flask.jsonify({"error": "user not found"}), 404)


@app.route("/api/register", methods=["POST"])
def register():
    user_data = database.user(db.AUTO_INC(), flask.request.json['email'],
                              flask.request.json['password'], [0], [0])
    hash = hashlib.md5(user_data.password.encode()).hexdigest()
    user_data.password = hash
    if db.add_user(user_data):
        return flask.make_response(flask.jsonify(db.get_user(user_data.email).__dict__), 201)
    return flask.make_response(flask.jsonify({"error": "user already exists"}), 400)


@app.route("/api/login", methods=["POST"])
def login():
    user_data = database.user(db.AUTO_INC(), flask.request.json['email'],
                              flask.request.json['password'], [0], [0])
    hash = hashlib.md5(user_data.password.encode()).hexdigest()
    user_from_db = db.get_user(user_data.email)
    if not user_from_db:
        return flask.make_response(flask.jsonify({"error": "user not found"}), 404)
    if hash != user_from_db.password:
        return flask.make_response(flask.jsonify({"error": "user pass wrong"}), 400)

    flask_login.login_user(user_from_db, remember=True)
    print(f"[LOGGER] {flask_login.current_user.__dict__}")
    return flask.make_response(flask.jsonify({"login": f"user {user_from_db.email}"}), 200)


@app.route("/api/logout")
@flask_login.login_required
def logout():
    u = flask_login.current_user
    flask_login.logout_user()
    print(f"[LOGGER] {flask_login.current_user.__dict__}")
    return flask.make_response(flask.jsonify({"logout": f"user {u}"}), 200)


@app.route("/api/post", methods=["POST"])
@flask_login.login_required
def create_post():
    print(f"[LOGGER] {flask_login.current_user.__dict__}")
    user_from_db = db.get_user(flask_login.current_user.email)
    if not user_from_db:
        return flask.make_response(flask.jsonify({"error": "user not found"}), 404)
    post_data = database.post(None, flask.request.json['text'], None, None)
    post_data.post_id = db.AUTO_INC()
    post_data.user_id = user_from_db.user_id
    post_data.time = db.AUTO_INC()
    if db.add_post(post_data):
        return flask.make_response(flask.jsonify(post_data.__dict__), 201)
    return flask.make_response(flask.jsonify({"error": "post error"}), 400)


@app.route("/api/<string:user_>/post", methods=["GET"])
def get_posts_by_user(user_):
    user_from_db = db.get_user(user_)
    if not user_from_db:
        return flask.make_response(flask.jsonify({"error": "user not found"}), 404)
    posts = db.get_posts_by_user(user_from_db.user_id)
    if not posts:
        posts = []
    else:
        posts = [post.__dict__ for post in posts]

    return flask.make_response(flask.jsonify({"posts": posts}), 200)


@app.route("/api/post/delete/<int:post_id>", methods=["DELETE"])
@flask_login.login_required
def delete_post(post_id):
    if db.delete_post(post_id):
        return flask.make_response(flask.jsonify({"deleted": "ok"}), 200)
    return flask.make_response(flask.jsonify({"error": "post not found"}), 404)


@app.route("/api/posts")
def get_all_posts():
    posts = db.get_all_posts()
    posts = [post.__dict__ for post in posts]
    return flask.make_response(flask.jsonify({"posts": posts}), 200)


@app.route("/api/search/<string:query>")
def search(query):
    users = db.get_users()
    res = []
    for user in users:
        if query in user.email:
            res.append(user.__dict__)

    return flask.make_response(flask.jsonify({"users": res}), 200)


@app.route("/api/post/edit/<int:post_id>", methods=["PUT"])
@flask_login.login_required
def update_post(post_id):
    data = database.post(**flask.request.json)

    if int(post_id) != int(data.post_id):
        return flask.make_response(flask.jsonify({"error": "post id modified"}), 400)
    if not db.update_post(data, data.post_id):
        return flask.make_response(flask.jsonify({"error": "something went wrong"}), 400)
    return flask.make_response(flask.jsonify({"post": data.__dict__}), 201)


@app.route("/api/post/like/<int:post_id>", methods=["POST"])
@flask_login.login_required
def like_post(post_id):
    if db.get_post_by_id(post_id):
        data = database.likes(flask_login.current_user.user_id, flask.request.json['post_id'])
        print(f"[LOG] Like {data.__dict__}")
        if int(post_id) != int(data.post_id):
            return flask.make_response(flask.jsonify({"error": "post id modified"}), 400)
        likes_user = db.get_user_likes(data.user_id)
        if likes_user:
            for like in likes_user:
                if int(like.post_id) == int(post_id):
                    db.delete_like(like)
                    return flask.make_response(flask.jsonify({"dislike": like.__dict__}), 200)
        db.add_like(data)
        return flask.make_response(flask.jsonify({"like": data.__dict__}), 201)
    return flask.make_response(flask.jsonify({"error": "post not found"}), 404)


@app.route("/api/post/<int:post_id>")
def get_post_by_id(post_id):
    post = db.get_post_by_id(post_id)
    if post:
        return flask.make_response(flask.jsonify({"post": post.__dict__}), 200)
    return flask.make_response(flask.jsonify({"error": "post not found"}), 404)


@app.route("/api/post/like/<int:post_id>", methods=["GET"])
def get_like_by_post(post_id):
    if not db.get_post_by_id(post_id):
        return flask.make_response(flask.jsonify({"error": "post not found"}), 404)
    like_ = db.get_post_likes(post_id)
    if like_:
        return flask.make_response(flask.jsonify({"likes": [like__.__dict__
                                                            for like__ in like_], "count": len(like_)}), 201)
    return flask.make_response(flask.jsonify({"likes": [], "count": 0}), 201)


@app.route("/api/user/follow/<int:user_id>", methods=["post"])
@flask_login.login_required
def follow_user(user_id):
    u = db.get_user_by_id(user_id)
    print(f"[LOGG] {u.followers}")
    if not u:
        return flask.make_response(flask.jsonify({"error": "user not found"}), 404)
    c_user = flask_login.current_user
    if c_user.user_id not in u.followers:
        u.followers.append(c_user.user_id)
        c_user.following.append(u.user_id)
        db.update_user(c_user)
        db.update_user(u)
        print(f"{c_user} has follow {u}")
        return flask.make_response(flask.jsonify({"follow": "followed"}), 200)

    u.followers.remove(c_user.user_id)
    c_user.following.remove(u.user_id)
    db.update_user(c_user)
    db.update_user(u)
    print(f"{c_user.email} has stop follow {u.email}")
    return flask.make_response(flask.jsonify({"follow": "stop"}), 200)



@app.route("/api/like/<string:user_email>")
@flask_login.login_required
def get_like_by_email(user_email):
    likes = db.get_user_likes(flask_login.current_user.user_id)
    if likes:
        return flask.make_response(flask.jsonify({"likes": [like.__dict__ for like in likes]}), 200)
    return flask.make_response(flask.jsonify({"likes": []}), 200)


@app.route("/api/message/",methods=['POST'])
def send_message():
    msg = database.message(**flask.request.json)

    if not db.get_user(msg.receiver):
        return flask.make_response(flask.jsonify({"error": "user not found"}), 404)
    if flask_login.current_user.email != msg.sender:
        return flask.make_response(flask.jsonify({"error": "you not logged in session"}), 400)
    msg.time = db.AUTO_INC()
    msg.msg_id = db.AUTO_INC()
    msg = db.add_message(msg)

    return flask.make_response(flask.jsonify({"message": msg.__dict__}), 200)

@app.route("/api/message/<string:user_a>/<string:user_b>")
def get_chat(user_a,user_b):
    if db.get_user(user_a) and db.get_user(user_b):
        chat = db.get_messages_by_chat(user_a,user_b)
        return flask.make_response(flask.jsonify({"chat":[msg.__dict__ for msg in chat]}), 200)
    return flask.make_response(flask.jsonify({"error": "user not found"}), 404)


if __name__ == '__main__':
    app.run(debug=True, host=configure.app_config.net_host, port=configure.app_config.port)
