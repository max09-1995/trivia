#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form, FlaskForm
from forms import VenueForm
from flask_migrate import Migrate
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean, BOOLEAN, DateTime
from datetime import datetime
from dateutil.parser import parse
from models import Show, Venue, Artist, app, moment, db


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  
  data = {}
  values = db.session.query(Venue.city.distinct())
  lastdata1 = {}

  for value in values:
    data1 = {}
    states = db.session.query(Venue).filter_by(city=value)
    data1['city'] = value[0]
    data1['state'] = states[0].state
    values = db.session.query(Venue).filter(Venue.city == value)
    
    for venue in values:
      data2 = {}
      data2['id'] = venue.id
      data2['name'] = venue.name
      data1.setdefault('venues', []).append(data2)
    
    data = [lastdata1 ,data1]
    lastdata1 = data1
  
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  
  venues = db.session.query(Venue).filter(Venue.name.contains(request.form['search_term']))

  venuecount = 0

  for venue in venues:
    venuecount = venuecount+1

  response={
    "count": venuecount,
    "data": venues
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  
  venuedata = db.session.query(Venue).filter_by(id=venue_id)

  past_shows = []
  past_shows_counter = 0
  upcoming_shows = []
  upcoming_shows_counter = 0

  past_shows = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
  past_shows_counter = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).count()
  
  upcoming_shows = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()
  upcoming_shows_counter = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).count()


  data={
    "id":venue_id,
    "name":venuedata[0].name,
    "genres": venuedata[0].genres,
    "address": venuedata[0].address,
    "city": venuedata[0].city,
    "state": venuedata[0].state,
    "phone": venuedata[0].phone,
    "website": venuedata[0].website,
    "facebook_link": venuedata[0].facebook_link,
    "seeking_talent": venuedata[0].seeking_talent,
    "seeking_description": venuedata[0].seeking_description,
    "image_link": venuedata[0].image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_counter,
    "upcoming_shows_count": upcoming_shows_counter
  }
 
  data = list(filter(lambda d: d['id'] == venue_id, [data]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  
  form = VenueForm(request.form)
  
  try:
    
    #seeking_talent = False
    #name = request.form['name']
    #city = request.form['city']
    #state = request.form['state']
    #address = request.form['address']
    #phone = request.form['phone']
    #image_link = request.form['image_link']
    #genre = request.form['genres']
    #facebook_link = request.form['facebook_link']
    #website = request.form['website']
    #seeking_talent = request.form['seeking_talent']
    #seeking_description = request.form['seeking_description']
  
    #venue = Venue(name=name, city=city, state=state, address=address, phone=phone,image_link=image_link, facebook_link=facebook_link, genres=genre, seeking_description=seeking_description, website=website,seeking_talent=seeking_talent)
    
    venue = Venue()

    form.populate_obj(venue)

    db.session.add(venue)
    
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
  
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    db.session.rollback()
  
  finally:
    
    db.session.close()

  return render_template('pages/home.html')
  #----------------------------------
  #show venue details
  #----------------------------------

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    #get records
    show_venues = Show.query.filter_by(venue_id=venue_id)
    venue_row = Venue.query.get(venue_id)
    
    #delete
    show_venues.delete()
    db.session.delete(venue_row)
    
    db.session.commit()
  
  except:
    print('except')
    db.session.rollback()

  finally:
    db.session.close()
    
  return render_template('/pages/home.html')
  
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  
  data = db.session.query(Artist).all()
  
  return render_template('/pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  
  artists = db.session.query(Artist).filter(Artist.name.contains(request.form['search_term']))
  artistcounter = 0

  for artist in artists:
    artistcounter = artistcounter +1


  response={
    "count": artistcounter,
    "data": artists
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

#--------------------------------------
# Show artist details
#--------------------------------------

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  
  artistdata = db.session.query(Artist).filter_by(id=artist_id)

  past_shows = []
  past_shows_counter = 0
  upcoming_shows = []
  upcoming_shows_counter = 0


  past_shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()
  past_shows_counter = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).count()
  
  upcoming_shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()
  upcoming_shows_counter = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).count()

  data={
    "id":artist_id,
    "name":artistdata[0].name,
    "genres": artistdata[0].genres,
    "city": artistdata[0].city,
    "state": artistdata[0].state,
    "phone": artistdata[0].phone,
    "website": artistdata[0].website,
    "facebook_link": artistdata[0].facebook_link,
    "seeking_venue": artistdata[0].seeking_venue,
    "seeking_description": artistdata[0].seeking_description,
    "image_link": artistdata[0].image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_counter,
    "upcoming_shows_count": upcoming_shows_counter,
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artistdata = db.session.query(Artist).filter_by(id=artist_id)
  
  artist={
    "id": artist_id,
    "name": artistdata[0].name,
    "genres": artistdata[0].genres,
    "city": artistdata[0].city,
    "state": artistdata[0].state,
    "phone": artistdata[0].phone,
    "website": artistdata[0].website,
    "facebook_link": artistdata[0].facebook_link,
    "seeking_venue": artistdata[0].seeking_venue,
    "seeking_description": artistdata[0].seeking_description,
    "image_link": artistdata[0].image_link
  }

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
 
  try:
    artist = Artist.query.get(artist_id)

    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form['genres']
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.website = request.form['website']
    artist.seeking_venue = request.form['seeking_venue']
    artist.seeking_venue = request.form['seeking_venue']
    artist.seeking_description = request.form['seeking_description']

    db.session.commit()

  except:

    db.session.rollback()

  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

#  Edit Venue
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venuedata = db.session.query(Venue).filter_by(id=venue_id)

  venue={
    "id": venue_id,
    "name": venuedata[0].name,
    "genres": venuedata[0].genres,
    "address": venuedata[0].address,
    "city": venuedata[0].city,
    "state": venuedata[0].state,
    "phone": venuedata[0].phone,
    "website": venuedata[0].website,
    "facebook_link": venuedata[0].facebook_link,
    "seeking_talent": venuedata[0].seeking_talent,
    "seeking_description": venuedata[0].seeking_description,
    "image_link": venuedata[0].image_link
  }
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  try:
    venue = Venue.query.get(venue_id)

    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.genres = request.form['genres']
    venue.address = request.form['address']
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website']
    venue.seeking_talent = request.form['seeking_talent']
    venue.seeking_description = request.form['seeking_description']

    db.session.commit()

  except:
    db.session.rollback()

  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
 
  
  try:
    
    seeking_venue= False
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form['genres']
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website = request.form['website']
    seeking_venue = request.form['seeking_venue']
    seeking_description = request.form['seeking_description']

    artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres,facebook_link=facebook_link, image_link=image_link,website=website, seeking_venue=seeking_venue,seeking_description=seeking_description)

    db.session.add(artist)
    
    db.session.commit()

    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  
  except:
    flash('Artist ' + request.form['name'] + ' was not successfully listed!')
    db.session.rollback()
  finally:
    db.session.close()
  
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
 
  shows = db.session.query(Show).all()
  data = []
  for show in shows:
    
    try:
      venue = db.session.query(Venue).filter_by(id=show.venue_id)
      artist = db.session.query(Artist).filter_by(id=show.artist_id)
      data2 = {
        "venue_id": show.venue_id,
        "venue_name": venue[0].name,
        "artist_id": show.artist_id,
        "artist_name": artist[0].name,
        "artist_image_link": artist[0].image_link,
        "start_time": show.start_time
       }
      data.append(data2)

    except:
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  
  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    
    db.session.add(show)
    # on successful db insert, flash success   
    flash('The show was successfully listed!')
    db.session.commit()
  except:
    db.session.rollback()
  
  finally:
    db.session.close()

    return render_template('pages/home.html')

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

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
