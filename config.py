class SystemConfig:

  DEBUG = True

  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': 'root',
      'password': 'dblec2020',
      'host': 'localhost:3306',
      'db_name': 'dblec'
  })

Config = SystemConfig