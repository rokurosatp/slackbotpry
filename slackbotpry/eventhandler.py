class EventHandler:
    def filter(self, event):
        raise NotImplementedError()
    def on_event(self, bot, event):
        raise NotImplementedError()
