import json
import os
from googleapiclient.discovery import build


class Video:

    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails', id=self.video_id).execute()
        self.video_title = self.video_response['items'][0]['snippet']['title']
        self.video_url = 'https://youtu.be/' + self.video_id
        self.views_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['commentCount']

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.video_id}')"

    def __str__(self):
        return f"{self.video_title}"

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id




