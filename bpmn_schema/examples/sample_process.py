"""
Simple BPMN process examples.

This module contains examples of simple BPMN processes demonstrating
common patterns and element usage.

Author: SimLab120
Date: 2025-07-03
"""

from datetime import datetime
from ..core.process import BPMNDiagram, Process
from ..core.events import Event, EventType, EventDefinition
from ..core.activities import Task, TaskType
from ..core.gateways import Gateway, GatewayType
from ..core.flows import SequenceFlow
from ..core.artifacts import DataObject, TextAnnotation


def create_simple_approval_process() -> BPMNDiagram:
    """
    Create a simple document approval process.
    
    This example demonstrates:
    - Start and end events
    - User tasks and service tasks
    - Exclusive gateway for decision making
    - Data objects for documents
    - Text annotations for documentation
    
    Returns:
        BPMNDiagram: Complete approval process diagram
    """
    # Create diagram
    diagram = BPMNDiagram(
        id="simple_approval_process",
        name="Simple Document Approval Process",
        created_by="SimLab120",
        created_at=datetime.now(),
        version="1.0"
    )
    
    # Create main process
    process = Process(
        id="approval_process",
        name="Document Approval Process",
        is_executable=True,
        process_type="private"
    )
    
    # Create events
    start_event = Event(
        id="start_document_request",
        name="Document Request Received",
        event_type=EventType.START,
        event_definition=EventDefinition.MESSAGE
    )
    
    end_approved = Event(
        id="end_approved",
        name="Document Approved",
        event_type=EventType.END
    )
    
    end_rejected = Event(
        id="end_rejected",
        name="Document Rejected",
        event_type=EventType.END
    )
    
    # Create tasks
    review_task = Task(
        id="review_document",
        name="Review Document",
        task_type=TaskType.USER_TASK,
        assignee="reviewer"
    )
    review_task.add_candidate_group("reviewers")
    review_task.set_position(150, 100)
    review_task.set_dimensions(100, 80)
    
    notify_approval = Task(
        id="notify_approval",
        name="Notify Approval",
        task_type=TaskType.SERVICE_TASK,
        implementation="email_service"
    )
    
    notify_rejection = Task(
        id="notify_rejection",
        name="Notify Rejection",
        task_type=TaskType.SERVICE_TASK,
        implementation="email_service"
    )
    
    # Create gateway
    decision_gateway = Gateway(
        id="approval_decision",
        name="Approval Decision",
        gateway_type=GatewayType.EXCLUSIVE
    )
    decision_gateway.set_as_diverging()
    decision_gateway.set_position(300, 100)
    
    # Create data objects
    document = DataObject(
        id="document",
        name="Document",
        state="Under Review"
    )
    
    # Create annotations
    process_note = TextAnnotation(
        id="process_note",
        name="Process Documentation",
        text="This process handles document approval requests from employees. Documents are reviewed by designated reviewers who can approve or reject them."
    )
    
    # Add elements to process
    process.add_flow_object(start_event)
    process.add_flow_object(review_task)
    process.add_flow_object(decision_gateway)
    process.add_flow_object(notify_approval)
    process.add_flow_object(notify_rejection)
    process.add_flow_object(end_approved)
    process.add_flow_object(end_rejected)
    
    process.add_artifact(document)
    process.add_artifact(process_note)
    
    # Create sequence flows
    flows = [
        SequenceFlow(
            id="flow_start_to_review",
            name="Submit Request",
            source_ref="start_document_request",
            target_ref="review_document"
        ),
        SequenceFlow(
            id="flow_review_to_decision",
            name="Complete Review",
            source_ref="review_document",
            target_ref="approval_decision"
        ),
        SequenceFlow(
            id="flow_approve",
            name="Approved",
            source_ref="approval_decision",
            target_ref="notify_approval",
            condition_expression="${approved == true}"
        ),
        SequenceFlow(
            id="flow_reject",
            name="Rejected",
            source_ref="approval_decision",
            target_ref="notify_rejection",
            condition_expression="${approved == false}"
        ),
        SequenceFlow(
            id="flow_approval_to_end",
            source_ref="notify_approval",
            target_ref="end_approved"
        ),
        SequenceFlow(
            id="flow_rejection_to_end",
            source_ref="notify_rejection",
            target_ref="end_rejected"
        )
    ]
    
    for flow in flows:
        process.add_connecting_object(flow)
    
    # Set default flow for gateway
    decision_gateway.set_default_flow("flow_reject")
    
    # Add process to diagram
    diagram.add_process(process)
    
    return diagram


def create_order_fulfillment_process() -> BPMNDiagram:
    """
    Create an order fulfillment process with parallel execution.
    
    This example demonstrates:
    - Parallel gateway usage
    - Multiple task types
    - Boundary events for timeouts
    - Multi-instance tasks
    
    Returns:
        BPMNDiagram: Order fulfillment process diagram
    """
    diagram = BPMNDiagram(
        id="order_fulfillment",
        name="Order Fulfillment Process",
        created_by="SimLab120",
        created_at=datetime.now()
    )
    
    process = Process(
        id="fulfillment_process",
        name="Order Fulfillment",
        is_executable=True
    )
    
    # Events
    start = Event(
        id="order_received",
        name="Order Received",
        event_type=EventType.START
    )
    
    timeout = Event(
        id="payment_timeout",
        name="Payment Timeout",
        event_type=EventType.BOUNDARY,
        event_definition=EventDefinition.TIMER,
        trigger="PT30M"  # 30 minutes
    )
    
    end = Event(
        id="order_completed",
        name="Order Completed",
        event_type=EventType.END
    )
    
    # Tasks
    validate_order = Task(
        id="validate_order",
        name="Validate Order",
        task_type=TaskType.BUSINESS_RULE_TASK,
        rule_implementation="order_validation_rules"
    )
    
    process_payment = Task(
        id="process_payment",
        name="Process Payment",
        task_type=TaskType.SERVICE_TASK,
        implementation="payment_service"
    )
    
    prepare_shipment = Task(
        id="prepare_shipment",
        name="Prepare Shipment",
        task_type=TaskType.USER_TASK
    )
    prepare_shipment.set_multi_instance_parallel("${order.items}", "item")
    
    send_confirmation = Task(
        id="send_confirmation",
        name="Send Confirmation",
        task_type=TaskType.SEND_TASK,
        message_ref="order_confirmation"
    )
    
    # Gateways
    parallel_split = Gateway(
        id="parallel_split",
        name="Process in Parallel",
        gateway_type=GatewayType.PARALLEL
    )
    parallel_split.set_as_diverging()
    
    parallel_join = Gateway(
        id="parallel_join",
        name="Join Parallel",
        gateway_type=GatewayType.PARALLEL
    )
    parallel_join.set_as_converging()
    
    # Add elements
    elements = [start, validate_order, parallel_split, process_payment, 
                prepare_shipment, parallel_join, send_confirmation, end, timeout]
    for element in elements:
        process.add_flow_object(element)
    
    # Attach timeout to payment task
    timeout.attach_to_activity("process_payment", interrupting=True)
    
    # Sequence flows
    flows = [
        SequenceFlow(id="f1", source_ref="order_received", target_ref="validate_order"),
        SequenceFlow(id="f2", source_ref="validate_order", target_ref="parallel_split"),
        SequenceFlow(id="f3", source_ref="parallel_split", target_ref="process_payment"),
        SequenceFlow(id="f4", source_ref="parallel_split", target_ref="prepare_shipment"),
        SequenceFlow(id="f5", source_ref="process_payment", target_ref="parallel_join"),
        SequenceFlow(id="f6", source_ref="prepare_shipment", target_ref="parallel_join"),
        SequenceFlow(id="f7", source_ref="parallel_join", target_ref="send_confirmation"),
        SequenceFlow(id="f8", source_ref="send_confirmation", target_ref="order_completed"),
    ]
    
    for flow in flows:
        process.add_connecting_object(flow)
    
    diagram.add_process(process)
    return diagram
