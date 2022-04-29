import Navbar from '../Navbar/Navbar';
import React from 'react';

import Plotly from "plotly.js-basic-dist";

import createPlotlyComponent from "react-plotly.js/factory";
const Plot = createPlotlyComponent(Plotly);

export default class PlotPoint extends React.Component {
  render() {
    var data = [
      {
        x: [1.5, 2, 3.2, 4.5, 5],
        y: [3, 3.2, 8, 10, 9],
        mode: 'markers',
        type: 'scatter',
        name: 'Others',
        text: ['EAST MELBOURNE, VIC', 'MELBOURNE AIRPORT, VIC', 'WEST MELBOURNE, VIC', 'SOUTH YARRA, VIC', 'SPRINGVALE, VIC'],
        marker: { size: 12 }
      },
      {
        x: [3],
        y: [6],
        mode: 'markers',
        type: 'scatter',
        name: 'Selected',
        text: ['MELBOURNE CBD, VIC'],
        marker: { size: 12 }
      }
    ];
    return (
      <dev>
          <Navbar plot={'active'}/>
          <Plot
            data={data}
            layout={ {
              width: 600, 
              height: 500, 
              showlegend: false,
              title: 'Pay Roll vs Happyness Plot',
              xaxis: {
                title: {
                  text: "Pay Roll (1,000 AUD/Week)"
                }
              },
              yaxis: {
                title: {
                  text: "Happyness"
                }
              }
            } }
        />
      </dev>
      
    );
  }
}


