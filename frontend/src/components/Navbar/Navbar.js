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
