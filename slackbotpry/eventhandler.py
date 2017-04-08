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
        return event.data['type'] == 'message'

    def on_event(self, event):
        if not 'subtype' in event.data:
            if 'text' in event.data:
                text = event.data['text']
                message = self.on_chat(event, text)
                if message:
                    self.last_post = event.post_message(message)
        else:
            if event.data['subtype'] == 'message_changed':
                text = event.data['message']['text']
                message = self.on_edit(event, text)
                if message:
                    self.last_post = event.post_message(message)

    def on_chat(self, event, text):
        return None

    def on_edit(self, event, text):
        return None


class SimpleMessageHandler(MessageHandler):
    def __init__(self, regex_str, chat_callback=None, edit_callback=None):
        MessageHandler.__init__(self)
        self.matcher = re.compile(regex_str)
        self.chat_callback = chat_callback
        self.edit_callback = edit_callback

    def accept(self, event):
        if MessageHandler.accept(self, event):
            if 'text' in event.data and self.matcher.search(event.data['text']):
                return True
            elif 'message' in event.data and self.matcher.search(event.data['message']['text']):
                return True
        return False

    def on_chat(self, event, text):
        return self.chat_callback(handler=self, event=event, text=text)

    def on_edit(self, event, text):
        return self.edit_callback(handler=self, event=event, text=text)
