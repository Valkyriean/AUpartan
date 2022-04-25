import React from 'react';

import Navbar from '../Navbar/Navbar';

export default class Home extends React.PureComponent {
  render() {
    return (
      <div>
        <Navbar home={'active'}/>
        <h1>I am Home page!</h1>
      </div>
    );
  }
}
