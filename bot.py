import slacker

class Bot:
    def __init__(self, slack: slacker.Slacker):
        self.api = slack
        self.cur_channel = 'bot_dev'
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
            user_id = self.api.users.get_user_id(dest_user)
            text = '<@{0}> {1}'.format(user_id, message)
        if channel is None:
            self.api.chat.post_message(self.cur_channel, text, as_user=True)
        else:
            self.api.chat.post_message(channel, text, as_user=True)