"""
BPMN Flow elements implementation.

This module contains all flow-related classes for BPMN modeling.
Flows are connecting objects that link flow objects together to create
the structure of a business process.

Author: SimLab120
Date: 2025-07-03
"""

from typing import List, Optional, Literal
from pydantic import Field
from .base import BPMNElement, BPMNElementType, Position


class SequenceFlow(BPMNElement):
    """
    BPMN Sequence Flow element implementation.
    
    Sequence flows are used to show the order in which activities will be
    performed in a process. They connect flow objects within a single pool.
    
    Sequence flows are represented as solid arrows in BPMN diagrams.
    
    Attributes:
        source_ref (str): ID of the source flow object
        target_ref (str): ID of the target flow object
        condition_expression (Optional[str]): Condition for conditional flows
        is_immediate (bool): Whether flow is immediate (no delay)
        waypoints (List[Position]): Visual waypoints for flow routing
    """
    
    source_ref: str = Field(..., description="ID of the source flow object")
    target_ref: str = Field(..., description="ID of the target flow object")
    condition_expression: Optional[str] = Field(None, description="Condition expression for conditional flows")
    is_immediate: bool = Field(False, description="Whether flow is immediate (no delay)")
    waypoints: List[Position] = Field(default_factory=list, description="Visual waypoints for flow routing")
    
    def __init__(self, **data):
        """
        Initialize a BPMN Sequence Flow.
        
        Args:
            **data: Sequence flow properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.SEQUENCE_FLOW, **data)
    
    def is_conditional(self) -> bool:
        """Check if this is a conditional sequence flow."""
        return self.condition_expression is not None
    
    def is_default(self) -> bool:
        """Check if this is a default sequence flow (determined by gateway)."""
        # Default flows are identified by being referenced in a gateway's default_flow property
        return False  # This would need to be determined by the containing process
    
    def set_condition(self, expression: str) -> None:
        """
        Set the condition expression for this sequence flow.
        
        Args:
            expression (str): Condition expression (e.g., "${approved == true}")
        """
        self.condition_expression = expression
    
    def add_waypoint(self, x: float, y: float) -> None:
        """
        Add a waypoint for visual routing of the flow.
        
        Args:
            x (float): X coordinate of waypoint
            y (float): Y coordinate of waypoint
        """
        self.waypoints.append(Position(x=x, y=y))
    
    def clear_waypoints(self) -> None:
        """Clear all waypoints for this flow."""
        self.waypoints.clear()
    
    def __str__(self) -> str:
        """String representation of the sequence flow."""
        condition_info = f" [{self.condition_expression}]" if self.is_conditional() else ""
        return f"Sequence Flow '{self.name}' ({self.source_ref} → {self.target_ref}){condition_info}"
    
    class Config:
        """Pydantic configuration for SequenceFlow elements."""
        validate_assignment = True


class MessageFlow(BPMNElement):
    """
    BPMN Message Flow element implementation.
    
    Message flows are used to show the flow of messages between separate
    process participants (pools). They cannot connect flow objects within
    the same pool.
    
    Message flows are represented as dashed arrows in BPMN diagrams.
    
    Attributes:
        source_ref (str): ID of the source element (must be in different pool)
        target_ref (str): ID of the target element (must be in different pool)
        message_ref (Optional[str]): Reference to message definition
        waypoints (List[Position]): Visual waypoints for flow routing
    """
    
    source_ref: str = Field(..., description="ID of the source element")
    target_ref: str = Field(..., description="ID of the target element")
    message_ref: Optional[str] = Field(None, description="Reference to message definition")
    waypoints: List[Position] = Field(default_factory=list, description="Visual waypoints for flow routing")
    
    def __init__(self, **data):
        """
        Initialize a BPMN Message Flow.
        
        Args:
            **data: Message flow properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.MESSAGE_FLOW, **data)
    
    def has_message_reference(self) -> bool:
        """Check if this message flow has a message reference."""
        return self.message_ref is not None
    
    def set_message_reference(self, message_ref: str) -> None:
        """
        Set the message reference for this message flow.
        
        Args:
            message_ref (str): Reference to the message definition
        """
        self.message_ref = message_ref
    
    def add_waypoint(self, x: float, y: float) -> None:
        """
        Add a waypoint for visual routing of the flow.
        
        Args:
            x (float): X coordinate of waypoint
            y (float): Y coordinate of waypoint
        """
        self.waypoints.append(Position(x=x, y=y))
    
    def clear_waypoints(self) -> None:
        """Clear all waypoints for this flow."""
        self.waypoints.clear()
    
    def __str__(self) -> str:
        """String representation of the message flow."""
        message_info = f" [Message: {self.message_ref}]" if self.has_message_reference() else ""
        return f"Message Flow '{self.name}' ({self.source_ref} ⇢ {self.target_ref}){message_info}"
    
    class Config:
        """Pydantic configuration for MessageFlow elements."""
        validate_assignment = True


class Association(BPMNElement):
    """
    BPMN Association element implementation.
    
    Associations are used to link artifacts and text to flow objects.
    They provide additional information about the process without affecting
    the sequence flow.
    
    Associations are represented as dotted lines in BPMN diagrams.
    
    Attributes:
        source_ref (str): ID of the source element
        target_ref (str): ID of the target element
        association_direction (Literal): Direction of association
        waypoints (List[Position]): Visual waypoints for association routing
    """
    
    source_ref: str = Field(..., description="ID of the source element")
    target_ref: str = Field(..., description="ID of the target element")
    association_direction: Literal["none", "one", "both"] = Field("none", description="Direction of association")
    waypoints: List[Position] = Field(default_factory=list, description="Visual waypoints for association routing")
    
    def __init__(self, **data):
        """
        Initialize a BPMN Association.
        
        Args:
            **data: Association properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.ASSOCIATION, **data)
    
    def is_directional(self) -> bool:
        """Check if this association has a direction."""
        return self.association_direction != "none"
    
    def is_bidirectional(self) -> bool:
        """Check if this association is bidirectional."""
        return self.association_direction == "both"
    
    def set_direction_none(self) -> None:
        """Set association as non-directional."""
        self.association_direction = "none"
    
    def set_direction_one(self) -> None:
        """Set association as unidirectional (source to target)."""
        self.association_direction = "one"
    
    def set_direction_both(self) -> None:
        """Set association as bidirectional."""
        self.association_direction = "both"
    
    def add_waypoint(self, x: float, y: float) -> None:
        """
        Add a waypoint for visual routing of the association.
        
        Args:
            x (float): X coordinate of waypoint
            y (float): Y coordinate of waypoint
        """
        self.waypoints.append(Position(x=x, y=y))
    
    def clear_waypoints(self) -> None:
        """Clear all waypoints for this association."""
        self.waypoints.clear()
    
    def __str__(self) -> str:
        """String representation of the association."""
        direction_symbols = {
            "none": "⋯",
            "one": "⋯>",
            "both": "<⋯>"
        }
        symbol = direction_symbols.get(self.association_direction, "⋯")
        return f"Association '{self.name}' ({self.source_ref} {symbol} {self.target_ref})"
    
    class Config:
        """Pydantic configuration for Association elements."""
        validate_assignment = True
