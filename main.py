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

"""
import json
from googleapiclient.discovery import build
from pytube import YouTube

def main():

    # Instantiate YouTube service
    api_service_name = "youtube"
    api_version = "v3"
    key = "AIzaSyCAAlooI2_y6qNeS_6eI8aOmQCQNqFjqM0"
    yt_service = build(api_service_name, api_version, developerKey=key)

    resp = yt_service.search().list(
        part="snippet",
        type="youtube#video",
        maxResults=2,
        q="surfing"
    ).execute()

    links = []
    for result in resp["items"]:
        if result["id"]["kind"] == "youtube#video":
            links.append("https://www.youtube.com/watch?v=" + result["id"]["videoId"])
    print(links)

    # print(json.dumps(resp, sort_keys=True, indent=4))

if __name__ == "__main__":
    main()