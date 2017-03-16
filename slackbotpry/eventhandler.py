from threading import Thread
from time import sleep
from queue import Queue
import re

class EventHandler:
    def __init__(self, bot):
        self.bot = bot
        self.inner_thread = None
        self.event_queue = Queue()
    def start(self):
        assert self.inner_thread is None
        thread = Thread(target=self.loop, daemon=True)
        thread.start()
        self.inner_thread = thread
    def loop(self):
        while True:
            event = self.event_queue.get()
            self.on_event(event)
            self.event_queue.task_done()
    def put_event(self, event):
        if self.accept(event):
            self.event_queue.put(event)
    def accept(self, event):
        raise NotImplementedError()
    def on_event(self, event):
        raise NotImplementedError()

class MessageHandler(EventHandler):
    def __init__(self, bot):
        EventHandler.__init__(self, bot)
    def accept(self, event):
        return event['type'] == 'message' and 'text' in event

class SimpleMessageHandler(MessageHandler):
    def __init__(self, bot, regex_str, callback):
        MessageHandler.__init__(self, bot)
        self.matcher = re.compile(regex_str)
        self.callback = callback
    def accept(self, event):
        return MessageHandler.accept(self, event) and self.matcher.search(event['text'])
    def on_event(self, event):
        self.callback(self.bot, event['text'])
