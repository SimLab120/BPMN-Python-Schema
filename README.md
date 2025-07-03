# BPMN Python Schema

A comprehensive Python library for Business Process Modeling Notation (BPMN) data modeling and validation.

## Overview

This library provides a complete implementation of BPMN 2.0 specification with strong typing, validation, and serialization capabilities. It covers all BPMN elements as defined in the official specification and popular tools like Lucidchart.

## Features

- **Complete BPMN 2.0 Coverage**: All flow objects, connecting objects, swimlanes, and artifacts
- **Strong Typing**: Full type hints and Pydantic validation
- **Serialization**: JSON and XML export/import capabilities
- **Validation**: Comprehensive BPMN diagram validation
- **Examples**: Real-world process modeling examples
- **Extensible**: Easy to extend with custom elements

## Installation

```bash
pip install bpmn-python-schema
```

Or install from source:

```bash
git clone https://github.com/SimLab120/bpmn-python-schema.git
cd bpmn-python-schema
pip install -e .
```

## Quick Start

```python
from bpmn_schema import BPMNDiagram, Process, Event, Task, Gateway, SequenceFlow
from bpmn_schema.core.events import EventType
from bpmn_schema.core.activities import TaskType
from bpmn_schema.core.gateways import GatewayType

# Create a simple approval process
diagram = BPMNDiagram(
    id="approval_process",
    name="Document Approval Process"
)

process = Process(
    id="main_process",
    name="Main Process",
    is_executable=True
)

# Create process elements
start = Event(
    id="start_event",
    name="Request Submitted",
    event_type=EventType.START
)

review_task = Task(
    id="review_task",
    name="Review Document",
    task_type=TaskType.USER_TASK
)

gateway = Gateway(
    id="approval_gateway",
    name="Approval Decision",
    gateway_type=GatewayType.EXCLUSIVE
)

# Add elements to process
process.add_flow_object(start)
process.add_flow_object(review_task)
process.add_flow_object(gateway)

# Create flows
flow1 = SequenceFlow(
    id="flow1",
    source_ref="start_event",
    target_ref="review_task"
)

process.add_connecting_object(flow1)

# Add process to diagram
diagram.add_process(process)

# Export to JSON
json_output = diagram.model_dump_json(indent=2)
print(json_output)
```

## BPMN Elements Coverage

### Flow Objects
- **Events**: Start, Intermediate, Boundary, End with all trigger types
- **Activities**: Tasks (User, Service, Script, etc.) and Subprocesses
- **Gateways**: Exclusive, Inclusive, Parallel, Complex, Event-based

### Connecting Objects
- **Sequence Flow**: Normal process flow
- **Message Flow**: Communication between pools
- **Association**: Connects artifacts to flow objects

### Swimlanes
- **Pools**: Process participants
- **Lanes**: Responsibility divisions

### Artifacts
- **Data Objects**: Process data with states
- **Data Stores**: Persistent storage
- **Groups**: Visual grouping
- **Text Annotations**: Documentation

## Examples

### Simple Process
```python
from bpmn_schema.examples import create_simple_approval_process

diagram = create_simple_approval_process()
print(f"Process has {len(diagram.processes[0].tasks)} tasks")
```

### Collaboration Process
```python
from bpmn_schema.examples import create_collaboration_process

diagram = create_collaboration_process()
print(f"Collaboration has {len(diagram.pools)} pools")
```

## Validation

```python
from bpmn_schema.validation import BPMNValidator

validator = BPMNValidator(diagram)
is_valid = validator.validate()
print(validator.get_validation_report())
```

## Documentation

- [API Reference](docs/api.md)
- [Examples](docs/examples.md)
- [Validation Guide](docs/validation.md)
- [Contributing](CONTRIBUTING.md)

## Requirements

- Python 3.8+
- Pydantic 2.0+
- typing-extensions (for Python < 3.10)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- GitHub Issues: [Report bugs or request features](https://github.com/SimLab120/bpmn-python-schema/issues)
- Documentation: [Full documentation](https://bpmn-python-schema.readthedocs.io/)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
