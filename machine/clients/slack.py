import logging
from typing import Callable

from slack import RTMClient, WebClient

from machine.clients.scheduling import Scheduler
from machine.settings import import_settings
from machine.utils import Singleton

logger = logging.getLogger(__name__)


class SlackClient(metaclass=Singleton):
    def __init__(self):
        _settings, _ = import_settings()
        slack_api_token = _settings.get('SLACK_API_TOKEN', None)
        http_proxy = _settings.get('HTTP_PROXY', None)
        self._rtm_client = RTMClient(token=slack_api_token, proxy=http_proxy)
        self._web_client = WebClient(token=slack_api_token, proxy=http_proxy)
        self._bot_info = {}

    @staticmethod
    def get_instance():
        return SlackClient()

    @staticmethod
    def register_rtm_callback(event: str, callback: Callable):
        RTMClient.on(event=event, callback=callback)

    def ping(self):
        self._rtm_client.ping()

    def _on_open(self, **payload):
        self._bot_info = payload['data']['self']

    @property
    def bot_info(self):
        return self._bot_info

    def start(self):
        self.register_rtm_callback('open', self._on_open)
        self._rtm_client.start()

    # @property
    # def users(self):
    #     return SlackWebClient.get_instance().server.users

    # @property
    # def channels(self):
    #     return Slack.get_instance().server.channels

    # @staticmethod
    # def retrieve_bot_info():
    #     return Slack.get_instance().server.login_data['self']

    # def fmt_mention(self, user):
    #     u = self.users.find(user)
    #     return "<@{}>".format(u.id)

    def send(self, channel, **kwargs):
        if 'ephemeral_user' in kwargs:
            return self._web_client.chat_postEphemeral(channel=channel, user=kwargs['ephemeral_user'], **kwargs)
        else:
            return self._web_client.chat_postMessage(channel=channel, **kwargs)

    def send_scheduled(self, when, channel, **kwargs):
        args = [self, channel]

        Scheduler.get_instance().add_job(SlackClient.send_webapi, trigger='date', args=args,
                                         kwargs=kwargs, run_date=when)

    def react(self, channel, ts, emoji):
        return self._web_client.reactions_add(name=emoji, channel=channel, timestamp=ts)

    def open_im(self, user):
        response = self._web_client.im_open(user=user)
        return response['channel']['id']

    # def send_dm(self, user, text):
    #     u = self.users.find(user)
    #     dm_channel = self.open_im(u.id)
    #
    #     self.send(dm_channel, text)
    #
    # def send_dm_scheduled(self, when, user, text):
    #     args = [self, user, text]
    #     Scheduler.get_instance().add_job(SlackClient.send_dm, trigger='date', args=args,
    #                                      run_date=when)
    #
    # def send_dm_webapi(self, user, text, attachments=None):
    #     u = self.users.find(user)
    #     dm_channel = self.open_im(u.id)
    #
    #     return Slack.get_instance().api_call(
    #         'chat.postMessage',
    #         channel=dm_channel,
    #         text=text,
    #         attachments=attachments,
    #         as_user=True
    #     )
    #
    # def send_dm_webapi_scheduled(self, when, user, text, attachments=None):
    #     args = [self, user, text]
    #     kwargs = {'attachments': attachments}
    #
    #     Scheduler.get_instance().add_job(SlackClient.send_dm_webapi, trigger='data', args=args,
    #                                      kwargs=kwargs)
