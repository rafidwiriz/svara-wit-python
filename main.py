from flask import Flask, request, make_response, jsonify, redirect
import requests
import datetime

from config import BASE_URL, BASE_URL_AUTH, ACCESS_TOKEN, ACCESS_TOKEN_GENDIGBADIG, APP_ACCESS_TOKEN

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
    title_album = req['entities']['title_album'][0]['value']
    name_artist = req['entities']['name_artist'][0]['value'] if req.get('entities').get('name_artist') else None

    params = {'query': title_album, 'type': 'Album'}
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN, 'x-consumer-username': ACCESS_TOKEN}
    r = requests.get(BASE_URL + "search", params=params, headers=headers)

    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://svara.id/Album/{}".format(id)

def music_play_artist(req):
    name_artist = req['entities']['name_artist'][0]['value']

    params = {'query': name_artist, 'type': 'Artist'}
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN, 'x-consumer-username': ACCESS_TOKEN}
    r = requests.get(BASE_URL + "search", params=params, headers=headers)

    r = r.json()
    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://svara.id/Artist/{}".format(id)

def music_play_popular(req):
    pass

def music_play_title(req):
    title_song = req['entities']['title_song'][0]['value']
    name_artist = req['entities']['name_artist'][0]['value'] if req.get('entities').get('name_artist') else None

    params = {'query': title_song, 'type': 'Music'}
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN, 'x-consumer-username': ACCESS_TOKEN}
    r = requests.get(BASE_URL + "search", params=params, headers=headers)

    r = r.json()
    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://svara.id/Music/{}".format(id)

def play_recommendation(req):
    pass

def playlist_play(req):
    pass

def radio_play(req):
    name_radio = req['entities']['name_radio'][0]['value']

    params = {'query': name_radio, 'type': 'Radio'}
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN, 'x-consumer-username': ACCESS_TOKEN}
    r = requests.get(BASE_URL + "search", params=params, headers=headers)

    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://svara.id/Radio/{}".format(id)

def radioContent_play_radio(req):
    pass

def radioContent_play_tag(req):
    pass

def radioContent_play_title(req):
    title_content = req['entities']['title_content'][0]['value']

    params = {'query': title_content, 'type': 'RadioContent'}
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN, 'x-consumer-username': ACCESS_TOKEN}
    r = requests.get(BASE_URL + "search", params=params, headers=headers)

    id = r[0]['topResult']['dataList'][0]['id']
    return "svara://svara.id/RadioContent/{}".format(id)

def search(req):
    if req.get('entities').get('query'):
        query = req['entities']['query'][0]['value']
    else:
        query = list(req['entities'].values())[0][0]['value']

    params = {'query': query}
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN, 'x-consumer-username': ACCESS_TOKEN}
    r = requests.get(BASE_URL + "search", params=params, headers=headers)

    return r.json()

if __name__ == "__main__":
    app.run()