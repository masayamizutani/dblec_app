from flask import Blueprint, request, make_response, jsonify, Response, render_template, abort
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from collections import defaultdict
from api.models.user import User, UserSchema, Anonymous
from api.models.report import Report, ReportSchema, ReportJoinSchema
from api.models.restaurant import Restaurant, RestaurantSchema
from api.models.follow import Follow, FollowSchema, FollowerJoinSchema
import json

# ルーティング設定
user_router = Blueprint('user_router', __name__)
login_manager = LoginManager()
login_manager.anonymous_user = Anonymous

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

# @user_router.route('/')
# def home():
#     return render_template("home.html", username=current_user.name)

# ログインしないと表示されないパス
@user_router.route('/protected/')
@login_required
def protected():
    return render_template("home.html", username=current_user.name)

@user_router.route('/login/', methods=['GET', 'POST'])
def login():
    if(request.method == "POST"):
        user_name = request.form["username"]
        user_object = User.getFilteredUser(name=user_name)
        user_schema = UserSchema(many=True)
        try:
            user = user_schema.dump(user_object)[0]
        except IndexError as e:
            return abort(401)
        
        # ユーザーチェック
        if(request.form["username"] == user['name'] and request.form["password"] == user['password']):
            # ユーザーが存在した場合はログイン
            login_user(LoginUser(username=user['name'], password=user['password']))

            user = User.getFilteredUser(user['name'])
            user_schema = UserSchema(many=True)
            user_id = user_schema.dump(user)[0]['id']
            follower_list = Follow.getFollowerList(user_id)
            follower_ids = [follower.inverse_follower_id for follower in follower_list]
            follower_ids.append(user_id)
            report = Report.getFilteredReportByUserIds(follower_ids)
            report_schema = ReportJoinSchema(many=True)
            return render_template("reports.html", reports=report_schema.dump(report), username=user_name)

            # return render_template("home.html", username=user_name)
        else:
            return abort(401)
    else:
        return render_template("login.html")

# ログアウトパス
@user_router.route('/logout/')
@login_required
def logout():
    logout_user()
    return render_template("home.html", username=current_user.name)

@user_router.route('/signup/', methods=['GET', 'POST'])
def signup():
    if(request.method == "POST"):
        user_name = request.form["username"]
        password = request.form["password"]
        user_object = User.getFilteredUser(user_name)
        user_schema = UserSchema(many=True)
        # print(user_schema.dump(user_object))
        # user = user_schema.dump(user_object)[0]
        # ユーザーチェック
        if len(user_schema.dump(user_object)) == 0:
            # ユーザーが存在しない場合は新規作成
            userData = {
                'name': user_name,
                'password': password
            }
            user = User.registUser(userData)
            user_schema = UserSchema(many=True)
            login_user(LoginUser(user_name, password))
            # return render_template("home.html")
            user = User.getFilteredUser(user_name)
            user_schema = UserSchema(many=True)
            user_id = user_schema.dump(user)[0]['id']
            follower_list = Follow.getFollowerList(user_id)
            follower_ids = [follower.inverse_follower_id for follower in follower_list]
            follower_ids.append(user_id)
            report = Report.getFilteredReportByUserIds(follower_ids)
            report_schema = ReportJoinSchema(many=True)
            return render_template("reports.html", reports=report_schema.dump(report), username=user_name)
        else:
            return abort(401)
    else:
        return render_template("signup.html")
'''
@user_router.route('/user/<username>', methods=['GET'])
def showUserReports(username):
    # cont = session.query(Content).all()
    # user = User.getFilteredUser("mizutani")
    user = User.getFilteredUser(username)
    user_schema = UserSchema(many=True)
    uid = user_schema.dump(user)[0]['id']
    # print(type(user))
    # uid = 1
    report = Report.getFilteredReport(uid)
    report_schema = ReportSchema(many=True)
    # return render_template("reports.html", reports=report_schema.dump(report), users=user_schema.dump(user))
    return render_template("reports.html", reports=report_schema.dump(report))
'''

@user_router.route('/user/', methods=['GET'])
def showUsers():
    user = User.getUserList()
    user_schema = UserSchema(many=True)
    return render_template("users.html", users=user_schema.dump(user))


@user_router.route('/user/<username>', methods=['GET'])
def showUserPage(username):
    user = User.getFilteredUser(username)
    user_schema = UserSchema(many=True)
    uid = user_schema.dump(user)[0]['id']
    report = Report.getFilteredReport(uid)
    # report_schema = ReportSchema(many=True)
    report_schema = ReportJoinSchema(many=True)
    cnt_follower = len(Follow.getFollowerList(uid))
    cnt_followed = len(Follow.getFollowedList(uid))
    if current_user.name == username:
        is_follow = False
    record = {
        'follower_id': current_user.id,
        'inverse_follower_id': uid
    }
    is_follow = Follow.is_following(record)
    
    return render_template("mypage.html", myid=current_user.id, uid=uid, is_follow=is_follow, login_user=current_user.name, username=username, cnt_follower=cnt_follower, cnt_followed=cnt_followed, reports=report_schema.dump(report))

@user_router.route('/user/<username>/following', methods=['GET'])
def showFollwers(username):
    user = User.getFilteredUser(username)
    user_schema = UserSchema(many=True)
    uid = user_schema.dump(user)[0]['id']
    following_ids = Follow.getFollowingsByIdJoin(uid)
    follower_schema = FollowerJoinSchema(many=True)
    #print(following_ids[0])
    # follower_names = 
    #return render_template("following.html", users=follower_ids)
    #print((follower_schema.dump(following_ids)[0]))
    return render_template("following.html", users=follower_schema.dump(following_ids), rel='follower')

@user_router.route('/user/<username>/followed', methods=['GET'])
def showFollweds(username):
    user = User.getFilteredUser(username)
    user_schema = UserSchema(many=True)
    uid = user_schema.dump(user)[0]['id']
    followed_ids = Follow.getFollowedList(uid)
    follower_schema = FollowerJoinSchema(many=True)
    
    return render_template("following.html", users=follower_schema.dump(followed_ids), rel='inverse_follower')

@user_router.route('/report/', methods=['POST'])
def postReport():
    print(request.form["restaurant_id"])
    record = {
        'user_id': current_user.id,
        'contents': request.form['contents'],
        'score': request.form["score"],
        'restaurant_id': request.form["restaurant_id"]
    }
    report = Report.registReport(record)
    return '''
    送信しました！
    <FORM>
        <INPUT type="button" value="戻る" onClick="history.back()">
    </FORM>
    '''

@user_router.route('/report/delete/', methods=['POST'])
def deleteReport():
    report = Report.deleteReport(request.form["id"])
    return '''
    削除しました！
    <FORM>
        <INPUT type="button" value="戻る" onClick="history.back()">
    </FORM>
    '''

@user_router.route('/report/edit/', methods=['GET', 'POST'])
def editReport():
    if request.method == 'POST':
        record = {
            'id': request.form['id'],
            'contents': request.form['contents'],
            'score': request.form["score"],
        }
        report = Report.updateReport(record)
        return '''
        更新しました！
        <FORM>
            <INPUT type="button" value="戻る" onClick="history.back(-2)">
        </FORM>
        '''
    else:
        report_object = Report.getReport(request.args.get('id'))
        # print(report)
        report_schema = ReportJoinSchema(many=True)
        report = report_schema.dump(report_object)[0]
        return render_template("edit.html", report=report)

@user_router.route('/', methods=['GET'])
def showReports():
    # cont = session.query(Content).all()
    # user = User.getFilteredUser("mizutani")
    if current_user.is_active:
        user_id = current_user.id
        follower_list = Follow.getFollowerList(user_id)
        follower_ids = [follower.inverse_follower_id for follower in follower_list]
        follower_ids.append(user_id)
        report = Report.getFilteredReportByUserIds(follower_ids)
        # report = Report.getFilteredReportByIdsJoin(follower_ids)
        # report_schema = ReportSchema(many=True)
        report_schema = ReportJoinSchema(many=True)
        # user = User.getUserList()
        # user_schema = UserSchema(many=True)
        # return render_template("reports.html", reports=report_schema.dump(report), users=user_schema.dump(user))
        return render_template("reports.html", reports=report_schema.dump(report))
    else:
        return render_template("home.html")


@user_router.route('/restaurant/', methods=['GET'])
def showRestaurants():
    restaurant = Restaurant.getRestaurantList()
    restaurant_schema = RestaurantSchema(many=True)
    return render_template("restaurants.html", restaurants=restaurant_schema.dump(restaurant))

@user_router.route('/restaurant/<restaurant_id>', methods=['GET'])
def showRestaurantReports(restaurant_id):
    restaurant = Restaurant.getFilteredRestaurant(restaurant_id)
    restaurant_schema = RestaurantSchema(many=True)
    # report = Report.getFilteredReportByRestaurantId(restaurant_id)
    # ここにfollowいれる
    user_id = current_user.id
    follower_list = Follow.getFollowerList(user_id)
    uids = [follower.inverse_follower_id for follower in follower_list]
    uids.append(user_id)
    # uids = [1,2]
    report, score = Report.getFilteredReportByIds(uids, restaurant_id)
    # report_schema = ReportSchema(many=True)
    report_schema = ReportJoinSchema(many=True)
    # print(report_schema.dump(report))
    return render_template("restaurant.html", restaurant=restaurant_schema.dump(restaurant)[0], reports=report_schema.dump(report), score=score)

@user_router.route('/follow/', methods=['POST'])
def follow():
    record = {
        'follower_id': request.form["follower_id"],
        'inverse_follower_id': request.form["inverse_follower_id"]
    }
    follow = Follow.follow(record)
    return '''
    フォローしました！
    <FORM>
        <INPUT type="button" value="戻る" onClick="history.back(-2)">
    </FORM>
    '''

@user_router.route('/unfollow/', methods=['POST'])
def unfollow():
    record = {
        'follower_id': request.form["follower_id"],
        'inverse_follower_id': request.form["inverse_follower_id"]
    }
    unfollow = Follow.unfollow(record)
    return'''
    フォロー解除しました！
    <FORM>
        <INPUT type="button" value="戻る" onClick="history.back(-2)">
    </FORM>
    '''

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

