import React, { Component } from 'react';
import { connect } from 'react-redux'

import './Month.css'
import moment from 'moment'

class Month extends Component {

constructor(props){
  super(props)
}

render() {
  return null;
}

}


const mapStateToProps = (state) => ({
  events: state.events
})
const ConnectedMonth = connect(
  mapStateToProps,
  null
)(Month)

export default ConnectedMonth