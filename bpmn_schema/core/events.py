"""
BPMN Event elements implementation.

This module contains all event-related classes and enums for BPMN modeling.
Events represent things that happen during the course of a business process.

Events are classified into three main types:
- Start Events: Indicate where a process begins
- Intermediate Events: Occur between start and end events
- End Events: Indicate where a process ends

Author: SimLab120
Date: 2025-07-03
"""

from typing import Optional
from enum import Enum
from .base import BPMNElement, BPMNElementType


class EventType(str, Enum):
    """
    Enumeration of BPMN event types.
    
    Events are categorized by their position in the process flow:
    - START: Process initiation events
    - INTERMEDIATE: Events that occur during process execution
    - BOUNDARY: Events attached to activities
    - END: Process termination events
    """
    
    START = "start"
    INTERMEDIATE = "intermediate"
    BOUNDARY = "boundary"
    END = "end"


class EventDefinition(str, Enum):
    """
    Enumeration of BPMN event definitions (triggers).
    
    Event definitions specify what triggers or is triggered by an event.
    Covers all BPMN 2.0 event trigger types.
    """
    
    NONE = "none"                           # No specific trigger
    MESSAGE = "message"                     # Message reception/sending
    TIMER = "timer"                         # Time-based triggers
    ERROR = "error"                         # Error conditions
    ESCALATION = "escalation"               # Escalation scenarios
    CANCEL = "cancel"                       # Transaction cancellation
    COMPENSATION = "compensation"           # Compensation activities
    CONDITIONAL = "conditional"             # Condition-based triggers
    LINK = "link"                          # Process linking
    SIGNAL = "signal"                      # Signal broadcasting
    TERMINATE = "terminate"                 # Process termination
    MULTIPLE = "multiple"                   # Multiple triggers (OR)
    PARALLEL_MULTIPLE = "parallel_multiple" # Multiple triggers (AND)


class Event(BPMNElement):
    """
    BPMN Event element implementation.
    
    Events represent something that happens during the course of a business process.
    They affect the flow of the process and usually have a trigger or a result.
    
    This class supports all BPMN 2.0 event types and definitions as specified
    in the official BPMN specification and common modeling tools.
    
    Attributes:
        event_type (EventType): Classification of the event (start, intermediate, boundary, end)
        event_definition (EventDefinition): Trigger type for the event
        is_interrupting (bool): Whether the event interrupts the parent activity (for boundary events)
        is_throwing (bool): Whether the event throws/sends rather than catches/receives
        trigger (Optional[str]): Specific trigger configuration (e.g., timer expression)
        attached_to_ref (Optional[str]): Reference to activity this event is attached to (boundary events)
        cancel_activity (bool): Whether boundary event cancels the attached activity
    """
    
    event_type: EventType = EventType.START
    event_definition: EventDefinition = EventDefinition.NONE
    is_interrupting: bool = True
    is_throwing: bool = False
    trigger: Optional[str] = None
    attached_to_ref: Optional[str] = None
    cancel_activity: bool = True
    
    def __init__(self, **data):
        """
        Initialize a BPMN Event.
        
        Args:
            **data: Event properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.EVENT, **data)
    
    def is_start_event(self) -> bool:
        """Check if this is a start event."""
        return self.event_type == EventType.START
    
    def is_end_event(self) -> bool:
        """Check if this is an end event."""
        return self.event_type == EventType.END
    
    def is_intermediate_event(self) -> bool:
        """Check if this is an intermediate event."""
        return self.event_type == EventType.INTERMEDIATE
    
    def is_boundary_event(self) -> bool:
        """Check if this is a boundary event."""
        return self.event_type == EventType.BOUNDARY
    
    def is_catching_event(self) -> bool:
        """Check if this event catches/receives rather than throws/sends."""
        return not self.is_throwing
    
    def is_throwing_event(self) -> bool:
        """Check if this event throws/sends rather than catches/receives."""
        return self.is_throwing
    
    def has_trigger(self) -> bool:
        """Check if this event has a specific trigger defined."""
        return self.event_definition != EventDefinition.NONE
    
    def is_timer_event(self) -> bool:
        """Check if this is a timer event."""
        return self.event_definition == EventDefinition.TIMER
    
    def is_message_event(self) -> bool:
        """Check if this is a message event."""
        return self.event_definition == EventDefinition.MESSAGE
    
    def is_error_event(self) -> bool:
        """Check if this is an error event."""
        return self.event_definition == EventDefinition.ERROR
    
    def is_signal_event(self) -> bool:
        """Check if this is a signal event."""
        return self.event_definition == EventDefinition.SIGNAL
    
    def attach_to_activity(self, activity_id: str, interrupting: bool = True) -> None:
        """
        Attach this event to an activity as a boundary event.
        
        Args:
            activity_id (str): ID of the activity to attach to
            interrupting (bool): Whether the event interrupts the activity
        """
        self.event_type = EventType.BOUNDARY
        self.attached_to_ref = activity_id
        self.is_interrupting = interrupting
    
    def set_timer_trigger(self, timer_expression: str) -> None:
        """
        Configure this event as a timer event.
        
        Args:
            timer_expression (str): Timer expression (ISO 8601 duration, date, or cycle)
        """
        self.event_definition = EventDefinition.TIMER
        self.trigger = timer_expression
    
    def set_message_trigger(self, message_ref: str) -> None:
        """
        Configure this event as a message event.
        
        Args:
            message_ref (str): Reference to the message definition
        """
        self.event_definition = EventDefinition.MESSAGE
        self.trigger = message_ref
    
    def set_error_trigger(self, error_code: str) -> None:
        """
        Configure this event as an error event.
        
        Args:
            error_code (str): Error code or reference
        """
        self.event_definition = EventDefinition.ERROR
        self.trigger = error_code
    
    def set_signal_trigger(self, signal_ref: str) -> None:
        """
        Configure this event as a signal event.
        
        Args:
            signal_ref (str): Reference to the signal definition
        """
        self.event_definition = EventDefinition.SIGNAL
        self.trigger = signal_ref
    
    def __str__(self) -> str:
        """String representation of the event."""
        trigger_info = f" ({self.event_definition.value})" if self.has_trigger() else ""
        return f"{self.event_type.value.title()} Event '{self.name}'{trigger_info}"
    
    class Config:
        """Pydantic configuration for Event elements."""
        use_enum_values = True
        validate_assignment = True
