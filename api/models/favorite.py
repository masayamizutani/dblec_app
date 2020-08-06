from api.database import db, ma
from .user import User
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

# followers = db.Table('follow',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('inverse_follower_id', db.Integer, db.ForeignKey('user.id'))
# )

class Follow(db.Model):
  __tablename__ = 'follow'

  follower_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
  inverse_follower_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True, nullable=False)

  #user = relationship("User") 
  #user = db.Tabel('user')
  #joined = db.session.query(user).filter(db.followed_id == user.id)
  follwers = db.session.query(Follow).outerjoin(Follow, User.id == Follow.follower_id).all()
  #user = relationship(
  #  'User', secondary=,
  #  primaryjoin=(follower_id == User.id),
  #  secondaryjoin=(inverse_follower_id == User.id),
  #  backref=db.backref('follow', lazy='dynamic'),
  #  lazy='dynamic')
  #print(user)

  def __init__(self, follower_id, inverse_follower_id):
    self.follower_id = follower_id,
    self.inverse_follower_id = inverse_follower_id

  def __repr__(self):
    return '<follow>'

  def follow(follow):
    if not Follow.is_following(follow):
      record = Follow(
        # id = id,
        follower_id = follow['follower_id'],
        inverse_follower_id = follow['inverse_follower_id'],
      )
    
      # insert into users(name, password) values(...)
      db.session.add(record)
      db.session.commit()

    return follow

  def unfollow(unfollow):  
    follower =  Follow.is_following(unfollow)
    if follower:
      # record = Follow(
      #   # id = id,
      #   follower_id = unfollow['follower_id'],
      #   inverse_follower_id = unfollow['inverse_follower_id'],
      # )
    
      # insert into users(name, password) values(...)
      db.session.delete(follower)
      db.session.commit()

    return unfollow

  def is_following(follow):
    follower = db.session.query(Follow).filter_by(follower_id = follow["follower_id"], inverse_follower_id = follow["inverse_follower_id"]).first()
    return follower if follower != None else False
  
  def getFollowerList(user_id):
    follower = db.session.query(Follow).filter_by(follower_id = user_id).all()
    return follower
  
  def getFollowedList(user_id):
    followed = db.session.query(Follow).filter_by(inverse_follower_id = user_id).all()
    return followed

  def join_followed():
    user = db.Tabel('user')
    joined = db.session.query(user).filter(db.followed_id == テーブル2.hoge_id)
    #: join()で結合させたいテーブルと条件を指定しselect()を呼び出し
    q = join(followed, pets, events.c.name == pets.c.name) \
        .select() \
        .where(events.c.type == 'litter')
    #: 最後にwith_only_columns()に取得したいカラムのリストを渡す    
    q =  q.with_only_columns(columns)

class FollowSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = Follow
      fields = ('follower_id', 'inverse_follower_id')
      load_instance = True

class FollowerJoinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = Follow
      fields = ('follower_id', 'inverse_follower_id', 'follower_name')
      load_instance = True