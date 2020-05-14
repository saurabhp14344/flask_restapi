from werkzeug.security import safe_str_cmp
from models.users import UserModel


def authenticate(username, password):
    user = UserModel.find_user_mapping(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_id_mapping(user_id)
