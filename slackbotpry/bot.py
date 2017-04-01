from slackclient import SlackClient
from time import sleep
import eventpool
from event import Event
from websocket import WebSocketConnectionClosedException

class Bot:
    def __init__(self, api_token, default_channel='random'):
        self.api = SlackClient(token=api_token)
        self.cur_channel = default_channel
        # 今後デフォルトで設定するかもしれないところ API じゃできないっぽい
        self.owner = ''
        self.user_dm = ''
        self.handlers = []
        self.pool = eventpool.EventPool()
    def add_eventhandler(self, handler):
        self.handlers.append(handler)
        handler.start()
    def mainloop(self):
        while True:
            try:
                if self.api.rtm_connect():
                    print('connected.')
                    while True:
                        data_list = self.api.rtm_read()
                        for data in data_list:
                            self.on_event(Event(self, data))
#                        self.pool.check_queue()
                        sleep(1)
                else:
                    print('connection failed.')
                    sleep(10)
            except WebSocketConnectionClosedException:
                print('reconnecting...')
                continue
            except KeyboardInterrupt:
                print('shutting down')
                break
        for handler in self.handlers:
            handler.event_queue.join()
    def on_event(self, event):
        if 'bot_id' in event.data or 'message' in event.data and 'bot_id' in event.data['message']:
            return
        for handler in self.handlers:
            handler.put_event(event)
#            if handler.accept(event):
#                record = eventpool.EventPoolRecord(handler, event)
#                self.pool.register(record)
    def post_message(self, message, channel=None, dest_user=None):
        """Post a Message
        Description:
            This method posts a message to channel (if channel is None, self.cur_channel).
        Arguments:
            message (str): message to post
        """
        print("post message")
        if dest_user is None:
            text = message
        else:
            text = '@{0} {1}'.format(dest_user, message)
        if channel is None:
            channel = self.cur_channel
        result = self.api.api_call('chat.postMessage', text=text, link_names=True, channel=channel, as_user=True)
        return result
    def add_reaction(self, emoji, channel, timestamp):
        result = self.api.api_call('reactions.add', name=emoji, channel=channel, timestamp=timestamp)
        return result
    def remove_reaction(self, emoji, channel, timestamp):
        result = self.api.api_call('reactions.remove', name=emoji, channel=channel, timestamp=timestamp)
        return result
