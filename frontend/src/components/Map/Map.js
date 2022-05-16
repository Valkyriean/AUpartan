// Group 1 Melbourne
// Qianjun Ding 1080391
// Zhiyuan Gao 1068184
// Jiachen Li 1068299
// Yanting Mu 1068314
// Chi Zhang 1067750

import React from 'react';
import './Map.css'
import mapboxgl from 'mapbox-gl';
import Navbar from '../Navbar/Navbar';
import * as ReactDOM from 'react-dom';
import Plotly from "plotly.js-basic-dist";
import createPlotlyComponent from "react-plotly.js/factory";

import {useEffect, useState, useRef} from 'react';

mapboxgl.accessToken = 'pk.eyJ1IjoieWFudGluZ211IiwiYSI6ImNsMmJob2EzczA3ZTMzZGw2bWFvaHRrd2IifQ.qOLO45RtuWppsIRM1pxqiw';
// const baseURL = "http://127.0.0.1:5000/request/map"
const baseURL = "http://172.26.133.167:3000/request/map"
const Plot = createPlotlyComponent(Plotly);


function RenderDataList () {
  const [list, setList] = useState([]);
  useEffect(()=>{
  fetch(baseURL, {
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
    <select class='mapSelect' id={'scenario-select'}>
      <option value="" disabled selected>Select data to plot...</option>
      {datas.map(todo => 
      <option key={todo}>{todo}</option>)}
    </select>
  )
};

export default class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      lng: 133.5,
      lat: -27,
      text: '',
      zoom: 3.7,
      map: null
    };
    
    this.mapContainer = React.createRef();
  }
  
  addPopup(map, el, lat, lng) {
    const placeholder = document.createElement('div');
    ReactDOM.render(el, placeholder);
    console.log("added a popup")
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
    this.setState({"map" : map})
  }

  renewPopup() {
    var obj = document.getElementById('scenario-select');
    if (obj) var scenario = obj.value;
    console.log(scenario)
    fetch(baseURL, {
      method: "POST",
      headers: {'Content-Type': 'application/json' },
      body: JSON.stringify({
        'request': "cityData",
        'scenario': scenario
      })
    })
    .then(response => response.json())
    .then(response => {
      while (document.getElementsByClassName("mapboxgl-popup").length){
        document.getElementsByClassName("mapboxgl-popup")[0].remove()
      }
      for (let city of response.cityList){
        var cityCoord = response.cityData[city][0]
        var cityValue = response.cityData[city][1]
        this.addPopup(this.state.map, (<p>{city + ": " + cityValue}</p>), cityCoord[0], cityCoord[1])
      }
    });
    
  }

  render() {
    return (
      <div>
        <Navbar map={'active'}/>
        <div ref={this.mapContainer} className="map-container" />
        <div class='mapSelectDiv' onChange={(e) => this.renewPopup()}>
          <RenderDataList />
        </div>
      </div>
    );
  }
}



    
    