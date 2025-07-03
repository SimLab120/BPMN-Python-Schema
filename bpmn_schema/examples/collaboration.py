"""
BPMN collaboration process examples.

This module contains examples of BPMN collaborations demonstrating
multi-participant processes with message flows.

Author: SimLab120
Date: 2025-07-03
"""

from datetime import datetime
from ..core.process import BPMNDiagram, Process
from ..core.events import Event, EventType, EventDefinition
from ..core.activities import Task, TaskType
from ..core.flows import SequenceFlow, MessageFlow
from ..core.swimlanes import Pool, Lane


def create_collaboration_process() -> BPMNDiagram:
    """
    Create a collaboration process between customer and supplier.
    
    This example demonstrates:
    - Multiple pools (participants)
    - Message flows between pools
    - Lanes within pools
    - Message events
    
    Returns:
        BPMNDiagram: Collaboration diagram
    """
    diagram = BPMNDiagram(
        id="purchase_collaboration",
        name="Purchase Order Collaboration",
        created_by="SimLab120",
        created_at=datetime.now()
    )
    
    # Customer Process
    customer_process = Process(
        id="customer_process",
        name="Customer Purchase Process",
        is_executable=True
    )
    
    # Customer events and tasks
    start_need = Event(
        id="customer_start",
        name="Need Identified",
        event_type=EventType.START
    )
    
    create_order = Task(
        id="create_purchase_order",
        name="Create Purchase Order",
        task_type=TaskType.USER_TASK
    )
    
    wait_confirmation = Event(
        id="wait_confirmation",
        name="Wait for Confirmation",
        event_type=EventType.INTERMEDIATE,
        event_definition=EventDefinition.MESSAGE,
        is_throwing=False
    )
    
    receive_goods = Task(
        id="receive_goods",
        name="Receive Goods",
        task_type=TaskType.USER_TASK
    )
    
    customer_end = Event(
        id="customer_end",
        name="Order Completed",
        event_type=EventType.END
    )
    
    # Add to customer process
    customer_elements = [start_need, create_order, wait_confirmation, receive_goods, customer_end]
    for element in customer_elements:
        customer_process.add_flow_object(element)
    
    # Customer sequence flows
    customer_flows = [
        SequenceFlow(id="cf1", source_ref="customer_start", target_ref="create_purchase_order"),
        SequenceFlow(id="cf2", source_ref="create_purchase_order", target_ref="wait_confirmation"),
        SequenceFlow(id="cf3", source_ref="wait_confirmation", target_ref="receive_goods"),
        SequenceFlow(id="cf4", source_ref="receive_goods", target_ref="customer_end")
    ]
    
    for flow in customer_flows:
        customer_process.add_connecting_object(flow)
    
    # Supplier Process
    supplier_process = Process(
        id="supplier_process",
        name="Supplier Order Processing",
        is_executable=True
    )
    
    # Supplier events and tasks
    receive_order = Event(
        id="receive_order",
        name="Order Received",
        event_type=EventType.START,
        event_definition=EventDefinition.MESSAGE
    )
    
    check_inventory = Task(
        id="check_inventory",
        name="Check Inventory",
        task_type=TaskType.SERVICE_TASK
    )
    
    send_confirmation = Task(
        id="send_confirmation",
        name="Send Confirmation",
        task_type=TaskType.SEND_TASK
    )
    
    prepare_shipment = Task(
        id="prepare_shipment",
        name="Prepare Shipment",
        task_type=TaskType.USER_TASK
    )
    
    ship_goods = Task(
        id="ship_goods",
        name="Ship Goods",
        task_type=TaskType.SEND_TASK
    )
    
    supplier_end = Event(
        id="supplier_end",
        name="Order Fulfilled",
        event_type=EventType.END
    )
    
    # Add to supplier process
    supplier_elements = [receive_order, check_inventory, send_confirmation, 
                        prepare_shipment, ship_goods, supplier_end]
    for element in supplier_elements:
        supplier_process.add_flow_object(element)
    
    # Supplier sequence flows
    supplier_flows = [
        SequenceFlow(id="sf1", source_ref="receive_order", target_ref="check_inventory"),
        SequenceFlow(id="sf2", source_ref="check_inventory", target_ref="send_confirmation"),
        SequenceFlow(id="sf3", source_ref="send_confirmation", target_ref="prepare_shipment"),
        SequenceFlow(id="sf4", source_ref="prepare_shipment", target_ref="ship_goods"),
        SequenceFlow(id="sf5", source_ref="ship_goods", target_ref="supplier_end")
    ]
    
    for flow in supplier_flows:
        supplier_process.add_connecting_object(flow)
    
    # Create Pools and Lanes
    customer_pool = Pool(
        id="customer_pool",
        name="Customer",
        is_executable=True,
        process_ref="customer_process"
    )
    
    # Customer lanes
    purchasing_lane = Lane(
        id="purchasing_lane",
        name="Purchasing Department"
    )
    purchasing_lane.add_flow_node("create_purchase_order")
    
    receiving_lane = Lane(
        id="receiving_lane",
        name="Receiving Department"
    )
    receiving_lane.add_flow_node("receive_goods")
    
    customer_pool.add_lane(purchasing_lane)
    customer_pool.add_lane(receiving_lane)
    
    supplier_pool = Pool(
        id="supplier_pool",
        name="Supplier",
        is_executable=True,
        process_ref="supplier_process"
    )
    
    # Supplier lanes
    sales_lane = Lane(
        id="sales_lane",
        name="Sales Department"
    )
    sales_lane.add_flow_node("receive_order")
    sales_lane.add_flow_node("send_confirmation")
    
    warehouse_lane = Lane(
        id="warehouse_lane",
        name="Warehouse"
    )
    warehouse_lane.add_flow_node("check_inventory")
    warehouse_lane.add_flow_node("prepare_shipment")
    warehouse_lane.add_flow_node("ship_goods")
    
    supplier_pool.add_lane(sales_lane)
    supplier_pool.add_lane(warehouse_lane)
    
    # Message Flows
    order_message = MessageFlow(
        id="order_message",
        name="Purchase Order",
        source_ref="create_purchase_order",
        target_ref="receive_order",
        message_ref="purchase_order"
    )
    
    confirmation_message = MessageFlow(
        id="confirmation_message",
        name="Order Confirmation",
        source_ref="send_confirmation",
        target_ref="wait_confirmation",
        message_ref="order_confirmation"
    )
    
    shipment_message = MessageFlow(
        id="shipment_message",
        name="Goods Shipment",
        source_ref="ship_goods",
        target_ref="receive_goods",
        message_ref="goods_shipment"
    )
    
    # Add everything to diagram
    diagram.add_process(customer_process)
    diagram.add_process(supplier_process)
    diagram.add_pool(customer_pool)
    diagram.add_pool(supplier_pool)
    diagram.add_message_flow(order_message)
    diagram.add_message_flow(confirmation_message)
    diagram.add_message_flow(shipment_message)
    
    return diagram


def create_insurance_claim_collaboration() -> BPMNDiagram:
    """
    Create an insurance claim processing collaboration.
    
    This example demonstrates:
    - Complex collaboration with multiple participants
    - Error handling with error events
    - Escalation scenarios
    - Timer events for SLA management
    
    Returns:
        BPMNDiagram: Insurance claim collaboration
    """
    diagram = BPMNDiagram(
        id="insurance_claim_collaboration",
        name="Insurance Claim Processing",
        created_by="SimLab120",
        created_at=datetime.now()
    )
    
    # This would be a more complex example with additional participants
    # like medical providers, adjusters, etc.
    # Implementation follows similar patterns as above
    
    return diagram
