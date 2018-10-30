
export const setEvents = (events) => ({
  type: 'SET_EVENTS',
  events: events
});
export const setLists = (lists) => ({
  type: 'SET_LISTS',
  lists: lists
});
export const setTime = (time) => ({
  type: 'SET_TIME',
  time: time
});
export const addLog = (s) => ({
  type: 'ADD_LOG',
  message: s
});

