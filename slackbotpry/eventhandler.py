from threading import Thread
from time import sleep
from queue import Queue
import re

class EventHandler:
    def __init__(self):
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
    def __init__(self):
        EventHandler.__init__(self)
        self.last_post = None
    def accept(self, event):
        return event.data['type'] == 'message' and 'text' in event.data
    def on_event(self, event):
        text = event.data['text']
        if not 'subtype' in event.data:
            message = self.on_chat(event, text)
            if message:
                self.last_post = event.post_message(message)
    def on_chat(self, event, text):
        return None

class SimpleMessageHandler(MessageHandler):
    def __init__(self, regex_str, callback):
        MessageHandler.__init__(self)
        self.matcher = re.compile(regex_str)
        self.callback = callback
    def accept(self, event):
        return MessageHandler.accept(self, event) and self.matcher.search(event.data['text'])
    def on_chat(self, event, text):
        return self.callback(event, event.data['text'])
