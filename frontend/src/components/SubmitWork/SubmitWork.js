import React, { useRef } from 'react';
import Navbar from '../Navbar/Navbar';
import Select from 'react-select'
import { Input, Button } from 'antd';
import './SubmitWork.css';

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

const handleSelectChange = (
  id,
  event
) => {
  console.log(id);
  console.log(event);
}

const OperatorSelectWriter = (
  id
) => {
  let idString = ''
  Object.keys(id).forEach(element => {
    idString = idString + id[element]
  }); 
  return(
    
    <dev>
      <Select id={idString + '-operator'} options={opt_Operator} onChange={handleSelectChange(idString + '-operator', this)}/>
    </dev>
  )
}

const TwitterSelectWriter = (
  id
) => {
  return(
    <div>
      <h2 class='indicator'>Get from Twitter:</h2>
      <label>Select city:
        <Select id={id + '-city'} options={opt_Twitter_City} />
      </label>
      <label>Search for:
        <Input id={id + '-word'} style={{ width: "99.5%", height: "35px", fontSize: "15px" }} placeholder="  e.g. kangaroo beats up man" />
      </label>
      <label>Select Get Method:
        <Select id={id + '-method'} options={opt_Twitter_method} />
      </label>
      <label>Select Processing Method:
        <Select id={id + '-process'} options={opt_Twitter_process} />
      </label>
    </div>
    
  )
}

const PreCalculatedWriter = (
  id
) => {
  return(
    <div>
      <h2 class='indicator'>Use Our Pre-Calculated Data:</h2>
      <label>Select city:
        <Select id={id + '-city'} options={opt_Twitter_City} />
      </label>
      <label>Search for:
        <Input id={id + '-word'} style={{ width: "99.4%", height: "35px", fontSize: "15px" }} placeholder="  e.g. kangaroo beats up man" />
      </label>
    </div>
    
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

export default class SubmitWork extends React.Component {
  state = {
    box: { },
    submit: { }, 
  };
  componentDidMount(){
    this.setState({ 
      box: {
        rendered: [
          <div>
            <button class = "default" id = "0" onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
          </div>
        ]
      }
    });
  };

  handleClick_Op(id) {
    var ids = id.split('-');
    var newBox = this.state.box;
    switch (ids.length) {
      case 1:
        console.log("id : " + id)
        newBox.rendered = [
          <OperatorSelectWriter {...id}/>
        ];
        newBox.children = [
          {
            rendered: [
              <div>
                <button class = "default" id = "0-0" onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button class = "default" id = "0-0" onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button class = "default" id = "0-0" onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
              </div>
            ]
          },
          {
            rendered: [
              <div>
                <button class = "default" id = "0-1" onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button class = "default" id = "0-1" onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button class = "default" id = "0-1" onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
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
                <button class = "default" id = {id + "-0"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button class = "default" id = {id + "-0"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button class = "default" id = {id + "-0"} onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
              </div>
            ]
          },
          {
            rendered: [
              <div>
                <button class = "default" id = {id + "-1"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button class = "default" id = {id + "-1"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button class = "default" id = {id + "-1"} onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
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
                <button class = "default" id = {id + "-0"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button class = "default" id = {id + "-0"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button class = "default" id = {id + "-0"} onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
              </div>
            ]
          },
          {
            rendered: [
              <div>
                <button class = "default" id = {id + "-1"} onClick={(e) => this.handleClick_Op(e.target.id)}>Add Operation</button>
              </div>,
              <div>
                <button class = "default" id = {id + "-1"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter</button>
                <button class = "default" id = {id + "-1"} onClick={(e) => this.handleClick_Get_precal(e.target.id)}>Add Our Pre-Calculated Data</button>
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
              <button class = "default" id = {id + "-0"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Get</button>
            ]
          },
          {
            rendered: [
              <button class = "default" id = {id + "-1"} onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Get</button>
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
          <div>
            <PreCalculatedWriter {...id}/>
          </div>
        ];
        break;
      case 2:
        newBox.children[parseInt(ids[1])].rendered = [
          <div>
            <PreCalculatedWriter {...id}/>
          </div>
        ];
        break;
      case 3:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].rendered = [
          <div>
            <PreCalculatedWriter {...id}/>
          </div>
        ];
        break;
      case 4:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children[parseInt(ids[3])].rendered = [
          <div>
            <PreCalculatedWriter {...id}/>
          </div>
        ];
        break;
      default:
        newBox.children[parseInt(ids[1])].children[parseInt(ids[2])].children[parseInt(ids[3])].children[parseInt(ids[4])].rendered = [
          <div>
            <PreCalculatedWriter {...id}/>
          </div>
        ];
    }
    this.setState({ box: newBox });
  };
  
  collectInput(id) {
    let result = document.getElementById('0-operator');
    console.log(result.options[result.selectedIndex].value);
    this.collectRecursive(this.state.box, '0');
  };

  collectRecursive(parent, id) {
    if (parent.children) {
      this.collectRecursive(parent.children[0], id + '-0');
      this.collectRecursive(parent.children[1], id + '-1');
    } else {
      console.log(id);
    }
  }

  render() {
    return (
      <div>
        <Navbar submitWork={'active'}/>
        <RecursiveComponent {...this.state.box} />
        <button class = 'submit' id='submit' onClick={(e) => this.collectInput(e.target.id)}> Submit Work </button>
      </div>
    );
  };
}
