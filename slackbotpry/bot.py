from slackclient import SlackClient

class Bot:
    def __init__(self, slack: SlackClient):
        self.api = slack
        self.cur_channel = 'random'
        # 今後デフォルトで設定するかもしれないところ API じゃできないっぽい
        self.owner = ''
        self.user_dm = ''
    def post_message(self, message, channel=None, dest_user=None):
        """Post a Message
        Description:
            This method posts a message to channel (if channel is None, self.cur_channel).
        Arguments:
            message (str): message to post
        """
        if dest_user is None:
            text = message
        else:
            text = '@{0} {1}'.format(dest_user, message)
        if channel is None:
            channel = self.cur_channel
        result = self.api.api_call('chat.postMessage', text=text, link_names=True, channel=channel, as_user=True)
        return result
