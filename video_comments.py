from googleapiclient.discovery import build
from env import *
import pandas as pd


def get_comments(video_ids):
    youtube = build('youtube', 'v3', developerKey=KEY)

    comments = []
    next_page_token = None
    for video_id in video_ids:
    # while True:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comment_details = {
                'Comment ID': item['id'],
                'Author': comment['authorDisplayName'],
                'Text': comment['textDisplay'],
                'Like Count': comment['likeCount'],
                'Published At': comment['publishedAt'],
                'Replies': []
            }

            if 'replies' in item:
                for reply in item['replies']['comments']:
                    reply_snippet = reply['snippet']
                    comment_details['Replies'].append({
                        'Reply ID': reply['id'],
                        'Author': reply_snippet['authorDisplayName'],
                        'Text': reply_snippet['textDisplay'],
                        'Like Count': reply_snippet['likeCount'],
                        'Published At': reply_snippet['publishedAt']
                    })

            comments.append(comment_details)

        # next_page_token = response.get('nextPageToken')

        # if not next_page_token:
        #     break

    return  pd.DataFrame(comments)


