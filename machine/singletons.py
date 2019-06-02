from apscheduler.schedulers.background import BackgroundScheduler
from slack import RTMClient, WebClient
from machine.settings import import_settings
from machine.utils import Singleton
from machine.utils.module_loading import import_string
from machine.utils.redis import gen_config_dict


class SlackRTMClient(metaclass=Singleton):
    def __init__(self):
        _settings, _ = import_settings()
        slack_api_token = _settings.get('SLACK_API_TOKEN', None)
        http_proxy = _settings.get('HTTP_PROXY', None)

        self._client = RTMClient(
            token=slack_api_token, proxy=http_proxy
        ) if slack_api_token else None

    def __getattr__(self, item):
        return getattr(self._client, item)

    @staticmethod
    def get_instance():
        return SlackRTMClient()


class SlackWebClient(metaclass=Singleton):
    def __init__(self):
        _settings, _ = import_settings()
        slack_api_token = _settings.get('SLACK_API_TOKEN', None)
        http_proxy = _settings.get('HTTP_PROXY', None)

        self._client = WebClient(
            token=slack_api_token, proxy=http_proxy
        ) if slack_api_token else None

    def __getattr__(self, item):
        return getattr(self._client, item)

    @staticmethod
    def get_instance():
        return SlackWebClient()


class Scheduler(metaclass=Singleton):
    def __init__(self):
        _settings, _ = import_settings()
        self._scheduler = BackgroundScheduler()
        if 'REDIS_URL' in _settings:
            redis_config = gen_config_dict(_settings)
            self._scheduler.add_jobstore('redis', **redis_config)

    def __getattr__(self, item):
        return getattr(self._scheduler, item)

    @staticmethod
    def get_instance():
        return Scheduler()


class Storage(metaclass=Singleton):
    def __init__(self):
        _settings, _ = import_settings()
        _, cls = import_string(_settings['STORAGE_BACKEND'])[0]
        self._storage = cls(_settings)

    def __getattr__(self, item):
        return getattr(self._storage, item)

    @staticmethod
    def get_instance():
        return Storage()
