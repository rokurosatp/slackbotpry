class Event:
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
    def post_message(self, text, channel=None):
        if channel is None:
            channel = self.data['channel']
        self.bot.post_message(text, channel)
