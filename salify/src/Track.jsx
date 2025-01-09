import './App.css'

function Track(props) {

  return (
    <>
      <div className='trackContainer'>
        <div className='trackInfo'>
          <img src={props.imgSrc} alt="Image of artist" />
          <div>
            <h3>{props.title}</h3>
            <h3>{props.artist}</h3>
          </div>
        </div>

        <h3>Sentiment score</h3>
      </div>
    </>
  )
}

export default Track
