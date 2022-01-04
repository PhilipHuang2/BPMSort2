import PySimpleGUI as sg
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

if __name__ == '__main__':
    os.environ['SPOTIPY_CLIENT_ID'] = "513c87d5305e44c9bbbcf7f8e449af17"
    os.environ['SPOTIPY_CLIENT_SECRET'] = "5728ca1e02404a5eaea4eed2b7b50074"
    os.environ['SPOTIPY_REDIRECT_URI'] = "https://google.com/"

    scope = "playlist-modify-public,playlist-modify-private,user-library-read"
    auth = SpotifyOAuth(scope=scope)
    sp = spotipy.Spotify(auth_manager=auth)
    auth_url = auth.get_authorize_url()
    try:
        webbrowser.open(auth_url)
        messageText = "Opened " +  str(auth_url) + " in your browser"
    except webbrowser.Error:
        messageText = "Please navigate here: " + str(auth_url)

    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text(messageText)],
              [sg.Text('Enter URL here'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Allowing Permission to your Spotify Songs', layout)

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        quit()
    if event == 'Ok':
        test = values[0]
    window.close()

    code = auth.parse_response_code(test)
    auth_token = auth.get_access_token(code, as_dict=False)
    results = sp.current_user_saved_tracks()
    playList = results['items']
    while results['next']:
        results = sp.next(results)
        playList.extend(results['items'])

    # taking in speed data
    total = len(playList)
    layout = [[sg.Text('Now Categorizing your music')],
              [sg.ProgressBar(total, orientation='h', size=(20, 20), key='progressbar')],
              [sg.Cancel()]]
    window = sg.Window('Loading music', layout)
    progress_bar = window['progressbar']

    speed = {}
    playTime = {}
    for idx, item in enumerate(playList):
        event, values = window.read(timeout=10)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            quit()
        track = item['track']
        bpm = sp.audio_features(track['uri'])[0]['tempo']
        roundedBPM = int(round(bpm, -1))
        speed.setdefault(roundedBPM, []).append(track['uri'])
        playTime.setdefault(roundedBPM, 0)
        playTime[roundedBPM] += track['duration_ms']
        progress_bar.update_bar(idx+1)
    window.close()

    # for key, value in sorted(speed.items()):
    #     print("You have", len(value), "songs that are", key, "BPM for a total playtime of",
    #           str(int(playTime[key] / 60000)) + ":" + str(int(playTime[key] / 1000 % 60)), "minutes.")
    # layout = [[sg.Text('Now Categorizing your music')],
    #           [sg.Text(speed.items())],
    #           [sg.Cancel()]]
    layout = []
    layout += [sg.Text('Here are your potential playlists sorted by BPM.')],
    for key, value in sorted(speed.items()):
        row = "You have " + str(len(value)) + " songs that are " + str(key) + " BPM for a total playtime of " \
              + str(int(playTime[key] / 60000)) + " : " + str(int(playTime[key] / 1000 % 60)) + " minutes."
        layout += [sg.Text(row)],
    layout += [sg.Text("Enter BPM here."), sg.InputText(do_not_clear=False)],
    layout += [sg.Button("Create Playlist"), sg.Cancel()],
    window = sg.Window('Playlist Selection', layout)
    while True:
        event, values = window.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            quit()
        if event == 'Create Playlist':
            if values[0].isnumeric():
                temp = int(values[0])
                if temp in speed.keys():
                    break
                else:
                    sg.popup_error("Please enter a BPM located above")
            else:
                sg.popup_error("Please enter a correct BPM")
    window.close()
    title = str(temp) + " BPM playlist"
    description = "This is a playlist made by Philip Huang of " + str(temp) + " BPM songs."
    new = sp.user_playlist_create(sp.me()['id'], title, True, False, description)
    sp.playlist_add_items(new['id'], speed[temp])
    layout = [[sg.Text("We created your playlist.  Have fun running!")], ]
    layout += [sg.Button("Close")],
    window = sg.Window("Created Playlist", layout)
    event, values = window.read()
    if event == 'Close' or event == sg.WIN_CLOSED:
        quit()
    window.close()

