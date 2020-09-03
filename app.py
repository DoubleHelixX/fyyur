#----------------------------------------------------------------------------#
# *   Imports
#----------------------------------------------------------------------------#
from colorama import (
  Fore, 
  Style
  )
from flask import (
  Flask, 
  render_template,
  request, Response,
  flash, redirect,
  url_for, jsonify
)
from models import (
  setup_db, 
  db,
  Venue,
  Artist,
  Show,
  format_datetime,
  db_drop_and_create_all,
  db_initialize_tables_json
)
from datetime import timedelta
import json
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from os import environ as env



#  *----------------------------------------------------------------------------#
#  *                                Create App
#  *----------------------------------------------------------------------------#

def create_app(test_config=None):
  app = Flask(__name__)
  app.debug = True
  setup_db(app)
  
  #  ?----------------------------------------------------------------------------#
  #  ?                               OPTIONAL
  #  ?               DROP, Create, and Initialize Database with Data
  #  ?----------------------------------------------------------------------------#
  #  db_drop_and_create_all()
  #  db_initialize_tables_json()

  #  *Checks that database configuration was processed correctly.
  #  if not configedDB:
  #    abort(500)
  
  # *-----------------------CORS (API configuration)------------------------#
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  # *----------------------- Access-Control-Allow configuration-------------#
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods',
                            'GET,POST,PATCH,PUT,DELETE,OPTIONS')
      return response
    
  
  # *set time format to specific formatting
  app.jinja_env.filters['datetime'] = format_datetime
 
  #  *----------------------------------------------------------------------------------------#
  #  *               END POINTS: GET, POST, PATCH, DELETE
  #  *----------------------------------------------------------------------------------------#

  @app.route('/')
  def index():
    return render_template('pages/home.html')
  
  
  #  *----------------------------------------------------------------------------#
  #  *                              Venue Endpoints
  #  *----------------------------------------------------------------------------#

  @app.route('/venues')
  def venues():
    error=False
    try:
      returnData=[]
      priorArea = {"state":'',
                  "city": ''}
      allVenues= Venue.query.filter(Venue.deleted==False).order_by('state','city').all()
      for venue in allVenues:
        if priorArea["state"] == venue.state and priorArea["city"] == venue.city:
          data= {
          "id": venue.id,
          "name": venue.name,
          "image_link": venue.image_link,
          "seeking_talent":venue.seeking_talent,
          "num_of_shows": venue.num_of_shows
          }        
        else:
          data= {
          "id": venue.id,
          "name": venue.name,
          "image_link": venue.image_link,
          "state": venue.state,
          "city": venue.city,
          "seeking_talent":venue.seeking_talent,
          "num_of_shows": venue.num_of_shows
          }
          
          priorArea["state"]= venue.state
          priorArea["city"] = venue.city        
        returnData.append(data)
    except():
      flash('An error occurred listing the Venues. Redirecting to home page')
      error =True
    finally:
      if(error):
        return redirect(url_for("index"))
      else:
        return render_template('pages/venues.html', venues=returnData)

  @app.route('/venues/search', methods=['POST'])
  def search_venues():
    error=False
    try:
      mockData={
        "count": 1,
        "data": [{
          "id": 2,
          "name": "The Dueling Pianos Bar",
          "num_upcoming_shows": 0,
        }]
      }
      # *Get search value from form
      searchTerm = request.form.get('search_term','').lower()
      print(f'{Fore.RED} Search Term: ' , searchTerm)
      perfectMatch =[]
      goodMatch=[]
      poorMatch=[]
      unfilteredMatch=[]
      count=0
      for row in db.session.query(Venue).filter(Venue.deleted==False).all():
        upcoming_shows = 0
        matchedVenues = Show.query.filter(Show.venue_id == row.id).all()
        if(matchedVenues):
          for venues in matchedVenues:
            if venues.start_time > datetime.today(): upcoming_shows =+1
        if searchTerm in row.name.lower():
          unfilteredMatch.append({
          "id": row.id,
          "name": row.name.title(),
          "num_upcoming_shows": upcoming_shows
          })
          count = count+1
      searchResult={
        "count": count,
        "data": unfilteredMatch
      }
    except:
      flash('An error occurred when searching for ', searchTerm )
      print(sys.exc_info())
    finally:
      db.session.close()
      if(error):
        return redirect(url_for('venues'))
      else:
        return render_template('pages/search_venues.html', results=searchResult, search_term=searchTerm)

  @app.route('/venues/<int:venue_id>')
  def show_venue(venue_id):
    error=True
    try:
      resultData=[]
      venueData = db.session.query(Venue).filter(Venue.deleted == False).all()
      for venue in venueData:
        pastShowsCount =0
        upcomingShowsCount=0
        pastShows=[]
        upcomingShows=[]
        #genres="".join(list(filter(lambda x : x!= '{' and x!='}', venue.genres ))).split(',')
        genres=venue.genres
        if venue.num_of_shows >0:
          showsData = db.session.query(Show, Artist).filter(Show.venue_id == venue.id).filter(Artist.id == Show.artist_id).all()
          for shows in showsData:
            print(f'{Fore.YELLOW} shows: {shows}')
            if shows[0].start_time > datetime.today() and not (shows[1].deleted or venue.deleted): 
              upcomingShowsCount +=1
              upcomingShows.append({
              "artist_id": shows[1].id,
              "artist_name": shows[1].name,
              "artist_image_link": shows[1].image_link,
              "start_time": str(shows[0].start_time),
              "deleted": shows[1].deleted,
              })
            else: 
              pastShowsCount +=1
              pastShows.append({
                "artist_id": shows[1].id,
                "artist_name": shows[1].name,
                "artist_image_link": shows[1].image_link,
                "start_time": str(shows[0].start_time),
                "deleted": shows[1].deleted,
              })
          
          resultData.append({
            "id": venue.id,
            "name": venue.name,
            "genres": genres,
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website":venue.website_link,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description":venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": pastShows,
            "upcoming_shows": upcomingShows,
            "past_shows_count": pastShowsCount,
            "upcoming_shows_count": upcomingShowsCount, 
          })  
        else:
          resultData.append({
            "id": venue.id,
            "name": venue.name,
            "genres": genres,
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website":venue.website_link,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description":venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": pastShows,
            "upcoming_shows": upcomingShows,
            "past_shows_count": pastShowsCount,
            "upcoming_shows_count": upcomingShowsCount, 
          }) 
      error=False 
      data = list(filter(lambda d: d['id'] == venue_id, resultData))[0] #works with 1 dictionary obj
    except expression as identifier:
      error=True
      print(f'{Fore.Yellow} Error Message: ' , identifier)
      flash('Error when accessing Database: Contact Customer Support if issue persist.')
    finally:
      if error: redirect(url_for('index'))
      else: return render_template('pages/show_venue.html', venue=data)

  @app.route('/venues/create', methods=['GET'])
  def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

  @app.route('/venues/create', methods=['POST'])
  def create_venue_submission():
    error=False
    try:
      form = VenueForm(request.form)
      # retrieve the form values
      vName=form.name.data
      vCity=form.city.data.title()
      vState=form.state.data
      vAddress=form.address.data
      vPhone=form.phone.data
      vGenres=form.genres.data
      vWebsite_link = form.website_link.data
      vImage_link=form.image_link.data
      vFacebook_link=form.facebook_link.data
      vSeeking_description=form.seeking_description.data
      #Retrieve BooleanField values and test them. work around hack - BooleanField is buggy
      try:
        #If it can't read it and causes error its not clicked indicating false
        vSeeking_talent= form.seeking_talent.data
      except:
        #set it to false
        vSeeking_talent=False
      finally:
        #if the return value is 'y' or anything else other than a bool then set to true
        if (isinstance(vSeeking_talent, bool) == False):
          vSeeking_talent=True
      newVenue = Venue(name=vName, city=vCity , state=vState, address=vAddress, phone=vPhone, genres=vGenres, image_link=vImage_link, facebook_link=vFacebook_link,seeking_talent=vSeeking_talent, seeking_description=vSeeking_description, website_link = vWebsite_link )
      
      db.session.add(newVenue)
      db.session.commit()
      flash('Venue ' + vName + ' was successfully listed!')
    except:
      error=True
      db.session.rollback()
      print(sys.exc_info())
      # DONE: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + vName + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
      db.session.close()
      if error: return redirect(url_for('create_venue_submission'))
      else: return redirect(url_for('index'))

  @app.route('/venues/<venue_id>/delete', methods=['POST'])
  def delete_venue(venue_id):
    error=False
    try:
      toBeDeleted = db.session.query(Venue).filter_by(id=venue_id).all()
      toBeDeleted[0].deleted=True

      db.session.commit()
      flash('Venue Deleted')
    except:
      error=True
      print('Could not delete: ' ,venue_id)
      flash('An error occurred. Venue could not be deleted.')
      print(sys.exc_info())
      db.session.rollback()
    finally:
      db.session.close()
      if error: return redirect(url_for('show_venue', venue_id=venue_id))
      else: return render_template('pages/home.html')
    
    
  @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
  def edit_venue(venue_id):
    error=False
    deletedError=False
    try:
      currentVenue = db.session.query(Venue).get(venue_id)
      if not currentVenue.deleted:
        form = VenueForm(obj=currentVenue)
        # genres=''.join(list(filter(lambda x : x!= '{' and x!='}' and x!='"', currentVenue.genres ))).split(',')
        genres=''
        for genre in currentVenue.genres:
          genres+= genre+ ', '
        print(f"{Fore.RED} currentVenue: ", genres)
        form.genres.data = (genres if genres else 0) # I make 0 my default
        mockVenue={
          "id": 1,
          "name": "The Musical Hop",
          "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
          "address": "1015 Folsom Street",
          "city": "San Francisco",
          "state": "CA",
          "phone": "123-123-1234",
          "website": "https://www.themusicalhop.com",
          "facebook_link": "https://www.facebook.com/TheMusicalHop",
          "seeking_talent": True,
          "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
          "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
        }
        returnedData={
          "id": currentVenue.id,
          "name": currentVenue.name,
          "genres": genres,
          "address": currentVenue.address,
          "city": currentVenue.city,
          "state": currentVenue.state,
          "phone": currentVenue.phone,
          "website_link": currentVenue.website_link,
          "facebook_link": currentVenue.facebook_link,
          "seeking_talent": currentVenue.seeking_talent,
          "seeking_description": currentVenue.seeking_description,
          "image_link": currentVenue.image_link
        }
      else: 
        deletedError=True
        flash("Venue Doesn't Exist")
    except expression as identifier:
      error=True
      db.rollback()
      print(f'{Fore.Yellow} Error Message: ' , identifier)
      flash('Error Venue could not be edited: Contact Customer Support if issue persist.')
    finally:
      db.session.close()
      if deletedError: return redirect(url_for('index'))
      else:
        if error: return redirect(url_for('show_venue', venue_id=venue_id))
        else: return render_template('forms/edit_venue.html', form=form, venue=returnedData)

  @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
  def edit_venue_submission(venue_id):
    error=False
    deletedError=False
    try:
      form = VenueForm(request.form)
      print(f'{Fore.BLUE} in hurrr: ' , 1)
      # retrieve the form values
      vName=form.name.data
      vCity=form.city.data.title()
      vState=form.state.data
      vAddress=form.address.data
      vPhone=form.phone.data
      vGenres=form.genres.data
      vWebsite_link = form.website_link.data
      vImage_link=form.image_link.data
      vFacebook_link=form.facebook_link.data
      vSeeking_description=form.seeking_description.data
      #Retrieve BooleanField values and test them. work around hack - BooleanField is buggy
      try:
        #If it can't read it and causes error its not clicked indicating false
        vSeeking_talent= form.seeking_talent.data
      except:
        #set it to false
        vSeeking_talent=False
      finally:
        #if the return value is 'y' or anything else other than a bool then set to true
        if (isinstance(vSeeking_talent, bool) == False):
          vSeeking_talent=True            
      # DONE: insert form data as a new Venue record in the db, instead
      currentVenueData = Venue.query.get(venue_id)
      if not currentVenueData.deleted:
        currentVenueData.name=vName
        currentVenueData.city=vCity
        currentVenueData.state=vState
        currentVenueData.address=vAddress
        currentVenueData.phone=vPhone
        currentVenueData.genres=vGenres
        currentVenueData.image_link=vImage_link
        currentVenueData.facebook_link=vFacebook_link
        currentVenueData.seeking_talent=vSeeking_talent
        currentVenueData.seeking_description=vSeeking_description
        currentVenueData.website_link = vWebsite_link     
        # print('Printing new venue obj: ' ,newVenue , ' || ' ,newVenue.query.all())
        # DONE: modify data to be the data object returned from db insertion
        db.session.add(currentVenueData)
        # on successful db insert, flash success
        db.session.commit()
        flash('Venue ' + vName + ' was successfully updated!')
      else: 
        deletedError=True
        flash("Venue doesn't Exist")
    except:
      error=True
      db.session.rollback()
      print(sys.exc_info())
      # *on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + vName + ' could not be edited.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
      db.session.close()
      if deletedError: return redirect(url_for('index'))
      else:
        if error: return render_template('/venues/{venue_id}/edit')
        else: return redirect(url_for('show_venue', venue_id=venue_id))

  #  *----------------------------------------------------------------------------#
  #  *                              Artist Endpoints
  #  *----------------------------------------------------------------------------#
  
  @app.route('/artists')
  def artists():
    try:
      returnData=[]
      priorArea = {"state":'',
                  "city": ''}
          
      allArtist= Artist.query.filter(Artist.deleted==False).order_by('state').order_by('city').all()
      for artist in allArtist:
        if priorArea["state"] == artist.state and priorArea["city"] == artist.city:
          data= {
          "id": artist.id,
          "name": artist.name,
          "image_link": artist.image_link,
          "seeking_venue":artist.seeking_venue,
          "num_of_shows": artist.num_of_shows
          }        
        else:
          data= {
          "id": artist.id,
          "name": artist.name,
          "image_link": artist.image_link,
          "state": artist.state,
          "city": artist.city,
          "seeking_venue":artist.seeking_venue,
          "num_of_shows": artist.num_of_shows
          }
          
          priorArea["state"]= artist.state
          priorArea["city"] = artist.city
          print(f'{Fore.YELLOW} whaaa {priorArea} , {priorArea["state"]}, {priorArea["city"]}')
          
        returnData.append(data)
    except:
      print(f'{Fore.RED} Error: ', sys.exc_info())
    finally:
      return render_template('pages/artists.html', artists=returnData)

  @app.route('/artists/search', methods=['POST'])
  def search_artists():
    try:
      # Get search value from form
      searchTerm = request.form.get('search_term','').lower()
      print(f'{Fore.RED} Search Term: ' , searchTerm)
      perfectMatch =[]
      goodMatch=[]
      poorMatch=[]
      unfilteredMatch=[]
      count=0
      for row in db.session.query(Artist).filter(Artist.deleted==False).all():
        upcoming_shows = 0
        matchedVenues = Show.query.filter(Show.venue_id == row.id).all()
        if(matchedVenues):
          for venues in matchedVenues:
            if venues.start_time > datetime.today(): upcoming_shows =+1
        if searchTerm in row.name.lower():
          unfilteredMatch.append({
          "id": row.id,
          "name": row.name.title(),
          "num_upcoming_shows": upcoming_shows
        })
          count = count+1
      
      searchResult={
        "count": count,
        "data": unfilteredMatch
      } 
    except:
      flash('An error occurred when searching for ', searchTerm )
      print(sys.exc_info())
    finally:
      db.session.close()
      return render_template('pages/search_artists.html', results=searchResult, search_term=searchTerm)
    return redirect(url_for('artists'))

  @app.route('/artists/<int:artist_id>')
  def show_artist(artist_id):
    error =True
    try:
      resultData=[]
      artistsData = db.session.query(Artist).filter(Artist.deleted == False).all()
      for artist in artistsData:
        pastShowsCount =0
        upcomingShowsCount=0
        pastShows=[]
        upcomingShows=[]
        #genres=''.join(list(filter(lambda x : x!= '{' and x!='}' and x!='"', artist.genres ))).split(',')
        genres=artist.genres
        
        if artist.num_of_shows >0:
          showsData = db.session.query(Show, Venue).filter(Show.artist_id == artist.id).filter(Venue.id == Show.venue_id).all()
          for shows in showsData:
            print(f'{Fore.YELLOW} shows: {shows}')
            if shows[0].start_time > datetime.today() and not (shows[1].deleted or artist.deleted): 
              upcomingShowsCount +=1
              upcomingShows.append({
              "venue_id": shows[1].id,
              "venue_name": shows[1].name,
              "venue_image_link": shows[1].image_link,
              "start_time": str(shows[0].start_time),
              "deleted": shows[1].deleted,
              })
            else: 
              pastShowsCount +=1
              pastShows.append({
                "venue_id": shows[1].id,
                "venue_name": shows[1].name,
                "venue_image_link": shows[1].image_link,
                "start_time": str(shows[0].start_time),
                "deleted": shows[1].deleted,
            })
          resultData.append({
            "id": artist.id,
            "name": artist.name,
            "genres": genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description":artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": pastShows,
            "upcoming_shows": upcomingShows,
            "past_shows_count": pastShowsCount,
            "upcoming_shows_count": upcomingShowsCount, 
          })  
        else:
          resultData.append({
            "id": artist.id,
            "name": artist.name,
            "genres": genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description":artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": pastShows,
            "upcoming_shows": upcomingShows,
            "past_shows_count": pastShowsCount,
            "upcoming_shows_count": upcomingShowsCount, 
          })  
      data = list(filter(lambda d: d['id'] == artist_id, resultData))[0]
      error=False
    except expression as identifier:
      print(f'{Fore.RED} omg {identifier}')
      flash("Warning: error")
      db.session.rollback()
    finally:
      db.session.close()
      if error: return redirect(url_for('index'))
      else: return render_template('pages/show_artist.html', artist=data)

  @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
  def edit_artist(artist_id):
    error=False
    deletedError=False
    try:
      currentArtist = db.session.query(Artist).get(artist_id)
      if not currentArtist.deleted:
        form = ArtistForm(obj=currentArtist)
        #genres=''.join(list(filter(lambda x : x!= '{' and x!='}' and x!='"', currentArtist.genres ))).split(',')
        genres=''
        for genre in currentArtist.genres:
          genres+= genre+ ', '
        print('genres', currentArtist.genres, 'format', genres)
        form.genres.data = (genres if genres else 0) # I make 0 my default
        returnedData={
          "id": currentArtist.id,
          "name": currentArtist.name,
          "genres": genres,
          "city": currentArtist.city,
          "state": currentArtist.state,
          "phone": currentArtist.phone,
          "website_link": currentArtist.website_link,
          "facebook_link": currentArtist.facebook_link,
          "seeking_venue": currentArtist.seeking_venue,
          "seeking_description": currentArtist.seeking_description,
          "image_link": currentArtist.image_link
        }
      else: 
        deletedError=True
        flash("Artist Doesn't Exist")
    except expression as identifier:
      error=True
      db.rollback()
      print(f'{Fore.Yellow} Error Message: ' , identifier)
      flash('Error Artist could not be edited: Contact Customer Support if issue persist.')
    finally:
      db.session.close()
      if deletedError: return redirect(url_for('index'))
      else:
        if error: return redirect(url_for('show_artist', artist_id=artist_id))
        else: return render_template('forms/edit_artist.html', form=form, artist=returnedData)

  @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
  def edit_artist_submission(artist_id):
    error=False
    deletedError=False
    try:
      form = ArtistForm(request.form)
      # retrieve the form values
      aName=form.name.data
      aCity=form.city.data.title()
      aState=form.state.data
      aPhone=form.phone.data
      aGenres=form.genres.data
      aWebsite_link = form.website_link.data
      aImage_link=form.image_link.data
      aFacebook_link=form.facebook_link.data
      aSeeking_description=form.seeking_description.data
      #Retrieve BooleanField values and test them. work around hack - BooleanField is buggy
      try:
        #If it can't read it and causes error its not clicked indicating false
        aSeeking_venue= form.seeking_venue.data
      except:
        #set it to false
        aSeeking_venue=False
      finally:
        #if the return value is 'y' or anything else other than a bool then set to true
        if (isinstance(aSeeking_venue, bool) == False):
          aSeeking_venue=True            
      # DONE: insert form data as a new Venue record in the db, instead
      currentArtistData = Artist.query.get(artist_id)
      if not currentArtistData.deleted:
        currentArtistData.name=aName
        currentArtistData.city=aCity
        currentArtistData.state=aState
        currentArtistData.phone=aPhone
        currentArtistData.genres=aGenres
        currentArtistData.image_link=aImage_link
        currentArtistData.facebook_link=aFacebook_link
        currentArtistData.seeking_venue=aSeeking_venue
        currentArtistData.seeking_description=aSeeking_description
        currentArtistData.website_link = aWebsite_link     
        
        db.session.add(currentArtistData)
        db.session.commit()
        flash('Venue ' + aName + ' was successfully updated!')
      else: 
        deletedError=True
        flash("Artist Doesn't Exist")
    except:
      error=True
      db.session.rollback()
      print(sys.exc_info())
      # DONE: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + aName + ' could not be edited.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
      db.session.close()
      if deletedError: return redirect(url_for('index'))
      if error: return render_template('/artists/{artist_id}/edit')
      else: return redirect(url_for('show_artist', artist_id=artist_id))

    return redirect(url_for('show_artist', artist_id=artist_id))
  
  @app.route('/artists/<artist_id>/delete', methods=['POST'])
  def delete_artist(artist_id):
    error=True
    try:
      toBeDeleted = db.session.query(Artist).filter_by(id=artist_id).all()
      toBeDeleted[0].deleted=True
      db.session.commit()
      flash('Artist Deleted')
    except:
      db.session.rollback()
      print('Could not delete: ' ,artist_id)
      flash('An error occurred. Artist could not be deleted.')
      print(sys.exc_info())
      error=True
    finally:
      db.session.close()
      if error: return redirect(url_for('show_artist', artist_id= artist_id))
      else: return redirect(url_for('index'))

  @app.route('/artists/create', methods=['GET'])
  def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

  @app.route('/artists/create', methods=['POST'])
  def create_artist_submission():
    try:
      form = ArtistForm(request.form)
      # retrieve the form values
      a_Name=form.name.data
      a_City=form.city.data.title()
      a_State=form.state.data
      a_Website_link=form.website_link.data
      a_Phone=form.phone.data
      a_Genres=form.genres.data
      a_Image_link=form.image_link.data
      a_Facebook_link=form.facebook_link.data
      a_Seeking_description=form.seeking_description.data
      print(f'{Fore.YELLOW} omggg')
      print(f'{Fore.YELLOW} Generes1:' , a_Name)  
      
      #Retrieve BooleanField values and test them. work around hack - BooleanField is buggy
      try:
        #If it can't read it and causes error its not clicked indicating false
        a_Seeking_venue= form.seeking_venue.data
      except:
        #set it to false
        a_Seeking_venue=False
      finally:
        #if the return value is 'y' or anything else other than a bool then set to true
        if (isinstance(a_Seeking_venue, bool) == False):
          a_Seeking_venue=True
      # DONE: insert form data as a new Venue record in the db, instead
      print(f'{Fore.YELLOW} sdasfafdas' , a_Seeking_description)
      newArtist = Artist(name=a_Name, city=a_City , state=a_State, website_link=a_Website_link, phone=a_Phone, genres=a_Genres, image_link=a_Image_link, facebook_link=a_Facebook_link,seeking_venue=a_Seeking_venue, seeking_description=a_Seeking_description)
      
      db.session.add(newArtist)
      db.session.commit()
      flash('Artist ' + a_Name + ' was successfully listed!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      # DONE: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + a_Name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
      db.session.close()
      return redirect(url_for('index'))

  #  *----------------------------------------------------------------------------#
  #  *                              Shows Endpoints
  #  *----------------------------------------------------------------------------#
  @app.route('/shows/<string:selected_genre>/<string:selected_pane>')
  def shows_specific(selected_genre='All', selected_pane = 'pane_header_upcoming'):
    form = GetFeaturedForm(request.form)
    error=None
    search=True
    featured_list=[]
    try:
      resultData={
        'past': [],
        'upcoming' : [],
        'genres': [
                  'All',
                  'Alternative', 
                  'Blues', 
                  'Classical', 
                  'Country', 
                  'Electronic',
                  'Folk', 
                  'Funk',
                  'Hip-Hop', 
                  'Heavy Metal',
                  'Instrumental', 
                  'Jazz', 
                  'Musical Theatre', 
                  'Pop', 
                  'Punk',
                  'R&B', 
                  'Reggae',
                  'Rock n Roll', 
                  'Soul', 
                  'Other'
                  ],
        'selected_genre': selected_genre.capitalize(),
        'selected_pane': selected_pane,
        'form':form,
        'featured': featured_list
        }
      #print('<<$', resultData['selected_pane'], resultData['selected_genre'])
      showsData = db.session.query(Show, Artist, Venue).filter(Show.artist_id == Artist.id).filter(Venue.id == Show.venue_id).order_by(Show.start_time.asc()).all()
    
      for shows in showsData:
        if shows[1].deleted and shows[2].deleted:
          shows[0].deleted= True
        if(shows[0].feature_time and not shows[0].deleted):
          if (shows[0].feature_time >= datetime.today()):
            featured_list.append({
                "venue_id": shows[2].id,
                "venue_name": shows[2].name,
                "venue_deleted": shows[2].deleted,
                "artist_id": shows[1].id,
                "artist_name": shows[1].name,
                "artist_deleted": shows[1].deleted,
                "artist_image_link": shows[1].image_link,
                "start_time": str(shows[0].start_time),
                "featured_time": str(shows[0].feature_time)
                })
            
        if not (shows[0].deleted):
          if selected_genre.capitalize() == 'All':
            #print('<@ehh', selected_genre.capitalize() == 'All')
            
            if (shows[0].start_time <= datetime.today()): 
              resultData['past'].append({
              "venue_id": shows[2].id,
              "venue_name": shows[2].name,
              "venue_deleted": shows[2].deleted,
              "artist_id": shows[1].id,
              "artist_name": shows[1].name,
              "artist_deleted": shows[1].deleted,
              "artist_image_link": shows[1].image_link,
              "start_time": str(shows[0].start_time)
              })
            elif (shows[0].start_time > datetime.today()): 
              resultData['upcoming'].append({
              "venue_id": shows[2].id,
              "venue_name": shows[2].name,
              "venue_deleted": shows[2].deleted,
              "artist_id": shows[1].id,
              "artist_name": shows[1].name,
              "artist_deleted": shows[1].deleted,
              "artist_image_link": shows[1].image_link,
              "start_time": str(shows[0].start_time)
              })
            else:
              error=True
          elif (selected_pane == 'pane_header_upcoming'):
            
            if (shows[0].start_time <= datetime.today()):
                resultData['past'].append({
                "venue_id": shows[2].id,
                "venue_name": shows[2].name,
                "venue_deleted": shows[2].deleted,
                "artist_id": shows[1].id,
                "artist_name": shows[1].name,
                "artist_deleted": shows[1].deleted,
                "artist_image_link": shows[1].image_link,
                "start_time": str(shows[0].start_time)
                })
            elif ((selected_genre.capitalize() in shows[2].genres or selected_genre.capitalize() in shows[1].genres)):
              #print('<#ehh', (selected_genre.capitalize() in shows[2].genres))
              search=True
              if  (shows[0].start_time > datetime.today()): 
                resultData['upcoming'].append({
                "venue_id": shows[2].id,
                "venue_name": shows[2].name,
                "venue_deleted": shows[2].deleted,
                "artist_id": shows[1].id,
                "artist_name": shows[1].name,
                "artist_deleted": shows[1].deleted,
                "artist_image_link": shows[1].image_link,
                "start_time": str(shows[0].start_time)
                })
          elif (selected_pane == 'pane_header_past'):
            if (shows[0].start_time > datetime.today()):
                resultData['upcoming'].append({
                "venue_id": shows[2].id,
                "venue_name": shows[2].name,
                "venue_deleted": shows[2].deleted,
                "artist_id": shows[1].id,
                "artist_name": shows[1].name,
                "artist_deleted": shows[1].deleted,
                "artist_image_link": shows[1].image_link,
                "start_time": str(shows[0].start_time)
                }) 
            elif ((selected_genre.capitalize() in shows[2].genres or selected_genre.capitalize() in shows[1].genres)):
              #print('<#ehh', (selected_genre.capitalize() in shows[2].genres))
              search=True
              if  (shows[0].start_time <= datetime.today()): 
                resultData['past'].append({
                "venue_id": shows[2].id,
                "venue_name": shows[2].name,
                "venue_deleted": shows[2].deleted,
                "artist_id": shows[1].id,
                "artist_name": shows[1].name,
                "artist_deleted": shows[1].deleted,
                "artist_image_link": shows[1].image_link,
                "start_time": str(shows[0].start_time)
                }) 
          else:
            search=False
    except expression as identifier:
      db.session.rollback()
      error=True
      print(identifier)
      flash('An error occurred.')
    finally:
      db.session.close()
      if not search:
        flash('No results found. Try a different genre.')
      if error:
        return render_template('pages/home.html')
      else:
        return render_template('pages/shows.html', shows=resultData)
      
  @app.route('/shows', methods=['POST','GET'])
  def shows(selected_genre='All', selected_pane = 'pane_header_upcoming'):
    date_format = '%Y-%m-%d %H:%M:%S' 
    form = GetFeaturedForm(request.form)
    error=None
    valid_show=None
    search=False
    try:
      # * Checking if there is a JSON body
      searchTerm = request.form.get('search_term',None)
      featured = request.form.get('options',None)
      exist=None
      if searchTerm:
        searchTerm= searchTerm.lower()
        selected_genre = 'Search'
        selected_pane = 'All'
      else:
        selected_genre = 'All'
        selected_pane = 'pane_header_upcoming'
      print('@', featured, form.show_id.data)
      default_past=[]
      default_upcoming=[]
      featured_list=[]
      resultData={
        'past': [],
        'upcoming' : [],
        'genres': [
                  'All',
                  'Alternative', 
                  'Blues', 
                  'Classical', 
                  'Country', 
                  'Electronic',
                  'Folk', 
                  'Funk',
                  'Hip-Hop', 
                  'Heavy Metal',
                  'Instrumental', 
                  'Jazz', 
                  'Musical Theatre', 
                  'Pop', 
                  'Punk',
                  'R&B', 
                  'Reggae',
                  'Rock n Roll', 
                  'Soul', 
                  'Other'
                  ],
        'selected_genre': selected_genre,
        'selected_pane': selected_pane,
        'form': form,
        'featured':featured_list
        }
      #print('<<$', resultData['selected_pane'], resultData['selected_genre'])
      mockData=[{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
      }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
      }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
      }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
      }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
      }]
      if featured:
        # exist = Show.query.get(form.show_id.data)
        exist = db.session.query(Show).get(form.show_id.data)
        print('@existing row' , exist)
        if exist:
          valid_show=True   
          if featured== '1':
            #print('@Featured: 1 hour: ', featured, ' time: ', ((datetime.today() + timedelta(hours=1)).strftime(date_format)))
            exist.feature_time= ((datetime.today() + timedelta(hours=1)).strftime(date_format))
            db.session.commit()
            
          elif featured == '2':
            #print('@Featured: 1 hour: ', featured, ' time: ', ((datetime.today() + timedelta(hours=6)).strftime(date_format)))
            exist.feature_time= ((datetime.today() + timedelta(hours=6)).strftime(date_format))
            db.session.commit()
            
          elif featured=='3':
            exist.feature_time= ((datetime.today() + timedelta(hours=24)).strftime(date_format))
            db.session.commit()
          else:
            db.session.rollback()
            error=True
        else:
          valid_show=False
      
      showsData = db.session.query(Show, Artist, Venue).filter(Show.artist_id == Artist.id).filter(Venue.id == Show.venue_id).order_by(Show.start_time.asc()).all()
      for shows in showsData:
        if shows[1].deleted and shows[2].deleted:
          shows[0].deleted= True
        if(shows[0].feature_time and not shows[0].deleted):
          if (shows[0].feature_time >= datetime.today()):
            featured_list.append({
                "venue_id": shows[2].id,
                "venue_name": shows[2].name,
                "venue_deleted": shows[2].deleted,
                "artist_id": shows[1].id,
                "artist_name": shows[1].name,
                "artist_deleted": shows[1].deleted,
                "artist_image_link": shows[1].image_link,
                "start_time": str(shows[0].start_time),
                "featured_time": str(shows[0].feature_time)
                })
        if searchTerm:
          print('!!!', searchTerm)
          if not (shows[0].deleted) and (searchTerm in shows[1].name.lower() or searchTerm in shows[2].name.lower()):
            if (shows[0].start_time <= datetime.today()): 
              resultData['past'].append({
              "venue_id": shows[2].id,
              "venue_name": shows[2].name,
              "venue_deleted": shows[2].deleted,
              "artist_id": shows[1].id,
              "artist_name": shows[1].name,
              "artist_deleted": shows[1].deleted,
              "artist_image_link": shows[1].image_link,
              "start_time": str(shows[0].start_time)
              })
              #print('<<<past', resultData['past'])
            
            elif (shows[0].start_time > datetime.today()): 
              resultData['upcoming'].append({
              "venue_id": shows[2].id,
              "venue_name": shows[2].name,
              "venue_deleted": shows[2].deleted,
              "artist_id": shows[1].id,
              "artist_name": shows[1].name,
              "artist_deleted": shows[1].deleted,
              "artist_image_link": shows[1].image_link,
              "start_time": str(shows[0].start_time)
              })
              #print('<<<upcoming', resultData['upcoming']) 
            else: 
              error=True
          else:
            if not len(resultData['upcoming']) and not len(resultData['past']):
              search = False 
              print('>A>A', len(resultData))
            else:
              search = True    
        elif not searchTerm:
          if not (shows[0].deleted):
            if (shows[0].start_time <= datetime.today()): 
              resultData['past'].append({
              "venue_id": shows[2].id,
              "venue_name": shows[2].name,
              "venue_deleted": shows[2].deleted,
              "artist_id": shows[1].id,
              "artist_name": shows[1].name,
              "artist_deleted": shows[1].deleted,
              "artist_image_link": shows[1].image_link,
              "start_time": str(shows[0].start_time)
              })
            elif (shows[0].start_time > datetime.today()): 
              resultData['upcoming'].append({
              "venue_id": shows[2].id,
              "venue_name": shows[2].name,
              "venue_deleted": shows[2].deleted,
              "artist_id": shows[1].id,
              "artist_name": shows[1].name,
              "artist_deleted": shows[1].deleted,
              "artist_image_link": shows[1].image_link,
              "start_time": str(shows[0].start_time)
              })
              #print('<<<upcoming', resultData['upcoming']) 
            else: 
              error=True
        else:
          error=True
    except:
      db.session.rollback()
      error=True
      print("@error")
      flash('An error occurred.')
    finally:
      db.session.close()
      if not search and  (not len (resultData['upcoming']) and not len(resultData['past'])):
        flash('No Results match.')
      if error:
        return render_template('pages/home.html')
      else:
        if valid_show==False:
          flash("Invalid Show ID, Create a show first :)")
        return render_template('pages/shows.html', shows=resultData)

  @app.route('/shows/create')
  def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

  @app.route('/shows/create', methods=['POST']) #create datatable
  def create_show_submission():
    error = True
    try:
      date_format = '%Y-%m-%d %H:%M:%S' 
      show = Show()
      form = ShowForm(request.form)
      artistID =form.artist_id.data
      venueID=form.venue_id.data
      startDate = str(form.start_time.data)
      venue = Venue.query.get(venueID) if Venue.query.get(venueID)!=None else False
      artist = Artist.query.get(artistID) if Artist.query.get(artistID)!=None else False
      print(f'{Fore.YELLOW} V: {venue and artist} , A: {artist}')
      if (venue and artist):
        if not (venue.deleted and artist.deleted):
          if (venue.seeking_talent and artist.seeking_venue ):
            show.artist_id = artistID
            show.venue_id = venueID
            show.start_time = datetime.strptime(startDate, date_format)
            venue.num_of_shows +=1
            artist.num_of_shows +=1
            db.session.add(show) 
            db.session.commit()
            error = False
            flash('Show was successfully listed!')
          else:
            if not artist.seeking_venue: 
              flash( artist.name +' is not seeking a venue - Artist ID: ' + str(artistID))
            if ( not venue.seeking_talent):
              flash(venue.name+ ' is not seeking talent - Venue ID: '+ str(venueID) )
        else:
          if not (artist.deleted):
            flash('Invalid Artist Id !')
          if not (venue.deleted ):
            flash('Invalid Venue Id !')
      else:
        if not (artist):
          flash('Invalid Artist Id !')
        if not (venue):
          flash('Invalid Venue Id !')
    except Exception as e:
      error=True
      print(f'{Fore.RED}Error ==> {e}')
      db.session.rollback()
    finally:
      db.session.close()
      if error:
        return redirect(url_for('create_shows')) 
      else:
        return redirect(url_for('index')) 
      
      
      
      
  #  *----------------------------------------------------------------------------#
  #  *                              Error Handlers
  #  *----------------------------------------------------------------------------#
  @app.errorhandler(404)
  def not_found_error(error):
      return render_template('errors/404.html'), 404

  @app.errorhandler(500)
  def server_error(error):
      return render_template('errors/500.html'), 500


  if not app.debug:
      file_handler = FileHandler('error.log')
      file_handler.setFormatter(
          Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
      )
      app.logger.setLevel(logging.INFO)
      file_handler.setLevel(logging.INFO)
      app.logger.addHandler(file_handler)
      app.logger.info('errors')
      
  # * Return app Object
  return app

# *----------------------------------------------------------------------------#
# *  Deploy
# *----------------------------------------------------------------------------#

# * Create App object
app = create_app()

# # *Local use:
# if __name__ == '__main__':
#   app.run(host = '127.0.0.1')

# *For Hyroku use:
#  run the app and specify port manually:
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True
    )
