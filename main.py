import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep


import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy import oauth2

from datetime import date, datetime
from pprint import pprint


CLIENT_SECRET = "2857b50e3d204827ba729b7fdf6e8851"
CLIENT_ID = "b6590ce256684904b1ce3cf19bffb7b1"
redirect_uri = 'http://example.com'
username = 'kuhyar93'


# driver.get("https://beatstar.fandom.com/wiki/Songs")
# songs = []
# for i in range(1, 473):
#     a_tag = driver.find_element(By.XPATH, f'//*[@id="mw-content-text"]/div/div/div[2]/div/div/table/tbody/tr[{i}]/td[3]/a')
#     song = a_tag.get_attribute('title')
#
#     songs.append(song)



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
# # print(soup)
# # # GET 100 SONGS
shits = []  # 419
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

# for song in song_names:
#     shits.append(song.get_text().strip())
#
# for i in range(len(shits)):
#     if shits[i].startswith("Additional") or shits[i].startswith("Imprint/"):
#         songs.append(shits[i+1])
# songs.pop(0)
# if len(songs) > 99:
#     songs.pop(len(songs) - 1)


# SINGERS
# singers = []
# singers_shit = soup.findAll(name="span", class_="c-label")
# for line in singers_shit:
#     item = line.get_text().strip()
#     if len(item) > 2 and item != 'NEW' and item != '-' and item != '100':
#         print(item)
#         singers.append(item)
#
# print(len(singers))
# if (item == "NEW" or item == "-" or item.startswith("0") or item.startswith("1") or item.startswith("2 ")
#         or item.startswith("3") or item.startswith("4") or item.startswith("5") or item.startswith("6 ")
#         or item.startswith("7") or item.startswith("8") or item.startswith("9")):
#     continue
# else:
#     singers.append(item)

# print(len(songs))
# print(len(singers))

# for i in range(len(songs)):
#     print(f"{i}. ")
#     print(f"Song Name: {songs[i]}")
#     print(f"Singer: {singers[i]}\n")


#spotify_playlist_names = []
# one = songs[0:100]
# two = songs[100:200]
# three = songs[200:300]
# four = songs[300:400]
# five = songs[400:473]

# print(len(one))
# print(len(two))
# print(len(three))
# print(len(four))
# print(len(five))
#
# print(one)
# print(two)
# print(three)
# print(four)
# print(five)


sp = spotipy.Spotify(auth_manager=oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                      redirect_uri=redirect_uri, scope="playlist-modify-public",
                                                      show_dialog=True, cache_path="token.txt"))

# # for item in playlists_data:
# #     spotify_playlist_names.append(item['name'])
# #
# # for playlist in spotify_playlist_names:
# #     print(playlist)

# new_playlist_name = "BEATSTAR"
new_playlist_name = f"Billboard top 100 songs {playlist_date}"
sp.user_playlist_create(user="kuhyar93", name=new_playlist_name)
#
playlists_data = sp.current_user_playlists()['items']

for item in playlists_data:
    if item['name'] == new_playlist_name:
        playlist_id = item['id']
        song_urls = [sp.search(song, 1, 0, "track")['tracks']['items'][0]['external_urls']['spotify'] for song in songs]
        sp.playlist_add_items(playlist_id=playlist_id, items=song_urls, position=0)

# pprint(playlists_data)


# playlist_ids = []

# for item in playlists_data:
#     playlist = item['external_urls']['spotify'].split('/')[4]

# pprint(playlists_data)

# # # # # GET the Songs' singers


# SPOTIFY_ENDPOINT = "https://api.spotify.com/v1/users/kuhyar93/playlists"
#


# token_dict = oauth_object.get_access_token()
# token = token_dict['access_token']
# spotifyObject = spotipy.Spotify(auth=token)
# user_name = spotifyObject.current_user()['id']
#


# To print the response in readable format.
# print(json.dumps(user_name, sort_keys=True, indent=4))

################## OPEN A SONG IN WEB BROWSER BY ITS NAME ####################

# while True:
#     print("Welcome to the project, " + user_name['display_name'])
#     print("0 - Exit the console")
#     print("1 - Search for a Song")
#     user_input = int(input("Enter Your Choice: "))
#     if user_input == 1:
#         search_song = input("Enter the song name: ")
#         results = spotifyObject.search(search_song, 1, 0, "track")
#         songs_dict = results['tracks']
#         song_items = songs_dict['items']
#         song = song_items[0]['external_urls']['spotify']
#         webbrowser.open(song)
#         print('Song has opened in your browser.')
#     elif user_input == 0:
#         print("Good Bye, Have a great day!")
#         break
#     else:
#         print("Please enter valid user-input.")
