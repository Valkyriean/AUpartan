// Group 1 Melbourne
// Qianjun Ding 1080391
// Zhiyuan Gao 1068184
// Jiachen Li 1068299
// Yanting Mu 1068314
// Chi Zhang 1067750


import React from 'react';
import Navbar from '../Navbar/Navbar';
import background from './img/back.jpg';
import aupartan from './img/AUpartan_tran.png';
import './Home.css'

export default class Home extends React.PureComponent {
  
  render() {
    return (
      <div>
        <Navbar home={'active'}/>
        <div style={{
          height: '95vh', 
          backgroundImage: `url(${background})`, 
          opacity: '0.1',
          }}
        />
        <h2 class='latinthingthing'>Ut Aurin et Spartanae Crescant in Existimationem Nostram</h2>
        <h2 class='description1'>Extendable Computing System Focused on City Liveabality Implimented By:</h2>
        <h2 class='description2'>Qianjun Ding --- Zhiyuan Gao --- Jiachen Li --- Yanting Mu --- Chi Zhang</h2>
        <img class='aupartan' src={aupartan} />
        <p className='author'>Background Image by: Chuyin Qi</p>
      </div>
    );
  }
}
