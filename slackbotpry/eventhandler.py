import re

class EventHandler:
    def filter(self, event):
        raise NotImplementedError()
    def on_event(self, bot, event):
        raise NotImplementedError()

class MessageHandler(EventHandler):
    def filter(self, event):
        return event['type'] == 'message' and 'text' in event

class SimpleMessageHandler(MessageHandler):
    def __init__(self, regex_str, callback):
        self.matcher = re.compile(regex_str)
        self.callback = callback
    def filter(self, event):
        return MessageHandler.filter(self, event) and self.matcher.search(event['text'])
    def on_event(self, bot, event):
        self.callback(bot, event['text'])
        
