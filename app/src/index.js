import React from 'react';
import ReactDOM from 'react-dom/client';
import 'mapbox-gl/dist/mapbox-gl.css';
import './index.css';
import Map from './components/Map/Map';
import Navbar from './components/Navbar/Navbar';
import Home from './components/Home/Home'
import reportWebVitals from './reportWebVitals';

import {BrowserRouter, Routes, Route,} from "react-router-dom";


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/Map' element={<Map />} />
    </Routes>
  </BrowserRouter>
);

reportWebVitals();


/*
  <React.StrictMode>
    <Navbar />
    <Home />
  </React.StrictMode>
*/