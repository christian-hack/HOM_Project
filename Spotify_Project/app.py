from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import json
import os.path
from os import path
import sqlite3 as sl

con = sl.connect('my-test.db')
app = Flask(__name__)

# assign 'key' variables for Spotify to verify application
app.secret_key = "ca46715f11484acdac1036ae59e8b93e"
app.config['SESSION_COOKIE_NAME'] = 'Christians Cookie'
TOKEN_INFO = "token_info"

#check to ensure previous login info is removed and delete if necessary to allow for new user login
if(path.exists("/Users/cphackelman/Desktop/Spotify_Project/.cache")):
    os.remove("/Users/cphackelman/Desktop/Spotify_Project/.cache")

#login page for user
@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

#create redirect page to refresh access tokens from Spotify API and redirect to getTopLists once tokens are verified
@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTopLists', _external=True))

@app.route('/getTopLists')
def getTopLists():
#ensure user session is still valid
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")
    sp = spotipy.Spotify(auth = token_info['access_token'])
#specify range of user data to retrieve as well as how much data to retrieve
#'long_term': spans several years
#'medium_term': spans last 6 months
#'short_term': spans last month
    results = sp.current_user_top_tracks(limit=50, offset = 0, time_range='medium_term')
#Retrieve user data into list
    for song in range(50):
        list = []
        list.append(results)
#Convert list to json file for further tokenization
        with open('top50_data.json', 'w', encoding='utf-8') as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
#load in json file for tokenization
    with open('top50_data.json') as f:
        data = json.load(f)
#take json file and store into list, 'results'
#create lists to separate differing values generated by Spotify API
    list_of_results = data[0]["items"]
    list_of_artist_names = []
    list_of_artist_uri = []
    list_of_song_names = []
    list_of_song_uri = []
    list_of_durations_ms = []
    list_of_explicit = []
    list_of_albums = []
    list_of_popularity = []
#populate each list according to variable
    for result in list_of_results:
        result["album"]
        this_artists_name = result["artists"][0]["name"]
        list_of_artist_names.append(this_artists_name)
        this_artists_uri = result["artists"][0]["uri"]
        list_of_artist_uri.append(this_artists_uri)
        list_of_songs = result["name"]
        list_of_song_names.append(list_of_songs)
        song_uri = result["uri"]
        list_of_song_uri.append(song_uri)
        list_of_duration = result["duration_ms"]
        list_of_durations_ms.append(list_of_duration)
        song_explicit = result["explicit"]
        list_of_explicit.append(song_explicit)
        this_album = result["album"]["name"]
        list_of_albums.append(this_album)
        song_popularity = result["popularity"]
        list_of_popularity.append(song_popularity)
#create lists to store songs and artists into respective tier
    s_tier_songs = []
    a_tier_songs = []
    b_tier_songs = []
    c_tier_songs = []
    d_tier_songs = []
    f_tier_songs = []

    s_tier_artist_names = []
    a_tier_artist_names = []
    b_tier_artist_names = []
    c_tier_artist_names = []
    d_tier_artist_names = []
    f_tier_artist_names = []

    #slice each list into appropriate tiers
    s_tier_artist_names = list_of_artist_names[0:8]
    s_tier_songs = list_of_song_names[0:8]
    a_tier_artist_names = list_of_artist_names[8:16]
    a_tier_songs = list_of_song_names[8:16]
    b_tier_artist_names = list_of_artist_names[16:24]
    b_tier_songs = list_of_song_names[16:24]
    c_tier_artist_names = list_of_artist_names[24:34]
    c_tier_songs = list_of_song_names[24:34]
    d_tier_artist_names = list_of_artist_names[34:42]
    d_tier_songs = list_of_song_names[34:42]
    f_tier_artist_names = list_of_artist_names[42:50]
    f_tier_songs = list_of_song_names[42:50]

    #merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    #merge lists into tiers accordingly
    s_tier = [(s_tier_songs[i], s_tier_artist_names[i]) for i in range(0, len(s_tier_songs))]
    a_tier = [(a_tier_songs[i], a_tier_artist_names[i]) for i in range(0, len(a_tier_songs))]
    b_tier = [(b_tier_songs[i], b_tier_artist_names[i]) for i in range(0, len(b_tier_songs))]
    c_tier = [(c_tier_songs[i], c_tier_artist_names[i]) for i in range(0, len(c_tier_songs))]
    d_tier = [(d_tier_songs[i], d_tier_artist_names[i]) for i in range(0, len(d_tier_songs))]
    f_tier = [(f_tier_songs[i], f_tier_artist_names[i]) for i in range(0, len(f_tier_songs))]
#utilize Jinja2 for variable use in html document
    return render_template('top50.html', 
    sTier = s_tier, 
    aTier = a_tier,
    bTier = b_tier,
    cTier = c_tier,
    dTier = d_tier,
    fTier = f_tier)

#@app.route('/getTopLists')
#def getTopLists():
def getApp():
    return app

#retrieve access token from Spotify API
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

#define what scope of data we want to retrieve, scope is how Spotify defines various segments of available user data
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = "9828445b08644a13a067e7959d1a4b6d",
        client_secret = "ca46715f11484acdac1036ae59e8b93e",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-top-read")