from pynput import mouse, keyboard as pn
from _collections_abc import Sequence
from abc import ABC, abstractmethod
from queue import Queue
from actions import KeyInputActions, KeyOutputActions

# abstract model for events
class Event(ABC):
    def __init__(self, label: str):
        self._label = label 
        ...

    @property 
    @abstractmethod
    def label(self):
        return self._label

# abstract model for handling events 
class EventHandler(ABC):
    def __init__(self, events: Sequence[Event]):
        self._events = events 
    
    # explicit processing of events must reside here
    # Best not called by the same object, but it can work.
    @abstractmethod
    def process(self): pass 

class OutputEvent(Event):
    def __init__(self, label: str, output_seq: Sequence[KeyOutputActions]):
        self._output_seq = output_seq
        super().__init__(label)

    @property
    def outputSeq(self):
        return self._output_seq

    @property
    def label(self):
        return self._label

# model adapts logic that input must have corresponding output
class InputEvent(Event):
    def __init__(self, label: str, input_keys: Sequence[KeyInputActions], output_event: OutputEvent):
        self._i_event = input_keys 
        self._o_event = output_event
        super().__init__(label)
    
    @property 
    def iEvent(self): 
        return self._i_event 

    @property 
    def oEvent(self): 
        return self._o_event

    @property 
    def label(self):
        return self._label

class IOEventHandler(EventHandler):
    def __init__(self, events: Sequence[InputEvent]):
        self._listener = pn.Listener(
                on_press=self.on_press,
                on_release=self.on_release 
                )

        self._o_eventq = Queue()
        self._keys_pressed = set()
        # For the instance manager to not
        # overload the stack.
        self._is_processing = False
        super().__init__(events)
    
    @property 
    def is_processing(self):
        return self._is_processing
    
    def _set_processing(self, state: bool):
        self._is_processing = state

    def process(self):
        if self._o_eventq.empty():
            # TODO: warning log that it tried to process something empty
            return 

        o_event = self._o_eventq.get()
        self._set_processing(True) 

        # TODO: Logic for processing event outputs
        for koa in o_event.outputSeq():
            ...
            
        self._set_processing(False)

    def on_press(self, key):
        self._keys_pressed.add(key)
        # TODO: Logic

    def on_release(self, key):
        self._keys_pressed.remove(key)
        # TODO: Logic

    def start(self):
        self._listener.start()

    def stop(self):
        self._listener.stop()
