import { useState } from 'react'
import './App.css'
import Track from "./Track"
import axios from 'axios';

// Hämta artist N 
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

  const submitForm = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const payload = Object.fromEntries(formData);

    try {
      const response = await axios.post('http://127.0.0.1:5000/process', {
        input_value: payload.playlist_link,
      });

      setOutputValue(response.data.output_value);
    } catch (error) {
      console.error('Error:', error);
    }

  };

  const allTracks = outputValue.track_scores.map((track, index) => 
    <Track key={index} score={track.score} title={track.track} artist={"Kent"} imgSrc={"https://upload.wikimedia.org/wikipedia/en/a/ad/Kentverkligen.jpg"}/>
  );

  return (
    <>
      <div className='container'>
        <h1>Salify</h1>
        <h2>Sentiment analysis of public Spotify playlists</h2>
        <p>Enter the link to a public Spotify playlist and get a reading on how positive or negative it is based on the lyrics. See also how each song affects the reading in order to optimize the mood of your playlist to fit your liking</p>

        <form onSubmit={submitForm}>
          <input type="text" name='playlist_link' placeholder='Link to Spotify playlist'/>
          <input type="submit" value="Analyse!"/>
        </form>

        <h2>{outputValue.playlist_mood}</h2>

        <div className='resultsContainer'>
          {allTracks}
        </div>
        
      </div>
    </>
  )
}

export default App
