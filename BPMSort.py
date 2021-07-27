import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    os.environ['SPOTIPY_CLIENT_ID'] = "513c87d5305e44c9bbbcf7f8e449af17"
    os.environ['SPOTIPY_CLIENT_SECRET'] = "5728ca1e02404a5eaea4eed2b7b50074"
    os.environ['SPOTIPY_REDIRECT_URI'] = "https://google.com/"

    scope = "playlist-modify-public,playlist-modify-private,user-library-read"
    auth = SpotifyOAuth(scope=scope)
    sp = spotipy.Spotify(auth_manager=auth)
    auth_url = auth.get_authorize_url()
    try:
        webbrowser.open(auth_url)
        print("Opened", auth_url, " in your browser")
    except webbrowser.Error:
        print("Please navigate here: %s", auth_url)

    response_url = input("Please enter the url here: ")
    code = auth.parse_response_code(response_url)
    auth_token = auth.get_access_token(code, as_dict=False)

    print("Hey, we are loading your music to check it out.")
    results = sp.current_user_saved_tracks()
    print("test")
    playList = results['items']
    while results['next']:
        results = sp.next(results)
        playList.extend(results['items'])

    # taking in speed data
    print("Now categorizing your music.")
    total = len(playList)
    speed = {}
    playTime = {}
    for idx, item in enumerate(playList):
        track = item['track']
        bpm = sp.audio_features(track['uri'])[0]['tempo']
        # int(bpm) for the bpm of each track round to the digits place
        # int(round(bpm, -1)) for the bpm of each track rounded to the tenth place
        roundedBPM = int(round(bpm, -1))
        speed.setdefault(roundedBPM, []).append(track['uri'])
        playTime.setdefault(roundedBPM, 0)
        playTime[roundedBPM] += track['duration_ms']
        print(idx, "out of", total, "songs checked.")
        # print(idx, track['artists'][0]['name'], " – ", track['name'], "- BPM:", int(bpm))

    # print out results.
    print("Hey, we have finished categorizing your music.  Here is what we have found.")
    options = []
    for key, value in sorted(speed.items()):
        options.append(key)
        print("You have", len(value), "songs that are", key, "BPM for a total playtime of",
              str(int(playTime[key] / 60000)) + ":" + str(int(playTime[key] / 1000 % 60)), "minutes.")
    goodInput = False
    while not goodInput:
        bpmInput = input("Please choose a BPM to create a playlist for: ")
        bpmInput = int(bpmInput)
        if bpmInput in speed.keys():
            goodInput = True
        else:
            input("That is not a valid BPM.  Please type in a correct BPM.")
    title = str(bpmInput) + " BPM playlist"
    description = "This is a playlist made by Philip Huang of " + str(bpmInput) + " BPM songs."
    new = sp.user_playlist_create(sp.me()['id'], title, True, False, description)
    sp.playlist_add_items(new['id'], speed[bpmInput])
    print("We have created your playlist.  Have fun running!")
