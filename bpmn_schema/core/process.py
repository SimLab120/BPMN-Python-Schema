"""
BPMN Process and Diagram container classes.

This module contains the main container classes for BPMN processes and diagrams.
These classes hold all the elements and provide the top-level structure.

Author: SimLab120
Date: 2025-07-03
"""

from typing import List, Optional, Union, Literal
from datetime import datetime
from pydantic import BaseModel, Field
from .base import BPMNElement, BPMNElementType
from .events import Event
from .activities import Task, SubProcess
from .gateways import Gateway
from .flows import SequenceFlow, MessageFlow, Association
from .swimlanes import Lane
from .artifacts import DataObject, DataStore, Group, TextAnnotation


class Process(BPMNElement):
    """
    BPMN Process element implementation.
    
    A process represents a business process and contains all the flow objects,
    connecting objects, and artifacts that make up that process.
    
    Attributes:
        is_executable (bool): Whether this process is executable
        is_closed (bool): Whether this process is closed to participants
        process_type (Literal): Type of process (private, public, none)
        definitional_collaboration_ref (Optional[str]): Reference to collaboration
        
        # Flow Objects
        events (List[Event]): All events in the process
        tasks (List[Task]): All tasks in the process
        gateways (List[Gateway]): All gateways in the process
        subprocesses (List[SubProcess]): All subprocesses in the process
        
        # Connecting Objects
        sequence_flows (List[SequenceFlow]): All sequence flows in the process
        associations (List[Association]): All associations in the process
        
        # Artifacts
        data_objects (List[DataObject]): All data objects in the process
        data_stores (List[DataStore]): All data stores in the process
        groups (List[Group]): All groups in the process
        text_annotations (List[TextAnnotation]): All text annotations in the process
        
        # Swimlanes
        lanes (List[Lane]): All lanes in the process
    """
    
    is_executable: bool = Field(False, description="Whether this process is executable")
    is_closed: bool = Field(False, description="Whether this process is closed to participants")
    process_type: Literal["none", "public", "private"] = Field("none", description="Type of process")
    definitional_collaboration_ref: Optional[str] = Field(None, description="Reference to collaboration")
    
    # Flow Objects
    events: List[Event] = Field(default_factory=list, description="All events in the process")
    tasks: List[Task] = Field(default_factory=list, description="All tasks in the process")
    gateways: List[Gateway] = Field(default_factory=list, description="All gateways in the process")
    subprocesses: List[SubProcess] = Field(default_factory=list, description="All subprocesses in the process")
    
    # Connecting Objects
    sequence_flows: List[SequenceFlow] = Field(default_factory=list, description="All sequence flows in the process")
    associations: List[Association] = Field(default_factory=list, description="All associations in the process")
    
    # Artifacts
    data_objects: List[DataObject] = Field(default_factory=list, description="All data objects in the process")
    data_stores: List[DataStore] = Field(default_factory=list, description="All data stores in the process")
    groups: List[Group] = Field(default_factory=list, description="All groups in the process")
    text_annotations: List[TextAnnotation] = Field(default_factory=list, description="All text annotations in the process")
    
    # Swimlanes
    lanes: List[Lane] = Field(default_factory=list, description="All lanes in the process")
    
    def __init__(self, **data):
        """
        Initialize a BPMN Process.
        
        Args:
            **data: Process properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.PROCESS, **data)
    
    # Flow Object Management
    def add_flow_object(self, element: Union[Task, Event, Gateway, SubProcess]) -> None:
        """
        Add a flow object to the process.
        
        Args:
            element: The flow object to add
        """
        if isinstance(element, Task):
            self.tasks.append(element)
        elif isinstance(element, Event):
            self.events.append(element)
        elif isinstance(element, Gateway):
            self.gateways.append(element)
        elif isinstance(element, SubProcess):
            self.subprocesses.append(element)
        else:
            raise ValueError(f"Invalid flow object type: {type(element)}")
    
    def add_connecting_object(self, flow: Union[SequenceFlow, Association]) -> None:
        """
        Add a connecting object to the process.
        
        Args:
            flow: The connecting object to add
        """
        if isinstance(flow, SequenceFlow):
            self.sequence_flows.append(flow)
        elif isinstance(flow, Association):
            self.associations.append(flow)
        else:
            raise ValueError(f"Invalid connecting object type: {type(flow)}")
    
    def add_artifact(self, artifact: Union[DataObject, DataStore, Group, TextAnnotation]) -> None:
        """
        Add an artifact to the process.
        
        Args:
            artifact: The artifact to add
        """
        if isinstance(artifact, DataObject):
            self.data_objects.append(artifact)
        elif isinstance(artifact, DataStore):
            self.data_stores.append(artifact)
        elif isinstance(artifact, Group):
            self.groups.append(artifact)
        elif isinstance(artifact, TextAnnotation):
            self.text_annotations.append(artifact)
        else:
            raise ValueError(f"Invalid artifact type: {type(artifact)}")
    
    def add_lane(self, lane: Lane) -> None:
        """
        Add a lane to the process.
        
        Args:
            lane: The lane to add
        """
        self.lanes.append(lane)
    
    # Element Retrieval
    def get_all_elements(self) -> List[BPMNElement]:
        """Get all elements in the process."""
        return (self.events + self.tasks + self.gateways + self.subprocesses +
                self.sequence_flows + self.associations + self.data_objects +
                self.data_stores + self.groups + self.text_annotations + self.lanes)
    
    def get_all_flow_objects(self) -> List[Union[Task, Event, Gateway, SubProcess]]:
        """Get all flow objects in the process."""
        return self.events + self.tasks + self.gateways + self.subprocesses
    
    def get_element_by_id(self, element_id: str) -> Optional[BPMNElement]:
        """
        Find an element by its ID.
        
        Args:
            element_id (str): ID of the element to find
            
        Returns:
            Optional[BPMNElement]: Element if found, None otherwise
        """
        for element in self.get_all_elements():
            if element.id == element_id:
                return element
        return None
    
    # Statistics and Analysis
    def get_start_events(self) -> List[Event]:
        """Get all start events in the process."""
        return [event for event in self.events if event.is_start_event()]
    
    def get_end_events(self) -> List[Event]:
        """Get all end events in the process."""
        return [event for event in self.events if event.is_end_event()]
    
    def get_user_tasks(self) -> List[Task]:
        """Get all user tasks in the process."""
        return [task for task in self.tasks if task.is_user_task()]
    
    def get_service_tasks(self) -> List[Task]:
        """Get all service tasks in the process."""
        return [task for task in self.tasks if task.is_service_task()]
    
    def count_elements(self) -> dict:
        """Get count of all element types."""
        return {
            "events": len(self.events),
            "tasks": len(self.tasks),
            "gateways": len(self.gateways),
            "subprocesses": len(self.subprocesses),
            "sequence_flows": len(self.sequence_flows),
            "associations": len(self.associations),
            "data_objects": len(self.data_objects),
            "data_stores": len(self.data_stores),
            "groups": len(self.groups),
            "text_annotations": len(self.text_annotations),
            "lanes": len(self.lanes)
        }
    
    def __str__(self) -> str:
        """String representation of the process."""
        counts = self.count_elements()
        total_elements = sum(counts.values())
        executable_info = " (executable)" if self.is_executable else ""
        return f"Process '{self.name}' [{total_elements} elements]{executable_info}"
    
    class Config:
        """Pydantic configuration for Process elements."""
        validate_assignment = True


class BPMNDiagram(BaseModel):
    """
    BPMN Diagram container implementation.
    
    The top-level container for a complete BPMN diagram. Contains processes,
    collaborations (pools), and global elements.
    
    Attributes:
        id (str): Unique identifier for the diagram
        name (Optional[str]): Human-readable name for the diagram
        target_namespace (str): XML namespace for the diagram
        
        # Main elements
        processes (List[Process]): All processes in the diagram
        pools (List[Pool]): All pools for collaborations
        message_flows (List[MessageFlow]): Message flows between pools
        
        # Global artifacts
        global_data_stores (List[DataStore]): Global data stores
        global_text_annotations (List[TextAnnotation]): Global text annotations
        
        # Metadata
        created_by (Optional[str]): Creator of the diagram
        created_at (Optional[datetime]): Creation timestamp
        modified_at (Optional[datetime]): Last modification timestamp
        version (str): Version of the diagram
    """
    
    id: str = Field(..., description="Unique identifier for the diagram")
    name: Optional[str] = Field(None, description="Human-readable name for the diagram")
    target_namespace: str = Field("http://bpmn.io/schema/bpmn", description="XML namespace for the diagram")
    
    # Main elements
    processes: List[Process] = Field(default_factory=list, description="All processes in the diagram")
    pools: List['Pool'] = Field(default_factory=list, description="All pools for collaborations")
    message_flows: List[MessageFlow] = Field(default_factory=list, description="Message flows between pools")
    
    # Global artifacts
    global_data_stores: List[DataStore] = Field(default_factory=list, description="Global data stores")
    global_text_annotations: List[TextAnnotation] = Field(default_factory=list, description="Global text annotations")
    
    # Metadata
    created_by: Optional[str] = Field(None, description="Creator of the diagram")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    modified_at: Optional[datetime] = Field(None, description="Last modification timestamp")
    version: str = Field("1.0", description="Version of the diagram")
    
    def add_process(self, process: Process) -> None:
        """
        Add a process to the diagram.
        
        Args:
            process: The process to add
        """
        self.processes.append(process)
    
    def add_pool(self, pool: 'Pool') -> None:
        """
        Add a pool to the diagram.
        
        Args:
            pool: The pool to add
        """
        self.pools.append(pool)
    
    def add_message_flow(self, message_flow: MessageFlow) -> None:
        """
        Add a message flow to the diagram.
        
        Args:
            message_flow: The message flow to add
        """
        self.message_flows.append(message_flow)
    
    def get_element_by_id(self, element_id: str) -> Optional[BPMNElement]:
        """
        Find any element by ID across the entire diagram.
        
        Args:
            element_id (str): ID of the element to find
            
        Returns:
            Optional[BPMNElement]: Element if found, None otherwise
        """
        # Search in processes
        for process in self.processes:
            element = process.get_element_by_id(element_id)
            if element:
                return element
        
        # Search in pools and lanes
        for pool in self.pools:
            if pool.id == element_id:
                return pool
            for lane in pool.lanes:
                if lane.id == element_id:
                    return lane
        
        # Search in message flows
        for message_flow in self.message_flows:
            if message_flow.id == element_id:
                return message_flow
        
        # Search in global artifacts
        for data_store in self.global_data_stores:
            if data_store.id == element_id:
                return data_store
        
        for annotation in self.global_text_annotations:
            if annotation.id == element_id:
                return annotation
        
        return None
    
    def is_collaboration(self) -> bool:
        """Check if this diagram represents a collaboration (has pools)."""
        return len(self.pools) > 0
    
    def get_all_processes(self) -> List[Process]:
        """Get all processes including those referenced by pools."""
        all_processes = self.processes.copy()
        # Add processes referenced by pools (if any)
        for pool in self.pools:
            if pool.process_ref:
                # In a real implementation, you'd resolve the reference
                pass
        return all_processes
    
    def count_all_elements(self) -> dict:
        """Get count of all elements across the entire diagram."""
        total_counts = {
            "processes": len(self.processes),
            "pools": len(self.pools),
            "message_flows": len(self.message_flows),
            "global_data_stores": len(self.global_data_stores),
            "global_text_annotations": len(self.global_text_annotations)
        }
        
        # Aggregate counts from all processes
        process_counts = {}
        for process in self.processes:
            counts = process.count_elements()
            for key, value in counts.items():
                process_counts[key] = process_counts.get(key, 0) + value
        
        total_counts.update(process_counts)
        return total_counts
    
    def __str__(self) -> str:
        """String representation of the diagram."""
        process_count = len(self.processes)
        pool_count = len(self.pools)
        collaboration_info = f" (collaboration with {pool_count} pools)" if self.is_collaboration() else ""
        return f"BPMN Diagram '{self.name}' [{process_count} processes]{collaboration_info}"
    
    class Config:
        """Pydantic configuration for BPMNDiagram."""
        validate_assignment = True


# Import Pool here to avoid circular imports
from .swimlanes import Pool
BPMNDiagram.model_rebuild()
