import React from 'react';
import './Map.css'
import mapboxgl from 'mapbox-gl';
import Navbar from '../Navbar/Navbar';

mapboxgl.accessToken = 'pk.eyJ1IjoieWFudGluZ211IiwiYSI6ImNsMmJob2EzczA3ZTMzZGw2bWFvaHRrd2IifQ.qOLO45RtuWppsIRM1pxqiw';
const baseURL = "http://127.0.0.1:5000"

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
      await fetch("http://127.0.0.1:5000/map", {
        method: "POST",
        headers: {'Content-Type': 'application/json' },
        body: JSON.stringify({
          'lat': e.lngLat["lat"],
          'lng': e.lngLat["lng"],
        })
      })
      .then(response => response.json())
      .then(response => {
        this.state.text = response.sum;
        //console.log(response.sum);
      });

      console.log(this.state.text);
      Markers.forEach((marker) => marker.remove())
      Markers = [];
      var popup = new mapboxgl.Popup({closeButton:false})
        .setText(this.state.text)
        .addTo(map);
      var marker = new mapboxgl.Marker()
        .setLngLat([e.lngLat["lng"], e.lngLat["lat"]])
        .addTo(map)
        .setPopup(popup);
      Markers.push(marker);
    });
  }

  render() {
    return (
      <div>
        <Navbar map={'active'}/>
        <div ref={this.mapContainer} className="map-container" />
      </div>
    );
  }
}
