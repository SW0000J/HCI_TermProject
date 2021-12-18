import random as rd
import pandas as pd
from googleapiclient.discovery import build

# pip install --upgrade google-api-python-client

# YOUTUBEAPI, VIDEOID만 수정하면 바로 동작합니다.
# get Google Youyube Api key : https://console.cloud.google.com/apis/dashboard

def getYoutubeComments(inputVideoId : str) -> list:
    comments = list()
    api_obj = build('youtube', 'v3', developerKey = #have to get developerKey)
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=inputVideoId, maxResults=100).execute() #videoID is video's Only code
    video_response = api_obj.videos().list(id=inputVideoId, part='snippet,contentDetails,statistics').execute()


    videoInfo = []
    videoInfo.append(str(video_response['items'][0]['snippet']['title']))
    videoInfo.append(str(video_response['items'][0]['statistics']['viewCount']))
    videoInfo.append(str(video_response['items'][0]['statistics']['likeCount']))
    videoInfo.append(str(video_response['items'][0]['statistics']['commentCount']))

    while response:
        for item in response['items']:
            randomLabel = str(int(rd.randrange(1, 3)))

            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount'], randomLabel])
    
            if item['snippet']['totalReplyCount'] > 0:
                for reply_item in item['replies']['comments']:
                    reply = reply_item['snippet']
                    comments.append([reply['textDisplay'], reply['authorDisplayName'], reply['publishedAt'], reply['likeCount'], randomLabel])
    
        if 'nextPageToken' in response:
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=inputVideoId, pageToken=response['nextPageToken'], maxResults=100).execute() #videoID is video's Only code
        else:
            break

    # have to fix #
    #df = pd.DataFrame(comments)
    #df.columns = ['comment', 'author', 'date', 'numLikes', 'label']
    #print(type(df))
    #print(df)
    #df.to_excel('results.xlsx', header=['comment', 'author', 'date', 'num_likes'], index=None)
    
    return comments, videoInfo