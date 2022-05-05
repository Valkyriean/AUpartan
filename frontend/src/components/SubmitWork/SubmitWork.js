import React from 'react';
import Navbar from '../Navbar/Navbar';
import './SubmitWork.css';

const OperatorSelectWriter = (
  id
) => {
  let idString = ''
  Object.keys(id).forEach(element => {
    idString = idString + id[element]
  }); 
  if (idString == '0'){
    return(
      <div>
        <div class='selectDiv'>
          <label>Select city:
            <select id={idString + '-operator'}>
              <option value = "" disabled selected>Select operation</option>
              <option value = "divide">A / B</option>
              <option value = "record A B">Scatter Plot A vs B</option>
              <option value = "record A">Bar chart Plot A (ignor B)</option>
            </select>
          </label>  
          <br/>
          <label>Select scale:
            <select id={'scale'}>
              <option value="" disabled selected>Select scale</option>
              <option value = "City">City</option>
              <option value = "SA3">SA3</option>
            </select>
          </label>
          <br/>
          <label>Task name:
            <input id={'name'} placeholder="  e.g. Percentage of people have favourable opinion of kangaroos" />
          </label>
        </div>
      </div>
    ) 
  } else {
    return(
      <div>
        <div class='selectDiv'>
          <label>Select city:
            <select id={idString + '-operator'}>
              <option value = "" disabled selected>Select operation</option>
              <option value = "divide">A / B</option>
              <option value = "record A B">Scatter Plot A vs B</option>
              <option value = "record A">Bar chart Plot A (ignor B)</option>
            </select>
          </label>  
        </div>
      </div>
    ) 
  }
}

const TwitterSelectWriter = (
  id
) => {
  let idString = ''
  Object.keys(id).forEach(element => {
    idString = idString + id[element]
  }); 
  return(
    <div>
      <h2 class='indicator'>Get from Twitter:</h2>
      <label>Select city:
        <select id={idString + '-city'}>
          <option value = "" disabled selected>Select city</option>
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
        <input id={idString + '-word'} placeholder="  e.g. kangaroo beats up man" />
      </label>
      <br/>
      <label>Select Get Method:
        <select id={idString + '-method'}>
          <option value = "" disabled selected>Select get method</option>
          <option value = "search">Search</option>
          <option value = "stream">Stream</option>
        </select>
      </label>
      <br/>
      <label>Select Processing Method:
        <select id={idString + '-process'}>
          <option value = "" disabled selected>Select process method</option>
          <option value = "count">Count</option>
          <option value = "sentiment">Sentiment (Average)</option>
        </select>
      </label>
    </div>
    
  )
}

const PreCalculatedWriter = (
  id
) => {
  let idString = ''
  Object.keys(id).forEach(element => {
    idString = idString + id[element]
  }); 
  return(
    <div>
      <h2 class='indicator'>Use Our Pre-Calculated Data:</h2>
      <label>Search for:
        <input id={idString + '-file'} placeholder="  e.g. kangaroo beats up man" />
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
  
  collectinput(id) {
    var jsonObj = this.collectRecursive(this.state.box, '0');
    jsonObj['scale'] = document.getElementById('scale').value;
    jsonObj['name'] = document.getElementById('name').value;
    console.log(jsonObj);
  };

  collectRecursive(parent, id) {
    var ret = {};
    if (parent.children) {
      for (const tag of ['operator']) {
        var obj = document.getElementById(id + '-' + tag);
        if (obj) ret[tag] = obj.value;
      }
      ret['data0'] = this.collectRecursive(parent.children[0], id + '-0');
      ret['data1'] = this.collectRecursive(parent.children[1], id + '-1');
      return ret;
    } else {
      for (const tag of ['city', 'word', 'method', 'process', 'file']) {
        var obj = document.getElementById(id + '-' + tag);
        if (obj) ret[tag] = obj.value;
      }
      return ret;
    }
  }

  render() {
    return (
      <div>
        <Navbar submitWork={'active'}/>
        <RecursiveComponent {...this.state.box} />
        <button class = "submit" id='submit' onClick={(e) => this.collectinput(e.target.id)}> Submit Work </button>
      </div>
    );
  };
}
