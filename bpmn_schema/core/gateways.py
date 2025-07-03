"""
BPMN Gateway elements implementation.

This module contains all gateway-related classes for BPMN modeling.
Gateways control the flow of the process by determining branching, forking,
merging, and joining of paths.

Author: SimLab120
Date: 2025-07-03
"""

from typing import Optional, Literal
from enum import Enum
from .base import BPMNElement, BPMNElementType


class GatewayType(str, Enum):
    """
    Enumeration of BPMN gateway types.
    
    Gateways control the flow of sequence flows in a process.
    Each gateway type has specific decision-making semantics.
    """
    
    EXCLUSIVE = "exclusive"                 # XOR - One path chosen (diamond with X)
    INCLUSIVE = "inclusive"                 # OR - One or more paths (diamond with circle)
    PARALLEL = "parallel"                   # AND - All paths (diamond with plus)
    COMPLEX = "complex"                     # Complex conditions (diamond with asterisk)
    EVENT_BASED = "event_based"             # Event-based decision (diamond with pentagon)
    EXCLUSIVE_EVENT_BASED = "exclusive_event_based"  # Exclusive event-based
    PARALLEL_EVENT_BASED = "parallel_event_based"    # Parallel event-based


class Gateway(BPMNElement):
    """
    BPMN Gateway element implementation.
    
    Gateways are used to control how sequence flows interact as they converge
    and diverge within a process. They act as decision points that determine
    which path(s) to take based on conditions or events.
    
    This class supports all BPMN 2.0 gateway types with their specific
    behaviors and properties.
    
    Attributes:
        gateway_type (GatewayType): Type of gateway determining its behavior
        gateway_direction (Literal): Direction of gateway (converging, diverging, mixed)
        default_flow (Optional[str]): Reference to default sequence flow
        instantiate (bool): Whether gateway instantiates the process (event-based)
        event_gateway_type (Optional[str]): Type for event-based gateways
    """
    
    gateway_type: GatewayType = GatewayType.EXCLUSIVE
    gateway_direction: Literal["unspecified", "converging", "diverging", "mixed"] = "unspecified"
    default_flow: Optional[str] = None
    instantiate: bool = False
    event_gateway_type: Optional[Literal["exclusive", "parallel"]] = None
    
    def __init__(self, **data):
        """
        Initialize a BPMN Gateway.
        
        Args:
            **data: Gateway properties including all base element properties
        """
        super().__init__(element_type=BPMNElementType.GATEWAY, **data)
    
    def is_exclusive(self) -> bool:
        """Check if this is an exclusive (XOR) gateway."""
        return self.gateway_type == GatewayType.EXCLUSIVE
    
    def is_inclusive(self) -> bool:
        """Check if this is an inclusive (OR) gateway."""
        return self.gateway_type == GatewayType.INCLUSIVE
    
    def is_parallel(self) -> bool:
        """Check if this is a parallel (AND) gateway."""
        return self.gateway_type == GatewayType.PARALLEL
    
    def is_complex(self) -> bool:
        """Check if this is a complex gateway."""
        return self.gateway_type == GatewayType.COMPLEX
    
    def is_event_based(self) -> bool:
        """Check if this is an event-based gateway."""
        return self.gateway_type in [
            GatewayType.EVENT_BASED,
            GatewayType.EXCLUSIVE_EVENT_BASED,
            GatewayType.PARALLEL_EVENT_BASED
        ]
    
    def is_diverging(self) -> bool:
        """Check if this is a diverging gateway (splits flow)."""
        return self.gateway_direction == "diverging"
    
    def is_converging(self) -> bool:
        """Check if this is a converging gateway (joins flow)."""
        return self.gateway_direction == "converging"
    
    def is_mixed(self) -> bool:
        """Check if this is a mixed gateway (both splits and joins)."""
        return self.gateway_direction == "mixed"
    
    def set_as_diverging(self) -> None:
        """Configure this gateway as diverging (splitting flow)."""
        self.gateway_direction = "diverging"
    
    def set_as_converging(self) -> None:
        """Configure this gateway as converging (joining flow)."""
        self.gateway_direction = "converging"
    
    def set_as_mixed(self) -> None:
        """Configure this gateway as mixed (both splitting and joining)."""
        self.gateway_direction = "mixed"
    
    def set_default_flow(self, flow_id: str) -> None:
        """
        Set the default sequence flow for this gateway.
        
        The default flow is taken when no other condition is met.
        Only applicable to exclusive and inclusive gateways.
        
        Args:
            flow_id (str): ID of the default sequence flow
        """
        if self.is_exclusive() or self.is_inclusive():
            self.default_flow = flow_id
        else:
            raise ValueError(f"Default flow not supported for {self.gateway_type.value} gateway")
    
    def enable_process_instantiation(self) -> None:
        """
        Enable process instantiation for event-based gateways.
        
        When enabled, the gateway can instantiate a new process instance
        when one of its events is triggered.
        """
        if self.is_event_based():
            self.instantiate = True
        else:
            raise ValueError("Process instantiation only supported for event-based gateways")
    
    def get_gateway_symbol(self) -> str:
        """
        Get the visual symbol character for this gateway type.
        
        Returns:
            str: Symbol character representing the gateway type
        """
        symbol_map = {
            GatewayType.EXCLUSIVE: "X",
            GatewayType.INCLUSIVE: "O",
            GatewayType.PARALLEL: "+",
            GatewayType.COMPLEX: "*",
            GatewayType.EVENT_BASED: "⬟",
            GatewayType.EXCLUSIVE_EVENT_BASED: "⬟",
            GatewayType.PARALLEL_EVENT_BASED: "⬟"
        }
        return symbol_map.get(self.gateway_type, "?")
    
    def __str__(self) -> str:
        """String representation of the gateway."""
        symbol = self.get_gateway_symbol()
        direction = f" ({self.gateway_direction})" if self.gateway_direction != "unspecified" else ""
        return f"{self.gateway_type.value.replace('_', ' ').title()} Gateway '{self.name}' [{symbol}]{direction}"
    
    class Config:
        """Pydantic configuration for Gateway elements."""
        use_enum_values = True
        validate_assignment = True
