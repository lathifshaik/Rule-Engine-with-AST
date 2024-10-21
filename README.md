# Rule Engine with Abstract Syntax Tree (AST)

## Overview

We are proud to present our successful implementation of a sophisticated 3-tier rule engine application. This project showcases a powerful system for determining user eligibility based on various attributes such as age, department, income, and spending patterns. By leveraging Abstract Syntax Trees (AST), we've created a flexible and dynamic platform for rule creation, combination, and modification.

## Key Achievements

- **Robust 3-Tier Architecture**: Implemented a complete system with a user-friendly UI, efficient API, and a solid backend.
- **Advanced AST Implementation**: Developed a complex data structure to represent and manipulate rules dynamically.
- **Efficient Data Storage**: Designed an optimized database schema for storing rules and application metadata.
- **Comprehensive API**: Created a full suite of API endpoints for rule management and evaluation.
- **Dynamic Rule Handling**: Successfully implemented creation, combination, and evaluation of complex rules.
- **Extensive Testing**: Developed a comprehensive test suite to ensure reliability and accuracy.

## Features

- Create individual rules with a user-friendly syntax
- Combine multiple rules using logical operators (AND, OR)
- Evaluate rules against JSON data
- RESTful API for rule management and evaluation
- Web interface for easy interaction with the rule engine
- Support for complex nested rules
- Efficient rule combination strategies

## Technical Details

### Data Structure

We implemented a sophisticated Node-based structure for our AST:

```python
class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type  # "operator" or "operand"
        self.value = value
        self.left = left
        self.right = right
```

This structure allows for dynamic rule changes and complex rule representations.

### Data Storage

We chose SQLite for its efficiency and ease of integration. Our schema supports storing complex rule structures and all necessary metadata.

### Sample Rules

Our system successfully handles complex rules such as:

```
((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
```

### API Design

We've implemented all required API endpoints with additional features:

1. `create_rule(rule_string)`: Creates an AST from a rule string.
2. `combine_rules(rules)`: Efficiently combines multiple rules into a single AST.
3. `evaluate_rule(data)`: Evaluates a rule against provided JSON data.

## Technologies Used

- **Backend:** Python 3.x, Flask, SQLAlchemy
- **Frontend:** HTML5, CSS (Tailwind CSS), JavaScript
- **Database:** SQLite
- **Testing:** unittest

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/lathifshaik/Rule-Engine-with-AST.git
   cd Rule-Engine-with-AST
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

The application will be running on `http://localhost:5000`.

## Usage

### API Endpoints

- `POST /create_rule`: Create a new rule
- `POST /evaluate_rule/<rule_id>`: Evaluate a rule against provided data
- `POST /combine_rules`: Combine multiple rules
- `GET /rules`: Get all existing rules
- `PUT /edit_rule/<rule_id>`: Edit an existing rule

### Web Interface

Our intuitive web interface at `http://localhost:5000` allows users to:

- Create and edit complex rules
- Evaluate rules against JSON data
- Combine multiple rules
- View and manage all existing rules

## Web Interface Screenshot

![Rule Engine Web Interface](rule_engine_interface.png)

*Our sleek and user-friendly interface for rule management*

## Running Tests

Execute our comprehensive test suite:

```
python -m unittest discover tests
```

## Rule Syntax

Our system supports a wide range of operations:

- Comparison: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Logical: `AND`, `OR`
- Nested parentheses for complex logic

Example: `(age > 18 AND status == "active") OR (score >= 75 AND category == "A")`


