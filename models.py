import os
from sqlalchemy import (
  Column,
  String,
  Integer,
  create_engine,
  select,
  func,
  DateTime
)
from datetime import datetime
from constants import (
  database_setup,
  jsonData,
  SECRET_KEY
)
import dateutil.parser
import babel
from sqlalchemy.orm import column_property
from flask_sqlalchemy import SQLAlchemy
import json
from flask import Flask
import pandas as pd
from flask_moment import Moment
#from manage import migration

# ------------------------------------------------------------------------------------------------------#
# *                        Configures DB connection
# *                                  and
# *               Binds flask application to SQLAlchemy service
# ------------------------------------------------------------------------------------------------------#
# *Global use or Local use (defaults to local if global isn't found)
database_path = os.environ.get('DATABASE_URL', "postgres://{}:{}@{}/{}".format(
    database_setup["user_name"], database_setup["password"], database_setup["port"], database_setup["database_name"]))

# ! OR just Local use below:
#  # database_path ="postgresql+psycopg2://{}:{}@{}/{}".format(database_setup['user_name'], database_setup['password'], database_setup['port'], database_setup['database_name'])

# ! For intergrating PANDAS
#  engine = create_engine(database_path)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    db.app = app
    db.init_app(app)
    db.create_all()
    
    # *-------------------------Configure Moment--------------------------#
    # *                       Formats Dates & Time
    # *-------------------------------------------------------------------#
    moment = Moment(app)
    
    #  ?----------------------------------------------------------------------------#
    #  ?                               OPTIONAL
    #  ?                      Localize Migration setup
    #  ?----------------------------------------------------------------------------#
    # migration(app,db)



# ------------------------------------------------------------------------------------------------------#
# *              Functions for dropping, creating, and initializing data within the database
# ------------------------------------------------------------------------------------------------------#
# *Drops and creates tables
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


# * Using CSV with Pandas
def db_initialize_tables_csv_pandas():
    engine = db.get_engine()
    csv_file_path = 'C:/Users/Public/bays_.csv'
    #  Read CSV with Pandas
    df = pd.read_csv(csv_file_path)
    print(df)
    #  Insert to DB
    df.to_sql('bays',
              con=engine,
              index=True,
              index_label='id',
              if_exists='replace')

# * Using Stored constant dictionary variables as the JSON data


def db_initialize_tables_json():
    # for i in jsonData:
    #     # print(i)
    #     for j in i['data']:
    #         new_bay = (Bay(
    #             bay=i['bay'],
    #             section=j['section'],
    #             name=j['name'],
    #             style=j['style'],
    #             row=j['row'],
    #             col=j['col'],
    #             notes=j['notes'],
    #             gender=j['gender'],
    #             img=j['img'],
    #         ))
    #         new_bay.insert()
    pass


# *----------------------------------------------------------------------------#
# *                            Models - ORM
# *----------------------------------------------------------------------------#
class Venue(db.Model):
      __tablename__ = 'venue'

      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String)
      city = db.Column(db.String(120))
      state = db.Column(db.String(120))
      address = db.Column(db.String(120))
      phone = db.Column(db.String(120))
      genres = db.Column(db.ARRAY(db.String(120))) 
      website_link = db.Column(db.String(120))
      image_link = db.Column(db.String(500))
      facebook_link = db.Column(db.String(120))
      seeking_talent = db.Column(db.Boolean, default = False)
      seeking_description = db.Column(db.String(250))
      num_of_shows = db.Column(db.Integer, default = 0)
      shows = db.relationship('Show', backref='venue', lazy=True)
      deleted = db.Column(db.Boolean, default = False)
      
      def __repr__(self):
        return f'<Venue {self.id} {self.name}>'
      
      
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(250))
    num_of_shows = db.Column(db.Integer, default = 0)
    shows = db.relationship('Show', backref='artist', lazy=True)
    deleted = db.Column(db.Boolean, default = False)
    
    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'



# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    deleted = db.Column(db.Boolean, default = False)
    feature_time = db.Column(db.DateTime, nullable=True)
    created_time = db.Column(db.DateTime, nullable=True, default=datetime.today())
    

# *----------------------------------------------------------------------------#
# *                             Filters.
# *----------------------------------------------------------------------------#

# * Moment Format Function
def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


# ! Optional reset PK int values
# def manageSequence(tableName,className):
#     #? ***REVISION LATER*** :  COUNT() Takes too long in large databases
#     #* maxCount = select([func.count()]).select_from(Todo)
#     maxCount = db.session.query(className).all().count(className.id)
#     #* Reset the auto PK increment sequence to current max
#     alterSeq= "ALTER SEQUENCE " + tableName +"_id_seq RESTART WITH " + str(maxCount) #substitute for 1 if starting off empty with todos
#     db.session.execute(alterSeq)
#     db.session.commit()
#     db.session.close()  
    
# *Reset chosen table
#manageSequence("venue",Venue)
 