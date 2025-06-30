from .utils.events import log_event

class EventLoggingMixin:
    def log_event(self, actor, action, instance, notes=None):
        log_event(actor, action, instance, notes)