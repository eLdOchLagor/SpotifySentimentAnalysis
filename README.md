![result](https://github.com/user-attachments/assets/bf71ae8c-b4d4-4918-8768-cd1a45f06d49)

# Sentiment Analysis of Public Spotify Playlists

This project was created as part of the course TNM108 at LIU. The program was written by two people using Python, Flask and ReactJS.

The project allows a user to enter the link to a public Spotify playlist, the program then performs sentiment analysis on the lyrics of the songs in the playlist using BERT. The ReactJS front-end then receives the sentiment scores from the Python backend using Flask.

## Fetching Lyrics
The lyrics was collected by first using the Spotify API to get the information about which songs the playlist contains. The Genius API was then used to collect the lyrics of each song. A python package called Lyricsgenius was used to abstract the API and make collecting lyrics very simple, only requiring 3 lines of code.

## Preprocessing

### Removing repeated lyrics (Chorus)

We quickly noticed a bias in the resulting sentiment scores due to the chorus being repeated. Songs with a sad chorus got a more negative score even if the rest of the song was positive. We used DBScan clustering to identify repeated lyrics even if they werent exactly identical, we then removed all occurences except one for each cluster.

### Chunking

Due to the maximum number of tokens that the BERT model could process was limited, for some songs with long lyrics, it had to be divided and processed in multiple passes.

## Model
We tried using VADER initially but found that the scores were not very accurate according to us. This was because VADER did not take into account the context of words, which is important for song lyrics that may contain metaphors for example. We then tried using BERT which does take into account context through "blocking", it gave a lot more accurate results. Since the data was not labeled, the measure of accuracy was subjective to what we found correct.
