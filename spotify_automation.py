import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="{ur_client_id}",
    client_secret="{ur_client_secret_code}",
    redirect_uri="https://example.com/callback",
    scope="playlist-modify-private"
))

# Step 1: Get date input
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# Step 2: Set headers and construct URL
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
}
url = "https://www.billboard.com/charts/hot-100/" + date

# Step 3: Make request
response = requests.get(url=url, headers=headers)

# Step 4: Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Step 5: Extract song titles
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
song_list = []
# Step 6: Print song names
for i, song in enumerate(song_names, 1):
    song_list.append(song)

print(song_list)

user_id = sp.current_user()["id"]

song_url = []
year = date.split("-")[0]
for song in song_list:
    results = sp.search(q=f"{song.strip()}", type="track", limit=1)
    if results:
        song_url.append(results["tracks"]["items"][0]["uri"])

playlist = sp.user_playlist_create(user=user_id, public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items = song_url)
sp.user_playlist_change_details(user=user_id, playlist_id=playlist["id"], name=f"{date} Billboard 100",description="Updated with Billboard Hot 100 songs")

    
