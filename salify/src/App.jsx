import { useState } from 'react'
import './App.css'
import Track from "./Track"
import axios from 'axios';
import loadingIcon from "./assets/loading.svg"
import VisualizeScore from "./VisualizeScore"

// Hämta bild N (optional)
// Disable button while loading L
// Styling N
// Visualisering  L
// Hosta frontend (optional)
// Hosta backend (optional)


function App() {
  const [outputValue, setOutputValue] = useState({
    track_scores: [], // Array to hold track names and their BERT scores
    playlist_mood: null, // Total mood score of the playlist
  });

  const [buttonDisabled, setButtonDisabled] = useState(false);

  const submitForm = async (e) => {
    e.preventDefault();
    setButtonDisabled(true);

    // Empty it if there already exists tracks
    setOutputValue({
      track_scores: [],
      playlist_mood: null,
    });

    const formData = new FormData(e.target);
    const payload = Object.fromEntries(formData);

    try {
      const response = await axios.post('https://spotifysentimentanalysis.onrender.com/process', {
        input_value: payload.playlist_link,
      });

      setButtonDisabled(false);
      setOutputValue(response.data.output_value);
    } catch (error) {
      console.error('Error:', error);
    }

  };

  const allTracks = outputValue.track_scores.map((track, index) => 
    <Track key={index} score={track.score} title={track.track} artist={"By: " + track.artist} imgSrc={track.artist_im_url}/>
  );

  return (
    <>
      <div className='container'>
        <h1>Salify</h1>
        <h2>Sentiment analysis of public Spotify playlists</h2>
        <p>Enter the link to a public Spotify playlist and get a reading on how positive or negative it is based on the lyrics. See also how each song affects the reading in order to optimize the mood of your playlist to fit your liking</p>

        <form onSubmit={submitForm}>
          <input type="text" name='playlist_link' placeholder='Link to Spotify playlist'/>
          <input type="submit" value="Analyse!" disabled={buttonDisabled}/>
        </form>

        {outputValue.playlist_mood && (
          <> 
            <h2>Playlist Sentiment: {outputValue.playlist_mood}</h2>
            <VisualizeScore score={outputValue.playlist_mood} width={400}/>
          </>
        )}

        {buttonDisabled && (
          <img src={loadingIcon} alt="loading" style={{width: "100px", marginTop: "10vh"}}/>
        )}
      
        <div className='resultsContainer'>
          {allTracks}
        </div>
        
      </div>
    </>
  )
}

export default App
