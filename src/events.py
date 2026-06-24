from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Event:
    pass

class EventListener(ABC):

    @abstractmethod
    def handle(self, event):
        pass

class EventProducer(ABC):

    @abstractmethod
    def publish(self, event: Event) -> None:
        pass


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
# class EventBus(EventProducer):

#     def __init__(self):
#         self._listeners = defaultdict(list)

#     def subscribe(
#         self,
#         event_type: type,
#         listener: EventListener
#     ):
#         self._listeners[event_type].append(listener)

#     def publish(self, event: Event):

#         for listener in self._listeners[type(event)]:
#             listener.handle(event)