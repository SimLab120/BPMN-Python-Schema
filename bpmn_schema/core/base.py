"""
Base classes and common types for BPMN elements.

This module defines the foundational classes and enums that all BPMN elements inherit from.
It provides common properties like positioning, dimensions, and element identification.

Author: SimLab120
Date: 2025-07-03
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum


class BPMNElementType(str, Enum):
    """
    Enumeration of all BPMN element types.
    
    This enum categorizes all BPMN elements according to the four main groups:
    - Flow Objects: PROCESS, TASK, EVENT, GATEWAY, SUBPROCESS, CALL_ACTIVITY
    - Connecting Objects: SEQUENCE_FLOW, MESSAGE_FLOW, ASSOCIATION
    - Swimlanes: POOL, LANE
    - Artifacts: DATA_OBJECT, DATA_STORE, GROUP, TEXT_ANNOTATION
    """
    
    # Flow Objects
    PROCESS = "process"
    TASK = "task"
    EVENT = "event"
    GATEWAY = "gateway"
    SUBPROCESS = "subprocess"
    CALL_ACTIVITY = "call_activity"
    
    # Connecting Objects
    SEQUENCE_FLOW = "sequence_flow"
    MESSAGE_FLOW = "message_flow"
    ASSOCIATION = "association"
    
    # Swimlanes
    POOL = "pool"
    LANE = "lane"
    
    # Artifacts
    DATA_OBJECT = "data_object"
    DATA_STORE = "data_store"
    GROUP = "group"
    TEXT_ANNOTATION = "text_annotation"


class Position(BaseModel):
    """
    Represents the x, y coordinates for positioning BPMN elements in a diagram.
    
    Used for visual layout and rendering of BPMN diagrams. Coordinates are typically
    in pixels or logical units depending on the rendering engine.
    
    Attributes:
        x (float): Horizontal position coordinate
        y (float): Vertical position coordinate
    """
    x: float = Field(..., description="Horizontal position coordinate")
    y: float = Field(..., description="Vertical position coordinate")
    
    def __str__(self) -> str:
        return f"Position(x={self.x}, y={self.y})"


class Dimensions(BaseModel):
    """
    Represents the width and height dimensions for BPMN elements.
    
    Used for visual layout and collision detection in BPMN diagrams.
    
    Attributes:
        width (float): Element width in logical units
        height (float): Element height in logical units
    """
    width: float = Field(..., gt=0, description="Element width (must be positive)")
    height: float = Field(..., gt=0, description="Element height (must be positive)")
    
    def __str__(self) -> str:
        return f"Dimensions(width={self.width}, height={self.height})"


class BPMNElement(BaseModel):
    """
    Base class for all BPMN elements.
    
    This abstract base class provides common properties and methods that all BPMN elements
    share, including identification, positioning, documentation, and custom properties.
    
    All specific BPMN elements (Events, Tasks, Gateways, etc.) inherit from this class.
    
    Attributes:
        id (str): Unique identifier for the element within the diagram
        name (Optional[str]): Human-readable name for the element
        element_type (BPMNElementType): Type classification of the element
        documentation (Optional[str]): Optional documentation or description
        position (Optional[Position]): Visual position in the diagram
        dimensions (Optional[Dimensions]): Visual dimensions of the element
        properties (Dict[str, Any]): Custom properties for extensibility
    """
    
    id: str = Field(..., description="Unique identifier for the element")
    name: Optional[str] = Field(None, description="Human-readable name for the element")
    element_type: BPMNElementType = Field(..., description="Type classification of the element")
    documentation: Optional[str] = Field(None, description="Optional documentation or description")
    position: Optional[Position] = Field(None, description="Visual position in the diagram")
    dimensions: Optional[Dimensions] = Field(None, description="Visual dimensions of the element")
    properties: Dict[str, Any] = Field(
        default_factory=dict,
        description="Custom properties for extensibility"
    )
    
    def __str__(self) -> str:
        """String representation of the BPMN element."""
        return f"{self.element_type.value}(id='{self.id}', name='{self.name}')"
    
    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return (
            f"{self.__class__.__name__}("
            f"id='{self.id}', "
            f"name='{self.name}', "
            f"element_type={self.element_type.value})"
        )
    
    def set_position(self, x: float, y: float) -> None:
        """
        Set the position of the element in the diagram.
        
        Args:
            x (float): Horizontal position coordinate
            y (float): Vertical position coordinate
        """
        self.position = Position(x=x, y=y)
    
    def set_dimensions(self, width: float, height: float) -> None:
        """
        Set the dimensions of the element.
        
        Args:
            width (float): Element width (must be positive)
            height (float): Element height (must be positive)
        """
        self.dimensions = Dimensions(width=width, height=height)
    
    def add_property(self, key: str, value: Any) -> None:
        """
        Add a custom property to the element.
        
        Args:
            key (str): Property key
            value (Any): Property value
        """
        self.properties[key] = value
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """
        Get a custom property value.
        
        Args:
            key (str): Property key
            default (Any): Default value if key not found
            
        Returns:
            Any: Property value or default
        """
        return self.properties.get(key, default)
    
    def has_position(self) -> bool:
        """Check if the element has position information."""
        return self.position is not None
    
    def has_dimensions(self) -> bool:
        """Check if the element has dimension information."""
        return self.dimensions is not None
    
    class Config:
        """Pydantic configuration for BPMN elements."""
        # Allow extra fields for extensibility
        extra = "allow"
        # Use enum values for serialization
        use_enum_values = True
        # Validate assignments
        validate_assignment = True
