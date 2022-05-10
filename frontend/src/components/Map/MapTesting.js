import React from 'react';
import './Map.css'
import mapboxgl from 'mapbox-gl';
import Navbar from '../Navbar/Navbar';
import * as ReactDOM from 'react-dom';
import Plotly from "plotly.js-basic-dist";
import createPlotlyComponent from "react-plotly.js/factory";

import {useEffect, useState, useRef} from 'react';

mapboxgl.accessToken = 'pk.eyJ1IjoieWFudGluZ211IiwiYSI6ImNsMmJob2EzczA3ZTMzZGw2bWFvaHRrd2IifQ.qOLO45RtuWppsIRM1pxqiw';
const baseURL = "http://127.0.0.1:5000"
const Plot = createPlotlyComponent(Plotly);


function RenderDataList () {
  const [list, setList] = useState([]);
  useEffect(()=>{
  fetch("http://127.0.0.1:5000/map", {
    method: "POST",
    headers: {'Content-Type': 'application/json' },
    body: JSON.stringify({
      'request': "dataList"
    })
  })
  .then(response => response.json())
  .then(response => {
    setList(response.dataList);     // replace with reading standard json
  });
  }, []);
  let datas = Array.from(list)
  return (
    <select class='mapSelect' id={'scale'}>
      <option value="" disabled selected>Select scale</option>
      {datas.map(todo => 
      <option key={todo}>{todo}</option>)}
    </select>
  )
};

export default class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      lng: 144.96,
      lat: -37.81,
      text: '',
      zoom: 9
    };
    this.mapContainer = React.createRef();
  }
  
  addPopup(map, el, lat, lng) {
    const placeholder = document.createElement('div');
    ReactDOM.render(el, placeholder);

    const marker = new mapboxgl.Popup()
                        .setDOMContent(placeholder)
                        .setLngLat({lng: lng, lat: lat})
                        .addTo(map);
  }

  componentDidMount() {
    const { lng, lat, zoom } = this.state;

    const map = new mapboxgl.Map({
    container: this.mapContainer.current,
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [lng, lat],
    zoom: zoom
    });
    
    let Markers = [];
    
    map.on('click', async (e) => {
      var data = [
        {
          x: [1.5, 2, 3.2, 4.5, 5],
          y: [3, 3.2, 8, 10, 9],
          mode: 'markers',
          type: 'scatter',
          name: 'Others',
          text: ['EAST MELBOURNE, VIC', 'MELBOURNE AIRPORT, VIC', 'WEST MELBOURNE, VIC', 'SOUTH YARRA, VIC', 'SPRINGVALE, VIC'],
          marker: { size: 12 }
        },
        {
          x: [3],
          y: [6],
          mode: 'markers',
          type: 'scatter',
          name: 'Selected',
          text: ['MELBOURNE CBD, VIC'],
          marker: { size: 12 }
        }
      ];

      this.addPopup(map, <Plot
            data={data}
            layout={ {
              width: 400, 
              height: 300, 
              showlegend: false,
              title: 'Pay Roll vs Happyness Plot',
              font: {
                size: 15,
              },
              xaxis: {
                title: {
                  text: "Pay Roll (1,000 AUD/Week)",
                  font: {
                    size: 10,
                  }
                }
              },
              yaxis: {
                title: {
                  text: "Happyness",
                  font: {
                    size: 10,
                  }
                }
              }
            } }
        />, e.lngLat["lat"], e.lngLat["lng"])
    });
  }

  

  render() {
    return (
      <div>
        <Navbar map={'active'}/>
        <div ref={this.mapContainer} className="map-container" />
        <div class='mapSelectDiv'>
          <RenderDataList />
        </div>
      </div>
    );
  }
}



    
    