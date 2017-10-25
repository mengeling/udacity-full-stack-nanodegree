from flask import flash, Flask, jsonify, make_response, redirect
from flask import render_template, request, url_for
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import random
import string
import httplib2
import json
import requests

from database_setup import Base, User, Genre, Movie

app = Flask(__name__)


# Connect to database
engine = create_engine('sqlite:///moviecatalog.db')
Base.metadata.bind = engine

# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Store client ID from the Google JSON file
client_id = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


@app.route('/')
@app.route('/genres/')
def showGenres():
    """This function loads all of the genres and movies from the database
    to be displayed on the landing page of the site"""

    # Get all genres and movies
    genres = session.query(Genre).all()
    movies = session.query(Movie).all()

    # Render genres.html template with all of the genres and movies
    return render_template('genres.html', genres=genres, movies=movies)


@app.route('/genres/<int:genre_id>/')
@app.route('/genres/<int:genre_id>/movies/')
def showGenre(genre_id):
    """This function loads a specific genre and the relevant movies
    from the database to be displayed on the genre's page"""

    # Get all genres, the specific genre, and that genre's movies
    genres = session.query(Genre).all()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(genre_id=genre_id).all()

    # Render genre.html template with the genre selected
    return render_template(
        'genre.html', genres=genres, genre=genre, movies=movies,
        movieCount=len(movies))


@app.route('/genres/<int:genre_id>/movies/<int:movie_id>/')
def showMovie(genre_id, movie_id):
    """This function loads a specific movie from the database"""

    # Get specific movie and user that added the movie
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movie = session.query(Movie).filter_by(id=movie_id).one()
    user = getUserInfo(movie.user_id)

    # Render movie.html template with the movie selected
    return render_template('movie.html', genre=genre, movie=movie, user=user)


@app.route('/movies/new/', methods=['GET', 'POST'])
def newMovie():
    """This function lets users add movies to the database"""

    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    # Retrieve genres
    genres = session.query(Genre).all()

    # Store new movie in database if user sends post request
    if request.method == 'POST':
        movie = Movie(
            name=request.form['name'], description=request.form['description'],
            rating=request.form['rating'], genre_id=request.form['genre'],
            user_id=login_session['user_id'])
        session.add(movie)
        session.commit()

        # Look up genre and then flash message with movie name and genre name
        genre = session.query(Genre).filter_by(id=movie.genre_id).one()
        flash('{} Added to {} Genre'.format(movie.name, genre.name))

        # Take user to the new movie's page
        return redirect(
            url_for('showMovie', genre_id=genre.id, movie_id=movie.id))
    else:

        # Render newMovie.html template if user hasn't sent post request
        return render_template('newMovie.html', genres=genres)


@app.route('/genres/<int:genre_id>/movies/new/', methods=['GET', 'POST'])
def newMovieWithGenre(genre_id):
    """This function lets users add movies to specific genres"""

    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    # Get genre object
    genre = session.query(Genre).filter_by(id=genre_id).one()

    # Store new movie in database if user sends post request
    if request.method == 'POST':
        movie = Movie(
            name=request.form['name'], description=request.form['description'],
            rating=request.form['rating'], genre_id=genre.id,
            user_id=login_session['user_id'])
        session.add(movie)
        session.commit()

        # Flash message with movie name and genre name
        flash('{} Added to {} Genre'.format(movie.name, genre.name))

        # Take user to the new movie's page
        return redirect(
            url_for('showMovie', genre_id=genre.id, movie_id=movie.id))
    else:

        # Render newMovie.html template if user hasn't sent post request
        return render_template('newMovieWithGenre.html', genre=genre)


@app.route(
    '/genres/<int:genre_id>/movies/<int:movie_id>/edit/',
    methods=['GET', 'POST'])
def editMovie(genre_id, movie_id):
    """This function allows authorized users to edit existing movies"""

    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    # Get selected movie, selected genre, and all genres
    genres = session.query(Genre).all()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movie = session.query(Movie).filter_by(id=movie_id).one()

    # Check if logged in user added the selected movie
    if movie.user_id != login_session['user_id']:
        return (
            "<script>function myFunction() {alert('You are not authorized "
            "to edit this movie.');}</script><body onload='myFunction()''>")

    # Store movie changes in database if user sends post request
    if request.method == 'POST':
        if request.form['name']:
            movie.name = request.form['name']
        if request.form['description']:
            movie.description = request.form['description']
        if request.form['rating']:
            movie.rating = request.form['rating']
        if request.form['genre']:
            movie.genre_id = request.form['genre']
        flash('Movie Successfully Edited {}'.format(movie.name))

        # Take user to the edited movie's updated page
        return redirect(
            url_for('showMovie', genre_id=movie.genre_id, movie_id=movie.id))
    else:

        # Render editMovie.html template if user hasn't sent post request
        return render_template(
            'editMovie.html', genres=genres, genre=genre, movie=movie)


@app.route(
    '/genres/<int:genre_id>/movies/<int:movie_id>/delete/',
    methods=['GET', 'POST'])
def deleteMovie(genre_id, movie_id):
    """This function allows authorized users to delete existing movies"""

    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    # Get movie and genre
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movie = session.query(Movie).filter_by(id=movie_id).one()

    # Check if logged in user added the selected movie
    if movie.user_id != login_session['user_id']:
        return (
            "<script>function myFunction() {alert('You are not authorized "
            "to delete this movie.');}</script><body onload='myFunction()''>")

    # Delete movie from database if user sends post request
    if request.method == 'POST':
        session.delete(movie)
        session.commit()
        flash('{} Successfully Deleted'.format(movie.name))

        # Take user to deleted movie's genre page
        return redirect(url_for('showGenres'))
    else:

        # Render deleteMovie.html template if user hasn't sent post request
        return render_template('deleteMovie.html', genre=genre, movie=movie)


@app.route('/login/')
def login():
    """This function creates a state token and then renders the login page"""

    # Create state token
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32))
    login_session['state'] = state

    # Render login template
    return render_template('login.html', state=state)


@app.route('/logout/')
def logout():
    """This function deletes login info and disconnect
    from third party authentication system with Google"""

    gdisconnect()
    del login_session['google_id']
    del login_session['access_token']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']

    # Redirect to home page
    return redirect(url_for('showGenres'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """This function uses Google OAuth to authenticate the user"""

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps("Invalid state parameter."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Get authorization code
    auth_code = request.data

    try:
        # Exchange authorization code for a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(auth_code)
    except FlowExchangeError:

        # Send error as JSON object if the auth code can't be authenticated
        response = make_response(json.dumps(
            "Failed to upgrade the authorization code."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain access token from credentials object and add it to Google URL
    access_token = credentials.access_token

    # Use httplib2 module to check Google to see if access token is valid
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
        .format(access_token))
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])

    # Send response as JSON object if access token had error(s)
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Send reponse if access token isn't intended for logged in user
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Send reponse if the client ID isn't intended for this app
    # Use client_id from client_secrets.json file
    if result['issued_to'] != client_id:
        response = make_response(json.dumps(
            "Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Send response if the user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(json.dumps(
            "Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store access token and google ID in the session
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # Get user info from Google
    url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    user_data = requests.get(url, params=params).json()

    # Store username, picture, and email in the session
    login_session['username'] = user_data['name']
    login_session['email'] = user_data['email']
    login_session['picture'] = user_data['picture']

    # Check if user already exists in database and add them if not
    user_id = getUserID(user_data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    return "Login Successful"


@app.route('/gdisconnect')
def gdisconnect():
    """This function disconnects user from Google OAuth"""

    # Get access token
    access_token = login_session.get('access_token')

    # Send message that the user isn't logged in if the access token is empty
    if access_token is None:
        response = make_response(json.dumps(
            "Current user not connected."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Revoke user's token
    url = (
        'https://accounts.google.com/o/oauth2/revoke?token={}'
        .format(access_token))
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]

    # Send error message if the token wasn't revoked successfully
    if result['status'] != '200':
        response = make_response(json.dumps(
            "Failed to revoke token for given user."), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


def createUser(login_session):
    """This function creates a new user from the Googe connect function"""

    # Get user's username, email, and picture from the login session
    user = User(
        name=login_session['username'], email=login_session['email'],
        picture=login_session['picture'])

    # Add the new user to the database
    session.add(user)
    session.commit()

    # Find the user ID assigned by the database and return it
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """This function uses the user ID to look up user's info from database"""

    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """This function uses user's email to find user's ID"""

    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/genres/JSON/')
def showGenresJSON():
    """This function JSONifies the genres for the home API endpoint"""

    genres = session.query(Genre).all()
    return jsonify(genres=[genre.serialize for genre in genres])


@app.route('/genres/<int:genre_id>/JSON/')
@app.route('/genres/<int:genre_id>/movies/JSON/')
def showGenreJSON(genre_id):
    """This function JSONifies the movies for the genre's API endpoints"""

    movies = session.query(Movie).filter_by(genre_id=genre_id).all()
    return jsonify(movies=[movie.serialize for movie in movies])


@app.route('/genres/<int:genre_id>/movies/<int:movie_id>/JSON/')
def showMovieJSON(genre_id, movie_id):
    """This function JSONifies the specific movie for movie's API endpoint"""

    movie = session.query(Movie).filter_by(id=movie_id).one()
    return jsonify(movie.serialize)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'secret_key'
    app.run(host='0.0.0.0', port=5000)
