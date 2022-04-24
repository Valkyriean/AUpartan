import React from 'react';
import {  Link } from "react-router-dom";
const navbar= () =>{
  return (
  <div>
    <li>
      <Link to="/">Home</Link>
    </li>
    <li>
      <Link to="/map">Map</Link>
    </li>
    <li>
      <Link to="/graph">Graphs</Link>
    </li>
  </div>
  );
}
export default navbar;