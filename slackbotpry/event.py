class Event:
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
    def post_message(self, text):
        channel = self.data['channel']
        return self.bot.post_message(text, channel)
    def add_reaction(self, emoji):
        channel = self.data['channel']
        timestamp = self.data['ts']
        return self.bot.add_reaction(emoji, channel, timestamp)
    def remove_reaction(self, emoji):
        channel = self.data['channel']
        timestamp = self.data['ts']
        return self.bot.remove_reaction(emoji, channel, timestamp)
