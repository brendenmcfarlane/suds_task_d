from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class Event:
    pass

@dataclass
class AddAgentAction(Event):
    agent_id: str
    action_type: str
    action_content: str

@dataclass
class MASStateUpdate(Event):
    question: str
    topology: dict
    transcript: list[str]

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

class QueueEventBus(EventBus):
    """This class implements a queue-based event bus that allows for the handling of 
    events in a first-in-first-out (FIFO) manner. When an event is published, it is 
    added to a queue, and the oldest event is processed by the first listener subscribed 
    to that event type. That listener is then unsubscribed. This ensures that events are 
    handled in the order they are received, and that each listener processes events one 
    at a time.
    """

    def __init__(self, n: int = 1):
        self._listeners = defaultdict(list)
        self._surplus_events = defaultdict(list)
        self._states = {AddAgentAction: 1, MASStateUpdate: n}

    def subscribe(
        self,
        event_type: type,
        listener: EventListener
    ):
        self._listeners[event_type].append(listener)
        self._update_surplus_events(event_type)


    def publish(self, event: Event):
        """ When an event is  published to a given event listener,
        that event is popped from the list of listeners for that event type.
        """
        for i in range(self._states.get(type(event), 1)):
            self._surplus_events[type(event)].append(event)
        self._update_surplus_events(type(event))
    
    def _update_surplus_events(self, event_type):
        while (len(self._surplus_events[event_type]) != 0) and len(self._listeners[event_type]) != 0:
            listener = self._listeners[event_type].pop(0)
            oldest_event = self._surplus_events[event_type].pop(0)
            listener.handle(oldest_event)
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