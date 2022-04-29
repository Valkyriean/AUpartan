import React from 'react';
import ReactDOM from 'react-dom/client';
import 'mapbox-gl/dist/mapbox-gl.css';
import './index.css';
import Home from './components/Home/Home'
import Map from './components/Map/Map';
import PlotPoint from './components/PlotPoint/PlotPoint'
import reportWebVitals from './reportWebVitals';
//import axios from 'axios';
import {BrowserRouter, Routes, Route,} from "react-router-dom";


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/Map' element={<Map />} />
      <Route path='/Plot' element={<PlotPoint />} />
    </Routes>
  </BrowserRouter>
);

reportWebVitals();