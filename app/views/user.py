import bcrypt

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt_identity

from ..jwt.blacklist import BLACKLIST
from ..db import db
from ..models import UserModel
from ..schemas import UserSchema


blp = Blueprint('users', __name__, description='Users API')


def _create_tokens(user):
    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_access_token(identity=user.id)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@blp.route('/register')
class UserRegisterView(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201)
    @blp.alt_response(400, description='User already exists')
    def post(self, data):
        username = data['username']
        if UserModel.query.filter(UserModel.username == username).first():
            abort(400, message='A user with that username already exists.')

        hash_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user = UserModel(username=username, password=hash_password)
        db.session.add(user)
        db.session.commit()

        return _create_tokens(user)


@blp.route('/login')
class UserLoginView(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200)
    @blp.alt_response(401, description='Invalid credentials')
    def post(self, data):
        username = data['username']
        password = data['password']
        user = UserModel.query.filter(UserModel.username == username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            return _create_tokens(user)
        abort(401, message='Invalid credentials')


@blp.route('/refresh')
class UserRefreshView(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {'access_token': access_token}


@blp.route('/logout')
class UserLogoutView(MethodView):
    @jwt_required(fresh=True)
    @blp.response(200)
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return ''


@blp.route('/users/<int:id>')
class UserView(MethodView):
    @jwt_required(fresh=True)
    @blp.response(200, UserSchema)
    @blp.alt_response(404, description='User not found')
    def get(self, id):
        user = UserModel.query.get_or_404(id)
        return user

    @jwt_required(fresh=True)
    @blp.response(204)
    @blp.alt_response(404, description='User not found')
    def delete(self, id):
        user = UserModel.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return ''
