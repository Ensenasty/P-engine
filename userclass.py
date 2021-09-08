from flask_login import UserMixin
from logzero import logger as log


class User(UserMixin):
    """A user of this page"""

    # @property
    # def is_authenticated(self):
    #     ...
    #     log.warning("{} not implemented yet..." % __name__)
    #     return False

    # @property
    # def is_active(self):
    #     log.warning("{} not implemented yet..." % __name__)
    #     ...
    #     return True

    # @property
    # def is_anonymous(self):
    #     log.warning("{} not implemented yet..." % __name__)
    #     ...
    #     return False

    # def get_id(self):
    #     log.warning("{} not implemented yet..." % __name__)
    #     return str(self.id)

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
