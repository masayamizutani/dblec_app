from flask import Blueprint, request, make_response, jsonify, Response, render_template, abort
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from collections import defaultdict
from api.models.user import User, UserSchema
import json

# ルーティング設定
user_router = Blueprint('user_router', __name__)
login_manager = LoginManager()

@user_router.record_once
def on_load(state):
    login_manager.init_app(state.app)

class LoginUser(object):
    def __init__(self, username, password, data=None):
        self.username = username
        self.password = password
        self.data = data

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(name=username).first()

@user_router.route('/')
def home():
    return Response("home: <a href='/login/'>Login</a> <a href='/protected/'>Protected</a> <a href='/logout/'>Logout</a>")

# ログインしないと表示されないパス
@user_router.route('/protected/')
@login_required
def protected():
    return Response('''
    protected<br />
    <a href="/logout/">logout</a>
    ''')

@user_router.route('/login/', methods=['GET', 'POST'])
def login():
    if(request.method == "POST"):
        user_name = request.form["username"]
        user_object = User.getFilteredUser(user_name)
        user_schema = UserSchema(many=True)
        user = user_schema.dump(user_object)[0]
        # ユーザーチェック
        if(request.form["username"] == user['name'] and request.form["password"] == user['password']):
            # ユーザーが存在した場合はログイン
            login_user(LoginUser(user['name'], user['password']))
            return Response('''
            login success!<br />
            <a href="/protected/">protected</a><br />
            <a href="/logout/">logout</a>
            ''')
        else:
            return abort(401)
    else:
        return render_template("login.html")

# ログアウトパス
@user_router.route('/logout/')
@login_required
def logout():
    logout_user()
    return Response('''
    logout success!<br />
    <a href="/login/">login</a>
    ''')

# @user_router.route('/users', methods=['GET'])
# def getUserList():
#     user = User.getFilteredUser("mizutani")
#     user_schema = UserSchema(many=True)

#     return make_response(jsonify({
#         'code': 200,
#         'users': user_schema.dump(user)
#       }))

# @user_router.route('/users', methods=['POST'])
# def registUser():

#     # jsonデータを取得する
#     jsonData = json.dumps(request.json)
#     userData = json.loads(jsonData)
#     print(userData)

#     user = User.registUser(userData)
#     user_schema = UserSchema(many=True)

#     return make_response(jsonify({
#         'code': 200,
#         'user': user
#     }))

