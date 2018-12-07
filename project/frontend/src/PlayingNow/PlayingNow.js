import React, { Component } from 'react';
import { connect } from 'react-redux'

import './PlayingNow.css'
import moment from 'moment'

function PlayingGroup(d, idx) {
  return (<div className="playingGroup">
    <div className="albumart"><img src={d.track.album_art}/></div>
    <div className="meta">
      <p className="title">{d.track.title}</p>
      <p className="artist-album">{d.track.artist} - {d.track.album}</p>
    </div>
  </div>)
}

class PlayingNow extends Component {

constructor(props){
  super(props)
}

render() {
  console.log(this.props.playing_now);
  return this.props.playing_now.map(PlayingGroup);
}

}


const mapStateToProps = (state) => ({
  playing_now: state.playing_now
})
const ConnectedPlayingNow = connect(
  mapStateToProps,
  null
)(PlayingNow)

export default ConnectedPlayingNow