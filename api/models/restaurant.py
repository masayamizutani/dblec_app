from api.database import db, ma
from sqlalchemy.dialects.mysql import DOUBLE as Double
import folium

class Restaurant(db.Model):
  __tablename__ = 'restaurant'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), nullable=False)
  contents = db.Column(db.String(50), nullable=False)
  lat = db.Column(Double, nullable=True)
  lng = db.Column(Double, nullable=True)

  def __init__(self, id, name, contents, lat, lng):
    self.id = id
    self.name = name
    self.contents = contents
    self.lat = lat
    self.lng = lng

  def __repr__(self):
    return '<Restaurant %r>' % self.id

  def getRestaurantList():

    # select * from user
    Restaurant_list = db.session.query(Restaurant).all()

    if Restaurant_list == None:
      return []
    else:
      return Restaurant_list

  def getFilteredRestaurant(id):
    restaurant = db.session.query(Restaurant).filter_by(id = id)
    return restaurant

  def registRestaurant(restaurant):
    # print(id)
    # id = 
    record = Restaurant(
      # id = id,
      name = restaurant['name'],
      contents = restaurant['contents'],
    )
   
    # insert into users(name, password) values(...)
    db.session.add(record)
    db.session.commit()

    return restaurant

  def showMap(self):
    copyright_osm = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    location = [self.lat, self.lng]
    map_ = folium.Map(location=location,
                    attr=copyright_osm,
                    zoom_start=17,
                    width='30%',
                    height='30%')
    folium.Marker(location, popup=self.name).add_to(map_)
    
    return map_


class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = Restaurant
      fields = ('id', 'name', 'contents')
      load_instance = True