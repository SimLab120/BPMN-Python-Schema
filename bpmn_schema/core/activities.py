"""
BPMN Activity elements implementation.

This module contains all activity-related classes for BPMN modeling.
Activities represent work performed within a business process.

Activities are divided into two main categories:
- Tasks: Atomic work units that cannot be broken down further
- Sub-processes: Compound activities that contain other activities

Author: SimLab120
Date: 2025-07-03
"""

from typing import List, Optional, Union, Literal
from enum import Enum
from datetime import datetime
from pydantic import Field
from .base import BPMNElement, BPMNElementType


class TaskType(str, Enum):
    """
    Enumeration of BPMN task types.
    
    Tasks are atomic activities that represent work performed by humans or systems.
    Each task type has specific semantics and properties.
    """
    
    TASK = "task"                           # Abstract/undefined task
    USER_TASK = "user_task"                 # Work performed by a human user
    SERVICE_TASK = "service_task"           # Automated service call
    MANUAL_TASK = "manual_task"             # Physical work not tracked by system
    SCRIPT_TASK = "script_task"             # Automated script execution
    BUSINESS_RULE_TASK = "business_rule_task"  # Business rule evaluation
    SEND_TASK = "send_task"                 # Message sending
    RECEIVE_TASK = "receive_task"           # Message reception


class SubProcessType(str, Enum):
    """
    Enumeration of BPMN subprocess types.
    
    Subprocesses are compound activities that contain other flow elements.
    """
    
    EMBEDDED = "embedded"                   # Embedded subprocess
    EVENT = "event"                         # Event subprocess
    CALL_ACTIVITY = "call_activity"         # Call to external process
    TRANSACTION = "transaction"             # Transaction subprocess
    AD_HOC = "ad_hoc"                      # Ad-hoc subprocess


class ActivityMarker(str, Enum):
    """
    Enumeration of activity markers.
    
    Markers indicate special behavior or characteristics of activities.
    """
    
    LOOP = "loop"                           # Standard loop
    PARALLEL_MULTI_INSTANCE = "parallel_multi_instance"      # Parallel multi-instance
    SEQUENTIAL_MULTI_INSTANCE = "sequential_multi_instance"  # Sequential multi-instance
    COMPENSATION = "compensation"           # Compensation activity
    AD_HOC = "ad_hoc"                      # Ad-hoc activity


class Task(BPMNElement):
    """
    BPMN Task element implementation.
    
    Tasks represent atomic work units that cannot be broken down further.
    They are the most granular level of work in a BPMN process.
    
    This class supports all BPMN 2.0 task types with their specific properties
    and behaviors as defined in the specification.
    
    Attributes:
        task_type (TaskType): Specific type of task
        markers (List[ActivityMarker]): Activity markers indicating special behavior
        
        # Human task properties
        assignee (Optional[str]): Specific user assigned to the task
        candidate_groups (List[str]): Groups that can claim the task
        candidate_users (List[str]): Users that can claim the task
        due_date (Optional[datetime]): Task due date
        priority (Optional[int]): Task priority level
        form_key (Optional[str]): Form definition for user tasks
        
        # Service task properties
        implementation (Optional[str]): Service implementation reference
        operation_ref (Optional[str]): Operation reference for service calls
        
        # Script task properties
        script (Optional[str]): Script content to execute
        script_format (Optional[str]): Script format/language
        
        # Send/Receive task properties
        message_ref (Optional[str]): Message reference
        operation (Optional[str]): Operation for message tasks
        instantiate (bool): Whether task instantiates the process
        
        # Business rule task properties
        rule_implementation (Optional[str]): Rule engine implementation
        decision_ref (Optional[str]): Decision reference
        
        # Multi-instance properties
        is_sequential (bool): Whether multi-instance is sequential
        loop_cardinality (Optional[str]): Number of instances expression
        completion_condition (Optional[str]): Completion condition expression
        collection (Optional[str]): Collection to iterate over
        element_variable (Optional[str]): Variable name for current element
    """
    
    task_type: TaskType = TaskType.TASK
    markers: List[ActivityMarker] = Field(default_factory=list)
    
    # Human task properties
    assignee: Optional[str] = None
    candidate_groups: List[str] = Field(default_factory=list)
    candidate_users: List[str] = Field(default_factory=list)
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    form_key: Optional[str] = None
    
    # Service task properties
    implementation: Optional[str] = None
    operation_ref: Optional[str] = None
    
    # Script task properties
    script: Optional[str] = None
    script_format: Optional[str] = None
    
    # Send/Receive task properties
    message_ref: Optional[str] = None
    operation: Optional[str] = None
    instantiate: bool = False
    
    # Business rule task properties
    rule_implementation: Optional[str] = None
    decision_ref: Optional[str] = None
    
    # Multi-instance properties
    is_sequential: bool = False
    loop_cardinality: Optional[str] = None
    completion_condition: Optional[str] = None
    collection: Optional[str] = None
    element_variable: Optional[str] = None
    
    def __init__(self, **data):
        """
        Initialize a BPMN Task.
        
        Args:
            **data: Task properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.TASK, **data)
    
    def is_user_task(self) -> bool:
        """Check if this is a user task."""
        return self.task_type == TaskType.USER_TASK
    
    def is_service_task(self) -> bool:
        """Check if this is a service task."""
        return self.task_type == TaskType.SERVICE_TASK
    
    def is_script_task(self) -> bool:
        """Check if this is a script task."""
        return self.task_type == TaskType.SCRIPT_TASK
    
    def is_multi_instance(self) -> bool:
        """Check if this task has multi-instance behavior."""
        return (ActivityMarker.PARALLEL_MULTI_INSTANCE in self.markers or
                ActivityMarker.SEQUENTIAL_MULTI_INSTANCE in self.markers)
    
    def is_parallel_multi_instance(self) -> bool:
        """Check if this task has parallel multi-instance behavior."""
        return ActivityMarker.PARALLEL_MULTI_INSTANCE in self.markers
    
    def is_sequential_multi_instance(self) -> bool:
        """Check if this task has sequential multi-instance behavior."""
        return ActivityMarker.SEQUENTIAL_MULTI_INSTANCE in self.markers
    
    def has_loop(self) -> bool:
        """Check if this task has loop behavior."""
        return ActivityMarker.LOOP in self.markers
    
    def assign_to_user(self, user_id: str) -> None:
        """
        Assign the task to a specific user.
        
        Args:
            user_id (str): ID of the user to assign the task to
        """
        self.assignee = user_id
    
    def add_candidate_group(self, group_id: str) -> None:
        """
        Add a candidate group that can claim this task.
        
        Args:
            group_id (str): ID of the group to add
        """
        if group_id not in self.candidate_groups:
            self.candidate_groups.append(group_id)
    
    def add_candidate_user(self, user_id: str) -> None:
        """
        Add a candidate user that can claim this task.
        
        Args:
            user_id (str): ID of the user to add
        """
        if user_id not in self.candidate_users:
            self.candidate_users.append(user_id)
    
    def set_multi_instance_parallel(self, collection: str, element_variable: str = "item") -> None:
        """
        Configure parallel multi-instance behavior.
        
        Args:
            collection (str): Collection expression to iterate over
            element_variable (str): Variable name for current element
        """
        self.markers.append(ActivityMarker.PARALLEL_MULTI_INSTANCE)
        self.collection = collection
        self.element_variable = element_variable
        self.is_sequential = False
    
    def set_multi_instance_sequential(self, collection: str, element_variable: str = "item") -> None:
        """
        Configure sequential multi-instance behavior.
        
        Args:
            collection (str): Collection expression to iterate over
            element_variable (str): Variable name for current element
        """
        self.markers.append(ActivityMarker.SEQUENTIAL_MULTI_INSTANCE)
        self.collection = collection
        self.element_variable = element_variable
        self.is_sequential = True
    
    def set_script(self, script_content: str, script_format: str = "javascript") -> None:
        """
        Configure script task properties.
        
        Args:
            script_content (str): The script content to execute
            script_format (str): Script format/language
        """
        self.task_type = TaskType.SCRIPT_TASK
        self.script = script_content
        self.script_format = script_format
    
    def __str__(self) -> str:
        """String representation of the task."""
        return f"{self.task_type.value.replace('_', ' ').title()} '{self.name}'"
    
    class Config:
        """Pydantic configuration for Task elements."""
        use_enum_values = True
        validate_assignment = True


class SubProcess(BPMNElement):
    """
    BPMN SubProcess element implementation.
    
    Subprocesses are compound activities that contain other flow elements.
    They can be used to group activities and define reusable process components.
    
    Attributes:
        subprocess_type (SubProcessType): Type of subprocess
        is_expanded (bool): Whether subprocess is expanded in diagram
        triggered_by_event (bool): Whether subprocess is triggered by events
        is_for_compensation (bool): Whether subprocess is for compensation
        markers (List[ActivityMarker]): Activity markers
        
        # Call Activity properties
        called_element (Optional[str]): Reference to called process or task
        called_element_type (Optional[str]): Type of called element
        
        # Transaction properties
        method (Optional[str]): Transaction method
        
        # Ad-hoc properties
        ordering (Optional[str]): Ordering of ad-hoc activities
        cancel_remaining_instances (bool): Whether to cancel remaining instances
        
        # Contained elements (for expanded subprocesses)
        elements (List[Union[Task, Event, SubProcess]]): Child elements
        sequence_flows (List[SequenceFlow]): Internal sequence flows
        boundary_events (List[Event]): Boundary events attached to subprocess
    """
    
    subprocess_type: SubProcessType = SubProcessType.EMBEDDED
    is_expanded: bool = True
    triggered_by_event: bool = False
    is_for_compensation: bool = False
    markers: List[ActivityMarker] = Field(default_factory=list)
    
    # Call Activity properties
    called_element: Optional[str] = None
    called_element_type: Optional[Literal["process", "global_task"]] = None
    
    # Transaction properties
    method: Optional[str] = None
    
    # Ad-hoc properties
    ordering: Optional[Literal["parallel", "sequential"]] = None
    cancel_remaining_instances: bool = True
    
    # Contained elements (for expanded subprocesses)
    elements: List[Union[Task, 'Event', 'SubProcess']] = Field(default_factory=list)
    sequence_flows: List['SequenceFlow'] = Field(default_factory=list)
    boundary_events: List['Event'] = Field(default_factory=list)
    
    def __init__(self, **data):
        """
        Initialize a BPMN SubProcess.
        
        Args:
            **data: SubProcess properties including all base element properties
        """
        # Set element type based on subprocess type
        if data.get('subprocess_type') == SubProcessType.CALL_ACTIVITY:
            super().__init__(element_type=BPMNElementType.CALL_ACTIVITY, **data)
        else:
            super().__init__(element_type=BPMNElementType.SUBPROCESS, **data)
    
    def is_call_activity(self) -> bool:
        """Check if this is a call activity."""
        return self.subprocess_type == SubProcessType.CALL_ACTIVITY
    
    def is_event_subprocess(self) -> bool:
        """Check if this is an event subprocess."""
        return self.subprocess_type == SubProcessType.EVENT
    
    def is_transaction(self) -> bool:
        """Check if this is a transaction subprocess."""
        return self.subprocess_type == SubProcessType.TRANSACTION
    
    def is_ad_hoc(self) -> bool:
        """Check if this is an ad-hoc subprocess."""
        return self.subprocess_type == SubProcessType.AD_HOC
    
    def add_element(self, element: Union[Task, 'Event', 'SubProcess']) -> None:
        """
        Add a child element to this subprocess.
        
        Args:
            element: The element to add
        """
        self.elements.append(element)
    
    def add_sequence_flow(self, flow: 'SequenceFlow') -> None:
        """
        Add a sequence flow within this subprocess.
        
        Args:
            flow: The sequence flow to add
        """
        self.sequence_flows.append(flow)
    
    def add_boundary_event(self, event: 'Event') -> None:
        """
        Add a boundary event to this subprocess.
        
        Args:
            event: The boundary event to add
        """
        event.attach_to_activity(self.id)
        self.boundary_events.append(event)
    
    def get_all_elements(self) -> List[Union[Task, 'Event', 'SubProcess']]:
        """Get all elements contained in this subprocess."""
        return self.elements
    
    def __str__(self) -> str:
        """String representation of the subprocess."""
        return f"{self.subprocess_type.value.replace('_', ' ').title()} '{self.name}'"
    
    class Config:
        """Pydantic configuration for SubProcess elements."""
        use_enum_values = True
        validate_assignment = True


# Update forward references for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .events import Event
    from .flows import SequenceFlow
