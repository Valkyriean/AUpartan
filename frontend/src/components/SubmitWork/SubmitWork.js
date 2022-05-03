import React from 'react';
import Navbar from '../Navbar/Navbar';
import './SubmitWork.css';
import 'antd/dist/antd.css';
import { Input } from 'antd';

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
    
    <div>
      <select id={idString + '-operator'}>
        <option value="" disabled selected>Select operation</option>
        <option value = "divide">A / B</option>
        <option value = "record A B">Scatter Plot A vs B</option>
        <option value = "record A">Bar chart Plot A (ignor B)</option>
      </select>
    </div>
  )
}

const TwitterSelectWriter = (
  id
) => {
  return(
    <div>
      <h2 class='indicator'>Get from Twitter:</h2>
      <label>Select city:
        <select id={id + '-city'}>
          <option value="" disabled selected>Select city</option>
          <option value = "Sydney">Sydney</option>
          <option value = "Melbourne">Melbourne</option>
          <option value = "Brisbane">Brisbane</option>
          <option value = "Darwin">Darwin</option>
          <option value = "Hobart">Hobart</option>
          <option value = "Perth">Perth</option>
          <option value = "Adelaide">Adelaide</option>
        </select>
      </label>
      <br/>
      <label>Search for:
        <Input id={id + '-word'} style={{ width: "99.5%", height: "35px", fontSize: "15px" }} placeholder="  e.g. kangaroo beats up man" />
      </label>
      <br/>
      <label>Select Get Method:
        <select id={id + '-method'} options={opt_Twitter_method}>

        </select>
      </label>
      <br/>
      <label>Select Processing Method:
        <select id={id + '-process'} options={opt_Twitter_process} />
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
        <select id={id + '-city'}>
          <option value="" disabled selected>Select city</option>
          <option value = "Sydney">Sydney</option>
          <option value = "Melbourne">Melbourne</option>
          <option value = "Brisbane">Brisbane</option>
          <option value = "Darwin">Darwin</option>
          <option value = "Hobart">Hobart</option>
          <option value = "Perth">Perth</option>
          <option value = "Adelaide">Adelaide</option>
        </select>
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
    console.log("id : " + id)
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
    var obj = document.getElementById('0-operator');
    console.log(obj.value);
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
        <button class = "submit" id='submit' onClick={(e) => this.collectInput(e.target.id)}> Submit Work </button>
      </div>
    );
  };
}
