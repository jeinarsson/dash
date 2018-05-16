from flask import render_template, request, escape, redirect, abort, jsonify
from project.www import app
from datetime import datetime
import json
from datetime import datetime, timedelta, timezone
from project.utils.ics import get_events_from_ics
import urllib.request
from itertools import groupby
from todoist.api import TodoistAPI

##
## Load config
##

try:
    import project.dash_config as dc
except ModuleNotFoundError as e:
    import project.dash_config_default as dc


##
## Routes
## 

@app.route("/api")
def api_index():
    
    return jsonify({})

@app.route("/api/events")
def api_events():

    all_events = []
    for cal in dc.CALENDARS:

        with urllib.request.urlopen(cal['url']) as response:
           ics_string = response.read()

        now = datetime.now(timezone.utc)
        past = now - timedelta(days=30)
        future = now + timedelta(days=30)
        events = get_events_from_ics(ics_string, past, future)
        for e in events:
            e['calendar']=cal['name']
            e['color']=cal['color']

        all_events += events

    def sortkey(e):
        if isinstance(e['startdt'], datetime):
            return e['startdt'].utctimetuple()
        else:
            return e['startdt'].timetuple()


    all_events.sort(key=sortkey)

    for e in all_events:
        # since flask jsonify doesn't handle tz, convert explicitly:
        e['startdt']=e['startdt'].isoformat()
        if e['enddt']:
            e['enddt']=e['enddt'].isoformat()

    return jsonify(all_events)


def todoist_item_to_dash(it):
    return {
            'id': it['id'],
            'parent_id': it['parent_id'],
            'content': it['content'],
            'order': it['item_order'],
            'indent': it['indent'],
            'priority': it['priority'],
            'checked': it['checked']
            }


@app.route("/api/lists")
def api_lists():

    api = TodoistAPI(dc.TODOIST['apikey'])
    api.sync()

    res = []

    for p in api.state['projects']:

        if (not 'projects' in dc.TODOIST) or p['name'] in dc.TODOIST['projects']:
            data = api.projects.get_data(p['id'])
            
            if not 'items' in data:
                print('response:', data)
                continue
                    
            raw_items = data['items']

            def get_children(parent_id):
                children = [todoist_item_to_dash(it) for it in
                    filter(lambda it: it['parent_id']==parent_id,  data['items'])]


                for c in children:
                    c['items'] = get_children(c['id'])

                return children

            items = get_children(None)

    
            res.append({
                'name': p['name'],
                'items': items,
                'color': p['color'],
                'raw_items': data['items']
                })

    return jsonify(res)