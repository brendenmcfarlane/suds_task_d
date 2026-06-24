from src.events import Event, EventProducer, EventListener
from collections import defaultdict

class EventBus(EventProducer):

    def __init__(self):
        self._listeners = defaultdict(list)

    def subscribe(
        self,
        event_type: type,
        listener: EventListener
    ):
        self._listeners[event_type].append(listener)

    def publish(self, event: Event):

        for listener in self._listeners[type(event)]:
            listener.handle(event)