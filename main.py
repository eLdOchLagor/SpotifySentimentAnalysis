from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

# Get these unique codes from dashboard
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Use client_id and client_secret to get temporary access token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def extract_playlist_id(playlist_link):
    if "playlist/" in playlist_link:
        return playlist_link.split("playlist/")[1].split("?")[0]
    return None

def get_songs_from_playlist(token, playlist_link):
    playlist_id = extract_playlist_id(playlist_link)

    if playlist_id == None:
        print("Incorrect link")
        return None
    
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]

    return json_result

token = get_token()
result = get_songs_from_playlist(token, "https://open.spotify.com/playlist/6GTsKH1x2qYJzAel3LcESW?si=73c0b446d1244498")

for index, item in enumerate(result):
    track_name = item["track"]["name"]
    print(f"Track {index + 1}: {track_name}")
    
