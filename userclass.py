from flask_login import UserMixin
from logzero import logger as log


class User(UserMixin):
    """A user of this page"""

    def __init__(self,tg_data):
        self.id = str(tg_data["id"])
        self.first_name = tg_data["first_name"]
        self.last_name = tg_data["last_name"]
        self.username = tg_data["username"]
        self.auth_date = tg_data["auth_date"]
        self.photo_url = tg_data["photo_url"]

    @property
    def is_authenticated(self):
        log.debug("{} ck" % __name__)
        return False

    @property
    def is_active(self):
        log.debug("{} ck" % __name__)
        return True

    @property
    def is_anonymous(self):
        log.debug("{} ck" % __name__)
        return False

    def get_id(self):
        log.warning("{} not implemented yet..." % __name__)
        return str(self.id)

    # def logout(self):
    #     log.warning("{} not implemented yet..." % __name__)
    #     ...
    #     return True

    @property
    def id(self):
        log.warning("{} not implemented yet..." % __name__)
        return 1

    def logout(self):
        log.warning("{} not implemented yet..." % __name__)
        return 1
