'''
in terminal
tutorial-env\Scripts\activate

$env:FLASK_APP = "app.py"


documentation for Spotipy and Spotify Web API
Spotipy library: https://pypi.org/project/spotipy/#documentation, https://spotipy.readthedocs.io/en/2.24.0/ 
Spotify Web API: https://developer.spotify.com/documentation/web-api

'''
from flask import Flask, request, url_for, render_template, session, redirect
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import time 
import math
import os 
from dotenv import load_dotenv
load_dotenv("config.env")
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

#https://developer.spotify.com/documentation/web-api/concepts/scopes
scopes_used = "user-library-read user-read-private playlist-modify-public playlist-modify-private user-top-read user-read-recently-played"
#scopes for reading, modify playlists  

app =Flask(__name__) #creates the flask application

app.secret_key= "hbadkjsJHBHJKB#QLSDSAD"  #the cookie 
app.config["SESSION_COOKIE_NAME"]= "aarons_Cookie" #stores the user's session
TOKEN_INFO = "token_info"

@app.route("/") #routes but also referred to as endpoints 
def index():
    token_info = session.get(TOKEN_INFO, None)
    if token_info: 
        # if logged in b/c we have token 
        return render_template("homepage_l.html")
    else:
        # not logged in 
        return render_template("homepage_ul.html")

@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/login")
def login(): # log u into spotify 
    sp_Oauth = create_spotifyOuth()
    auth_url = sp_Oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/redirect")
def redirectPage():
    sp_Oauth = create_spotifyOuth()
    session.clear()
    code= request.args.get('code')
    token_info=sp_Oauth.get_access_token(code)
    session[TOKEN_INFO]= token_info #save the token information in the session
    return redirect(url_for('index', _external=True))

@app.route("/topTracks")
def topTracks():
    try: 
        token_info = get_token()
    except: 
        print("user not logged in")
        return redirect(url_for("login", _external= False)) #return user to login page

    sp=spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = (sp.current_user_top_tracks(limit=10, offset=0))

    top_track_names= [top_track['name'] for top_track in top_tracks['items']]
    top_track_img = [top_track['album']['images'][0]['url'] for top_track in top_tracks['items']]  #images dict was nested under album inside items               
    
    top_track_alb= [top_track['duration_ms'] for top_track in top_tracks['items']]
    formated_dur =[]
    for track in top_track_alb: #convert into minutes, seconds 
        track = track/1000 #b/c miliseconds
        min = track//60
        sec = track % 60
        formated_dur.append((int(min),math.floor(sec)))

    return render_template("topsongs.html", song_list=top_track_names, image_list = top_track_img, length = formated_dur) 

@app.route("/topArtists")
def topArtists():
    #improvements : play a top track of that artist using js?
    try: 
        token_info = get_token()
    except: 
        print("user not logged in")
        return redirect(url_for("login", _external= False)) #return user to login page

    sp=spotipy.Spotify(auth=token_info['access_token'])
    top_artists = (sp.current_user_top_artists(limit=10, offset=0))
    top_artists_names= [top_artist['name'] for top_artist in top_artists['items']]
    top_artists_pic= [top_artist['images'][0]['url'] for top_artist in top_artists ['items']]
    return render_template("topartists.html", names=top_artists_names, pictures=top_artists_pic)

 
def get_token(): #to refresh token and check if theres even a token
    token_info = session.get(TOKEN_INFO, None)
    if not token_info: # if is None
        raise "exception "
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60 
    if is_expired:
        sp_Oauth= create_spotifyOuth()
        token_info = sp_Oauth.refresh_access_token(token_info['refresh_token'])
        session[TOKEN_INFO]=token_info
    return token_info

def create_spotifyOuth() : #everytime use object use a new one
    return SpotifyOAuth(client_id =CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=url_for("redirectPage", _external=True), #url_for is a good way to not hardcode the path _external=True will create an absolute path
                                                scope=scopes_used)
'''
scopes_used = "user-library-read playlist-modify-public playlist-modify-private user-top-read user-read-recently-played"
#scopes for reading, modify playlists
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id ="",
                                                client_secret="",
                                                redirect_uri="http://localhost:3000",
                                                scope=scopes_used))
user= sp.current_user()
userID =user["id"]
name_playlist = input("name of playlist created: ")                 #got to add something when the input is nothing b/c it gives error
description_of_playlist = input("description of playlist: ")
#user_choice = input("based off top artists or tracks: ") this should be a drop down menu 


new_playlist = sp.user_playlist_create( #create new playlist 
    user=userID,
    name=name_playlist,
    public=True,          #perhaps also an option to keep it private
    collaborative=False,
    description = description_of_playlist)

# Extract the playlist ID from the new_playlist dictionary
playlist_id = new_playlist['id']

top_artist= sp.current_user_top_artists(limit=3, offset=0, time_range='medium_term')  #get the top artists returns in dict form, we want["items"]["id"] 
artist_ids = [artist['id'] for artist in top_artist['items']]

#current_user_top_tracks(limit=20, offset=0, time_range='medium_term')
top_tracks= sp.current_user_top_tracks(limit=2, offset=0, time_range='medium_term')
top_track_ids= [top_track['id'] for top_track in top_tracks['items']]

#recommendations(seed_artists=None, seed_genres=None, seed_tracks=None, limit=20, country=None, **kwargs) Minimum: 1. Maximum: 100. default 20
#Get a list of recommended tracks for one to five seeds. (at least one of seed_artists, seed_tracks and seed_genres are needed)
# dict form also, ["tracks"]["id"]
list_of_recs = sp.recommendations(seed_artists=artist_ids,
                seed_genres=None,
                seed_tracks=top_track_ids,
                limit=20,
                country=None)



rec_track_ids = [track['id'] for track in list_of_recs['tracks']]



sp.user_playlist_add_tracks(user=userID, playlist_id=playlist_id, tracks=rec_track_ids)



#based on 5's, we can just do top 20?30? tracks played and then loop through them
#add it to the list and filter out songs already in library 
#we need the IDs 



#current_user_top_artists(limit=20, offset=0, time_range='medium_term') get top artists
#current_user_top_tracks(limit=20, offset=0, time_range='medium_term')  get top tracks
#search(q, limit=10, offset=0, type='track', market=None)            search 
#user_playlist_add_tracks(user, playlist_id, tracks, position=None)    add track to playlist
#user_playlist_remove_specific_occurrences_of_tracks(user, playlist_id, tracks, snapshot_id=None) remove tracks (possible for duplicates)

'''
