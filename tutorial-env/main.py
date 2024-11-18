'''
in terminal
$env:SPOTIPY_CLIENT_ID="e58f127ad4a0477bb887ebd3fbec37e3"
$env:SPOTIPY_CLIENT_SECRET="76fdc0cb18e84cd2b69905d9544bd431"
$env:SPOTIPY_REDIRECT_URI="http://localhost:3000"


documentation for Spotipy and Spotify Web API
Spotipy library: https://pypi.org/project/spotipy/#documentation, https://spotipy.readthedocs.io/en/2.24.0/ 
Spotify Web API: https://developer.spotify.com/documentation/web-api

works for improvement:
flask
tokens so others can use it 
filter our songs reccomended that are already in ur liked library and reissue new songs 

error check- 
name playlist = empty
name description = empty

'''
import spotipy 
from spotipy.oauth2 import SpotifyOAuth

#https://developer.spotify.com/documentation/web-api/concepts/scopes
scopes_used = "user-library-read playlist-modify-public playlist-modify-private user-top-read user-read-recently-played"
#scopes for reading, modify playlists

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id ="e58f127ad4a0477bb887ebd3fbec37e3",
                                                client_secret="76fdc0cb18e84cd2b69905d9544bd431",
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
