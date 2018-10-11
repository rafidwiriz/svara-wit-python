from flask import Flask, request, make_response, jsonify, redirect
import requests
import datetime

from config import *

app = Flask(__name__)
WIT_TOKEN = 'RUU3F6BNDSDLL7RO6ZLL6V6IKN3Z5T4W'

@app.route('/wit', methods=['POST'])
def wit():
    req = request.get_json(silent=True, force=True)
    txt = req.get('text')

    params = {'v': get_string_date(), 'q': txt}
    headers = {'Authorization': 'Bearer ' + WIT_TOKEN}
    res = requests.get("https://api.wit.ai/message", params=params, headers=headers)
    res = res.json()

    if res['entities']['intent']:
        r = intent_switch(res, res['entities']['intent'][0]['value'])

    if r:
        if (type(r) == list):
            print(type(r))
            r = make_response(jsonify(r))
            r.headers['Content-Type'] = "application/json"
            r = (r, 200)
        else:
            r = redirect(r, code=302)
    else:
        r = make_response(jsonify({"text": "Oops. Something went wrong!"}))
        r.headers['Content-Type'] = "application/json"
        r = (r, 404)

    return r

def get_string_date():
    now = datetime.date.today()

    y = "{}".format(now.year)
    m = "%02{}".format(now.month)
    d = "%02{}".format(now.day)
    
    return (y + m + d)

def read_value(entity):
    return entity[0]['value']

def search_svara(params):
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN, 'x-consumer-username': ACCESS_TOKEN}
    r = requests.get(BASE_URL + "search", params=params, headers=headers)

    return r.json()

def intent_switch(req, act):
    FUNC_DICT = {
        'add_to_library': addTo_library,
        'add_to_playlist': addTo_playlist,
        'music.add_to_queue': music_addTo_queue,
        'music.play_album': music_play_album,
        'music.play_artist': music_play_artist,
        'music.play_popular': music_play_popular,
        'music.play_title': music_play_title,
        'play_recommendation': play_recommendation,
        'playlist.play': playlist_play,
        'radio.play': radio_play,
        'radio_content.play_radio': radioContent_play_radio,
        'radio_content.play_tag': radioContent_play_tag,
        'radio_content.play_title': radioContent_play_title,
        'search': search,
    }
    
    return FUNC_DICT[act](req)

def addTo_library(req):
    pass

def addTo_playlist(req):
    pass

def music_addTo_queue(req):
    pass

def music_play_album(req):
    title_album = read_value(req['entities']['title_album'])
    name_artist = read_value(req['entities']['name_artist']) if req.get('entities').get('name_artist') else None

    params = {'query': title_album, 'type': 'Album'}
    r = search_svara(params)

    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://play.svara.id/Album/{}".format(id)

def music_play_artist(req):
    name_artist = read_value(req['entities']['name_artist'])

    params = {'query': name_artist, 'type': 'Artist'}
    r = search_svara(params)

    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://play.svara.id/Artist/{}".format(id)

def music_play_popular(req):
    pass

def music_play_title(req):
    title_song = read_value(req['entities']['title_song'])
    name_artist = read_value(req['entities']['name_artist']) if req.get('entities').get('name_artist') else None

    params = {'query': title_song, 'type': 'Music'}
    r = search_svara(params)

    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://play.svara.id/Music/{}".format(id)

def play_recommendation(req):
    pass

def playlist_play(req):
    name_playlist = read_value(req['entities']['name_playlist'])

    params = {'query': name_playlist, 'type': 'Playlist'}
    r = search_svara(params)

    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://play.svara.id/Playlist/{}".format(id)

def radio_play(req):
    name_radio = read_value(req['entities']['name_radio'])

    params = {'query': name_radio, 'type': 'Radio'}
    r = search_svara(params)

    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://play.svara.id/Radio/{}".format(id)

def radioContent_play_radio(req):
    name_radio = read_value(req['entities']['name_radio'])

    params = {'query': name_radio, 'type': 'RadioContent'}
    r = search_svara(params)

    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://play.svara.id/RadioContent/{}".format(id)

def radioContent_play_tag(req):
    tag = read_value(req['entities']['tag'])

    params = {'query': tag, 'type': 'RadioContent'}
    r = search_svara(params)

    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://play.svara.id/RadioContent/{}".format(id)

def radioContent_play_title(req):
    title_content = read_value(req['entities']['title_content'])
    episode = read_value(req['entities']['episode']) if req.get('entities').get('episode') else None

    params = {'query': title_content, 'type': 'RadioContent'}
    r = search_svara(params)

    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://play.svara.id/RadioContent/{}".format(id)

def search(req):
    if req.get('entities').get('query'):
        query = read_value(req['entities']['query'])
    else:
        query = read_value(list(req['entities'].values())[0])

    params = {'query': query}

    return search_svara(params)

if __name__ == "__main__":
    app.run()