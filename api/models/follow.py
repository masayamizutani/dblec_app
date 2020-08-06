from api.database import db, ma
from .user import User
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from marshmallow import Schema, fields

# follower = db.Table('follow',
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
  #follweres = db.session.query(Follow).outerjoin(Follow, User.id == Follow.follower_id)
  #followers = db.session.query(followers).outerjoin(followers, User.id == followers.inverse_follower_id)
  #user = relationship(
  #  'User', secondary="user",
  #  primaryjoin=(follower_id == User.id),
  #  secondaryjoin=(inverse_follower_id == User.id),
  #  backref=db.backref('follow', lazy="joined"), lazy="joined"
  #  )
  #print(type(user))

  follower = relationship(
    'User',
    primaryjoin=(follower_id == User.id),
    #backref="user"
  )

  inverse_follower = relationship(
    'User',
    primaryjoin=(inverse_follower_id == User.id),
    #backref="user"
  )

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
      db.session.query(Follow).filter_by(follower_id = unfollow["follower_id"], inverse_follower_id = unfollow["inverse_follower_id"]).delete()
      db.session.commit()

    return unfollow

  def is_following(follow):
    follower = db.session.query(Follow).filter_by(follower_id = follow["follower_id"], inverse_follower_id = follow["inverse_follower_id"]).first()
    return True if follower != None else False
  
  def getFollowerList(user_id):
    follower = db.session.query(Follow).filter_by(follower_id = user_id).all()
    return follower
  
  def getFollowedList(user_id):
    followed = db.session.query(Follow).filter_by(inverse_follower_id = user_id).all()
    return followed

  def getFollowingsByIdJoin(user_id):
    following = db.session.query(Follow).filter_by(follower_id=user_id).join(User, User.id == Follow.inverse_follower_id).all()
    # report = db.session.query(Report).filter(Report.user_id.in_(user_ids), Report.restaurant_id == restaurant_id)
    # report = db.session.query(Report).filter(Report.user_id == user_ids, Report.restaurant_id == restaurant_id)
    return following
  #def getFollowingsByUserIds(use_id):
  #  followed = db.session.query(Follow).filter_by(inverse_follower_id = user_id).all()

  def getFollowedByIdJoin(user_id):
    following = db.session.query(Follow).filter_by(inverse_follower_id=user_id).join(User, User.id == Follow.follower_id).all()
    # report = db.session.query(Report).filter(Report.user_id.in_(user_ids), Report.restaurant_id == restaurant_id)
    # report = db.session.query(Report).filter(Report.user_id == user_ids, Report.restaurant_id == restaurant_id)
    return following

class FollowSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = Follow
      fields = ('follower_id', 'inverse_follower_id')
      load_instance = True

class FollowerJoinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = Follow
      fields = ('follower_id', 'inverse_follower_id', 'follower', 'inverse_follower')
      #user = fields
      load_instance = True