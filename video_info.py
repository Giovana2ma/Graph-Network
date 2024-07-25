from googleapiclient.discovery import build
from env import *
import pandas as pd


def get_video_details(video_id):
    youtube = build('youtube', 'v3', developerKey=KEY)
    request = youtube.videos().list(part='snippet,statistics', id=video_id)
    response = request.execute()
    return response

def collect_video_details(video_ids):
    video_details = []
    for video_id in video_ids:
        response = get_video_details(video_id)

        for item in response['items']:
            video_info = {
                'Video_ID': item['id'],
                'Title': item['snippet']['title'],
                'Description': item['snippet']['description'],
                'Tags': item['snippet'].get('tags', []),
                'Category_ID': item['snippet']['categoryId'],
                'View_Count': item['statistics'].get('viewCount', 0),
                'Like_Count': item['statistics'].get('likeCount', 0),
                'Dislike_Count': item['statistics'].get('dislikeCount', 0),
                'Comment_Count': item['statistics'].get('commentCount', 0)
            }
            video_details.append(video_info)
    return pd.DataFrame(video_details)
    

