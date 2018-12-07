import { setPlayingNow } from '../actions/'
import { appendLog } from '../Log';

class PlayingNowProvider {
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

        fetch('/api/sonos/playing')
          .then(response => {
            if (!response.ok) {
              appendLog('Request to /api/sonos/playing failed: ' + response.status + ' ' + response.statusText)
            }
            return response
          })
          .then(d => d.json())
          .then(d => {
            this.dispatch(setPlayingNow(d));
            this.restartTimer();
          })        
    }    
}

export default PlayingNowProvider;