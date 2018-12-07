import { combineReducers } from 'redux'
import moment from 'moment';

const events = (state = [], action) => {
  switch (action.type) {
    case 'SET_EVENTS':
      return action.events
    default:
      return state
  }
}

const lists = (state = [], action) => {
  switch (action.type) {
    case 'SET_LISTS':
      return action.lists
    default:
      return state
  }
}

const playing_now = (state = [], action) => {
  switch (action.type) {
    case 'SET_PLAYING_NOW':
      return action.playing_now
    default:
      return state
  }
}


const time = (state = moment(), action) => {
  switch (action.type) {
    case 'SET_TIME':
      return action.time
    default:
      return state
  }
}
const log_messages = (state = [], action) => {
  switch (action.type) {
    case 'ADD_LOG':
      let timestamp = moment().format('L LTS');
      let new_state = state.slice(0,5)
      new_state.splice(0,0,timestamp + ' ' + action.message)
      return new_state
    default:
      return state
  }
}




const rootReducer = combineReducers({
	events,
  lists,
  playing_now,
  time,
  log_messages
})

export default rootReducer