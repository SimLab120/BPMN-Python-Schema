"""
BPMN Artifact elements implementation.

This module contains all artifact-related classes for BPMN modeling.
Artifacts provide additional information about the process but do not
directly affect the sequence flow.

Author: SimLab120
Date: 2025-07-03
"""

from typing import Optional
from pydantic import Field
from .base import BPMNElement, BPMNElementType


class DataObject(BPMNElement):
    """
    BPMN Data Object artifact implementation.
    
    Data objects represent information flowing through the process.
    They show the data requirements of activities and can represent
    both electronic and physical documents.
    
    Data objects are displayed as rectangles with a folded corner.
    
    Attributes:
        is_collection (bool): Whether this represents a collection of items
        item_subject_ref (Optional[str]): Reference to the data type
        state (Optional[str]): Current state of the data object
    """
    
    is_collection: bool = Field(False, description="Whether this represents a collection of items")
    item_subject_ref: Optional[str] = Field(None, description="Reference to the data type")
    state: Optional[str] = Field(None, description="Current state of the data object")
    
    def __init__(self, **data):
        """
        Initialize a BPMN Data Object.
        
        Args:
            **data: Data object properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.DATA_OBJECT, **data)
    
    def set_state(self, state: str) -> None:
        """
        Set the state of the data object.
        
        Args:
            state (str): State description (e.g., "Draft", "Approved", "Rejected")
        """
        self.state = state
    
    def set_as_collection(self, collection: bool = True) -> None:
        """
        Set whether this data object represents a collection.
        
        Args:
            collection (bool): Whether this is a collection
        """
        self.is_collection = collection
    
    def has_state(self) -> bool:
        """Check if this data object has a state defined."""
        return self.state is not None
    
    def __str__(self) -> str:
        """String representation of the data object."""
        collection_info = " (collection)" if self.is_collection else ""
        state_info = f" [{self.state}]" if self.has_state() else ""
        return f"Data Object '{self.name}'{collection_info}{state_info}"
    
    class Config:
        """Pydantic configuration for DataObject elements."""
        validate_assignment = True


class DataStore(BPMNElement):
    """
    BPMN Data Store artifact implementation.
    
    Data stores represent persistent data storage such as databases,
    file systems, or any other form of data repository that exists
    beyond the lifetime of the process.
    
    Data stores are displayed as cylinders (database symbols).
    
    Attributes:
        capacity (Optional[int]): Storage capacity (if limited)
        is_unlimited (bool): Whether storage capacity is unlimited
        item_subject_ref (Optional[str]): Reference to the data type stored
    """
    
    capacity: Optional[int] = Field(None, description="Storage capacity (if limited)")
    is_unlimited: bool = Field(True, description="Whether storage capacity is unlimited")
    item_subject_ref: Optional[str] = Field(None, description="Reference to the data type stored")
    
    def __init__(self, **data):
        """
        Initialize a BPMN Data Store.
        
        Args:
            **data: Data store properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.DATA_STORE, **data)
    
    def set_capacity(self, capacity: int) -> None:
        """
        Set the storage capacity of the data store.
        
        Args:
            capacity (int): Storage capacity
        """
        self.capacity = capacity
        self.is_unlimited = False
    
    def set_unlimited_capacity(self) -> None:
        """Set the data store to have unlimited capacity."""
        self.capacity = None
        self.is_unlimited = True
    
    def has_capacity_limit(self) -> bool:
        """Check if this data store has a capacity limit."""
        return not self.is_unlimited and self.capacity is not None
    
    def __str__(self) -> str:
        """String representation of the data store."""
        capacity_info = ""
        if self.has_capacity_limit():
            capacity_info = f" (capacity: {self.capacity})"
        elif self.is_unlimited:
            capacity_info = " (unlimited)"
        return f"Data Store '{self.name}'{capacity_info}"
    
    class Config:
        """Pydantic configuration for DataStore elements."""
        validate_assignment = True


class Group(BPMNElement):
    """
    BPMN Group artifact implementation.
    
    Groups provide visual grouping of elements without affecting the
    execution semantics. They are used for documentation and analysis
    purposes to highlight related activities or concepts.
    
    Groups are displayed as rounded rectangles with dashed borders.
    
    Attributes:
        category_value_ref (Optional[str]): Reference to category definition
    """
    
    category_value_ref: Optional[str] = Field(None, description="Reference to category definition")
    
    def __init__(self, **data):
        """
        Initialize a BPMN Group.
        
        Args:
            **data: Group properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.GROUP, **data)
    
    def set_category(self, category_ref: str) -> None:
        """
        Set the category reference for this group.
        
        Args:
            category_ref (str): Reference to category definition
        """
        self.category_value_ref = category_ref
    
    def has_category(self) -> bool:
        """Check if this group has a category reference."""
        return self.category_value_ref is not None
    
    def __str__(self) -> str:
        """String representation of the group."""
        category_info = f" (category: {self.category_value_ref})" if self.has_category() else ""
        return f"Group '{self.name}'{category_info}"
    
    class Config:
        """Pydantic configuration for Group elements."""
        validate_assignment = True


class TextAnnotation(BPMNElement):
    """
    BPMN Text Annotation artifact implementation.
    
    Text annotations provide additional information about the process
    in the form of text comments. They can be associated with any
    flow object through associations.
    
    Text annotations are displayed as text with a bracket on the left side.
    
    Attributes:
        text (str): The annotation text content
        text_format (str): Format of the text (default: plain text)
    """
    
    text: str = Field(..., description="The annotation text content")
    text_format: str = Field("text/plain", description="Format of the text")
    
    def __init__(self, **data):
        """
        Initialize a BPMN Text Annotation.
        
        Args:
            **data: Text annotation properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.TEXT_ANNOTATION, **data)
    
    def set_text(self, text: str) -> None:
        """
        Set the text content of the annotation.
        
        Args:
            text (str): Text content
        """
        self.text = text
    
    def set_format(self, text_format: str) -> None:
        """
        Set the text format.
        
        Args:
            text_format (str): Text format (e.g., "text/plain", "text/html")
        """
        self.text_format = text_format
    
    def is_plain_text(self) -> bool:
        """Check if this annotation uses plain text format."""
        return self.text_format == "text/plain"
    
    def is_html(self) -> bool:
        """Check if this annotation uses HTML format."""
        return self.text_format == "text/html"
    
    def get_text_length(self) -> int:
        """Get the length of the text content."""
        return len(self.text)
    
    def __str__(self) -> str:
        """String representation of the text annotation."""
        preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        return f"Text Annotation '{self.name}': {preview}"
    
    class Config:
        """Pydantic configuration for TextAnnotation elements."""
        validate_assignment = True
