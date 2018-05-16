import moment from 'moment'
import { setLists } from '../actions/'
class ListsProvider {
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

        fetch('/api/lists')
          .then(response => {
            if (!response.ok) {
              console.log(response)
              this.restartTimer();
            }
            return response
          })
          .then(d => d.json())
          .then(d => {
            this.dispatch(setLists(d));

            this.restartTimer();
          })        
    }    
}

export default ListsProvider;