from api.database import db, ma
from flask_login import UserMixin

class User(UserMixin, db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)

  def __init__(self, id, name, password):
    self.id = id
    self.name = name
    self.password = password

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

  def registUser(user):
    record = User(
      id = user['id'],
      name = user['name'],
      password = user['password']
    )
   
    # insert into users(name, address, tel, mail) values(...)
    db.session.add(record)
    db.session.commit()

    return user

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = User
      fields = ('id', 'name', 'password')
      load_instance = True