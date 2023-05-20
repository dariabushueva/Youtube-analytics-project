import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.channel['items'][0]['snippet']['title']

    @property
    def description(self):
        return self.channel['items'][0]['snippet']['description']

    @property
    def url(self):
        return "https://www.youtube.com/channel/" + self.__channel_id

    @property
    def video_count(self):
        return self.channel['items'][0]['statistics']['videoCount']

    @property
    def subscribers(self):
        return self.channel['items'][0]['statistics']['subscriberCount']

    @property
    def views_count(self):
        return self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, file_name):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""

        data_channel = (
            {"channel_id": self.__channel_id,
             "title": self.title,
             "description": self.description,
             "url": self.url,
             "video_count": self.video_count,
             "subscribers": self.subscribers,
             "views_count": self.views_count
            }
        )

        with open(file_name, "w", encoding='utf-8') as file:
            json.dump(data_channel, file, indent=4, ensure_ascii=False)


