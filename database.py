import simpleSQL


class user:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class DataBase:

    @staticmethod
    def get():
        return DataBase()

    def __init__(self):
        with simpleSQL.connect(host="localhost", user="root",
                               password="7874", database="fbclone",
                               create_and_ignore=True) as db:
            user_table = user(db.types.column(db.types.varchar(50), nullable=False),
                              db.types.column(db.types.varchar(100), nullable=False))
            db.create_table(user, user_table, primary_key="email")
            db.commit()

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
        print(user_)
        return user_
