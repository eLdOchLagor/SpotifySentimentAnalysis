from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import lyricsgenius

# Behöver installeras via pip: lyricsgenius, requests, dotenv

load_dotenv()

# For api access
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
genius_token = os.getenv("GENIUS_TOKEN")

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

# Visar sig att sista delen av länken är playlistId, extraherar den
def extract_playlist_id(playlist_link):
    if "playlist/" in playlist_link:
        return playlist_link.split("playlist/")[1].split("?")[0]
    return None

# Returnerar alla items från spellistan
def get_songs_from_playlist(token, playlist_link,number_of_songs):
    playlist_id = extract_playlist_id(playlist_link)

    if playlist_id == None:
        print("Incorrect link")
        return None
    
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={number_of_songs}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]

    return json_result

#VADER
# import SentimentIntensityAnalyzer class from vaderSentiment.vaderSentiment module.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Function to print sentiments of the sentence.
def sentiment_scores(sentence):

    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    
    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("Sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("Sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("Sentence was rated as ", sentiment_dict['pos']*100, "% Positive")

    print("Sentence Overall Rated As", end=" ")

    # Decide sentiment as positive, negative, or neutral
    if sentiment_dict['compound'] >= 0.05 :
        print("Positive")
    elif sentiment_dict['compound'] <= -0.05 :
        print("Negative")
    else :
        print("Neutral")
    return sentiment_dict['compound']

token = get_token()
result = get_songs_from_playlist(token, "https://open.spotify.com/playlist/5LGIV5y28xtKrNV07jLDzr?si=927db9fe697947ee",12)

# Configure Genius
genius = lyricsgenius.Genius(genius_token,timeout=30)
genius.verbose = False # Turn off status messeges in console
genius.remove_section_headers = True # Get rid of for example "[Chorus]" text

all_lyrics = []

# Visar namnet för alla låtar i spellistan
for index, item in enumerate(result):
    track_name = item["track"]["name"]
    
    song = genius.search_song(track_name)
    
    if song:
        # Add the song's lyrics to the list
        all_lyrics.append({"track": track_name, "lyrics": song.lyrics})
        print(f"Lyrics fetched for '{track_name}'")
    else:
        print(f"Lyrics not found for '{track_name}'")

# Save all the lyrics to a JSON file after the loop
with open("lyrics.json", "w", encoding="utf-8") as json_file:
    json.dump(all_lyrics, json_file, ensure_ascii=False, indent=4)

print("All lyrics saved to lyrics.json")

playlist_mood = 0
for item in all_lyrics:
    playlist_mood += sentiment_scores(item["lyrics"])

playlist_mood = playlist_mood/len(all_lyrics)
print(playlist_mood)
