from evoting import login_manager
import flask_login

class User(flask_login.UserMixin):
    def __init__(self, pesel):
        self.id = pesel

@login_manager.user_loader
def user_loader(pesel):
    return User(pesel)

@login_manager.request_loader
def request_loader(pesel):
    return User(pesel)