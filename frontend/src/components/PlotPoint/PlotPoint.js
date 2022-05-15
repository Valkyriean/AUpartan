import React from 'react';
import Navbar from '../Navbar/Navbar';
import {useEffect, useState, useRef} from 'react';
import Plotly from "plotly.js-basic-dist";
import './PlotPoint.css'
import createPlotlyComponent from "react-plotly.js/factory";

const Plot = createPlotlyComponent(Plotly);

function useWindowSize() {
  // Initialize state with undefined width/height so server and client renders match
  // Learn more here: https://joshwcomeau.com/react/the-perils-of-rehydration/
  const [windowSize, setWindowSize] = useState({
    width: undefined,
    height: undefined,
  });

  useEffect(() => {
    // Handler to call on window resize
    function handleResize() {
      // Set window width/height to state
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    // Add event listener
    window.addEventListener("resize", handleResize);

    // Call handler right away so state gets updated with initial window size
    handleResize();

    // Remove event listener on cleanup
    return () => window.removeEventListener("resize", handleResize);
  }, []); // Empty array ensures that effect is only run on mount

  return windowSize;
}

function RenderDataList () {
  const [list, setList] = useState([]);
  useEffect(()=>{
  fetch("http://172.26.133.167:3000/request/plot", {
    method: "POST",
    headers: {'Content-Type': 'application/json' },
    body: JSON.stringify({
      'request': "plotList"
    })
  })
  .then(response => response.json())
  .then(response => {
    setList(response.plotList);     // replace with reading standard json
  });
  }, []);
  let datas = Array.from(list)
  return (
    <select class='mapSelect' id={'scenario-select'}>
      <option value="" disabled selected>Select scenario to Plot...</option>
      {datas.map(todo => 
      <option key={todo}>{todo}</option>)}
    </select>
  )
};

const RenderPlot = ({
  data,
  titleLabel,
  xLabel,
  yLabel
}) => {
  console.log(data)
  var size = useWindowSize();
  return (
    <Plot
      data={[data]} 
      layout={ {
        width: Math.floor(size.width * 0.99), 
        height: Math.floor(size.height * 0.94), 
        showlegend: false,
        title: titleLabel,
        xaxis: {
          title: {
            text: xLabel,

          }
        },
        yaxis: {
          title: {
            text: yLabel
          }
        }
      } }
    />
  )
}

export default class PlotPoint extends React.Component {
  state = {
    plt: {},
  };
  
  componentDidMount(){
    this.setState( {plt : {data: {x:[1,2,3,4,5,5,5.5,6,5.5,5,5.5,6,7,7], y:[5,0,5,0,5,2,3,1,0,2,3,1,3,0], marker: {size: 15}}}})
  }

  getData(){
    var obj = document.getElementById('scenario-select');
    if (obj) var scenario = obj.value;
    fetch("http://172.26.133.167:3000/request/plot", {
      method: "POST",
      headers: {'Content-Type': 'application/json' },
      body: JSON.stringify({
        'request': 'getData',
        'scenario': scenario
      })
    })
    .then(response => response.json())
    .then(response => {
      console.log(response);
      this.setState( {plt : {"data": response.data, "titleLabel": response.titleLabel , "xLabel": response.xLabel, "yLabel": response.yLabel}})
    });
  }

  render() {
    return (
      <div> 
          <Navbar plot={'active'}/>
          <div class="plot-container">
            <RenderPlot {...this.state.plt} />
          </div>
          <div class="plot-selectDiv">
            <RenderDataList />
            <button className="plot" onClick={(e) => this.getData()}>Plot!</button>
          </div>
          
          
      </div>
      
    );
  }
}


