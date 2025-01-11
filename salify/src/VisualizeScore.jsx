import './App.css'

function VisualizeScore(props) {
  

  return (
    <>
      <div className='visualizeContainer' style={{width: props.width + "px"}}>
        <div className='visualizePoint' style={{left: (props.width/2 + props.score * props.width/2) + "px" }}></div>
      </div>
    </>
  )
}

export default VisualizeScore
