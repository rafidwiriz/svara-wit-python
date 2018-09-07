from flask import Flask, request, make_response, jsonify
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
        r = make_response(jsonify(r))
        r.headers['Content-Type'] = "application/json"
        r = (r, 200)
    else:
        r = make_response(jsonify({ "text": "Oops. Something went wrong!" }))
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
    pass

def music_play_artist(req):
    pass

def music_play_popular(req):
    pass

def music_play_title(req):
    pass

def play_recommendation(req):
    pass

def playlist_play(req):
    pass

def radio_play(req):
    pass

def radioContent_play_radio(req):
    pass

def radioContent_play_tag(req):
    pass

def radioContent_play_title(req):
    pass

def search(req):
    params = {'query': req['entities']['query'][0]['value']}
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN, 'x-consumer-username': ACCESS_TOKEN}
    r = requests.get(BASE_URL + "search", params=params, headers=headers)

    return r.json()

if __name__ == "__main__":
    app.run()