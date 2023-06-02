from datetime import timedelta
import os
import isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс для плей-листа ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.get_playlist_info()['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.playlist_id}')"

    def __str__(self):
        return f"{self.title}"

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    def get_playlist_info(self):
        """Возвращает информацию о плейлисте"""
        request = self.get_service().playlists().list(part="snippet", id=self.playlist_id)
        response = request.execute()
        return response

    def get_playlist_videos_info(self):
        """Возвращает информацию о видеороликах в плейлисте"""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)).execute()

        return video_response

    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""

        total_duration = timedelta(0)
        for video in self.get_playlist_videos_info()['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""

        max_likes = 0
        best_video = None
        for video in self.get_playlist_videos_info()['items']:
            likes = int(video['statistics']['likeCount'])
            if likes > max_likes:
                max_likes = likes
                best_video = video

            if best_video is not None:
                best_video = video['id']

        return f"https://youtu.be/" + best_video


