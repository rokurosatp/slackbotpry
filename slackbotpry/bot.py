import traceback
import sys
from slackclient import SlackClient
from time import sleep
from .event import Event
from websocket import WebSocketConnectionClosedException


class Bot:
    """Bot class
    EXAMPLE: this example creates a simple bot. replying message to message containing 'hello'.
        bot = Bot(<API token string>)
        bot.add_eventhandler(SimpleMessageHandler(r'hello', lambda **kw: 'Hi'))
        bot.mainloop()
    """
    def __init__(self, api_token, default_channel='random'):
        """initalizer
        ARGUMENTS:
            api_token (str): API Token to manipulate your bot. 
            default_channel (str): Name of channel which the bot posts as default(exclude replying message)
        """
        self.api = SlackClient(token=api_token)
        self.cur_channel = default_channel
        # 今後デフォルトで設定するかもしれないところ API じゃできないっぽい
        self.owner = ''
        self.user_dm = ''
        self.handlers = []
        self.exit_flag = False

    def add_eventhandler(self, handler):
        """Add Event Handler.
        ARGUMENTS:
            handler (EventHandler): Event Handler Object to add in bot.
        """
        self.handlers.append(handler)
        handler.start()

    def mainloop(self):
        """do mainloop
        """
        while not self.exit_flag:
            try:
                if self.api.rtm_connect():
                    print('connected.')
                    while not self.exit_flag:
                        data_list = self.api.rtm_read()
                        for data in data_list:
                            if data:
                                self.on_event(Event(self, data))
#                        self.pool.check_queue()
                        sleep(1)
                else:
                    print('connection failed.')
                    sleep(10)
            except (WebSocketConnectionClosedException, ConnectionResetError, TimeoutError):
                pass
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                print('connecttion was lost by above unhandled exception')
            except KeyboardInterrupt:
                print('shutting down')
                break
            sleep(30)
            print('reconnecting...')
#        for handler in self.handlers:
#            handler.event_queue.join()
        sleep(3)

    def shutdown(self):
        self.exit_flag = True

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
        Args:
            message (str): message to post
        """
        print("post message")
        if dest_user is None:
            text = message
        else:
            text = '@{0} {1}'.format(dest_user, message)
        if channel is None:
            channel = self.cur_channel
        result = self.api.api_call(
            'chat.postMessage', text=text, link_names=True, channel=channel, as_user=True)
        return result

    def edit_message(self, message, post_event):
        """Edit a posted message
        Args:
            message (str): Message String of the updated post
            post_event (dict): Result of post_message method of the post to edit.
        """
        result = self.api.api_call(
            'chat.update', text=message, channel=post_event['channel'], ts=post_event['ts'])
        return result

    def add_reaction(self, emoji, channel, timestamp):
        """Add reaction to post choosed by channel name and time stamp.
        Args:
            emoji (str): Emoji expression of reaction to add
            channel (str): Name of channel of post
            timestamp (str): Timestamp of post
        """
        result = self.api.api_call(
            'reactions.add', name=emoji, channel=channel, timestamp=timestamp)
        return result

    def remove_reaction(self, emoji, channel, timestamp):
        """Remove reaction of post choosed by channel name and time stamp.
        Args:
            emoji (str): Emoji expression of reaction to remove
            channel (str): Name of channel of post
            timestamp (str): Timestamp of post
        """
        result = self.api.api_call(
            'reactions.remove', name=emoji, channel=channel, timestamp=timestamp)
        return result

    def upload_file(self, path, channel):
        with open(path, 'rb') as f:
            self.api.api_call('files.upload', file=f, channels=channel)
