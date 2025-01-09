import { useState } from 'react'
import './App.css'
import Track from "./Track"

function App() {
  const [count, setCount] = useState(0)

  const submitForm = (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const payload = Object.fromEntries(formData);

    console.log(payload.playlist_link)
  };

  return (
    <>
      <div className='container'>
        <h1>Salify</h1>
        <h2>Sentiment analysis of public Spotify playlists</h2>

        <form onSubmit={submitForm}>
          <input type="text" name='playlist_link' placeholder='Link to Spotify playlist'/>
          <input type="submit" value="Analyse"/>
        </form>

        <div className='resultsContainer'>
          <Track title={"Kräm (så nära får ingen gå)"} artist={"Kent"} imgSrc={"https://upload.wikimedia.org/wikipedia/en/a/ad/Kentverkligen.jpg"}/>
          <Track title={"Kräm (så nära får ingen gå)"} artist={"Kent"} imgSrc={"https://upload.wikimedia.org/wikipedia/en/a/ad/Kentverkligen.jpg"}/>
        </div>
        
      </div>
    </>
  )
}

export default App
