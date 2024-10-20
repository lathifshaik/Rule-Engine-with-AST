# Rule Engine with AST

## Introduction

This project implements a sophisticated 3-tier rule engine application using Flask, SQLAlchemy, and Abstract Syntax Tree (AST) to determine user eligibility based on various attributes such as age, department, income, and spending. The system allows for dynamic creation, combination, and modification of conditional rules.

## Features

- Create individual rules using a string representation
- Combine multiple rules into a single rule using AND/OR operators
- Evaluate rules against user data
- Store rules in a SQLite database
- RESTful API for rule management and evaluation
- Frontend interface using HTML, Bootstrap CSS, and JavaScript
- Comprehensive error handling and input validation
- Unit testing suite

## Project Structure

```
rule-engine-ast/
│
├── app.py                 # Main Flask application setup
├── config.py              # Configuration file for the Flask app
├── models.py              # Database models using SQLAlchemy
├── rules.py               # Core logic for creating, combining, and evaluating rules
├── test_rules.py          # Unit tests for the rule engine functionality
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   └── index.html
└── README.md              # This file
```

## Technologies Used

- Backend: Python 3.8+, Flask 2.0+
- Database: SQLite, SQLAlchemy
- Frontend: HTML5, Bootstrap 5, JavaScript (ES6+)
- Testing: unittest
- Version Control: Git

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/lathifshaik/Rule-Engine-with-AST.git
   cd rule-engine-ast
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the Flask application:
   ```
   flask run
   ```

## Configuration

The application uses a configuration file (`config.py`) to manage different settings. You can modify this file to change database settings, secret keys, and other configuration options.

Key configuration options:
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `SECRET_KEY`: Secret key for session management
- `DEBUG`: Enable/disable debug mode

## API Endpoints

- `POST /create_rule`: Create a new rule
  - Request body: `{"name": "Rule Name", "rule_string": "age > 18 AND department == 'Sales'"}`

- `POST /evaluate_rule/<rule_id>`: Evaluate a rule against provided data
  - Request body: `{"age": 25, "department": "Sales", "salary": 50000}`

- `POST /combine_rules`: Combine multiple rules into a single rule
  - Request body: `{"rule_ids": [1, 2, 3], "operator": "AND"}`

- `GET /rules`: Get all rules

- `PUT /edit_rule/<rule_id>`: Edit an existing rule
  - Request body: `{"rule_string": "age >= 21 AND department == 'Marketing'"}`

## Usage Examples

1. Creating a rule:
   ```
   curl -X POST http://localhost:5000/create_rule -H "Content-Type: application/json" -d '{"name": "Adult in Sales", "rule_string": "age >= 18 AND department == \"Sales\""}'
   ```

2. Evaluating a rule:
   ```
   curl -X POST http://localhost:5000/evaluate_rule/1 -H "Content-Type: application/json" -d '{"age": 25, "department": "Sales"}'
   ```

3. Combining rules:
   ```
   curl -X POST http://localhost:5000/combine_rules -H "Content-Type: application/json" -d '{"rule_ids": [1, 2], "operator": "OR"}'
   ```

## Security Measures

1. Input Validation: All user inputs are validated to prevent injection attacks.
2. CORS (Cross-Origin Resource Sharing): Configured to restrict access from unauthorized domains.
3. SQL Injection Prevention: Using SQLAlchemy ORM to prevent SQL injection attacks.
4. Secret Key: A strong secret key is used for session management.

## Testing

To run the unit tests:

```
python -m unittest test_rules.py
```

The test suite covers:
- Creating individual rules
- Combining rules
- Evaluating rules against various data inputs
- Edge cases and error handling


## Libraries and Dependencies

- Flask (2.0.1): Web framework for building the API
- SQLAlchemy (1.4.23): ORM for database operations
- Flask-SQLAlchemy (2.5.1): Flask extension for SQLAlchemy integration
- Flask-Migrate (3.1.0): Database migration tool
- Flask-CORS (3.0.10): Handling Cross-Origin Resource Sharing
- pytest (6.2.5): Testing framework

For a complete list of dependencies, refer to `requirements.txt`.

## Troubleshooting

- If you encounter database errors, ensure your SQLite file has the correct permissions.
- For "Module not found" errors, verify that all dependencies are installed and your virtual environment is activated.
- If API calls fail, check the server logs for detailed error messages.
