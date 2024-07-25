from video_comments import *
from video_info import *
from videos import *

def collect_videos_from_channels(channel_ids):
    all_videos = []

    for channel_id in channel_ids:
        videos = get_all_videos(channel_id)
        all_videos.extend(videos)

    df = pd.DataFrame(all_videos)
    return df

# List of channel IDs
channel_ids = [
    'UChIjQmxk48Fn8UYdJH2NaoQ'   # Another example channel ID
]

# Collect videos and create a DataFrame
video_id = collect_videos_from_channels(channel_ids)
print(video_id)

video_ids = video_id['Video_ID'].tolist()

# detailed_video_info = collect_video_details(video_ids)
detailed_video_comments = get_comments(video_ids)

# print(detailed_video_info)
print(detailed_video_comments)