class Event:
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
    def post_message(self, text, channel=None):
        if channel is None:
            channel = self.data['channel']
        self.bot.post_message(text, channel)
    def add_reaction(self, emoji, channel=None, timestamp=None):
        if channel is None:
            channel = self.data['channel']
        if timestamp is None:
            timestamp = self.data['ts']
        self.bot.add_reaction(emoji, channel, timestamp)
    def remove_reaction(self, emoji, channel=None, timestamp=None):
        if channel is None:
            channel = self.data['channel']
        if timestamp is None:
            timestamp = self.data['ts']
        self.bot.remove_reaction(emoji, channel, timestamp)
