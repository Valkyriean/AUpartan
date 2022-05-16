// Group 1 Melbourne
// Qianjun Ding 1080391
// Zhiyuan Gao 1068184
// Jiachen Li 1068299
// Yanting Mu 1068314
// Chi Zhang 1067750

import React from 'react';
import './Navbar.css';

export default class Navbar extends React.PureComponent {
  
  render() {
    return (
      <ul>
        <li><a class={this.props.home} href="/">Home</a></li>
        <li><a class={this.props.map} href="/app/map">Map</a></li>
        <li><a class={this.props.plot} href="/app/plot">Plot</a></li>
        <li><a class={this.props.submitWork} href="/app/submit">Submit Work</a></li>
      </ul>
    );
  }
}
