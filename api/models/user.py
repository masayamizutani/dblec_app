from api.database import db, ma
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.name = 'Guest'

class User(UserMixin, db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)

  def __init__(self, name, password):
    # self.id = id
    self.name = name
    self.password = password
    # self.followed = followed

  def __repr__(self):
    return '<User %r>' % self.name

  def getUserList():

    # select * from user
    user_list = db.session.query(User).all()

    if user_list == None:
      return []
    else:
      return user_list

  def getFilteredUser(name):
    user = db.session.query(User).filter_by(name = name)
    return user
  
  def getFilteredUserById(self, user_id):
    user = db.session.query(User).filter_by(id = user_id)
    return user

  def registUser(user):
    # print(id)
    # id = 
    # user_id = db.session.query(User).order_by(db.desc(User.id.desc())).limit(1).first()
    # user_list = db.session.query(User).all()
    record = User(
      # id = user_id+1,
      name = user["name"],
      password = user["password"]
      # followed = self.followed
    )
   
    # insert into users(name, password) values(...)
    db.session.add(record)
    db.session.flush()
    db.session.commit()

    return user

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = User
      fields = ('id', 'name', 'password')
      load_instance = True