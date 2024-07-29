
import requests
import spotipy
from time import sleep
from spotipy import oauth2
from bs4 import BeautifulSoup
from datetime import date, datetime
from pprint import pprint


CLIENT_SECRET = "your_client_secret"
CLIENT_ID = "your_ID"
redirect_uri = 'http://example.com'
username = 'kuhyar93'



# Getting a specific date from the user

print("Enter a specific date to get the top 100 songs of that date according to billboard.")
year = int(input("Enter Year(YYYY): "))
month = int(input("Enter Month(MM): "))
day = int(input("Enter Day(DD): "))
playlist_date = date(year, month, day)

URL = f"https://www.billboard.com/charts/hot-100/{playlist_date}/"
print(URL)
# print(URL)
response = requests.get(url=URL)
response.raise_for_status()
billboard_wb = response.text
soup = BeautifulSoup(billboard_wb, 'html.parser')

# song_names = soup.findAll(name='h3', id="title-of-a-story")
song_names_h3 = soup.select("li ul li h3")
songs = [item.get_text().strip() for item in song_names_h3]
# # for song in song_names:
# #     print(song)
singers_span = soup.select("li ul li span")
#
singers = [singers_span[i].get_text().strip() for i in range(0, len(singers_span) - 1, 7)]

for i in range(len(songs)):
    print(f"{i}.")
    print(f"Song Name: {songs[i]}")
    print(f"Singer Name: {singers[i]}\n")



sp = spotipy.Spotify(auth_manager=oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                      redirect_uri=redirect_uri, scope="playlist-modify-public",
                                                      show_dialog=True, cache_path="token.txt"))

new_playlist_name = f"Billboard top 100 songs {playlist_date}"
sp.user_playlist_create(user="kuhyar93", name=new_playlist_name)

playlists_data = sp.current_user_playlists()['items']

for item in playlists_data:
    if item['name'] == new_playlist_name:
        playlist_id = item['id']
        song_urls = [sp.search(song, 1, 0, "track")['tracks']['items'][0]['external_urls']['spotify'] for song in songs]
        sp.playlist_add_items(playlist_id=playlist_id, items=song_urls, position=0)


