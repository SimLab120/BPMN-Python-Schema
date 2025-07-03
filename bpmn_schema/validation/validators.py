"""
BPMN diagram validation implementation.

This module provides comprehensive validation for BPMN diagrams to ensure
they conform to BPMN 2.0 specification and best practices.

Author: SimLab120
Date: 2025-07-03
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum
from ..core.process import BPMNDiagram, Process
from ..core.events import Event, EventType
from ..core.activities import Task
from ..core.gateways import Gateway
from ..core.flows import SequenceFlow


class ValidationSeverity(str, Enum):
    """Severity levels for validation messages."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationResult(BaseModel):
    """Individual validation result."""
    severity: ValidationSeverity
    element_id: Optional[str]
    element_type: Optional[str]
    message: str
    rule_name: str
    
    def __str__(self) -> str:
        element_info = f" (element: {self.element_id})" if self.element_id else ""
        return f"{self.severity.upper()}: {self.message}{element_info}"


class ValidationRule:
    """Base class for validation rules."""
    
    def __init__(self, name: str, severity: ValidationSeverity = ValidationSeverity.ERROR):
        self.name = name
        self.severity = severity
    
    def validate(self, diagram: BPMNDiagram) -> List[ValidationResult]:
        """Override this method to implement validation logic."""
        raise NotImplementedError


class StartEventRule(ValidationRule):
    """Validate that processes have appropriate start events."""
    
    def __init__(self):
        super().__init__("start_event_rule")
    
    def validate(self, diagram: BPMNDiagram) -> List[ValidationResult]:
        results = []
        
        for process in diagram.processes:
            start_events = process.get_start_events()
            
            if len(start_events) == 0:
                results.append(ValidationResult(
                    severity=self.severity,
                    element_id=process.id,
                    element_type="Process",
                    message="Process must have at least one start event",
                    rule_name=self.name
                ))
            elif len(start_events) > 1:
                results.append(ValidationResult(
                    severity=ValidationSeverity.WARNING,
                    element_id=process.id,
                    element_type="Process",
                    message=f"Process has {len(start_events)} start events (multiple start events should be used carefully)",
                    rule_name=self.name
                ))
        
        return results


class EndEventRule(ValidationRule):
    """Validate that processes have appropriate end events."""
    
    def __init__(self):
        super().__init__("end_event_rule")
    
    def validate(self, diagram: BPMNDiagram) -> List[ValidationResult]:
        results = []
        
        for process in diagram.processes:
            end_events = process.get_end_events()
            
            if len(end_events) == 0:
                results.append(ValidationResult(
                    severity=ValidationSeverity.WARNING,
                    element_id=process.id,
                    element_type="Process",
                    message="Process should have at least one end event",
                    rule_name=self.name
                ))
        
        return results


class SequenceFlowRule(ValidationRule):
    """Validate sequence flow connections."""
    
    def __init__(self):
        super().__init__("sequence_flow_rule")
    
    def validate(self, diagram: BPMNDiagram) -> List[ValidationResult]:
        results = []
        
        for process in diagram.processes:
            # Check for disconnected elements
            flow_objects = process.get_all_flow_objects()
            
            for flow_obj in flow_objects:
                incoming_flows = [f for f in process.sequence_flows if f.target_ref == flow_obj.id]
                outgoing_flows = [f for f in process.sequence_flows if f.source_ref == flow_obj.id]
                
                # Start events should have no incoming flows
                if isinstance(flow_obj, Event) and flow_obj.is_start_event():
                    if incoming_flows:
                        results.append(ValidationResult(
                            severity=self.severity,
                            element_id=flow_obj.id,
                            element_type="StartEvent",
                            message="Start events cannot have incoming sequence flows",
                            rule_name=self.name
                        ))
                
                # End events should have no outgoing flows
                if isinstance(flow_obj, Event) and flow_obj.is_end_event():
                    if outgoing_flows:
                        results.append(ValidationResult(
                            severity=self.severity,
                            element_id=flow_obj.id,
                            element_type="EndEvent",
                            message="End events cannot have outgoing sequence flows",
                            rule_name=self.name
                        ))
                
                # Activities should have incoming and outgoing flows (unless start/end)
                if isinstance(flow_obj, Task):
                    if not incoming_flows and not outgoing_flows:
                        results.append(ValidationResult(
                            severity=ValidationSeverity.WARNING,
                            element_id=flow_obj.id,
                            element_type="Task",
                            message="Task is not connected to any sequence flows",
                            rule_name=self.name
                        ))
        
        return results


class GatewayRule(ValidationRule):
    """Validate gateway usage."""
    
    def __init__(self):
        super().__init__("gateway_rule")
    
    def validate(self, diagram: BPMNDiagram) -> List[ValidationResult]:
        results = []
        
        for process in diagram.processes:
            for gateway in process.gateways:
                incoming_flows = [f for f in process.sequence_flows if f.target_ref == gateway.id]
                outgoing_flows = [f for f in process.sequence_flows if f.source_ref == gateway.id]
                
                # Gateways should have at least one incoming and one outgoing flow
                if len(incoming_flows) == 0:
                    results.append(ValidationResult(
                        severity=self.severity,
                        element_id=gateway.id,
                        element_type="Gateway",
                        message="Gateway must have at least one incoming sequence flow",
                        rule_name=self.name
                    ))
                
                if len(outgoing_flows) == 0:
                    results.append(ValidationResult(
                        severity=self.severity,
                        element_id=gateway.id,
                        element_type="Gateway",
                        message="Gateway must have at least one outgoing sequence flow",
                        rule_name=self.name
                    ))
                
                # Diverging gateways should have multiple outgoing flows
                if gateway.is_diverging() and len(outgoing_flows) < 2:
                    results.append(ValidationResult(
                        severity=ValidationSeverity.WARNING,
                        element_id=gateway.id,
                        element_type="Gateway",
                        message="Diverging gateway should have multiple outgoing flows",
                        rule_name=self.name
                    ))
                
                # Converging gateways should have multiple incoming flows
                if gateway.is_converging() and len(incoming_flows) < 2:
                    results.append(ValidationResult(
                        severity=ValidationSeverity.WARNING,
                        element_id=gateway.id,
                        element_type="Gateway",
                        message="Converging gateway should have multiple incoming flows",
                        rule_name=self.name
                    ))
        
        return results


class BPMNValidator:
    """
    BPMN diagram validator.
    
    Validates BPMN diagrams against BPMN 2.0 specification and best practices.
    """
    
    def __init__(self, diagram: BPMNDiagram):
        """
        Initialize validator with a BPMN diagram.
        
        Args:
            diagram (BPMNDiagram): Diagram to validate
        """
        self.diagram = diagram
        self.rules: List[ValidationRule] = [
            StartEventRule(),
            EndEventRule(),
            SequenceFlowRule(),
            GatewayRule(),
        ]
        self.results: List[ValidationResult] = []
    
    def add_rule(self, rule: ValidationRule) -> None:
        """
        Add a custom validation rule.
        
        Args:
            rule (ValidationRule): Rule to add
        """
        self.rules.append(rule)
    
    def validate(self) -> bool:
        """
        Validate the diagram against all rules.
        
        Returns:
            bool: True if no errors found, False otherwise
        """
        self.results.clear()
        
        for rule in self.rules:
            rule_results = rule.validate(self.diagram)
            self.results.extend(rule_results)
        
        # Return True if no errors (warnings and info are OK)
        return not any(result.severity == ValidationSeverity.ERROR for result in self.results)
    
    def get_validation_report(self) -> str:
        """
        Get a formatted validation report.
        
        Returns:
            str: Formatted validation report
        """
        if not self.results:
            return "Validation passed: No issues found."
        
        report_lines = ["BPMN Validation Report", "=" * 25, ""]
        
        # Group by severity
        errors = [r for r in self.results if r.severity == ValidationSeverity.ERROR]
        warnings = [r for r in self.results if r.severity == ValidationSeverity.WARNING]
        infos = [r for r in self.results if r.severity == ValidationSeverity.INFO]
        
        if errors:
            report_lines.extend(["ERRORS:", ""])
            for error in errors:
                report_lines.append(f"  • {error.message} (Element: {error.element_id})")
            report_lines.append("")
        
        if warnings:
            report_lines.extend(["WARNINGS:", ""])
            for warning in warnings:
                report_lines.append(f"  • {warning.message} (Element: {warning.element_id})")
            report_lines.append("")
        
        if infos:
            report_lines.extend(["INFO:", ""])
            for info in infos:
                report_lines.append(f"  • {info.message} (Element: {info.element_id})")
            report_lines.append("")
        
        # Summary
        report_lines.extend([
            "SUMMARY:",
            f"  Errors: {len(errors)}",
            f"  Warnings: {len(warnings)}",
            f"  Info: {len(infos)}",
            f"  Total Issues: {len(self.results)}"
        ])
        
        return "\n".join(report_lines)
    
    def get_errors(self) -> List[ValidationResult]:
        """Get all error-level validation results."""
        return [r for r in self.results if r.severity == ValidationSeverity.ERROR]
    
    def get_warnings(self) -> List[ValidationResult]:
        """Get all warning-level validation results."""
        return [r for r in self.results if r.severity == ValidationSeverity.WARNING]
    
    def has_errors(self) -> bool:
        """Check if validation found any errors."""
        return any(result.severity == ValidationSeverity.ERROR for result in self.results)
    
    def has_warnings(self) -> bool:
        """Check if validation found any warnings."""
        return any(result.severity == ValidationSeverity.WARNING for result in self.results)
