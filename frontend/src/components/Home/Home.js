import React, { Children } from 'react';
import Navbar from '../Navbar/Navbar';
import './Home.css';

const RecursiveComponent = ({
  rendered,
  children
}) => {
  const hasChildren = (children) => children && children.length;

  return (
    <div id='main'>
      {rendered}
      {hasChildren(children) &&
        children.map((child) => (
          <RecursiveComponent {...child} />
        ))}
    </div>
    
  );
};

export default class Home extends React.Component {
  state = {
    box: {}
  };
  componentDidMount(){
    this.setState({ box: {
      rendered: [
        <button id = "0" onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>,
        <button id = "0" onClick={(e) => this.handleClick_Get(e.target.id)}>Add Get</button>
      ]
    } });
  };

  handleClick_Op(id) {
    var ids = id.split('-');
    var newBox = this.state.box;
    switch (ids.length) {
      case 1:
        newBox.rendered = [
          <dev>
            <p>operation: a ba a ba a ba a ba a ba</p>
          </dev>
        ];
        newBox.children = [
          {
            rendered: [
              <button id = "0-0" onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>,
              <button id = "0-0" onClick={(e) => this.handleClick_Get(e.target.id)}>Add Get</button>
            ]
          },
          {
            rendered: [
              <button id = "0-1" onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>,
              <button id = "0-1" onClick={(e) => this.handleClick_Get(e.target.id)}>Add Get</button>
            ]
          }
        ];
        break;
      case 2:
        newBox.children[parseInt(ids[1])].rendered = [
          <dev>
            <p>operation: a ba a ba a ba a ba a ba</p>
          </dev>
        ];
        newBox.children[parseInt(ids[1])].children = [
          {
            rendered: [
              <button id = {id + "-0"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>,
              <button id = {id + "-0"} onClick={(e) => this.handleClick_Get(e.target.id)}>Add Get</button>
            ]
          },
          {
            rendered: [
              <button id = {id + "-1"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>,
              <button id = {id + "-1"} onClick={(e) => this.handleClick_Get(e.target.id)}>Add Get</button>
            ]
          }
        ];
        break;
      case 3:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].rendered = [
          <dev>
            <p>operation: a ba a ba a ba a ba a ba</p>
          </dev>
        ];
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children = [
          {
            rendered: [
              <button id = {id + "-0"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>,
              <button id = {id + "-0"} onClick={(e) => this.handleClick_Get(e.target.id)}>Add Get</button>
            ]
          },
          {
            rendered: [
              <button id = {id + "-1"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>,
              <button id = {id + "-1"} onClick={(e) => this.handleClick_Get(e.target.id)}>Add Get</button>
            ]
          }
        ];
        break;
      default:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children[parseInt(ids[3])].rendered = [
          <dev>
            <p>operation: a ba a ba a ba a ba a ba</p>
          </dev>
        ];
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children[parseInt(ids[3])].children = [
          {
            rendered: [
              <button id = {id + "-0"} onClick={(e) => this.handleClick_Get(e.target.id)}>Add Get</button>
            ]
          },
          {
            rendered: [
              <button id = {id + "-1"} onClick={(e) => this.handleClick_Get(e.target.id)}>Add Get</button>
            ]
          }
        ];
    }
    
    this.setState({ box: newBox });
  };

  handleClick_Get(id) {
    var ids = id.split('-');
    var newBox = this.state.box;
    switch (ids.length) {
      case 1:
        newBox.rendered = [
          <dev>
            <p>get a ba a ba</p>
          </dev>
        ];
        break;
      case 2:
        newBox.children[parseInt(ids[1])].rendered = [
          <dev>
            <p>get a ba a ba</p>
          </dev>
        ];
        break;
      case 3:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].rendered = [
          <dev>
            <p>get a ba a ba</p>
          </dev>
        ];
        break;
      case 4:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children[parseInt(ids[3])].rendered = [
          <dev>
            <p>get a ba a ba</p>
          </dev>
        ];
        break;
      default:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children[parseInt(ids[3])].children[parseInt(ids[4])].rendered = [
          <dev>
            <p>get a ba a ba</p>
          </dev>
        ];
        
    }
    
    this.setState({ box: newBox });
  };
  
  render() {
    
    return (
      <div>
        <Navbar home={'active'}/>
        <RecursiveComponent {...this.state.box} />
        
      </div>
    );
  }
}
