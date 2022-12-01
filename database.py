import flask_login

import simpleSQL


class user(flask_login.UserMixin):
    def __init__(self, user_id, email, password, followers, following):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.followers = followers
        self.following = following

    def get_id(self):
        return str(self.user_id)


class post:
    def __init__(self, post_id, text, user_id, time):
        self.post_id = post_id
        self.text = text
        self.user_id = user_id
        self.time = time


class likes:
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id


class DataBase:

    @staticmethod
    def get(conf):
        return DataBase(conf)

    def AUTO_INC(self):
        return self.AUTO_INC_

    def __init__(self, app_conf):
        print(f"[LOG] init DATABASE start...")

        self.host = app_conf.db_host
        self.user = app_conf.user
        self.password = app_conf.password
        self.database = app_conf.database
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            user_table = user(db.types.column(db.types.integer(), nullable=False, auto_increment=True),
                              db.types.column(db.types.varchar(50), nullable=False, unique=True),
                              db.types.column(db.types.varchar(100), nullable=False),
                              db.types.column(db.types.objType(1000), nullable=False),
                              db.types.column(db.types.objType(1000), nullable=False))
            post_table = post(db.types.column(db.types.integer(), auto_increment=True),
                              db.types.column(db.types.text(50)),
                              db.types.column(db.types.integer(), nullable=False),
                              db.types.column(db.types.integer()))
            like_table = likes(db.types.column(db.types.integer(), nullable=False)
                               , db.types.column(db.types.integer(), nullable=False))

            db.create_table(user, user_table, primary_key="user_id", auto_increment_value=1000)
            db.create_table(post, post_table, primary_key="post_id",
                            foreign_key="user_id", reference=("user", "user_id"),
                            ondelete=True, onupdate=True)
            db.create_table(likes, like_table, foreign_key="post_id", reference=("post", "post_id")
                            , ondelete=True, onupdate=True)
            db.update_column_to_date("post", "time", default=True, on_update=True)
            db.query_alter_table_forgkey("likes", foreign_key="user_id", reference=("user", "user_id"),
                                         ondelete=True, onupdate=True)

            db.commit()
            self.AUTO_INC_ = db.AUTO_INC
            print(f"[LOG] init DATABASE done success...")

    def update_user(self,user_):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            db.query_update_table(user,user_)
            db.commit()


    def add_user(self, user_obj: user):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            if not db.query_filter_by(user, "user_id", user_obj.user_id, first=True):
                db.insert_to(user, user_obj)
                code = 1
            else:
                code = 0
            db.commit()
        return code

    def get_user_by_id(self, user_id) -> [user, None]:
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            u = db.query_filter_by(user, "user_id", user_id, first=True)
            if u:
                return u
            return None

    def add_post(self, post_obj: post):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:

            if not db.query_filter_by(post, "post_id", post_obj.post_id, first=True):
                db.insert_to(post, post_obj)
                code = 1
            else:
                code = 0
            db.commit()
        return code

    def remove_user(self, user_id):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            if db.query_filter_by(user, "user_id", user_id, first=True):
                db.query_delete_by(user, ("user_id", user_id))
                code = 1
            else:
                code = 0
            db.commit()
        return code

    def get_user(self, email) -> user:
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            user_ = db.query_filter_by(user, "email", email, first=True)

        return user_

    def get_posts_by_user(self, user_id):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            users = db.query_filter_by(post, "user_id", user_id)

        return users

    def get_users(self):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            users = db.query_all(user)

        return users

    def delete_like(self, like):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            # like_ = db.query_filters(post, f"post_id = \"{like.post_id}\" AND user_email = \"{like.user_email}\""
            #                          , first=True)

            db.delete(like)
            db.commit()

    def reset(self):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            db.drop_table(likes)
            db.drop_table(post)

    def delete_post(self, post_id):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            post_ = db.query_filter_by(post, "post_id", post_id, first=True)
            if post_:
                db.query_delete_by(post, ("post_id", post_id))
                code = 1
                db.commit()
            else:
                code = 0

        return code

    def get_all_posts(self):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            posts = db.query_all(post)

        return posts

    def get_user_likes(self, user_id):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            likes_ = db.query_filter_by(likes, "user_id", user_id)

        return likes_

    def get_post_likes(self, post_id):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            likes_ = db.query_filter_by(likes, "post_id", post_id)

        return likes_

    def add_like(self, like_):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            like__ = db.insert_to(likes, like_)
            db.commit()
        return like__

    def get_post_by_id(self, post_id):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:
            post_ = db.query_filter_by(post, "post_id", post_id, first=True)

        return post_

    def update_post(self, data, post_id):
        with simpleSQL.connect(host=self.host, user=self.user,
                               password=self.password, database=self.database,
                               create_and_ignore=True) as db:

            post_ = db.query_filter_by(post, "post_id", post_id, first=True)
            if not post_:
                code = 0

            else:
                db.query_update_table(post, data, prime_indexes="time")
                code = 1
                db.commit()
        return code
