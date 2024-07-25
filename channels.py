from googleapiclient.discovery import build
from datetime import datetime
from env import *
import pandas as pd

def get_channel_info(channel_ids):
    youtube = build('youtube', 'v3', developerKey=KEY)
    all_channels = []

    for channel_id in channel_ids:
        request = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        )
        response = request.execute()
        
        for item in response['items']:
            channel_data = {
                'channel_id': item['id'],
                'title': item['snippet']['title'],
                'view_count': item['statistics']['viewCount'],
                'subscriber_count': item['statistics']['subscriberCount'],
                'video_count': item['statistics']['videoCount']
            }
            all_channels.append(channel_data)

    df = pd.DataFrame(all_channels)
    return df

channel_ids = [
    'UChIjQmxk48Fn8UYdJH2NaoQ'   
]

channel_stats = get_channel_info(channel_ids)

channel_stats.to_csv('channel_stats.csv', index=False)