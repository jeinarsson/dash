from flask import render_template, request, escape, redirect, abort, jsonify
from project.www import app
import json
from itertools import groupby
from todoist.api import TodoistAPI
import project.utils.events as events
import project.dash_config as dc


##
## Routes
## 

@app.route("/api")
def api_index():
    
    return jsonify({})

@app.route("/api/events")
def api_events():

    all_events = events.get_events()
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