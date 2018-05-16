import React, { Component } from 'react';
import { connect } from 'react-redux'

import './Agenda.css'

import moment from 'moment';


export function eventTr(now) {
  return function(d,idx) {

    let timestamp = (
      <span className='timestamp'>
      { d.startdt.format('h') + (d.startdt.minutes() ? d.startdt.format('[:]mm') : '') + d.startdt.format('a')}
      </span>
      );

    let reminderIconClass = 'reminder-icon';
    let reminderText = null;
    if (d.is_reminder && d.startdt.isBefore(now,'day')) {
      reminderIconClass += ' overdue'
      reminderText = (
        <span className='reminder-text'>{now.diff(d.startdt,'days')} days overdue</span>
        )
    }
    if (d.startdt.isSame(now,'day')) {
      reminderIconClass += ' today'
    }

    let reminderIcon = (
      d.is_reminder ? <i className={"far fa-bell "+reminderIconClass}></i> : null
      )

    if (d.allday) timestamp = null;
    let trClass = '';
    if (!d.allday && !d.is_reminder && d.enddt < now) {
      trClass = 'passed'
    }
    if (d.is_reminder && d.reminder_is_done) {
      trClass = 'passed'
    }

    return (
      <tr key={idx} className={trClass}>
      <td className='event-symbol'><span style={{color: d.color}}>[{d.calendar[0]}]</span></td>
      <td className='event-data'>{reminderIcon}{reminderText}{timestamp}<span className='summary'>{d.summary}</span></td>
      </tr>
      );
  }
}

class Agenda extends Component {

constructor(props){
  super(props)
  this.agendaDay = this.agendaDay.bind(this);

  this.numDays = 6;
}

render() {
  let today = this.props.time;
  let days = []
  for (let k=1; k <= this.numDays; k++) {
    let date = today.clone().add(k, 'day');
    let events = this.props.events.filter( (e) => {
      if (e.allday){
        return !(e.startdt.isAfter(date,'day') || e.enddt.clone().subtract(1,'day').isBefore(date,'day'));
      } else {
        return !(e.startdt.isAfter(date,'day') || e.enddt.isBefore(date,'day'));
      }
    });

    if (events.length) {
      days.push({
        date: date,
        events: events
      })
    }
  }
  return (
  <div className="Agenda">
  {days.map(this.agendaDay)}
  </div>
  )

}

agendaDay(d,idx) {
  return (
    <div className='agendaDay' key={idx}>
    <table><tbody><tr>
    <td className='agendaDayLabel'>
    <span className='weekday'>{d.date.format('dddd')}</span><br/>
    <span className='fromnow'>{d.date.startOf('day').from(moment().startOf('day')).replace('in a day', 'Tomorrow')}</span><br/>
    <span className='date'>{d.date.format('ll')}</span>
    </td>
    <td className='agendaDayEvents'>
    <table className='eventRowTable'><tbody>
    { d.events.map(eventTr(this.props.time)) }
    </tbody></table>
    </td>
    </tr></tbody></table>
    </div>
  );
}



}



const mapStateToProps = (state) => ({
  events: state.events,
  time: state.time
})
const ConnectedAgenda = connect(
  mapStateToProps,
  null
)(Agenda)


export default ConnectedAgenda