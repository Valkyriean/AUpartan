import React from 'react';
import Navbar from '../Navbar/Navbar';
import Select from 'react-select'
import { Input } from 'antd';
import './Home.css';

const opt_Operator = [
  { value: 'divide', label: 'A / B' },
  { value: 'record A B', label: 'Scatter Plot A vs B' },
  { value: 'record A', label: 'Bar chart Plot A (ignor B)' }
]

const opt_Twitter_City = [
  { value: 'Sydney', label: 'Sydney' },
  { value: 'Melbourne', label: 'Melbourne' },
  { value: 'Brisbane', label: 'Brisbane' },
  { value: 'Darwin', label: 'Darwin' },
  { value: 'Hobart', label: 'Hobart' },
  { value: 'Perth', label: 'Perth' },
  { value: 'Adelaide', label: 'Adelaide' },
]

const opt_Twitter_method = [
  { value: 'search', label: 'Search' },
  { value: 'stream', label: 'Stream' }
]

const opt_Twitter_process = [
  { value: 'count', label: 'Count' },
  { value: 'sentiment', label: 'Sentiment (Average)' }
]

const OperatorSelectWriter = ({
  id
}) => {
  return(
    <dev>
      <Select id={id} options={opt_Operator} />
    </dev>
  )
}

const TwitterSelectWriter = ({
  id
}) => {
  return(
    <dev>
      <h2 class='indicator'>Get from Twitter:</h2>
      <label>Select city:
        <Select id={id} options={opt_Twitter_City} />
      </label>
      <label>Search for:
        <Input id={id} style={{ width: "99.5%", height: "35px", fontSize: "15px" }} placeholder="  e.g. kangaroo beats up man" />
      </label>
      <label>Select Get Method:
        <Select id={id} options={opt_Twitter_method} />
      </label>
      <label>Select Processing Method:
        <Select id={id} options={opt_Twitter_process} />
      </label>
    </dev>
    
  )
}

const RecursiveComponent = ({
  rendered,
  children
}) => {
  const hasChildren = (children) => children && children.length;
  return (
    <div class='main'>
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
        <div>
          <button id = "0" onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
        </div>
      ]
    } });
  };

  handleClick_Op(id) {
    var ids = id.split('-');
    var newBox = this.state.box;
    switch (ids.length) {
      case 1:
        newBox.rendered = [
          <OperatorSelectWriter {...id}/>
        ];
        newBox.children = [
          {
            rendered: [
              <div>
                <button id = "0-0" onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button id = "0-0" onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button id = "0-0" onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
              </div>
            ]
          },
          {
            rendered: [
              <div>
                <button id = "0-1" onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button id = "0-1" onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button id = "0-1" onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
              </div>
            ]
          }
        ];
        break;
      case 2:
        newBox.children[parseInt(ids[1])].rendered = [
          <OperatorSelectWriter {...id}/>
        ];
        newBox.children[parseInt(ids[1])].children = [
          {
            rendered: [
              <div>
                <button id = {id + "-0"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button id = {id + "-0"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button id = {id + "-0"} onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
              </div>
            ]
          },
          {
            rendered: [
              <div>
                <button id = {id + "-1"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button id = {id + "-1"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button id = {id + "-1"} onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
              </div>
            ]
          }
        ];
        break;
      case 3:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].rendered = [
          <OperatorSelectWriter {...id}/>
        ];
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children = [
          {
            rendered: [
              <div>
                <button id = {id + "-0"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button id = {id + "-0"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button id = {id + "-0"} onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
              </div>
            ]
          },
          {
            rendered: [
              <div>
                <button id = {id + "-1"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button id = {id + "-1"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button id = {id + "-1"} onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
              </div>
            ]
          }
        ];
        break;
      default:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children[parseInt(ids[3])].rendered = [
          <OperatorSelectWriter {...id}/>
        ];
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children[parseInt(ids[3])].children = [
          {
            rendered: [
              <button id = {id + "-0"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Get</button>
            ]
          },
          {
            rendered: [
              <button id = {id + "-1"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Get</button>
            ]
          }
        ];
    }
    this.setState({ box: newBox });
  };

  handleClick_Get_twitter(id) {
    var ids = id.split('-');
    var newBox = this.state.box;
    switch (ids.length) {
      case 1:
        newBox.rendered = [
          <TwitterSelectWriter {...id}/>
        ];
        break;
      case 2:
        newBox.children[parseInt(ids[1])].rendered = [
          <TwitterSelectWriter {...id}/>
        ];
        break;
      case 3:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].rendered = [
          <TwitterSelectWriter {...id}/>
        ];
        break;
      case 4:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children[parseInt(ids[3])].rendered = [
          <TwitterSelectWriter {...id}/>
        ];
        break;
      default:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children[parseInt(ids[3])].children[parseInt(ids[4])].rendered = [
          <TwitterSelectWriter {...id}/>
        ];
    }
    this.setState({ box: newBox });
  };

  handleClick_Get_precal(id) {
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
