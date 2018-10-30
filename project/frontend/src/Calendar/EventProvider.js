import moment from 'moment'
import { setEvents } from '../actions/'
import { appendLog } from '../Log';

class EventProvider {
    constructor(dispatch, interval) {
    	this.dispatch = dispatch;
    	this.interval = interval;
        this.timer = null;
        this.run = this.run.bind(this)
        this.stop = this.stop.bind(this)
    }
    restartTimer() {
        this.stop();
        if (!this.timer) {
            this.timer = setTimeout(this.run, this.interval);
        }
    }
    stop() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }
    run() {
        this.stop()

        fetch('/api/events')
          .then(response => {
            if (!response.ok) {
              appendLog('Request to /api/events failed: ' + response.status + ' ' + response.statusText)
            }
            return response
          })
          .then(d => d.json())
          .then(d => {

            d.forEach(e => {
                e.startdt = moment(e.startdt);
                e.enddt = moment(e.enddt);
            });


          
            this.dispatch(setEvents(d));

            this.restartTimer();
          })        
    }    
}

export default EventProvider;