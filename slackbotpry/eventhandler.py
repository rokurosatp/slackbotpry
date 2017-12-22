from threading import Thread
from time import sleep
from queue import Queue
import re


class EventHandler:
    """Base class of Event Handler Object
    """
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
        """choose event to handle
        Summary:
            Handler selects handled event by implementing this method
        Returns:
            If the handler will handle message True, other False
        """
        raise NotImplementedError()

    def on_event(self, event):
        raise NotImplementedError()


class MessageHandler(EventHandler):
    """Base class of Message Handler Object
    Description:
        The handler is customized by implementing on_chat and on_edit handler.
        If you would like handler simply reply to patterned message, use SimpleMessageHandler.
    """
    def __init__(self):
        EventHandler.__init__(self)
        self.last_post = None

    def accept(self, event):
        return event.data['type'] == 'message'
      
    erase_chars = "<>"
    def __to_plane__(self, text: str):
        for c in MessageHandler.erase_chars:
            text = text.replace(c, "")
        return text

    def on_event(self, event):
        if not 'subtype' in event.data:
            if 'text' in event.data:
                text = self.__to_plane__(event.data['text'])
                result = self.on_chat(event, text)
                if isinstance(result, dict) and 'message' in result:
                    # Messageに種類あるのかわからないけど確認
                    if result['message']['type'] == 'message':
                        self.last_post = result
        else:
            if event.data['subtype'] == 'message_changed':
                text = self.__to_plane__(event.data['message']['text'])
                result = self.on_edit(event, text)
                
    def on_chat(self, event, text):
        """Handling post message event on pattern (or filter funciton) matched message
        Descripton:
            This Method is implemented on interited class.
            In MessageHandlerClass only returns None.
        Examples: This implementated method repeats user posted text
            def on_chat(self, event, text):
                event.post_message(text)
        Args:
            event (Event): Detected Event object
            text (str): posted chat message.
        """
        return None

    def on_edit(self, event, text):
        """Handling message edited event
        Descripton:
            This Method is implemented on interited class.
            In MessageHandlerClass only returns None.
        Args:
            event (Event): Detected Event object
            text (str): Edited chat message text.
        Returns:
            The Result of api_call result Handling process
        Examples: This implementated method changes the last post of bot into text of user edited message
            def on_edit(self, event, text):
                return event.edit_message(text, self.last_post):
        """
        return None

class SimpleMessageHandler(MessageHandler):
    """Simple Message Handler Class.
    Arguments:
        regex_str (str): match pattern of post message process by handler
        chat_callback (function):
            function to handle on_chat (function signature is def func(**kwargs)->[dict, str, or None])
            kwargs corresponds arguments of on_chat method of MessageHandler.
            return value is same as on_chat method.
        edit_callback (function):
            function to handle on_edit (function signature is def func(**kwargs)->[dict, str, or None])
            kwargs corresponds arguments of on_chat method of MessageHandler.
            return value is same as on_chat method.
    """
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
        message = self.chat_callback(handler=self, event=event, text=text)
        if isinstance(message, str):
            return event.post_message(message)
        else:
            return message
    def on_edit(self, event, text):
        return self.edit_callback(handler=self, event=event, text=text)
