"""
TubeSampler v1 Documentation

Step 1 - Log into my Spotify account and get list of
         songs in TubeSampler playlist

Step 2 - Go to YouTube and get links for each song in
         the list

Step 3 (Optional) - Scan TubeSampler folder on computer
         and mark which songs have already been downloaded
         to avoid downloading repeat songs

Step 4- Use PyTube to download songs to TubeSampler folder



To install dependencies, run the following commands:

pip install pytube
pip install --upgrade google-api-python-client
pip install --upgrade google-auth-oauthlib google-auth-httplib2
pip install spotipy
pip install

"""
import sys
import json
import spotipy
import spotipy.util as util
from googleapiclient.discovery import build
from pytube import YouTube
import subprocess


def main():

    spotify_username = "thegreatbelow1"
    input_folder = "\"C:\\Users\Stefano Daniel\Desktop\TubeSampler\\tube\\" # WARNING! THIS STRING IS MISSING QUOTE ON END AND EXPECTS IT TO BE APPENDED AT WRITE-TIME.
    output_folder = "\"C:\\Users\Stefano Daniel\Desktop\TubeSampler\\tube\output\\" # WARNING! THIS STRING IS MISSING QUOTE ON END AND EXPECTS IT TO BE APPENDED AT WRITE-TIME.
    with open("secrets.json", "r") as read_file:
            client_secrets = json.load(read_file)

    # List of songs to download
    query_list = []

    # Log into my Spotify
    scope = "user-library-read"
    token = util.prompt_for_user_token(spotify_username,scope,
            client_id=client_secrets["spotify"]["clientId"],
            client_secret=client_secrets["spotify"]["clientSecret"],
            redirect_uri=client_secrets["spotify"]["redirectUri"])
    if token:
        sp = spotipy.Spotify(auth=token)
        # Hardcoded value for TubeSampler playlist id
        playlist = sp.user_playlist(spotify_username, "6hb8DXMX8caJ5k2E41TSea", fields="tracks")
        for entry in playlist["tracks"]["items"]:
            name = entry["track"]["name"]
            artist = entry["track"]["artists"][0]["name"]
            query_list.append(artist + " " + name)
        # print(json.dumps(playlist["tracks"]["items"][0]["track"], indent=4))
    else:
        print("Can't get token for " + spotify_username)
    
    # print(query_list)

    # Instantiate YouTube service
    api_service_name = "youtube"
    api_version = "v3"
    yt_service = build(api_service_name, api_version, 
            developerKey=client_secrets["google"]["apiKey"])

    
    # Collect YouTube link for every song in the playlist
    links = []
    video_titles = []
    for query in query_list:
        resp = yt_service.search().list(
            part="snippet",
            type="youtube#video",
            maxResults=5,
            q=query
        ).execute()

        # Find the first video hit (ie. not a channel hit)
        for result in resp["items"]:
            if result["id"]["kind"] == "youtube#video":
                video_titles.append(result["snippet"]["title"])
                links.append("https://www.youtube.com/watch?v=" + result["id"]["videoId"])
                break

    # Download each video from stream with highest average bit rate
    for link in links:
        try:
            yt = YouTube(link)
            yt.streams.filter(progressive=True).order_by("abr").desc().first().download()
        except:
            # Some regex error or some bullshit
            pass
    
    print("Huh?")
    """
    video_titles = [
        "Mac Miller - Red Dot Music (ft Action Bronson) (NoDJCDQ)",
        "Mac Miller - Watching Movies (Official Audio)"
    ]
    """
    # Strip audio from each video
    for video_title in video_titles:
        input_filename = video_title + ".mp4"
        output_filename = video_title + ".wav"
        command = "ffmpeg -i %s -ab 160k -ac 2 -ar 44100 -vn %s" % (input_folder + input_filename + "\"", output_folder + output_filename + "\"")
        # print(command)
        subprocess.call(command, shell=True)

if __name__ == "__main__":
    main()