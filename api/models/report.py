from api.database import db, ma
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy import desc
from .user import User
from .restaurant import Restaurant
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
import datetime

class Report(db.Model):
  __tablename__ = 'report'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
  contents = db.Column(db.String(50), nullable=False)
  score = db.Column(db.Integer, nullable=False)
  restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.id'), nullable=False)
  created_at = db.Column(Timestamp, default=datetime.datetime.now())

  user = relationship("User", backref="report")
  restaurant = relationship("Restaurant", backref="report")
  # report = relationship("Report", backref="users")

  def __init__(self, user_id, contents, score, restaurant_id):
    # self.id = id
    self.user_id = user_id
    self.contents = contents
    self.score = score
    self.restaurant_id = restaurant_id

  def __repr__(self):
    return '<Report %r>' % self.id

  def getReport(id):
    report = db.session.query(Report).filter_by(id=id).all()
    return report

  def getReportList():

    # select * from user
    report_list = db.session.query(Report).all()

    if report_list == None:
      return []
    else:
      return report_list

  def getFilteredReport(user_id):
    report = db.session.query(Report).\
      filter_by(user_id = user_id).\
      join(User, User.id == Report.user_id).\
      join(Restaurant, Restaurant.id == Report.restaurant_id).\
      order_by(desc(Report.created_at)).all()
    return report

  def getFilteredReportByUserIds(user_ids):
    report = db.session.query(Report).\
      filter(Report.user_id.in_(user_ids)).\
      join(User, User.id == Report.user_id).\
      join(Restaurant, Restaurant.id == Report.restaurant_id).\
      order_by(desc(Report.created_at)).all()
    # report = db.session.query(Report).filter(Report.user_id == user_ids, Report.restaurant_id == restaurant_id)
    return report

  def getFilteredReportByRestaurantId(restaurant_id):
    report = db.session.query(Report).\
    filter_by(restaurant_id = restaurant_id).\
    join(User, User.id == Report.user_id).\
    join(Restaurant, Restaurant.id == Report.restaurant_id).\
    order_by(desc(Report.created_at)).all()
    return report
  
  def getFilteredReportByIds(user_ids, restaurant_id):
    report = db.session.query(Report).filter(Report.user_id.in_(user_ids), Report.restaurant_id == restaurant_id).join(User, User.id == Report.user_id).join(Restaurant, Restaurant.id == Report.restaurant_id).all()
    score = 0
    if len(report) != 0:
      score = db.session.query(func.avg(Report.score)).filter(Report.user_id.in_(user_ids), Report.restaurant_id == restaurant_id).first()[0]
    score = '{:.1f}'.format(score)
    return report, score
  
  def getFilteredReportByIdsJoin(user_ids, restaurant_id):
    report = db.session.query(Report).filter(Report.user_id.in_(user_ids), Report.restaurant_id == restaurant_id).join(User, User.id == Report.user_id).join(Restaurant, Restaurant.id == Report.restaurant_id).all()
    # report = db.session.query(Report).filter(Report.user_id.in_(user_ids), Report.restaurant_id == restaurant_id)
    # report = db.session.query(Report).filter(Report.user_id == user_ids, Report.restaurant_id == restaurant_id)
    return report

  def deleteReport(id):
    db.session.query(Report).filter(Report.id==id).delete()
    db.session.commit()

  def updateReport(report):
    report_object = db.session.query(Report).filter_by(id=report['id']).first()
    report_object.contents = report['contents']
    report_object.score = report['score']
   
    db.session.commit()
    return report

  def registReport(report):
    # print(id)
    # id = 
    record = Report(
      # id = id,
      user_id = report['user_id'],
      contents = report['contents'],
      score = report['score'],
      restaurant_id = report['restaurant_id'],
    )
   
    # insert into users(name, password) values(...)
    db.session.add(record)
    db.session.commit()

    return report

class ReportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = Report
      fields = ('id', 'user_id', 'contents', 'score', 'restaurant_id')
      load_instance = True

class ReportJoinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = Report
      fields = ('id', 'user_id', 'contents', 'score', 'restaurant_id', 'created_at', 'user', 'restaurant')
      load_instance = True