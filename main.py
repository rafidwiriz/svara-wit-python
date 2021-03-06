from flask import Flask, request, make_response, jsonify, redirect
import requests
import datetime
import time

from config import *

app = Flask(__name__)
WIT_TOKEN = 'RUU3F6BNDSDLL7RO6ZLL6V6IKN3Z5T4W'

@app.route('/', methods=["GET"])
def index():
    return "Hello World!"

@app.route('/wit', methods=['POST'])
def wit():
    t0 = time.time()
    req = request.get_json(silent=True, force=True)
    txt = req.get('text')

    params = {'v': get_string_date(), 'q': txt}
    headers = {'Authorization': 'Bearer ' + WIT_TOKEN}
    t1 = time.time()
    res = requests.get("https://api.wit.ai/message", params=params, headers=headers)
    td0 = time.time() - t1
    res = res.json()

    if res['entities']['intent']:
        r, td1 = intent_switch(res, res['entities']['intent'][0]['value'])
        r['apiTime'] = {'WitTime': int(td0 * 1000), 'SvaraTime': int(td1 * 1000)}

    if r:
        r = make_response(jsonify(r))
        r = (r, 200)
    else:
        r = make_response(jsonify({"text": "Oops. Something went wrong!"}))
        r = (r, 404)

    return r

@app.route('/wit-sound', methods=['POST'])
def witSound():
    params = {'v': get_string_date()}
    headers = {'Authorization': 'Bearer ' + WIT_TOKEN, 'Content-Type': 'audio/mpeg3'}
    t0 = time.time()
    res = requests.post("https://api.wit.ai/speech", params=params, headers=headers, data=request.get_data())
    td0 = time.time() - t0
    res = res.json()

    if res['entities']['intent']:
        r, td1 = intent_switch(res, res['entities']['intent'][0]['value'])
        r['apiTime'] = {'WitTime': int(td0 * 1000), 'SvaraTime': int(td1 * 1000)}

    if r:
        r = make_response(jsonify(r))
        r.headers['Content-Type'] = "application/json"
        r = (r, 200)
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

    t = time.time()
    r = requests.get(BASE_URL + "search", params=params, headers=headers)
    td = time.time() - t
    r = r.json()

    top = r.pop(0)
    r = {'topResult': top['topResult'], 'results': r}

    return r, td

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

    return search_svara(params)

def music_play_artist(req):
    name_artist = read_value(req['entities']['name_artist'])

    params = {'query': name_artist, 'type': 'Artist'}

    return search_svara(params)

def music_play_popular(req):
    pass

def music_play_title(req):
    title_song = read_value(req['entities']['title_song'])
    name_artist = read_value(req['entities']['name_artist']) if req.get('entities').get('name_artist') else None

    params = {'query': title_song, 'type': 'Music'}

    return search_svara(params)

def play_recommendation(req):
    pass

def playlist_play(req):
    name_playlist = read_value(req['entities']['name_playlist'])

    params = {'query': name_playlist, 'type': 'Playlist'}

    return search_svara(params)

def radio_play(req):
    name_radio = read_value(req['entities']['name_radio'])

    params = {'query': name_radio, 'type': 'Radio'}

    return search_svara(params)

def radioContent_play_radio(req):
    name_radio = read_value(req['entities']['name_radio'])

    params = {'query': name_radio, 'type': 'RadioContent'}

    return search_svara(params)

def radioContent_play_tag(req):
    tag = read_value(req['entities']['tag'])

    params = {'query': tag, 'type': 'RadioContent'}

    return search_svara(params)

def radioContent_play_title(req):
    title_content = read_value(req['entities']['title_content'])
    episode = read_value(req['entities']['episode']) if req.get('entities').get('episode') else None

    params = {'query': title_content, 'type': 'RadioContent'}

    return search_svara(params)

def search(req):
    if req.get('entities').get('query'):
        query = read_value(req['entities']['query'])
    else:
        query = read_value(list(req['entities'].values())[0])

    params = {'query': query}

    return search_svara(params)

if __name__ == "__main__":
    app.run()