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
const time = (state = moment(), action) => {
  switch (action.type) {
    case 'SET_TIME':
    	return action.time
    default:
      return state
  }
}



const rootReducer = combineReducers({
	events,
  lists,
	time
})

export default rootReducer