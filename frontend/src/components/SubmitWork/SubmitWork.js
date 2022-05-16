// Group 1 Melbourne
// Qianjun Ding 1080391
// Zhiyuan Gao 1068184
// Jiachen Li 1068299
// Yanting Mu 1068314
// Chi Zhang 1067750

import React from 'react';
import Navbar from '../Navbar/Navbar';
import './SubmitWork.css';
import {useEffect, useState, useRef} from 'react';

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
      <label>Search for:   
        <input id={idString + '-word'} placeholder="  e.g. kangaroo beats up man" />
      </label>
      <br/>
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

function PreCalculatedWriter_City (id) {
  console.log(id)
  id = id[0] + id[1] + id[2] 
  console.log(id)
  const [list, setList] = useState([]);
  useEffect(()=>{
  fetch("http://172.26.133.167:3000/request/submit", {
    method: "POST",
    headers: {'Content-Type': 'application/json' },
    body: JSON.stringify({
      'request': "preCalculatedList_City"
    })
  })
  .then(response => response.json())
  .then(response => {
    setList(response.preCalculatedList);     // replace with reading standard json
  });
  }, []);
  let datas = Array.from(list)
  return (
    <label>Select Data:   
      <select id={id + '-preCal'}>
        <option value="" disabled selected>Select pre-calculated data from AURIN </option>
        {datas.map(todo => 
        <option key={todo}>{todo}</option>)}
      </select>
    </label>
  )
};

function PreCalculatedWriter_SA3 (id) {
  console.log(id)
  id = id[0] + id[1] + id[2] 
  console.log(id)
  const [list, setList] = useState([]);
  useEffect(()=>{
  fetch("http://172.26.133.167:3000/request/submit", {
    method: "POST",
    headers: {'Content-Type': 'application/json' },
    body: JSON.stringify({
      'request': "preCalculatedList_SA3"
    })
  })
  .then(response => response.json())
  .then(response => {
    setList(response.preCalculatedList);     // replace with reading standard json
  });
  }, []);
  let datas = Array.from(list)
  return (
    <label>Select Data: 
      <select id={id + '-preCal'}>
        <option value="" disabled selected>Select pre-calculated data from AURIN </option>
        {datas.map(todo => 
        <option key={todo}>{todo}</option>)}
      </select>
    </label>
  )
};

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
            <div>
              <button class = "default" id = "0" onClick={(e) => this.handleClick_Op_City_1(e.target.id)}>Request Bar Chart (7 Major Cities)</button>
              <button class = "default" id = "0" onClick={(e) => this.handleClick_Op_SA3_1(e.target.id)}>Request Bar Chart (Melbourne Suburbs)</button>
            </div>
            <div>
              <button class = "default" id = "0" onClick={(e) => this.handleClick_Op_City_2(e.target.id)}>Request Scatter Plot (7 Major Cities)</button>
              <button class = "default" id = "0" onClick={(e) => this.handleClick_Op_SA3_2(e.target.id)}>Request Scatter Plot (Melbourne Suburbs)</button>
            </div>
          </div>
        ]
      }
    });
  };

  handleClick_Op_City_2(id) {
    console.log("id : " + id)
    var newBox = this.state.box;
    newBox.rendered = [
      <div class='selectDiv'>
        <p id='City'>Scale = City</p>
        <label>Task name:
            <input id={'name'} placeholder="  e.g. people have favourable opinion of kangaroos" />
        </label>
      </div>
    ];
    newBox.children = [
      {
        rendered: [
          <div>
            <button class = "default" id = "0-0" onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter (search)</button>
            <button class = "default" id = "0-0" onClick={(e) => this.handleClick_Get_precal(e.target.id, 'City')}>Add Pre-Calculated Data (from AURIN)</button>
          </div>
        ]
      },
      {
        rendered: [
          <div>
            <button class = "default" id = "0-1" onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter (search)</button>
            <button class = "default" id = "0-1" onClick={(e) => this.handleClick_Get_precal(e.target.id, 'City')}>Add Pre-Calculated Data (from AURIN)</button>
          </div>
        ]
      }
    ];
    this.setState({ box: newBox });
  };

  handleClick_Op_SA3_2(id) {
    console.log("id : " + id)
    var newBox = this.state.box;
    newBox.rendered = [
      <div class='selectDiv'>
        <p id='SA3'>Scale = Suburbs in Melbourne</p>
        <label>Task name:
            <input id={'name'} placeholder="e.g. people have favourable opinion of kangaroos" />
        </label>
      </div>
    ];
    newBox.children = [
      {
        rendered: [
          <div>
            <button class = "default" id = "0-0" onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter (search)</button>
            <button class = "default" id = "0-0" onClick={(e) => this.handleClick_Get_precal(e.target.id, 'SA3')}>Add Pre-Calculated Data (from AURIN)</button>
          </div>
        ]
      },
      {
        rendered: [
          <div>
            <button class = "default" id = "0-1" onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter (search)</button>
            <button class = "default" id = "0-1" onClick={(e) => this.handleClick_Get_precal(e.target.id, 'SA3')}>Add Pre-Calculated Data (from AURIN)</button>
          </div>
        ]
      }
    ];
    this.setState({ box: newBox });
  };

  handleClick_Op_City_1(id) {
    console.log("id : " + id)
    var newBox = this.state.box;
    newBox.rendered = [
      <div class='selectDiv'>
        <p id='City'>Scale = City</p>
        <label>Task name:
            <input id={'name'} placeholder="  e.g. people have favourable opinion of kangaroos" />
        </label>
      </div>
    ];
    newBox.children = [
      {
        rendered: [
          <div>
            <button class = "default" id = "0-0" onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter (search)</button>
            <button class = "default" id = "0-0" onClick={(e) => this.handleClick_Get_precal(e.target.id, 'City')}>Add Pre-Calculated Data (from AURIN)</button>
          </div>
        ]
      }
    ];
    this.setState({ box: newBox });
  };

  handleClick_Op_SA3_1(id) {
    console.log("id : " + id)
    var newBox = this.state.box;
    newBox.rendered = [
      <div class='selectDiv'>
        <p id='SA3'>Scale = Suburbs in Melbourne</p>
        <label>Task name:
            <input id={'name'} placeholder="e.g. people have favourable opinion of kangaroos" />
        </label>
      </div>
    ];
    newBox.children = [
      {
        rendered: [
          <div>
            <button class = "default" id = "0-0" onClick={(e) => this.handleClick_Get_twitter(e.target.id)}>Add Data from Twitter (search)</button>
            <button class = "default" id = "0-0" onClick={(e) => this.handleClick_Get_precal(e.target.id, 'SA3')}>Add Pre-Calculated Data (from AURIN)</button>
          </div>
        ]
      }
    ];
    this.setState({ box: newBox });
  };

  handleClick_Get_twitter(id) {
    var ids = id.split('-');
    var newBox = this.state.box;
    newBox.children[parseInt(ids[1])].rendered = [
      <TwitterSelectWriter {...id}/>
    ];
    this.setState({ box: newBox });
  };

  handleClick_Get_precal(id, scale) {
    var ids = id.split('-');
    var newBox = this.state.box;
    if (scale == 'SA3'){
      newBox.children[parseInt(ids[1])].rendered = [
      <div>
        <PreCalculatedWriter_SA3 {...id}/>
      </div>
    ];
    }
    if (scale == 'City'){
      newBox.children[parseInt(ids[1])].rendered = [
        <div>
          <h2 class='indicator'>Get Pre-Calculated Data:</h2>
          <PreCalculatedWriter_City {...id}/>
        </div>
      ];
    }
    
    
    this.setState({ box: newBox });
  };
  
  collectinput() {
    var ret = {'request': "task"};
    for (const tag of ['SA3', 'City']) {
      var obj = document.getElementById(tag);
      if (obj) ret['scale'] = tag;
    }
    
    for (const tag of ['name', '0-0-word', '0-0-process', '0-0-preCal', '0-1-word', '0-1-process', '0-1-preCal']) {
      var obj = document.getElementById(tag);
      if (obj) ret[tag] = obj.value;
    }
    console.log(ret)
    
    fetch("http://172.26.133.167:3000/request/submit", {
    method: "POST",
    headers: {'Content-Type': 'application/json' },
    body: JSON.stringify(ret)
    }).then(response => response.json())
    .then(response => {
      console.log(response.state);
      if (response.state == 'success') {
        document.getElementById('submit').style.color = 'green';
        document.getElementById('submit').textContent = 'success';
        document.getElementById('submit').disabled = true;
      }
      if (response.state == 'failed') {
        window.location.assign("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
      }
    });
  };

  render() {
    return (
      <div>
        <Navbar submitWork={'active'}/>
        <RecursiveComponent {...this.state.box} />
        <button class = "submit" id='submit' onClick={(e) => this.collectinput()}> Submit Work </button>
      </div>
    );
  };
}
