import './App.css'
import VisualizeScore from "./VisualizeScore"

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
        <div>
          <h3>{props.score}</h3>
          <VisualizeScore score={props.score} width={200}/>
        </div>
      </div>
    </>
  )
}

export default Track
