import React, { Component } from 'react';
import { connect } from 'react-redux'
import { dispatch } from './';
import { addLog } from './actions/';

import './Log.css';


class Log extends Component {

    constructor(props) {
        super(props)
    }

    itemLi(d, idx) {
        return (
            <li key={idx}>{d}</li>
        )
    }
    render() {

        let lines = this.props.messages;
        console.log(lines)
        let output = (<div className="Log">
            <ul>
                { lines.map(this.itemLi) }
            </ul>
        </div>
        );
        console.log(output);
        return output;
    }



}



const mapStateToProps = (state) => ({
    messages: state.log_messages
})
const ConnectedLog = connect(
    mapStateToProps,
    null
)(Log)

export default ConnectedLog

export const appendLog = s => dispatch(addLog(s));