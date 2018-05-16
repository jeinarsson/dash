import React, { Component } from 'react';
import { connect } from 'react-redux'
import { eventTr } from './Agenda'

import './Today.css'


class Today extends Component {

constructor(props){
  super(props)
}

render() {

  let today = this.props.time;
  let events = this.props.events.filter( (e) => {
    if (e.startdt.isAfter(today,'day')) {
      return false;
    }
    if (e.is_reminder && !e.reminder_is_done) {
      return true;
    }
    if (e.allday){
      return !e.enddt.clone().subtract(1,'day').isBefore(today,'day');
    } else {
      return !e.enddt.isBefore(today,'day');
    }
  });  
  return (<div className="Today">
    <h1 className='Time'>{today.format('LT')}</h1>
    <h1 className='Date'>{today.format('dddd LL')}</h1>
    <table className='eventRowTable'><tbody>
    { events.map(eventTr(today)) }
    </tbody></table>
    </div>
    )
}



}



const mapStateToProps = (state) => ({
  events: state.events,
  time: state.time
})
const ConnectedToday = connect(
  mapStateToProps,
  null
)(Today)

export default ConnectedToday