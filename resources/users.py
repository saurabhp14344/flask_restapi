from flask_restful import Resource, reqparse
from models.users import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field can not be left blank!')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field can not be left blank!')

    def post(self):
        data = UserRegister.parser.parse_args()
        # check user exist or not
        if UserModel.find_user_mapping(data['username']):
            return {'message': 'user already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User create successfully.'}
