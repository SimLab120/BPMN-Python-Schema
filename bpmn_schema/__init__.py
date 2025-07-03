from .core.base import BPMNElement, Position, Dimensions
from .core.events import Event, EventType, EventDefinition
from .core.activities import Task, TaskType, SubProcess, SubProcessType, ActivityMarker
from .core.gateways import Gateway, GatewayType
from .core.flows import SequenceFlow, MessageFlow, Association
from .core.swimlanes import Pool, Lane
from .core.artifacts import DataObject, DataStore, Group, TextAnnotation
from .core.process import Process, BPMNDiagram

__version__ = "1.0.0"
__author__ = "SimLab120"
__email__ = "simlab120@example.com"
__license__ = "MIT"

__all__ = [
    "BPMNElement", "Position", "Dimensions",
    "Event", "EventType", "EventDefinition",
    "Task", "TaskType", "SubProcess", "SubProcessType", "ActivityMarker",
    "Gateway", "GatewayType",
    "SequenceFlow", "MessageFlow", "Association",
    "Pool", "Lane",
    "DataObject", "DataStore", "Group", "TextAnnotation",
    "Process", "BPMNDiagram",
]
