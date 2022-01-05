# BPM Sorter Synopsis
This is a simple application that asks the user to see their spotify playlist using the 
Spotify API and sort their songs by BPM(beats per minutes).  Then it creates one playlist for the user using based on 1 BPM.

# Important Imports 
## Spotipy
The python library to access the Spotify API, essential to the project and simplify the call I
send to the API.
## PYSimpleGUI
A GUI Library I used to create the front end for this project and guides the user through process.
## Webbrowser
The Authentication method I use for the Spotify API is the Authorization Code Flow which opens 
up a web page for the user to input into the program to allow permission into your Spotify 
Playlist.  Webbrowser is the way I open up the page in 
your browser.
# Process
1. Download BPM Sorter.exe
2. Run BPM Sorter.exe
3. The program will open a tab in your chosen web browser.  Copy the url and input it into the input box.
   ![test](\Images\Tutorial 1.png)
4. The program will load all your songs, ask the Spotify API for their BPMs, and sort them.
5. Then the program will display all your songs with the BPMs rounded for simplicity’s sake and ask you for 1 BPM to create a playlist around
6. Then you are done!!! Congratulations
