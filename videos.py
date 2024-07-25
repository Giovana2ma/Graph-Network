from googleapiclient.discovery import build
from datetime import datetime
from env import *
import pandas as pd

def get_info(video):
    date = video['snippet']['publishedAt']
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    video_id = video['snippet']['resourceId']['videoId']
    return date, video_id

def get_playlist_id(channel_id):
    youtube = build('youtube', 'v3', developerKey=KEY)

    channel_request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )

    channel_response = channel_request.execute()
    playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return playlist_id

def get_all_videos(channel_id):
    youtube = build('youtube', 'v3', developerKey=KEY)

    video_details = []

    playlist_id = get_playlist_id(channel_id)
    
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            date, video_id = get_info(item)
            if date < datetime(2018, 1, 1):
                return video_details
            video_details.append({'channel_id': channel_id,'video_id': video_id,'date': date.strftime('%Y-%m-%d')})

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return video_details

def collect_videos_from_channels(channel_ids):
    all_videos = []

    for channel_id in channel_ids:
        videos = get_all_videos(channel_id)
        all_videos.extend(videos)

    df = pd.DataFrame(all_videos)
    return df

channel_ids_df = pd.read_csv('channel_stats.csv')
channel_ids = channel_ids_df['channel_id'].tolist()

# Collect video data
video_data = collect_videos_from_channels(channel_ids)

video_data.to_csv('videos_ids.csv', index=False)