from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = "YOUR CLIENT ID"
CLIENT_SECRET = "YOUR CLIENT SECRET"

## scraping informations from Billboard

user_choice = input("Which year do you want to travel to?\nType the date in this format YYYY-MM-DD: ")
URL = f'https://www.billboard.com/charts/hot-100/{user_choice}'

year = user_choice.split('-')[0]

response = requests.get(URL)
web_site = response.text

soup = BeautifulSoup(web_site, 'html.parser')

all_songs = soup.find_all(name='span', class_='chart-element__information__song text--truncate color--primary')
songs_title = [song.get_text() for song in all_songs]

## authenticating on Spotify

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               )
                     )

user_id = sp.current_user()['id']

spotify_uris = []

for song in songs_title:
    result = sp.search(q=f"track: {song} year: {year}", type='track')
    try:
        uri = result['tracks']['items'][0]['uri']
        spotify_uris.append(uri)
    except IndexError:
        print(f"{song} not found. Skipped.")

playlist_name = f"{user_choice} Billboard 100"

playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=spotify_uris)
