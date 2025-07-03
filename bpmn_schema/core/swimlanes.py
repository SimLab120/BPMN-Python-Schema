"""
BPMN Swimlane elements implementation.

This module contains swimlane-related classes for BPMN modeling.
Swimlanes are used to organize activities based on who performs them
or what functional area they belong to.

Author: SimLab120
Date: 2025-07-03
"""

from typing import List, Optional
from pydantic import Field
from .base import BPMNElement, BPMNElementType


class Lane(BPMNElement):
    """
    BPMN Lane element implementation.
    
    Lanes are subdivisions within a pool that organize activities based on
    roles, responsibilities, or departments. They provide visual organization
    and responsibility assignment within a process.
    
    Lanes are typically displayed as horizontal bands within a pool.
    
    Attributes:
        flow_node_refs (List[str]): References to flow nodes contained in this lane
        child_lanes (List[Lane]): Child lanes for nested lane structures
        partition_element_ref (Optional[str]): Reference to partition element
    """
    
    flow_node_refs: List[str] = Field(default_factory=list, description="Flow nodes contained in this lane")
    child_lanes: List['Lane'] = Field(default_factory=list, description="Child lanes for nested structures")
    partition_element_ref: Optional[str] = Field(None, description="Reference to partition element")
    
    def __init__(self, **data):
        """
        Initialize a BPMN Lane.
        
        Args:
            **data: Lane properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.LANE, **data)
    
    def add_flow_node(self, node_id: str) -> None:
        """
        Add a flow node reference to this lane.
        
        Args:
            node_id (str): ID of the flow node to add
        """
        if node_id not in self.flow_node_refs:
            self.flow_node_refs.append(node_id)
    
    def remove_flow_node(self, node_id: str) -> None:
        """
        Remove a flow node reference from this lane.
        
        Args:
            node_id (str): ID of the flow node to remove
        """
        if node_id in self.flow_node_refs:
            self.flow_node_refs.remove(node_id)
    
    def add_child_lane(self, lane: 'Lane') -> None:
        """
        Add a child lane to this lane.
        
        Args:
            lane (Lane): Child lane to add
        """
        self.child_lanes.append(lane)
    
    def has_child_lanes(self) -> bool:
        """Check if this lane has child lanes."""
        return len(self.child_lanes) > 0
    
    def has_flow_nodes(self) -> bool:
        """Check if this lane contains flow nodes."""
        return len(self.flow_node_refs) > 0
    
    def get_all_flow_nodes(self) -> List[str]:
        """
        Get all flow node references including those in child lanes.
        
        Returns:
            List[str]: All flow node IDs in this lane and its children
        """
        all_nodes = self.flow_node_refs.copy()
        for child_lane in self.child_lanes:
            all_nodes.extend(child_lane.get_all_flow_nodes())
        return all_nodes
    
    def __str__(self) -> str:
        """String representation of the lane."""
        node_count = len(self.get_all_flow_nodes())
        child_info = f" ({len(self.child_lanes)} child lanes)" if self.has_child_lanes() else ""
        return f"Lane '{self.name}' [{node_count} nodes]{child_info}"
    
    class Config:
        """Pydantic configuration for Lane elements."""
        validate_assignment = True


class Pool(BPMNElement):
    """
    BPMN Pool element implementation.
    
    Pools represent participants in a process collaboration. They contain
    the activities that a single participant performs. Pools can contain
    lanes to further organize activities by roles or responsibilities.
    
    Pools are the top-level containers in BPMN collaborations and are
    typically displayed as large rectangles containing the process.
    
    Attributes:
        is_executable (bool): Whether the pool contains an executable process
        process_ref (Optional[str]): Reference to the process definition
        lanes (List[Lane]): Lanes within this pool
        participant_multiplicity (Optional[int]): Number of participant instances
        is_horizontal (bool): Whether the pool is oriented horizontally
    """
    
    is_executable: bool = Field(False, description="Whether the pool contains an executable process")
    process_ref: Optional[str] = Field(None, description="Reference to the process definition")
    lanes: List[Lane] = Field(default_factory=list, description="Lanes within this pool")
    participant_multiplicity: Optional[int] = Field(None, description="Number of participant instances")
    is_horizontal: bool = Field(True, description="Whether the pool is oriented horizontally")
    
    def __init__(self, **data):
        """
        Initialize a BPMN Pool.
        
        Args:
            **data: Pool properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.POOL, **data)
    
    def add_lane(self, lane: Lane) -> None:
        """
        Add a lane to this pool.
        
