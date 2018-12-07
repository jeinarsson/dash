import soco

import project.dash_config as dc

def get_track_info(device):
    info = device.get_current_track_info()
    return {
        'artist': info['artist'],
        'album': info['album'],
        'album_art': info['album_art'],
        'title': info['title'],
        'duration': info['duration'],
        'position': info['position']
    }

def get_group_info(group):
    return [m.player_name for m in group.members]

def get_playing():

    if not 'ip' in dc.SONOS:
        return []


    entry_device = soco.core.SoCo(dc.SONOS['ip'])
    print(entry_device)
    result = []
    for group in entry_device.all_groups:
        
        d = group.coordinator
        
        if not d.get_current_transport_info()['current_transport_state'] == 'PLAYING':
            continue
        

        track_info = get_track_info(d)
        group_info = get_group_info(group)

        result.append({'group': group_info, 'track': track_info})

    return result
