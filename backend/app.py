from math import ceil
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import lyricsgenius
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN

# Behöver installeras via pip: lyricsgenius, requests, python-dotenv, vaderSentiment

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
def get_songs_from_playlist(token, playlist_link,number_of_songs = 20):
    playlist_id = extract_playlist_id(playlist_link)

    if playlist_id == None:
        print("Incorrect link")
        return None
    
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={number_of_songs}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]

    return json_result

def get_artist_image_by_name(token,artist_name):
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    search_results = result.json()
    artist_id = search_results['artists']['items'][0]['id']
    artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
    artist_response = get(artist_url, headers=headers)
    artist_data = artist_response.json()
    artist_images = artist_data['images']
    largest_image_url = artist_images[0]['url']
    return largest_image_url

def remove_repeated_sections_advanced(lyrics):
    lines = [line.strip() for line in lyrics.split("\n") if line.strip()]
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Embed lines
    embeddings = model.encode(lines)
    
    # Cluster using DBSCAN
    clustering = DBSCAN(eps=0.5, min_samples=2, metric='cosine').fit(embeddings)
    cluster_labels = clustering.labels_
    
    # Keep only the first occurrence of each cluster
    seen_clusters = set()
    unique_lines = []
    
    for line, cluster in zip(lines, cluster_labels):
        if cluster == -1 or cluster not in seen_clusters:
            unique_lines.append(line)
            seen_clusters.add(cluster)
    
    return "\n".join(unique_lines)
        
token = get_token()
happy_ex = "https://open.spotify.com/playlist/6GTsKH1x2qYJzAel3LcESW?si=13d4a1d361684328"
sad_ex = "https://open.spotify.com/playlist/5vsVEsAqzKWbHXHbk4uL7S?si=0fa2863970b048ea"

# Configure Genius
genius = lyricsgenius.Genius(genius_token,timeout=30)
genius.verbose = False # Turn off status messeges in console
genius.remove_section_headers = True # Get rid of for example "[Chorus]" text

# Initialize BERT Sentiment Analysis
bert = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

#FLASK
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route('/process', methods=['POST'])
def process_input():
    data = request.json  # Get input data sent by React app
    input_value = data.get('input_value')
    
    # Process the input here (call your Python function)
    output_value = process(input_value)
    
    return jsonify({'output_value': output_value})

def process(input_value):
    result = get_songs_from_playlist(token, input_value, 5)

    all_lyrics = []
    track_scores = []

    # Visar namnet för alla låtar i spellistan
    for item in result:
        track_name = item["track"]["name"]
    
        song = genius.search_song(track_name)
        artist = item["track"]["artists"][0]["name"]
        artist_im_url = get_artist_image_by_name(token,artist)
        if song:
            # Add the song's lyrics to the list
            all_lyrics.append({"track": track_name, "lyrics": song.lyrics, "artist": artist, "artist_im_url":  artist_im_url})
            print(f"Lyrics fetched for '{track_name}'")
        else:
            print(f"Lyrics not found for '{track_name}'")
    
    playlist_mood = 0
    for item in all_lyrics:
        lyrics_processed = remove_repeated_sections_advanced(item["lyrics"])

        # Divide the lyrics into multiple chunks if the lyrics exceeds 512 words
        parts = [lyrics_processed[i:i+512] for i in range(0, len(lyrics_processed), 512)]

        totalBertScore = 0
        for part in parts:
            bert_result = bert(part)[0]
            bert_score = bert_result["score"] if bert_result["label"] == "POSITIVE" else -bert_result["score"]
            totalBertScore += bert_score
        totalBertScore /= len(parts)

        playlist_mood += totalBertScore

        track_scores.append({"track": item["track"], "score": totalBertScore, "artist": item["artist"], "artist_im_url":  item["artist_im_url"]})

    playlist_mood = playlist_mood/len(all_lyrics)
    
    return {"track_scores": track_scores, "playlist_mood": playlist_mood}

if __name__ == '__main__':
    app.run(debug=True)



