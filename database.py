import simpleSQL


class user:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class post:
    def __init__(self, post_id, text, user_email):
        self.post_id = post_id
        self.text = text
        self.user_email = user_email


class DataBase:

    @staticmethod
    def get():
        return DataBase()

    def AUTO_INC(self):
        return self.AUTO_INC_

    def __init__(self):
        with simpleSQL.connect(host="localhost", user="root",
                               password="7874", database="fbclone",
                               create_and_ignore=True) as db:
            user_table = user(db.types.column(db.types.varchar(50), nullable=False),
                              db.types.column(db.types.varchar(100), nullable=False))
            post_table = post(db.types.column(db.types.integer(), auto_increment=True),
                              db.types.column(db.types.text(long=True)),
                              db.types.column(db.types.varchar(50), nullable=False))
            db.create_table(user, user_table, primary_key="email")
            db.create_table(post, post_table, primary_key="post_id",
                            auto_increment_value=100,
                            foreign_key="user_email", reference=("user", "email"))
            db.commit()
            self.AUTO_INC_ = db.AUTO_INC

    def add_user(self, user_obj: user):
        with simpleSQL.connect(host="localhost", user="root",
                               password="7874", database="fbclone",
                               create_and_ignore=True) as db:
            if not db.query_filter_by(user, "email", user_obj.email, first=True):
                db.insert_to(user, user_obj)
                code = 1
            else:
                code = 0
            db.commit()
        return code

    def add_post(self, post_obj: post):
        with simpleSQL.connect(host="localhost", user="root",
                               password="7874", database="fbclone",
                               create_and_ignore=True) as db:

            if not db.query_filter_by(post, "post_id", post_obj.post_id, first=True):
                db.insert_to(post, post_obj)
                code = 1
            else:
                code = 0
            db.commit()
        return code

    def remove_user(self, email):
        with simpleSQL.connect(host="localhost", user="root",
                               password="7874", database="fbclone",
                               create_and_ignore=True) as db:
            if db.query_filter_by(user, "email", email, first=True):
                db.query_delete_by(user, ("email", email))
                code = 1
            else:
                code = 0
            db.commit()
        return code

    def get_user(self, email):
        with simpleSQL.connect(host="localhost", user="root",
                               password="7874", database="fbclone",
                               create_and_ignore=True) as db:
            user_ = db.query_filter_by(user, "email", email, first=True)

        return user_

    def get_posts_by_user(self, user_email):
        with simpleSQL.connect(host="localhost", user="root",
                               password="7874", database="fbclone",
                               create_and_ignore=True) as db:
            users = db.query_filter_by(post, "user_email", user_email)

        return users

    def get_users(self):
        with simpleSQL.connect(host="localhost", user="root",
                               password="7874", database="fbclone",
                               create_and_ignore=True) as db:

            users = db.query_all(user)

        return users

    def delete_post(self, post_id):
        with simpleSQL.connect(host="localhost", user="root",
                               password="7874", database="fbclone",
                               create_and_ignore=True) as db:
            post_ = db.query_filter_by(post, "post_id", post_id, first=True)
            if post_:
                db.query_delete_by(post, ("post_id", post_id))
                code = 1
            else:
                code = 0
            db.commit()
        return code

    def get_all_posts(self):
        with simpleSQL.connect(host="localhost", user="root",
                               password="7874", database="fbclone",
                               create_and_ignore=True) as db:
            posts = db.query_all(post)

        return posts