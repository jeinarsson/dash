import React, { Component } from 'react';
import { dispatch } from './'

import EventProvider from './Calendar/EventProvider'
import TimeProvider from './TimeProvider'
import Month from './Calendar/Month';
import Agenda from './Calendar/Agenda';
import Today from './Calendar/Today';
import ListsProvider from './Lists/ListsProvider';
import List from './Lists/List';

import Log from './Log';
import { appendLog } from './Log';
import './App.css';



class App extends Component {

constructor(props) {
    super(props)
    this.dataProviders = [
        new EventProvider(dispatch, 10*60*1000),
        // new ListsProvider(dispatch, 10*60*1000),
        new TimeProvider(dispatch, 10*1000)
    ]
}
componentDidMount() {
    this.dataProviders.forEach(p => p.run())
} 
componentWillUnmount() {
    this.dataProviders.forEach(p => p.stop())
}

render() {
return (
        <div>
        <div className="region fullscreen below"> <div className="container"></div></div>
        <div className="region top left"><div className="container">
        <Today/>
        <Agenda/>
        </div></div>
        <div className="region top center"><div className="container"></div></div>
        <div className="region top right"><div className="container">
        </div></div>
        <div className="region upper third"><div className="container"></div></div>
        <div className="region middle center"><div className="container"></div></div>
        <div className="region lower third"><div className="container"><br/></div></div>
        <div className="region bottom left"><div className="container"></div></div>
        <div className="region bottom center"><div className="container"></div></div>
        <div className="region bottom right"><div className="container">
        <Log/>
        </div></div>
        <div className="region fullscreen above"><div className="container"></div></div>
        </div>
    )
}

}

export default App;
