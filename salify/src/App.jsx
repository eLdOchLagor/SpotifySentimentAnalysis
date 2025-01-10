import { useState } from 'react'
import './App.css'
import Track from "./Track"
import axios from 'axios';


function App() {
  const [outputValue, setOutputValue] = useState('');

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

  return (
    <>
      <div className='container'>
        <h1>{outputValue}</h1>
        <h2>Sentiment analysis of public Spotify playlists</h2>
        <p>Enter the link to a public Spotify playlist and get a reading on how positive or negative it is based on the lyrics. See also how each song affects the reading in order to optimize the mood of your playlist to fit your liking</p>

        <form onSubmit={submitForm}>
          <input type="text" name='playlist_link' placeholder='Link to Spotify playlist'/>
          <input type="submit" value="Analyse!"/>
        </form>

        <div className='resultsContainer'>
          <Track title={"Kräm (så nära får ingen gå)"} artist={"Kent"} imgSrc={"https://upload.wikimedia.org/wikipedia/en/a/ad/Kentverkligen.jpg"}/>
          <Track title={"VinterNoll2"} artist={"Kent"} imgSrc={"https://upload.wikimedia.org/wikipedia/en/3/35/Kent-VinterNoll2.jpg"}/>
        </div>
        
      </div>
    </>
  )
}

export default App
