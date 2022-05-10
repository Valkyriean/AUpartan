import React from 'react';
import ReactDOM from 'react-dom/client';
import 'mapbox-gl/dist/mapbox-gl.css';
import './index.css';
import Home from './components/Home/Home'
import Map from './components/Map/MapTesting';
import PlotPoint from './components/PlotPoint/PlotPoint'
import SubmitWork from './components/SubmitWork/SubmitWork';
import reportWebVitals from './reportWebVitals';
//import axios from 'axios';
import {BrowserRouter, Routes, Route,} from "react-router-dom";


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/app/map' element={<Map />} />
      <Route path='/app/plot' element={<PlotPoint />} />
      <Route path='/app/submit' element={<SubmitWork />} />

      
    </Routes>
  </BrowserRouter>
);

reportWebVitals();